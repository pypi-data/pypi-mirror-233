#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#

# read version from installed package
try:  # Python < 3.10 (backport) 
    from importlib_metadata import version 
except ImportError: 
    from importlib.metadata import version 
try:
    __version__ = version("ivcap_df")
except Exception:
    __version__ = "???" # should only happen when running the local examples

from .schema import Schema, DEF_SCHEMA
from .column import Column, IdColumn, RefColumn, ColType, ENTITY_COL_NAME
from .connector import Connector, create_connector
from .dataSet import DataSet, DataItem
from .types import NotAuthorizedException
