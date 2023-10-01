#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
import pandas as pd
import pandas.io.sql as sqlio
import numpy as np
from functools import reduce
import uuid
import json
from ivcap_df.column import NAMESPACE_IVCAP

from pycozo import Client
from pycozo.client import QueryException

from ivcap_df import Schema, ColType, Column, Connector


from urllib.parse import quote 
from datetime import datetime

from typing import Iterable, Callable, List, Sequence, Tuple

import json

from ivcap_df import Schema, ColType, Column, RefColumn, IdColumn, ENTITY_COL_NAME

SchemaType = {
    ColType.ENTITY: 'String', #'Uuid',
    ColType.UUID: 'Uuid',
    ColType.REF: 'String', #'Uuid',
    ColType.FLOAT16: 'Float',
    ColType.FLOAT32: 'Float',
    ColType.FLOAT64: 'Float',
    ColType.FLOAT128: 'Float',
    ColType.INT8: 'Int',
    ColType.INT16: 'Int',
    ColType.INT32: 'Int',
    ColType.INT64: 'Int',
    ColType.UINT8: 'Int',
    ColType.UINT16: 'Int',
    ColType.UINT32: 'Int',
    ColType.UINT64: 'Int',
    ColType.DATETIME64_NS_TZ: 'String',
    ColType.DATE: 'String',
    ColType.STRING: 'String',
    ColType.BOOLEAN: 'Bool',
}

REL2JSON_SCHEMA = 'sys__rel2json_schema'
REL_SCHEMA_REF = 'sys__rel_schema_ref'

class CozoConnector(Connector):
    path2connector = {}
    
    @classmethod
    def create(cls, **kwargs) -> 'CozoConnector':
        path = kwargs.get('path')
        if path == None:
            raise Exception("Missing 'path'")
        c = cls.path2connector.get(path)
        if c == None:
            c = cls(path=path)
            cls.path2connector[path] = c
        return c

    
    def __init__(self, **kwargs):
        """
        Create a COZO connector with the following paramters:
        
        path - Path to directory containing RocksDB files 
        """
        path = kwargs.get('path')
        if path == None:
            raise Exception("Missing 'path'")
        self._db = Client(engine='rocksdb', path=path, dataframe=True)
        self._path = path
        self._urn2schema = {}
        # Ensure that schema mapping relation exists - will only succeed first time with new backend
        #self.query(':create sys__rel2json_schema { rel_name: String, urn: String => json_schema: String }')
        self._create_relation(REL2JSON_SCHEMA, '{ rel_name: String, urn: String, namespace: String => json_schema: String }')
        self._create_relation(REL_SCHEMA_REF, '{ from: String, to: String, name: String => is_reverse: Bool, hash: String }')

    def _create_relation(self, name: str, definition: str):
        try:
            self.query(':create ' + name + ' ' + definition)
        except QueryException as qe:
            pass
        except Exception as ex:
            self.close()
            raise ex


    def close(self):
        if self._db != None and self._db.embedded:
            self._db.embedded.close()
            self._db = None
            del self.__class__.path2connector[self._path]

    def query(self, script:str, params=None):
        if self._db == None:
            raise Exception("connector is already closed")
        return self._db.run(script, params)

    def insert_data_frame(self, df: pd.DataFrame, schema: Schema, **kwargs):
        """Insert content of 'df' into table represented by 'schema'. If 'ignoreDuplicateRecords'
        is set, quietly drop any records in 'df' which have an identical 'record-id' to what is already
        stored in the table."""
        
        #  ?[a, b] <- [[1, 'one'], [3, 'three']]
        #  :put rel {a => b}
        verbose = kwargs.get('verbose', False)
        cols = schema.columns
        
        def colF(col, r):
            el = r.get(col.name)
            if el == None or pd.isna(el):
                if col.required:
                    raise Exception(f"Required column '{col.name}' cannot by None - {r}")
                return 'null'

            if col.ctype == ColType.STRING:
                el = f"'{el}'"
            elif col.ctype == ColType.UUID:
                el = f"'{str(el)}'" if isinstance(el, uuid.UUID) else 'null'
            elif col.ctype == ColType.ENTITY or col.ctype == ColType.REF:
                el = f"'{col.get_urn_for(el)}'" if not pd.isnull(el) else '"urn:error:undefined"'
            elif col.ctype == ColType.DATE:
                if isinstance(el, str):
                    # TODO: Verify that the string is in proper date format
                    el = f"'{el}'"
                else:
                    el = f"'{el.strftime('%Y-%m-%d')}'" if not pd.isnull(el) else 'null'
            elif col.ctype == ColType.DATETIME64_NS_TZ:
                if isinstance(el, str):
                    # TODO: Verify that the string is in proper dateTime format
                    el = f"'{el}'"
                else:
                    el = f"'{str(el.to_datetime64())}'" if not pd.isnull(el) else 'null'
            else:
                el = str(el)
            return el

        # sort columns according to schema
        # and turn UUID and date into str
        def rowF(row):
            rec = map(lambda col: colF(col, row), cols)
            # return list(rec) # 
            return f"[{','.join(rec)}]"

        records = df.apply(rowF, axis=1)
        rs = ',\n'.join(records)
        head = f"?[{','.join(map(lambda c: _safe_name(c.name), schema.columns))}] <- [\n{rs}]"
        rel_name = f"{schema.namespace}__{schema.name}_{schema.version}"
        rel = _relation(schema, lambda c: _safe_name(c.name))
        put = f":put {rel_name} { '{' + rel + '}'}"
        cmd = f"{head}\n{put}"
        if verbose:
            print(cmd)
        try:
            return self.query(cmd)
        except QueryException as qe:
            print(f"Error: {qe} - cmd: {cmd}")
            raise qe

    def get_all_for_schema(self, schema: Schema, debug:bool = False) -> pd.DataFrame:
        """Get all accessible entities of type `Schema`.
        
        This query is primarily used for schemas representing 'controlled vocabulary'.

        Args:
            schema (Schema): Schema of elements queried.

        Returns:
            pd.DataFrame: A dataframe holding all accessible entities
        """
        # ?[a, b, c, d] := *blue_growth__seagrass_species_1[a, b, c, d]
        rel_name = f"{schema.namespace}__{schema.name}_{schema.version}"
        args = ', '.join(list(map(lambda c: c.name, schema.columns)))
        q = f"?[{args}] := *{rel_name}[{args}]"
        if debug:
            print("get_all_for_schema#query", q)
        r = self.query(q)
        return r

    def query_to_df(self, query: str) -> pd.DataFrame:
        """Execute 'sql' query and return result as dataframe."""
        r = self.query(query)
        return r


    def register_schema(self, schema: Schema, verbose: bool = False):
        """Register the 'schema' in the metadata registry.

        Args:
            schema (Schema): Schema to register and persist
            verbose (bool, optional): Be chatty when true. Defaults to False.

        Returns:
            _type_: _description_
        """

        # Create a relation based on the schema definition

        rel = f"{schema.namespace}__{schema.name}_{schema.version}"
        #     :replace dept_info {
        #         company_name: String,
        #         department_name: String,
        #         =>
        #         head_count: Int,
        #         address: String,
        #     }
        def elf(c):
            name = _safe_name(c.name)
            type = SchemaType[c.ctype]
            if c.is_nullable():
                type = type + "?"
            return f"{name}: {type}"

        keys = filter(lambda c: c.ctype == ColType.ENTITY, schema.columns)
        values = filter(lambda c: c.ctype != ColType.ENTITY, schema.columns)
        
        kt = map(elf, keys)
        vt = map(elf, values)
        cols = ', '.join(kt) + " => " + ', '.join(vt)
        entry = f"?[{','.join(map(lambda c: _safe_name(c.name), schema.columns))}] <- []"
        rel_def = ':replace ' + rel + ' {' + cols + '}'
        cmd1 = f"{entry}\n{rel_def}"

        # Add the Json Schema serialised definition to REL2JSON_SCHEMA
        js = json.dumps(schema.to_json_schema())
        entry2 = f"?[rel_name, urn, namespace, json_schema] <- [[\"{rel}\", \"{schema.urn}\", \"{schema.namespace}\",___\"{js}\"___]]"
        put2 = ':put ' + REL2JSON_SCHEMA + ' { rel_name, urn, namespace => json_schema }'
        cmd2 = f"{entry2}\n{put2}"

        # Add 'schema links' for every RefColumn in schema
        # ' { from: String, to: String => name: String }')
        rows = []
        for c in schema.columns:
            if c.ctype == ColType.REF:
                p1 = f"'{schema.urn}', '{c.urn}', '{c.name}'"
                id1 = uuid.uuid5(NAMESPACE_IVCAP, p1)
                rows.append(f"[{p1}, false, '{id1}']")

                revName = f"~{c.name}"
                p2 = f"'{c.urn}', '{schema.urn}', '{revName}'"
                id2 = uuid.uuid5(NAMESPACE_IVCAP, p2)
                rows.append(f"[{p2}, true, '{id2}']")

        # def lm(c: RefColumn):
        #     #return f"[\"{schema.urn}\", \"{c.urn}\", \"{c.name}\"]"
        #     return [schema.urn, c.urn, c.name]

        # rows = list(map(lm, filter(lambda c: c.ctype == ColType.REF, schema.columns)))
        if len(rows) > 0:
            row_s = f"[{','.join(rows)}]"
            entry3 = f"?[from, to, name, is_reverse, hash] <- {row_s}"
            put3 = ':put ' + REL_SCHEMA_REF + ' { from, to, name => is_reverse, hash }'
            #cmd3 = f"{entry3}\n{put3}"
            cmd3 = "{\n" + entry3 + "\n" + put3 + "\n}"
        else:
            cmd3 = ""

        # Insert all 
        cmd = "{\n" + cmd1 + "\n}\n{\n" + cmd2 + "\n}\n" + cmd3
        if verbose: print(cmd)
        return self.query(cmd)

    
    def get_schema(self, urn: str, verbose=False) -> Schema:
        """Return schema 'name' built from information stored in the database"""
        schema = self._urn2schema.get(urn)
        if schema != None:
            return schema

        # don't use f-string as we don't accidentially want to 'execute' schema
        # actually not sure if this is really a problem
        q = "?[json] := *sys__rel2json_schema[_1, '" + urn + "', _2, json ]"
        if verbose: print("cozo_connector#get_schema", q)
        r = self.query(q)
        if len(r) == 0:
            raise Exception(f"Unknown schema '{urn}'")
        if len(r) != 1:
            raise Exception("Unexpected result from db")
        js = r.iloc[0][0]
        j = json.loads(js)
        schema = Schema.from_dict(j)
        self._urn2schema[urn] = schema
        return schema

    def get_all_schemas_for_namespace(self, namespace: str, verbose=False) -> Sequence[Schema]:
        q = "?[json] := *sys__rel2json_schema[_1, _2, '" + namespace + "', json ]"
        if verbose: print("cozo_connector#get_all_schemas_for_namespace", q)
        r = self.query(q)
        
        def f(el):
            js = el.iloc[0]
            j = json.loads(js)
            return Schema.from_dict(j)
            
        return r.apply(f, axis=1).values.tolist()        

def _relation(schema: Schema, mapF: Callable[[Column], str]) -> str:
    keys = filter(lambda c: c.ctype == ColType.ENTITY, schema.columns)
    values = filter(lambda c: c.ctype != ColType.ENTITY, schema.columns)
    
    kt = map(mapF, keys)
    vt = map(mapF, values)
    rel = ', '.join(kt) + " => " + ', '.join(vt)
    return rel

def _safe_name(name):
    if name == ENTITY_COL_NAME:
        return 'ivcap_id'
    n = name.replace(':', '_').replace('.', '_')
    if n.startswith('_'):
        n = 'x' + n
    return n