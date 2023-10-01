#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
import types
import re
import pandas as pd
import numpy as np


from ivap_provenance import Schema, IdColumn, RefColumn, Column, ColType
from ivcap_df.sql.sql_connector import SqlConnector

sqlType = {
    ColType.UUID: 'UUID',
    ColType.REF: lambda s: f'UUID REFERENCES {_sql_name(s.ref_schema)}',
    ColType.REF: lambda s: f'UUID', ### NOTE: Remove when having bootstrapped other tables
    ColType.FLOAT16: 'FLOAT4',
    ColType.FLOAT32: 'FLOAT4',
    ColType.FLOAT64: 'FLOAT8',
    ColType.FLOAT128: 'FLOAT8',
    ColType.INT8: 'SMALINT',
    ColType.INT16: 'SMALINT',
    ColType.INT32: 'INTEGER',
    ColType.INT64: 'BIGINT',
    ColType.UINT8: lambda s: sqlType[ColType.INT8], # no U type available
    ColType.UINT16: lambda s: sqlType[ColType.INT16],
    ColType.UINT32: lambda s: sqlType[ColType.INT32],
    ColType.UINT64: lambda s: sqlType[ColType.INT64],
    ColType.DATETIME64_NS_TZ: 'TIMESTAMPTZ',
    ColType.STRING: 'TEXT',
    ColType.BOOLEAN: 'BOOLEAN',
}

def _sql_name(orig: str) -> str:
    """Returns a sql 'friendly' name.
    
    Names in SQL must begin with a letter (a-z) or underscore (_). Subsequent characters in a 
    name can be letters, digits (0-9), or underscores. """
    return re.sub(r'[^a-zA-Z0-9_]', '__', orig)

def col2create(col: Column) -> str:
    tf = sqlType.get(col.ctype)
    #print('TYPE', isinstance(tf, types.LambdaType))
    if tf is None:
        raise Exception(f'SQL type mapper for "{col.ctype}" is missing')
    stype = tf(col) if isinstance(tf, types.LambdaType) else tf
    if isinstance(col, IdColumn):
        stype += ' PRIMARY KEY'
    return f'{col.name} {stype}'

def create_database_from_schema(schema: Schema) -> str:
    cols = (',\n'.join(list(map(col2create, schema.columns))))
    table_name = _sql_name(schema.name)
    return f'CREATE TABLE IF NOT EXISTS {table_name} (\n{cols}\n);'

def append_data_frame(df: pd.DataFrame, schema: Schema, db: SqlConnector):
    """Append data frame to relation defined by 'schema'.
    
    NOTE: This is VERY non-optimal
    """
    if not schema.is_valid(df):
        raise Exception('dataframe is not compatible with schema')
    table_name = _sql_name(schema.name)
    # Creating a list of tupples from the dataframe values
    tpls = [tuple(x) for x in df.to_numpy()]

    cols = ','.join(df.columns)
    values = ['%s'] * len(df.columns)
    sql = "INSERT INTO %s(%s) VALUES(%s)" % (table_name, cols, ','.join(values))

    db.execute_batch(sql, tpls)

def query_to_df(sql: str, db: SqlConnector) -> pd.DataFrame:
    """Execute 'sql' query and return result as dataframe."""
    return db.query_to_df(sql)
