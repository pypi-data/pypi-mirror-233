#!/usr/bin/env python
# coding: utf-8
#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#


import pandas as pd
import pandas.io.sql as sqlio
import numpy as np
import time 
import os
import re
from functools import reduce
import uuid

from datetime import datetime

from typing import Iterable, Callable, List, Tuple


import sys
import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
from psycopg2.extras import execute_batch

from ivcap_df.column import Schema, ColType, Column, RefColumn, IdColumn, ENTITY_COL_NAME

SCHEMA_TABLE_NAME = '__schema_definitions__'

class SqlConnector():
    
    def __init__(self, **kwargs):
        """
        Create a database connector with the following paramters:
        
        database – the database name (database is a deprecated alias)
        user – user name used to authenticate
        password – password used to authenticate
        host – database host address (defaults to UNIX socket if not provided)
        port – connection port number (defaults to 5432 if not provided)
        """
        self._db_params = kwargs
        database = kwargs.get('database')
        
        user = kwargs.get('user', os.getenv('USER'))
        password = kwargs.get('password')
        cred = user
        if password:
            cred = f"{cred}:{password}"
        
        host = kwargs.get('host')
        port = kwargs.get('port', '5432')
        self._url = f"postgresql+psycopg2://{cred}@{host}:{port}/{database}"
        print(f".... connection url {self._url}")


    def _show_psycopg2_exception(self, err):
        # get details about the exception
        err_type, err_obj, traceback = sys.exc_info()
        # get the line number when exception occured
        line_n = traceback.tb_lineno
        # print the connect() error
        print ("\npsycopg2 ERROR:", err, "on line number:", line_n)
        print ("psycopg2 traceback:", traceback, "-- type:", err_type)
        # psycopg2 extensions.Diagnostics object attribute
        print ("\nextensions.Diagnostics:", err.diag)
        # print the pgcode and pgerror exceptions
        print ("pgerror:", err.pgerror)
        print ("pgcode:", err.pgcode, "\n")

    def _connect(self) -> psycopg2.extensions.connection:
        conn = None
        try:
            print(f".... connecting to database server '{self._db_params.get('host')}:'{self._db_params.get('database')}'")
            conn = psycopg2.connect(**self._db_params)
            print(".... connection successful")

        except OperationalError as err:
            # passing exception to function
            show_psycopg2_exception(err)
            # set the connection to 'None' in case of error
            conn = None

        return conn

    def _wrap_execute_database(self, f: Callable[[psycopg2.extensions.cursor], None]):
        """Call 'f' to execute commands on postgres server."""
        conn = self._connect()
        conn.autocommit = True

        if conn!=None:
            try:
                cursor = conn.cursor();
                f(cursor)

                cursor.close()
                conn.close()
                print(".... transaction succeeded")

            except OperationalError as err:
                self._show_psycopg2_exception(err)
                conn = None
    
    def execute(self, cmd: str, vars = None) -> None:
        """Execute single command."""
        return self._wrap_execute_database(lambda cursor: cursor.execute(cmd, vars))

    def execute_batch(self, cmd: str, argslist, page_size=100) -> None:
        """Execute single command."""
        f = lambda cursor: execute_batch(cursor, cmd, argslist, page_size)
        return self._wrap_execute_database(f)
    
    def execute_query(self, cmd: str) -> List[Tuple]:
        """Execute single query and return result."""
        result = []
        def f(cursor):
            cursor.execute(cmd)
            rows = cursor.fetchall()
            result.extend(rows)

        self._wrap_execute_database(f)
        return result

    def execute_database(self, cmds: Iterable[str]):
        """Execute sequence of commands on postgres server."""

        def f(cursor): 
            for cmd in cmds:
                cursor.execute(cmd)

        return self._wrap_execute_database(f)
            
    # Define function using cursor.executemany() to insert the dataframe
    def insert_data_frame(self, df: pd.DataFrame, schema: Schema, ignoreDuplicateRecords = True):
        """Insert content of 'df' into table represented by 'schema'. If 'ignoreDuplicateRecords'
        is set, quietly drop any records in 'df' which have an identical 'record-id' to what is already
        stored in the table."""
        
        tableName = safe_table_name(schema.name)
        def f(cursor): 
            # sort columns according to schema
            # and turn UUID into str
            def f(h, c):
                name = c.name
                s = df[name]
                if c.ctype == ColType.ENTITY or c.ctype == ColType.REF or c.ctype == ColType.UUID:
                    s = s.apply(lambda el: str(el) if isinstance(el, uuid.UUID) else None)
                if c.ctype == ColType.DATETIME64_NS_TZ:
                    s = s.apply(lambda el: str(el.to_datetime64()) if not pd.isnull(el) else None)
                h[name] = s
                return h
            df2 = pd.DataFrame(reduce(f, schema.columns, {}))

            # Creating a list of tuples from the dataframe values
            tpls = [tuple(x) for x in df2.to_numpy()]

            #cols = ','.join(df.columns)
            cols = ','.join(map(lambda c: c.sql_col_name(), schema.columns))
            values = ['%s'] * len(df.columns)
            cmd = f"INSERT INTO %s(%s) VALUES(%s)"
            if ignoreDuplicateRecords:
                cmd += f" ON CONFLICT({ENTITY_COL_NAME}) DO NOTHING"
                
            sql = cmd % (tableName, cols, ','.join(values))
            #print(sql)
            cursor.executemany(sql, tpls)
            
        return self._wrap_execute_database(f)          

    def create_database(self, db_name: str, drop_first = False):
        """Create database on postgres server. If 'drop_first' is true, drop existing one first"""

        cmds = [f"DROP DATABASE IF EXISTS {db_name};"] if drop_first else []
        cmds.append(f"CREATE DATABASE {db_name};")
        self.execute_database(cmds)

    def drop_database(self, db_name: str):
        """Drop database on postgres server."""

        cmds = [f"DROP DATABASE IF EXISTS {db_name};"]
        self.execute_database(cmds)

    def query_to_df(self, sql: str) -> pd.DataFrame:
        """Execute 'sql' query and return result as dataframe."""
        dfx = sqlio.read_sql_query(sql, self._url)
#         with self._connect() as conn:
#             #dfx = pd.read_sql(sql, conn)
#             dfx = sqlio.read_sql_query(sql, conn)
        return dfx

    def create_db_table(self, schema: Schema, failQuietly = False):
        """Create a database table for entities described by 'schema'"""
        tableName = schema.sql_table()
        if self.table_exists(tableName):
            if failQuietly:
                return
            raise Exception(f"A table ('{tableName}') for this schema already exists")

        cols = ', '.join(map(lambda c: f"{c.sql_col_name()} {c.sql_type()}", schema.columns))
        tableName = safe_table_name(schema.name)
        cmds = [f"CREATE TABLE IF NOT EXISTS {tableName}({cols});"]
        return self.execute_database(cmds)
    
    def table_exists(self, name: str) -> bool:
        """ Return True if table 'name' exists in the database, otherwise return false."""
        schemaName = 'public'
        select = ("SELECT FROM information_schema.tables \n"
                     f"WHERE  table_schema = '{schemaName}'"
                     f"AND    table_name   = '{name}'")
        return self._exists_in_db(select)
    
    def _exists_in_db(self, select_q: str) -> bool:
        """Runs a SELECT EXISTS query on 'select_q' and returns TRUE if it indeed exists"""
        res = self.execute_query(f"SELECT EXISTS ({select_q});")
        if len(res) != 1:
            raise Exception(f"Expected single result row, but got '{res}'")
        t = res[0] # expect a tuple of 1 - either (True,) or (False,)
        if len(t) != 1:
            raise Exception(f"Expected tuple of length 1 but got '{t}''")
        return t[0]
    
    def create_schema_table(self):
        """Create a table for storing schema information"""
        tableName = SCHEMA_TABLE_NAME
        if self.table_exists(tableName):
            print(".. schema table already defined")
            return # Already set

        cmd = (f"CREATE TABLE IF NOT EXISTS {tableName} (\n"
               "id SERIAL,\n"
               "table_name TEXT,\n"
               "col_name TEXT,\n"
               "col_id SMALLINT,\n"
               "col_type SMALLINT,\n"
               "ref_schema TEXT\n"
               ");"
              )
        return self.execute_database([cmd])
        
    def persist_schema(self, schema: Schema, failQuietly = False):
        """Persist the description of 'schema' in the database."""
        self.create_schema_table() # make sure the repective table exists
        
        tableName = safe_table_name(schema.name)
        cols = ['table_name', 'col_name', 'col_id', 'col_type', 'ref_schema']
        
        if self._exists_in_db(f"SELECT FROM {SCHEMA_TABLE_NAME} WHERE table_name = '{tableName}'"):
            if not failQuietly:
                raise Exception(f"Schema '{schema.name}' already persisted")
            return
        
        def mf(el: (int, Column)):
            i, c = el
            ref = ''
            if isinstance(c, RefColumn):
                ref = c.schema_name()

            t = (tableName, c.name, i, c.ctype.value, ref)
            return t

        tpls = list(map(mf, enumerate(schema.columns)))
        
        def df(cursor): 
            values = ['%s'] * len(cols)
            sql = "INSERT INTO %s(%s) VALUES(%s)" % (SCHEMA_TABLE_NAME, ','.join(cols), ','.join(values))
            #print(sql)
            cursor.executemany(sql, tpls)
            
        return self._wrap_execute_database(df)
    
    def get_schema(self, name: str) -> Schema:
        """Return schema 'name' built from information stored in the database"""
        tname = safe_table_name(name)
        q = f"SELECT col_name, col_type, ref_schema from {SCHEMA_TABLE_NAME} WHERE table_name = '{tname}' ORDER BY col_id;"
        res = self.execute_query(q)
        if len(res) == 0:
            raise Exception(f"Cannot find schema '{name}'.")

        def to_col(r): 
            cname, ctype_i, ref = r
            ctype = ColType(ctype_i)
            if cname == 'record_id':
                return IdColumn()
            if ctype == ColType.REF:
                return RefColumn(cname, ref)
            else:
                return Column(cname, ctype)

        cols = map(to_col, res)
        return Schema(name, list(cols))        
       
    
def safe_table_name(name):
    return re.sub('-', '_', re.sub(':', '__', name)).lower()
