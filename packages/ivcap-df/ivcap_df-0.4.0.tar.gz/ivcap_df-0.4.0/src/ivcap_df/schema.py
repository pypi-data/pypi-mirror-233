#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from __future__ import annotations # postpone evaluation of annotations 
from dataclasses import dataclass
from typing import Collection, List, Sequence, Optional, Dict, Any, Tuple, Callable, Union
from pandas import DataFrame, Series, isnull
import types
import uuid
from functools import reduce
import re
from graphviz import Digraph

from .types import URN

from .column import Column, IdColumn, ColType, NAMESPACE_IVCAP, ENTITY_COL_NAME
from .connector import Connector
from .dataSet import DataSet, DataItem

DEF_SCHEMA = "https://json-schema.org/draft/2019-09/hyper-schema"
SUPPORTED_SCHEMAS = [DEF_SCHEMA]

DOT_COLORS = [
    '#9e0142', '#d53e4f', '#f46d43', '#fdae61', '#fee08b',
    '#e6f598', '#abdda4', '#66c2a5', '#3288bd', '#5e4fa2',
]
DOT_ALPHA = '22'

@dataclass(frozen=True)
class Schema:
    """Defines the name columns of a schema."""

    @classmethod
    def load(cls, conn: Connector, name: str, namespace: str, version = 1) -> Schema:
        urn = cls.create_urn(name, namespace, version)
        return conn.get_schema(urn)

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> Schema:
        # {
        #   '$id': 'urn:blue_growth:schema.named_location.1',
        #   '$schema': 'https://json-schema.org/draft/2019-09/hyper-schema',
        #   'title': 'urn:blue_growth:schema.named_location.1',
        #   'description': 'Named location',
        #   'type': 'object',
        #   'properties': {
        #     'entity': {
        #       'type': 'string',
        #       'format': 'uri',
        #       'description': 'The unique identifier for this record'
        #     },
        #     'name': {'type': 'string'}
        #   },
        #   'required': ['entity', 'name']
        # }
        schema_name = dict.get('$schema')
        if not schema_name in SUPPORTED_SCHEMAS:
            raise Exception(f"Schema '{schema_name}' is not one of the supported schemas")

        required = dict.get('required', [])
        properties = dict.get('properties', {})
        columns = []
        for pname, pdef in properties.items():
            preq = pname in required
            col = Column.from_dict(pname, pdef, preq)
            columns.append(col)

        name, namespace, version = cls.parse_urn(dict.get('$id'))
        description = dict.get('description')
        return cls(name, namespace, description, columns, version)


    @classmethod
    def walk(cls, conn: Connector, schemas: Collection[Union['Schema', str]], verbose=False) -> DataFrame:
        """Starting from the schemas defined `schemaURNs` loads all schemas reachable through RefColumns
        
        Return a dataframe with each row representing one of the discovered schemas

        Args:
            conn (Connector): Connector to query data from
            schemas (Collection[Union[Schema, str]]): A list of schemas or schema URNs
            verbose (bool, optional): Be chatty

        Returns:
            DataFrame: [name:str, namespace:str, version:int, schema:Schema]
            
        """
        d = {}
        
        def w(urn):
            if urn in d.keys():
                return
            s = conn.get_schema(urn, verbose)
            d[urn] = s
            for c in s.columns:
                if c.ctype == ColType.REF:
                    w(c.schema_name())

        for el in schemas:
            if hasattr(el, 'urn'):
                urn = el.urn
            else:
                urn = el
            w(urn)
            
        # turn into a dataframe
        df = DataFrame(list(map(lambda urn: list(Schema.parse_urn(urn)), d.keys())),
                    columns=['name', 'namespace', 'version'],
                    index=d.keys())
        df['schema'] = d.values()
        return df

    @classmethod
    def create_urn(cls, name: str, namespace: str, version = 1) -> str:
        urn = f"urn:{namespace}:schema:{name}.{version}"
        return urn

    @classmethod
    def parse_urn(cls, urn: str) -> Tuple[str, str, int]:
        match = re.search(r"urn:([^:]*):schema[:\.]([^\.]*)\.*([0-9]*)$", urn)
        if not match:
            raise Exception(f"Cannot parse schema urn '{urn}'")
        namespace = match.group(1)
        name = match.group(2)
        version_s = match.group(3)
        if version_s is None:
            version = 1
        else:
            version = int(version_s)
        return (name, namespace, version)

    @classmethod
    def urn2urn_prefix(cls, urn: str) -> str:
        name, namespace, version = cls.parse_urn(urn)
        return f"urn:{namespace}:{name}.{version}#"

    @classmethod
    def to_dot(cls, schemas: Sequence['Schema'], digraph:Optional[Digraph]=None, fontSize=12) -> Digraph:
        """Return a dot DIgraph which describes the properties of the schemas
        and the links/references between them.
        
        Calling this from inside Jupyter will display the graph assuming graphviz is installed

        Args:
            schemas (Sequence[Schema]): _description_

        Returns:
            Digraph: A graphiz Digraph
        """
        
        if digraph is None:
            digraph = Digraph(node_attr={'fontsize':str(fontSize)}, edge_attr={'fontsize':str(fontSize)})
            digraph.attr(rankdir='LR')

        def add_schema(schema, colors):
            def short_gname(name):
                pa = name.split(':')
                if len(pa) > 3:
                    return name.split(':')[3]
                else: 
                    print(f"Misformatted urn '{pa}'")
                    return "???"

            attr = []
            refs = []
            name = short_gname(schema.urn)
            for c in schema.columns:
                req = '' if c.required else '?'
                if c.ctype == ColType.ENTITY:
                    continue
                elif c.ctype == ColType.REF:
                    refs.append((c.name + req, short_gname(c.schema_name())))
                else:
                    attr.append(f"{c.name}{req}: {c.ctype.value}")

            left = lambda s: s + ' \l'
            digraph.node(name, f"{name}|{' '.join(map(left, attr))}", shape = "record", style='filled', fillcolor=colors[schema.namespace])
            for (label, ref) in refs:
                digraph.edge(name, ref, label=label)

        def color_map():
            colors = {}
            for s in schemas:
                colors[s.namespace] = 'white' # default
            citems = colors.keys()
            cnt = len(citems)
            if len(citems) > 1:
                # Assign colors from DOT_COLORS
                spread = 1.0 * (len(DOT_COLORS) - 1) / (cnt - 1)
                for i, k in enumerate(citems):
                    colors[k] = f"{DOT_COLORS[round(i * spread)]}{DOT_ALPHA}"
            return colors

        for schema in schemas:
            add_schema(schema, color_map())
        return digraph

    name: str
    namespace: str
    version: int
    urn: str
    description: str
    columns: Sequence[Column]
    idColumn: Column
    urnPrefix: str
    _ds: DataSet

    def __init__(self, 
                 name: str, 
                 namespace: str, 
                 description: str, 
                 columns: Sequence[Column], 
                 version = 1
    ):
        """Create and return an instance of a Schema.

        Args:
            name (str): A short name of schema
            namespace (str): The namespace for this schema
            description (str): A description added to the schema
            columns (Sequence[Column]): A sequence of `Column` instances describing the attributes of the schema
            version (int, optional): An optional version of this schema. Defaults to 1.

        Raises:
            Exception: _description_
        """
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'namespace', namespace)
        object.__setattr__(self, 'version', version)
        urn = self.__class__.create_urn(name, namespace, version)
        object.__setattr__(self, 'urn', urn)
        urnPrefix = self.__class__.urn2urn_prefix(urn)
        object.__setattr__(self, 'urnPrefix', urnPrefix)
        object.__setattr__(self, 'description', description)
        idc = None
        for i, c in enumerate(columns):
            if isinstance(c, IdColumn):
                if i == 0:
                    idc = c
                else:
                    raise Exception('Do NOT define an <IdColumn> unless in first position')
        if idc is None:
            idc = IdColumn()
            columns.insert(0, idc)
        object.__setattr__(self, 'columns', columns)
        object.__setattr__(self, 'idColumn', idc)
        object.__setattr__(self, '_ds', DataSet(self))

    def __getitem__(self, colName: str) -> Column:
        for c in self.columns:
            if c.name == colName:
                return c
        raise KeyError(colName)
    
    def entity(self, **kwargs) -> DataItem:
        if not self._ds:
            object.__setattr__(self, '_ds', DataSet(self))
        return self._ds.add(**kwargs)

    def stage_entities(self, df: DataFrame, mapper = None, indexF=None) -> Series:
        """Create entities according to this schema for every row in 'df'

        Args:
            df (DataFrame): dataframe holding an entity in every row
            mapper (_type_, optional): An optional mapper frpm row to named property. Defaults to None.
            indexF (_type_, optional): Optional property name which should be used as index for returned series. Defaults to None.

        Raises:
            Exception: If no mapper was found for a mandatory property

        Returns:
            Series: A series containing the respective DataItem for each row in 'df'
        """
        if mapper is None:
            mapper = {}
        valCols= list(filter(lambda c: c != self.idColumn, self.columns))
        dfCols = df.columns.to_list()
        
        def create_mapper(name, mapper):
            if isinstance(mapper, types.LambdaType):
                return mapper
            if isinstance(mapper, str):
                # 'mapper' should be column name in df
                if mapper in dfCols:
                    return def_mapper(mapper)
                else:
                    raise Exception(f"mapper name '{mapper}' for '{name}' is not a dataframe column. Use a lambda function if this is supposed to be a constant")
            # looks like a constant
            return lambda r: mapper
                  
        def def_mapper(cname):
            # this is necessary as python doesn't create a new scope inside a loop only inside a function
            return lambda r: r[cname]
        
        for vc in valCols:
            cname = vc.name
            if cname in mapper:
                mapper[cname] = create_mapper(cname, mapper[cname])
            elif cname in dfCols:
                mapper[cname] = def_mapper(cname)
            elif vc.required:
                raise Exception(f"no mapper found for required column '{cname}'")
                
        if isinstance(indexF, str):
            name = indexF
            indexF = lambda r, d: d[name]
            
        def f(r):
            d = {}
            for (k, m) in mapper.items():
                d[k] = m(r)
            try:
                e = self.entity(**d)
            except Exception as ex:
                raise Exception(f"While creating entity for '{d}' - {ex}")
                
            if indexF:
                idx = indexF(r, d)
            else:
                idx = e.id.split('#')[1]
            return Series([idx, e], index=['idx', '_'])

        ds = df.apply(f, axis=1).set_index('idx').squeeze()
        self._ds.add_data_items(ds)
        return ds

    def is_valid(self, 
                 df: DataFrame, 
                 verbose: Optional[bool] = False
                 ) -> bool:
        cols = {}
        for c in self.columns:
            cols[c.name] = c
        for colName in df.columns:
            col = cols.get(colName)
            if col is None:
                if verbose:
                    print(f'is_valid: Unknown dataframe column "{colName}"')
                return False
            series = df[colName]
            if not col.is_valid(series):
                if verbose:
                    print(f'is_valid: Dataframe column "{colName}:{series.dtype}" doesn\'t match schema type "{col.ctype.name}".')
                return False
        return True

    def is_equal(self, other: Schema) -> bool:
        """Return True if 'other' is an identical schema definition"""
        if self.urn != other.urn:
            print('.. names differ')
            return False
        if len(self.columns) != len(other.columns):
            print('.. number of columns differ')
            return False
        n2c = {}
        for c in self.columns:
            n2c[c.name] = c
        for oc in other.columns:
            c = n2c.get(oc.name)
            if not c:
                print(f".. unknown column '{oc.name}'")
                return False
            if not c.is_equal(oc):
                print(f".. columns '{oc.name}' differ - {c} - {oc}")
                return False
        return True

    def column(self, name: str) -> Column:
        """Return the column instance for `name`

        Args:
            name (str): Name of column

        Returns:
            Column: instance of 'Column' or None if there is no column with that name
        """
        return next(filter(lambda c: c.name == name, self.columns), None)
    
    @property
    def column_names(self) -> List[str]:
        """Return a list of all column names"""
        return list(map(lambda c: c.name, filter(lambda c: c != c.ctype != ColType.ENTITY, self.columns)))

    def property(self, name: str) -> Column:
        """Alias for 'column'"""
        return self.column(name)
    
    def persist(self, 
                connector: Connector, 
                only_entities: Optional[bool] = False, 
                policy: Optional[URN] = None,
                verbose: Optional[bool] = False):
        """Persist this schema as well as all staged entities

        Args:
            connector (Connector): Connector to persistence provider
            only_entities (bool, optional): If true do NOT persist schema definition. Defaults to True.
            verbose (bool, optional): Be chatty. Defaults to False.
        """
        if not only_entities:
            connector.register_schema(self, policy=policy, verbose=verbose)
        if not self._ds.isempty():
            self.persist_dataframe(connector, self._ds.df, policy=policy, verbose=verbose)

    def create_dataframe(self,
                         data: Sequence[Sequence[Any]], 
                         columns:Optional[Sequence[str]] = None, 
                         indexF: Optional[Callable[[Sequence[Any]], str]] = None,
                         addEntityColumn=False,
                         ) -> DataFrame: 
        """Creates and returns a dataframe with columns set according to this schema.

        Args:
            data (Sequence[Sequence[Any]]): A sequence of rows to insert into the dataframe
            columns (Optional[Sequence[str]], optional): An optional list of column names if `data` is not ordered according to schema order
            indexF (Optional[Callable[[Sequence[Any]], str]], optional): If defined, this function, given the row sequencem should return the index for this row.
            addEntityColumn (bool, optional): If true, add an `entity` column which combines the urn of this schema with the row's index (or `indexF`). Defaults to False.

        Raises:
            Exception: If `columns` contains a columns name which is not an attribute of this schema

        Returns:
            DataFrame: a dataframe with columns as defined by this schema and content as defined by `data`
        """
        colNames = list(map(lambda c: c.name, filter(lambda c: c.ctype != ColType.ENTITY, self.columns)))
        if not columns:
            columns = colNames
        else:
            for c in columns:
                if c not in colNames:
                    raise Exception(f"Column name '{c}' not defined in schema")
                
        def def_index(r):
            return self.create_uuid(''.join([str(c) for c in r]))
                            
        if not indexF:
            indexF = def_index
            
        df = DataFrame(data, columns=columns, index=map(indexF, data))

        if addEntityColumn:
            idx = Series(map(lambda v: self.urnPrefix + str(v).replace(' ','_').replace(':','_').lower(), df.index.values))
            df.insert(0, ENTITY_COL_NAME, idx.values)
        else:
            df.index.rename('entity', inplace=True)
        return df
    
    def persist_dataframe(self, 
        connector: Connector,
        df: DataFrame, 
        index_f: Optional[Callable[[Sequence[Any]], str]] = None,
        policy: Optional[URN] = None,
        verbose: Optional[bool] =False,
    ) -> DataFrame:
        if index_f != None or ENTITY_COL_NAME not in df.columns:
            df = self.add_entity_id(df, index_f, True)
        connector.insert_data_frame(df, self, policy=policy, verbose=verbose)
        return df
    
    def dataset(self, connector: Connector = None) -> 'DataSet':
        """Return all entities found for the references schema as a DataSet

        Args:
            connector (Connector, optional): Connector to retrieve data from. Defaults to None.

        Raises:
            Exception: _description_

        Returns:
            DataSet: A dataset containing all elements found for the referenced schema
        """
        from .dataSet import DataSet # defer import to avoid circular dependency
        df = connector.get_all_for_schema(self)
        self._ds.add_df(df)
        return DataSet(self, dataFrame=df)

    def get_current_dataset(self) -> 'DataSet':
        """Return the dataset currently associated with this schema.

            This dataset contains all the items previously fetched via `dataset` or 
            added one by one through `entity`.

        Returns:
            DataSet: A dataset containing all elements currently maintained by this schema instance
        """
        if not self._ds:
            object.__setattr__(self, '_ds', DataSet(self))
        return self._ds

    def query_one(self, query: str, local_dict: Dict[str, Any]={}, failQuietly=False) -> DataItem:
        """Try to find a single data item which is returned by `query`.
        
        Args:
            query (str): Query string as defined by panda's DataFrame#query
            local_dict (Dict[str, Any], optional): Optionally maps '@' variables in `query` to values. Defaults to {}.
            failQuietly (bool, optional): If nothing found and set to true return None, otherwise raise exception. Defaults to False.

        Raises:
            Exception: If none or multiple entities are found and 'failQuietly' is set to False

        Returns:
            DataItem: DataItem found as result of query
        """
        return self._ds.query_one(query, local_dict, failQuietly)
    
    def query(self, query: str, local_dict: Dict[str, Any]={}) -> Sequence[DataItem]:
        """Returns a sequence of DataItems which fulfill `query`.
        
        Args:
            query (str): Query string as defined by panda's DataFrame#query
            local_dict (Dict[str, Any], optional): Optionally maps '@' variables in `query` to values. Defaults to {}.

        Returns:
            Sequence[DataItem]: Sequence of data items contained in this set
        """
        return self._ds.query(query, local_dict)
        
    def create_uuid(self, text) -> uuid.UUID: 
        return uuid.uuid5(NAMESPACE_IVCAP, self.urnPrefix + str(text))
    
    def create_entity_id(self, hashes: Sequence[str]) -> str:
        s = ''.join(hashes)
        return self.urnPrefix + str(self.create_uuid(s))

    def create_entity_id_mapper(self, indexF: Optional[Callable[[Sequence[Any]], str]] = None) -> Callable[[Sequence[Any]], str]:
        if not indexF:
            indexF = lambda r: self.create_uuid(''.join([str(c) for c in r]))
            
        def map(rec):
            idx = indexF(rec)
            return self.urnPrefix + str(idx).replace(' ','_').replace(':','_').lower()
            
        return map

    
    def add_entity_id(self, 
                      df: DataFrame, 
                      indexF: Optional[Callable[[Sequence[Any]], str]] = None, 
                      inplace=False,
                      override=False,
                      ) -> DataFrame:
        """Add an Column.ENTITY_COL_NAME column holding either the result of indexF or a UUIDv5 calculated over the content of the entire row"""

        if not override and ENTITY_COL_NAME in df.columns:
            # already has entity column
            return df
        
        entityMapper = self.create_entity_id_mapper(indexF)
        idx = Series(df.apply(entityMapper, axis=1))
        if not inplace:
            df = df.copy()
        if ENTITY_COL_NAME in df.columns:
            del df[ENTITY_COL_NAME]
        df.insert(0, ENTITY_COL_NAME, idx.values)
        return df

    # {
    #    "$schema": "http://json-schema.org/draft-04/schema#",
    #    "title": "Product",
    #    "description": "A product from Acme's catalog",
    #    "type": "object",
    #    "properties": {
    #       "id": {
    #          "description": "The unique identifier for a product",
    #          "type": "integer"
    #       },
    #       "price": {
    #          "type": "number",
    #          "minimum": 0,
    #          "exclusiveMinimum": true
    #       }
    #    },
    #    "required": ["id", "name", "price"]
    # }
    def to_json_schema(self, schema=DEF_SCHEMA):
        properties = {}
        for c in self.columns:
            properties[c.name] = c.to_json_schema()
        required = list(map(lambda c: c.name, filter(lambda c: c.required, self.columns)))
        return {
            "$id": self.urn,
            "$schema": schema,
            #"base": "https://example.com/api/",
            "title": self.urn,
            "description": self.description,
            "type": "object",
            "properties": properties,
            "required": required,
        }
            
    def df_to_json(self, df):
        def f(h, c):
            name = c.name
            s = df[name]
            if c.ctype == c.ctype == ColType.UUID:
                s = s.apply(lambda el: str(el) if isinstance(el, uuid.UUID) else None)
            if c.ctype == ColType.DATETIME64_NS_TZ:
                s = s.apply(lambda el: str(el.to_datetime64()) if not isnull(el) else None)
            h[name] = s
            return h
        
        df2 = DataFrame(reduce(f, self.columns, {}))
        return df2.to_json(orient='records', indent=2)

    def is_schema(self) -> bool:
        """Primarily used by RefColumn to identify a Schema object without importing this class (circular dependency)"""
        return True

    def graph(self, depth=99, digraph:Optional[Digraph]=None, fontSize=12, verbose=False) -> Digraph:
        """Return a Graphviz Digraph showing the dependency graph for all items currently known to this schema.

        Args:
            depth (int, optional): Number of levels to expand to. Defaults to 99.
            digraph (Optional[Digraph], optional): Digraph object. If set to None, one is being created. Defaults to None.
            fontSize (int, optional): Font size for node and edge label if digraph is created internally . Defaults to 12.
            verbose (bool, optional): If set report on items visited. Defaults to False.

        Returns:
            Digraph: The digraph nodes and edges have been added
        """
        return self._ds.graph(depth=depth, digraph=digraph, fontSize=fontSize, verbose=verbose)

    def __repr__(self):
        def col_name(c):
            n = c.name
            if not c.required:
                n += '?'
            return n
        cols = list(map(col_name, self.columns))
        return f"<Schema urn={self.urn}, columns={cols}>"
