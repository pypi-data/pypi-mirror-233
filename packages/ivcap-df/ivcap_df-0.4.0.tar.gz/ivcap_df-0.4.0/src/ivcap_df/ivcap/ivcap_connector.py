#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
import pandas as pd
import pandas.io.sql as sqlio
import os
import uuid
from sys import maxsize as MAXSIZE

from datetime import datetime

from typing import IO, Any, Dict, Optional, Sequence
from ivcap_df.connector import Connector

from ivcap_df.schema import SUPPORTED_SCHEMAS

from ivcap_client import IVCAP, Metadata, Artifact

import os

from ivcap_df import Schema, ColType, ENTITY_COL_NAME
from ivcap_df.types import URN

class IvcapConnector(Connector):

    def __new__(cls, *args, **kwargs) -> 'IvcapConnector':
        kwargs['__recursive__'] = True
        return super().__new__(cls, *args, **kwargs)

    def __enter__(self) -> 'IvcapConnector':
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type or exc_value or traceback:
            print(f"... exit: exc_type={exc_type}, exc_value={exc_value}, traceback={traceback}")

    def __init__(self, **kwargs):
        """
        Create an IVCAP client with the following paramters:
        
        url - URL of the IVCAP cluster API  [IVCAP_URL]
        jwt - Access token [IVCAP_JWT]
        account_id - Account ID to use [IVCAP_ACCOUNT_ID]
        host - Set if cluster is accessed through an ssh tunnel
        """
        url = kwargs.get('url', os.getenv('IVCAP_URL', 'https://api.ivcap.net'))
        token = kwargs.get('jwt', os.getenv('IVCAP_JWT'))
        account_id = kwargs.get('account_id', os.getenv('IVCAP_ACCOUNT_ID'))
        # headers = {}
        # if kwargs.get('host'):
        #     headers['Host'] = kwargs['host']
        
        self._ivcap = IVCAP(url=url, token=token, account_id=account_id)
        #print(f".... connection url {self._client}")


    def insert_record(self, rec_id: str, record: Dict[str, Any], schema: Schema, verbose=False) -> str:
        """Insert a single record defined by 'schema'."""

        dcols = record.keys()
        cols = list(filter(lambda c: c.ctype != ColType.ENTITY and c.name in dcols, schema.columns))
        mandatory = set(filter(lambda c: c.required and c.ctype != ColType.ENTITY, schema.columns))
        if mandatory.intersection(set(cols)) != mandatory:
            missing = ','.join(map(lambda c: c.name, mandatory - set(cols)))
            raise Exception(f"Missing manadatory column(s) '{missing}'")


        # sort columns according to schema
        # and turn UUID into str
        def f(r):
            rec = {"$schema": schema.urn}
            for col in cols:
                el = r[col.name]
                if col.ctype == ColType.UUID:
                    el = str(el) if isinstance(el, uuid.UUID) else None
                elif col.ctype == ColType.REF:
                    if not pd.isnull(el):
                        pass # already in the right format
                    else:
                        el = "urn:error:undefined" if col.required else None
                elif col.ctype == ColType.DATETIME64_NS_TZ:
                    try:
                        el = str(el.to_datetime64()) if not pd.isnull(el) else None
                    except Exception as ex:
                        if isinstance(el, datetime):
                            el = el.isoformat()
                        else:
                            if isinstance(el, str):
                                pass # ok, already a string. TODO: Maybe we should check if string is properly formatted
                            else:
                                raise Exception(f"Column '{col.name}' doesn't contain datetime value - '{ex}'")
                    
                if el == None or pd.isna(el):
                    continue
                rec[col.name] = el
            return {
                "entity": rec_id,
                "schema": schema.urn,
                "aspect": rec
            }

        mr = f(record)
        md = self._ivcap.add_metadata(**mr)
        return md.urn
    
    def insert_data_frame(self, 
                          df: pd.DataFrame, 
                          schema: Schema, 
                          policy: Optional[URN] = None,
                          ignore_duplicate_records: Optional[bool] = True,
                          verbose=False):
        """Insert content of 'df' into table represented by 'schema'. If 'ignore_duplicate_records'
        is set, quietly drop any records in 'df' which have an identical 'record-id' to what is already
        stored in the table."""

        dcols = df.columns.to_list()
        cols = list(filter(lambda c: c.ctype != ColType.ENTITY and c.name in dcols, schema.columns))
        mandatory = set(filter(lambda c: c.required and c.ctype != ColType.ENTITY, schema.columns))
        if mandatory.intersection(set(cols)) != mandatory:
            missing = ','.join(map(lambda c: c.name, mandatory - set(cols)))
            raise Exception(f"Missing manadatory column(s) '{missing}'")


        # sort columns according to schema
        # and turn UUID into str
        def f(r):
            rec = {"$schema": schema.urn}
            for col in cols:
                el = r[col.name]
                if col.ctype == ColType.UUID:
                    el = str(el) if isinstance(el, uuid.UUID) else None
                elif col.ctype == ColType.REF:
                    el = el if not pd.isnull(el) else "urn:error:undefined"
                elif col.ctype == ColType.DATETIME64_NS_TZ:
                    try:
                        el = str(el.to_datetime64()) if not pd.isnull(el) else None
                    except Exception as ex:
                        raise Exception(f"Column '{col.name}' doesn't contain datetime value - '{ex}'")

                    
                if el == None or pd.isna(el):
                    continue
                rec[col.name] = el
            return {
                "entity": r[ENTITY_COL_NAME],
                "schema": schema.urn,
                "aspect": rec,
                "policy": policy
            }

        records = df.apply(f, axis=1)
        print(f"... Uploading {len(records)} meta record(s) ", end='')
        def mf(r):
            self._ivcap.add_metadata(**r)
            if verbose:
                print('.', end='')

        rid = list(map(mf, records))
        if verbose:
            print(f" Done")
        return rid

    def query_to_df(self, sql: str) -> pd.DataFrame:
        """Execute 'sql' query and return result as dataframe."""
        dfx = sqlio.read_sql_query(sql, self._url)
#         with self._connect() as conn:
#             #dfx = pd.read_sql(sql, conn)
#             dfx = sqlio.read_sql_query(sql, conn)
        return dfx

            
    def register_schema(self, schema: Schema, policy = None,fail_quietly = False, verbose=False):
        """Register the 'schema' in the metadata registry."""
        try:
            self._ivcap.add_metadata(entity=schema.urn, aspect=schema.to_json_schema(), policy=policy)
        except Exception as exec:
            if not fail_quietly:
                raise exec 

    def get_schema(self, name: str, verbose=False) -> Schema:
        """Return schema 'name' built from information stored in the database"""
        for schema_type in SUPPORTED_SCHEMAS:
            m = list(self._ivcap.search_metadata(entity=name, schema_prefix=schema_type))
            if m and len(m) > 0:
                break
        if len(m) != 1:
            raise Exception(f"cannot find schema '{name}'")
        schema = Schema.from_dict(m[0].aspect)
        return schema
    
    def get_all_for_schema(self, 
                           schema: Schema, 
                           *, 
                           entity: Optional[str]=None,
                           filter: Optional[str]=None,
                           at_time: Optional[datetime]=None,
    ) -> pd.DataFrame:
        """Get all accessible entities of type `Schema`.
        
        This query is primarily used for schemas representing 'controlled vocabulary'.

        Args:
            schema (Schema): Schema of elements queried.
            entity (URN): If set, restrict to records for this entity 
            filter (str): If set, additionally restrict to records passing this filter,
            at_time(datetime): Return records 'known' at that time

        Returns:
            pd.DataFrame: A dataframe holding all accessible entities
        """
        cnames = list(map(lambda c: c.name, schema.columns))

        def m(rec: Metadata):
            row = []
            aspect = rec.aspect
            for c in schema.columns:
                if c.ctype == ColType.ENTITY:
                    row.append(rec.entity)
                #elif c.ctype == ColType.REF:
                else:
                    v = aspect.get(c.name)
                    if v == None:
                        v = c.default
                    row.append(v)

            return row
        
        rows = list(map(m, self._ivcap.search_metadata(
            schema_prefix=schema.urn, entity=entity,
            filter=filter, at_time=at_time)))
        df = pd.DataFrame(rows, columns=cnames)
        return df

    def get_all_schemas_for_namespace(self, name: str, verbose=False) -> Sequence[Schema]:
        raise Exception("not implemented")

    def close(self):
        pass

    def __repr__(self):
        return f"<IvcapConnector url={self._ivcap.url}>"

    def upload_artifact(self,
        *,
        name: Optional[str] = None,
        file_path: Optional[str] = None,
        io_stream: Optional[IO] = None,
        content_type:  Optional[str] = None, 
        content_size: Optional[int] = -1, 
        chunk_size: Optional[int] = MAXSIZE, 
        retries: Optional[int] = 0, 
        retry_delay: Optional[int] = 30
    ) -> Artifact:
        """Uploads content which is either identified as a `file_path` or `io_stream`. In the
        latter case, content type need to be provided.

        Args:
            file_path (Optional[str]): File to upload
            io_stream (Optional[IO]): Content as IO stream. 
            content_type (Optional[str]): Content type - needs to be declared for `io_stream`.
            content_size (Optional[int]): Overall size of content to be uploaded. Defaults to -1 (don't know).
            chunk_size (Optional[int]): Chunk size to use for each individual upload. Defaults to MAXSIZE.
            retries (Optional[int]): The number of attempts should be made in the case of a failed upload. Defaults to 0.
            retry_delay (Optional[int], optional): How long (in seconds) should we wait before retrying a failed upload attempt. Defaults to 30.
        """
        return self._ivcap.upload_artifact(
            name=name,
            file_path=file_path,
            io_stream=io_stream,
            content_type=content_type,
            content_size=content_size,
            chunk_size=chunk_size,
            retries=retries,
            retry_delay=retry_delay,
        )
    
# def _process_error(method: str, r: Response, verbose: bool):
#     if verbose:
#         print(f"Error: {method} failed with {r.status_code} - {r.content}")
#     if r.status_code == 401:
#         raise NotAuthorizedException()
#     pass
