#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from __future__ import annotations # postpone evaluation of annotations 
from enum import Enum, unique
from dataclasses import dataclass
import numpy as np
import pandas as pd
from pandas import Series
from pandas.api.types import is_datetime64_any_dtype as is_datetime, is_string_dtype, is_bool_dtype
import re
import uuid
from typing import Any, Optional, Union, Dict

from .connector import Connector

NAMESPACE_IVCAP = uuid.uuid5(uuid.NAMESPACE_DNS, 'ivcap-1.0')
ENTITY_COL_NAME = '_id'

ANY_SCHEMA = 'urn:ivcap:schema:any.1'

@unique
class ColType(Enum):
    ENTITY = 'entity'
    UUID = 'uuid'
    URN = 'urn'
    URI = 'uri'
    ARTIFACT = 'artifact'
    REF = 'ref'
    FLOAT16 = 'float16'
    FLOAT32 = 'float32'
    FLOAT64 = 'float64'
    # FLOAT128 = 'float128'
    INT8 = 'int8'
    INT16 = 'int16'
    INT32 = 'int32'
    INT64 = 'int64'
    UINT8 = 'uint8'
    UINT16 = 'uint16'
    UINT32 = 'uint32'
    UINT64 = 'uint64'
    DATETIME64_NS_TZ = 'datetime_tz'
    DATE = 'date'
    STRING = 'string'
    BOOLEAN = 'boolean'   


JsonSchemaType = {
    # the first two are handled in their respective sub class
    # ColType.ENTITY: lambda c: {"type": "string", "description": "The unique identifier for this record",},    
    # ColType.UUID: lambda c: {"type": "string", "format": "uuid"},
    # ColType.REF: lambda c: {"type": "string", "format": "uri", "stype": "ref"},
    ColType.URN: lambda c: {"type": "string", "format": "uri"},
    ColType.URI: lambda c: {"type": "string", "format": "uri"},
    ColType.ARTIFACT: lambda c: {"type": "string", "format": "uri"},
    ColType.FLOAT16: lambda c: {"type": "number" },
    ColType.FLOAT32: lambda c: {"type": "number" },
    ColType.FLOAT64: lambda c: {"type": "number" },
    # ColType.FLOAT128: lambda c: {"type": "number" },
    ColType.INT8: lambda c: {"type": "integer" },
    ColType.INT16: lambda c: {"type": "integer" },
    ColType.INT32: lambda c: {"type": "integer" },
    ColType.INT64: lambda c: {"type": "integer" },
    ColType.UINT8: lambda c: {"type": "integer" },
    ColType.UINT16: lambda c: {"type": "integer" },
    ColType.UINT32: lambda c: {"type": "integer" },
    ColType.UINT64: lambda c: {"type": "integer" },
    ColType.DATE: lambda c: {"type": "string", "format": "date"},
    ColType.DATETIME64_NS_TZ: lambda c: {"type": "string", "format": "date-time"},
    ColType.STRING: lambda c: {"type": "string"},
    ColType.BOOLEAN: lambda c: {"type": "boolean"},
}

uuid_re = re.compile('^[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}$')

def validate_uuid(e) -> bool:
    if isinstance(e, uuid.UUID):
        return False
    if isinstance(e, str):
        return uuid_re.match(e) is None
    return True

def validate_urn(e) -> bool:
    if not isinstance(e, str):
        return False
    return e.startswith('urn:')

def validate_artifact(e) -> bool:
    if not isinstance(e, str):
        return False
    return e.startswith('urn:ivcap:artifact')

seriesValidator = {
    ColType.ENTITY: lambda s: next(filter(validate_urn, s), None) is None,
    ColType.UUID: lambda s: next(filter(validate_uuid, s), None) is None,
    ColType.URN: lambda s: next(filter(validate_urn, s), None) is None,
    ColType.URI: is_string_dtype, # TODO: Make more specific
    ColType.ARTIFACT: lambda s: next(filter(validate_artifact, s), None) is None,
    ColType.REF: lambda s: next(filter(validate_urn, s), None) is None,
    ColType.FLOAT16: lambda s: s.dtype == np.float16 or s.dtype.name == 'float16',
    ColType.FLOAT32: lambda s: s.dtype == np.float32 or s.dtype.name == 'float32',
    ColType.FLOAT64: lambda s: s.dtype == np.float64 or s.dtype.name == 'float64',
    # ColType.FLOAT128: lambda s: s.dtype == np.float128 or s.dtype.name == 'float128',
    ColType.INT8: lambda s: s.dtype == np.int8 or s.dtype == pd.Int8Dtype(),
    ColType.INT16: lambda s: s.dtype == np.int16 or s.dtype == pd.Int16Dtype(),
    ColType.INT32: lambda s: s.dtype == np.int32 or s.dtype == pd.Int32Dtype(),
    ColType.INT64: lambda s: s.dtype == np.int64 or s.dtype == pd.Int64Dtype(),
    ColType.UINT8: lambda s: s.dtype == np.uint8 or s.dtype == pd.UInt8Dtype(),
    ColType.UINT16: lambda s: s.dtype == np.uint16 or s.dtype == pd.UInt16Dtype(),
    ColType.UINT32: lambda s: s.dtype == np.uint32 or s.dtype == pd.UInt16Dtype(),
    ColType.UINT64: lambda s: s.dtype == np.uint64 or s.dtype == pd.UInt16Dtype(),
    ColType.DATETIME64_NS_TZ: lambda s: is_datetime(s),
    ColType.STRING: is_string_dtype,
    ColType.BOOLEAN: is_bool_dtype,
}

pandaTypes = {
    ColType.ENTITY: np.dtype('U'),
    ColType.UUID: np.dtype('U'),
    ColType.URN: np.dtype('U'),
    ColType.URI: np.dtype('U'),
    ColType.ARTIFACT: np.dtype('U'),
    ColType.REF: np.dtype('U'),
    ColType.FLOAT16: np.dtype('f2'),
    ColType.FLOAT32: np.dtype('f4'),
    ColType.FLOAT64: np.dtype('f8'),
    # ColType.FLOAT128: np.dtype('f16'),
    ColType.INT8: np.dtype('i1'),
    ColType.INT16: np.dtype('i2'),
    ColType.INT32: np.dtype('i4'),
    ColType.INT64: np.dtype('i8'),
    ColType.UINT8: np.dtype('u1'),
    ColType.UINT16: np.dtype('u2'),
    ColType.UINT32: np.dtype('u4'),
    ColType.UINT64: np.dtype('u8'),
    ColType.DATETIME64_NS_TZ: np.dtype('M8[ns]'),
    ColType.STRING: np.dtype('U'),
    ColType.BOOLEAN: np.dtype('?'),
}

    
@dataclass(frozen=True)
class Column:
    """Defines the name and type of a schema column."""

    @classmethod
    def from_dict(cls, name: str, definition: Dict[str, Any], required=True) -> Column:
        # {
        #    'type': 'string',
        #    'format': 'uri',
        #    'description': 'The unique identifier for this record'
        # }
        type = definition.get('type')
        if type is None:
            raise Exception(f"Missing 'type'in column description '{dict}'")
        stype = definition.get('stype')
        format = definition.get('format')
        if stype is None:
            # lets make a conservative bet
            if type == 'string':
                if format == 'data-time':
                    ctype = ColType.DATETIME64_NS_TZ
                else:
                    ctype = ColType.STRING
            elif type == 'number':
                ctype = ColType.FLOAT64
            elif type == 'integer':
                ctype = ColType.INT64
            else:
                # shouldn't really get here
                ctype = ColType.STRING
        else:
            # this may throw an exception
            ctype = ColType.__call__(stype)
        if ctype == ColType.ENTITY:
            return IdColumn()
        elif ctype == ColType.REF:
            return RefColumn.from_dict(name, definition, required)
        else:
            return cls(name, ctype, 
                description=definition.get('description'), 
                default=definition.get('default'), 
                required=required
            )

    name: str
    ctype: ColType
    description: str
    default: Any  # should really be of same type as 'ColType'implied
    required: bool

    def __init__(self, name: str, ctype: ColType, **kwargs):
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'ctype', ctype)
        object.__setattr__(self, 'description', kwargs.get('description'))
        object.__setattr__(self, 'default', kwargs.get('default'))
        object.__setattr__(self, 'required', kwargs.get('required', True))

    def is_nullable(self) -> bool:
        return not self.required

    def def_value(self):
        return self.default
    
    def is_valid(self, series: Series) -> bool:
        """Check if pandas 'series'is approriate for this column's defined 'ctype'"""
        vf = seriesValidator.get(self.ctype)
        if vf is None:
            raise Exception(f'Series validator for "{self.ctype}" is missing')
        return vf(series) if vf else False
    
    def is_equal(self, other: 'Column') -> bool:
        return self.name == other.name and self.ctype == other.ctype
    
    def to_json_schema(self):
        p = JsonSchemaType[self.ctype](self)
        p['stype'] = self.ctype.value
        if self.default != None:
            p['default'] = self.default
        if self.description != None:
            p['description'] = self.description
        return p

    def hash_value(self, v: Any) -> str:
        """Returns a string representation of 'v' for use in entity hash

        Args:
            v (Any): column value

        Returns:
            str: A string to be used in creating an entity ID
        """
        return str(v)
    
    def __repr__(self):
        return f"<Column name={self.name}, stype={self.ctype}>"
   
    
    # # TODO: Move to db_access.py
    # def sql_type(self) -> str:
    #     return sqlType[self.ctype]
    
    # # TODO: Move to db_access.py
    # def sql_col_name(self) -> str:
    #     return safe_sql_name(self.name)
    
@dataclass(frozen=True)
class IdColumn(Column):
    def __init__(self):
        super().__init__(ENTITY_COL_NAME, ColType.ENTITY)

    def is_nullable(self):
        # Required
        return False 

    def is_equal(self, other: Column) -> bool:
        if isinstance(other, IdColumn):
            return self.name == other.name
        return False

    def to_json_schema(self):
        return {
            'type': 'string',
            'stype': ColType.ENTITY.value,
            'format': 'uri',
            'description': 'The unique identifier for this record',
        }

    def get_urn_for(self, ref: str) -> str:
        """Returns the urn of the reference 'ref' assuming to be a value of this column type.
        
        Args:
            v (Any): column value

        Returns:
            str: The URN of referenced entity
        """
        if isinstance(ref, str):
            return ref
        else:
            raise Exception(f"Cannot resolve urn for '{ref}'")

    def hash_value(self, v: Any) -> str:
        """Returns a string representation of 'v' for use in entity hash

        Args:
            v (Any): column value

        Returns:
            str: An empty string as the IdColumn should not be part of the entity hash
        """
        return ''

    def __repr__(self):
        return f"<IdColumn>"

    # # TODO: Move to db_access.py
    # def sql_type(self) -> str:
    #     return 'UUID PRIMARY KEY'

@dataclass(frozen=True)
class RefColumn(Column):
    @classmethod
    def from_dict(cls, name: str, definition: Dict[str, Any], required=True) -> RefColumn:
        # 'targetSchema': {'$ref': 'urn:blue_growth:schema.quadrant.1'},
        # 'type': 'string',
        # 'stype': 'ref',
        # 'format': 'uri',        
        targetSchema = definition.get('targetSchema')
        if targetSchema is None:
            raise Exception(f"Missing 'targetSchema' in property '{name}'")
        schemaURN = targetSchema.get('$ref')
        if schemaURN is None:
            raise Exception(f"Missing '$ref' in 'targetSchema' in property '{name}'")
        return cls(name, schemaURN, required=required)

    _schema: 'Schema'
    urn: str
    
    def __init__(self, name: str, schema_or_urn: Optional[Union['Schema', str]] = ANY_SCHEMA , **kwargs):
        super().__init__(name, ColType.REF, **kwargs)
        if hasattr(schema_or_urn, 'is_schema'):
            schema = schema_or_urn
            urn = schema.urn
        else:
            schema = None
            urn = str(schema_or_urn)
            if not urn.startswith('urn:'):
                raise Exception(f"Expected a URN as schema reference, but got '{urn}'")

        object.__setattr__(self, '_schema', schema) # 'frozen'already applies to constructor
        object.__setattr__(self, 'urn', urn)
        from .schema import Schema # avoid circular dependency
        urnPrefix = Schema.urn2urn_prefix(urn)
        object.__setattr__(self, '_urnPrefix', urnPrefix)
        
    def is_equal(self, other: Column) -> bool:
        if isinstance(other, RefColumn):
            return self.name == other.name and self.schema_name() == other.schema_name()
        return False
        
    # # TODO: Move to db_access.py
    # def sql_type(self) -> str:
    #     return 'UUID'

    def schema_name(self) -> str:
        return self.urn

    def schema(self, connector: Connector = None) -> 'Schema':
        if self._schema == None:
            # Need to fetch it
            if connector is None:
                raise Exception("Missing 'connector' required for schema lookup")
            schema = connector.get_schema(self.urn)
            object.__setattr__(self, '_schema', schema) # 'frozen'already applies to constructor
        return self._schema
    
    def dataset(self, connector: Connector = None) -> 'DataSet':
        """Return all entities found for the references schema as a DataSet

        Args:
            connector (Connector, optional): Connector to retrieve data from. Defaults to None.

        Raises:
            Exception: _description_

        Returns:
            DataSet: A dataset containing all elements found for the referenced schema
        """
        schema = self.schema(connector)
        return schema.dataset(connector)

    def to_json_schema(self):
        return {
            'targetSchema': { "$ref": self.urn },
            'type': 'string', 
            'stype': ColType.REF.value,
            'format': 'uri',
            'description': f"Reference to schema '{self.urn}'",
        }
        
    def get_urn_for(self, ref: Union['DataSet', str]) -> str:
        """Returns the urn of the reference 'ref' assuming to be a value of this column type.
        
        

        Args:
            v (Any): column value

        Returns:
            str: The URN of referenced entity
        """
        if isinstance(ref, str):
            urn = ref
        elif hasattr(ref, 'id'):
            urn = ref.id
        else:
            raise Exception(f"Cannot find reference id for '{ref}'")
        if not urn.startswith(self._urnPrefix):
            raise Exception(f"'{urn}' is NOT a reference to schema '{self.urn}'")
        return urn

    def hash_value(self, v: Any) -> str:
        """Returns a string representation of 'v' for use in entity hash

        Args:
            v (Any): column value

        Returns:
            str: The URN of referenced entity
        """
        return self.get_urn_for(v)

    def __repr__(self):
        return f"<RefColumn urn={self.urn}, required={self.required}>"

    # # TODO: Move to db_access.py
    # def sql_schema_name(self) -> str:
    #     sname = self.schema_name()
    #     return save_sql_name(sname)

    # # TODO: Move to db_access.py
    # def sql_col_name(self) -> str:
    #     sname = self.schema_name()
    #     sname = sname if sname.endswith('_id') else f'{sname}_id'
    #     return safe_sql_name(sname)


def create_uuid(text) -> uuid.UUID: 
    return uuid.uuid5(NAMESPACE_IVCAP, text)

def safe_sql_name(name):
    return re.sub('-', '_', re.sub(':', '__', name)).lower()
