#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from __future__ import annotations # postpone evaluation of annotations 
from typing import Any, Dict, Optional, Callable, Sequence, Tuple, Union
from dataclasses import dataclass
from pandas import DataFrame, Series
from typing import TYPE_CHECKING, Sequence
from graphviz import Digraph

from .column import ColType, ENTITY_COL_NAME
if TYPE_CHECKING:
    from .schema import Schema


@dataclass(frozen=True)
class DataItem():
    @classmethod
    def graph_many(cls, *seedItems: Sequence['DataItem'], depth=99, digraph:Optional[Digraph]=None, fontSize=12, verbose=False) -> Digraph:
        """Return a Graphviz Digraph showing the dependency graph for items in `*seedItems`.

        Args:
            depth (int, optional): Number of levels to expand to. Defaults to 99.
            digraph (Optional[Digraph], optional): Digraph object. If set to None, one is being created. Defaults to None.
            fontSize (int, optional): Font size for node and edge label if digraph is created internally . Defaults to 12.
            verbose (bool, optional): If set report on items visited. Defaults to False.

        Returns:
            Digraph: The digraph nodes and edges have been added
        """
        if digraph is None:
            digraph = Digraph(node_attr={'fontsize':str(fontSize)}, edge_attr={'fontsize':str(fontSize)})
            digraph.attr(rankdir='LR')
            
        def add_entity(item: Union[DataItem, str]):
            if isinstance(item, str):
                return set()
            
            def short_gname(name):
                typ, id = name.split(':')[2].split('#')
                return f"{typ}#{id[:8]}"

            attr = []
            refs = []
            id = item.id if hasattr(item, 'id') else str(item)
            name = short_gname(id)
            if hasattr(item, 'props'):
                for (pname, val, ctype) in item.props():
                    if ctype != ColType.REF:
                        attr.append(f"{pname} = {val}")
                    else:
                        if val:
                            id = val.id if hasattr(val, 'id') else str(val)
                            refs.append((pname, short_gname(id), val))
                        else:
                            # should we add undefined links?
                            pass

            left = lambda s: s + ' \l'
            digraph.node(name, f"{name}|{' '.join(map(left, attr))}", shape = "record")
            for (label, ref, _) in refs:
                digraph.edge(name, ref, label=label)
            return set(map(lambda e: e[2], refs))

        missing = set(seedItems)
        known = set()
        level = 0
        while len(missing) > 0 and level < depth:
            s = missing
            missing = set()
            for el in s:
                if verbose: print(f".. processing {el}")
                known.add(el)
                reachable = add_entity(el)
                missing = missing.union(reachable - known)
            level += 1
        return digraph

    id: str
    schema: Schema
    _data: Sequence[Any]
    
    def __init__(self, id: str, data: Sequence[Any], schema: Schema):
        object.__setattr__(self, 'id', id)
        object.__setattr__(self, 'schema', schema)
        object.__setattr__(self, '_data', data)
        
    def prop(self, name: str) -> Any:
        for i, col in enumerate(self.schema.columns):
            if col.name == name:
                return self._data[i]
        raise Exception(f"Property '{name}' not defined in schema")
        
    def props(self) -> Sequence[Tuple[str, Any, ColType]]:
        """Return a sequence of tuples (propName, propValue, colType) one for each property

        Returns:
            Sequence[Tuple[str, Any, ColType]]: A sequence of tuples (propName, propValue, colType)
        """
        idColumn = self.schema.idColumn
        return list(map(lambda p: (p[0].name, p[1], p[0].ctype), 
                        filter(lambda e: e[0] != idColumn, 
                               zip(self.schema.columns, self._data))))        
        
    def graph(self, depth=99, digraph:Optional[Digraph]=None, fontSize=12, verbose=False) -> Digraph:
        """Return a Graphviz Digraph showing the dependency graph for this item.

        Args:
            depth (int, optional): Number of levels to expand to. Defaults to 99.
            digraph (Optional[Digraph], optional): Digraph object. If set to None, one is being created. Defaults to None.
            fontSize (int, optional): Font size for node and edge label if digraph is created internally . Defaults to 12.
            verbose (bool, optional): If set report on items visited. Defaults to False.

        Returns:
            Digraph: The digraph nodes and edges have been added
        """
        # self.__class__ do not seem to work for data classes
        return DataItem.graph_many(self, depth=depth, digraph=digraph, fontSize=fontSize, verbose=verbose)

    def __repr__(self):
        (name, id) = self.id.split(':')[2].split('#')
        k = self.schema.columns[1].name
        v = self._data[1]
        if len(self._data) > 2: 
            hasMore = ' ...'
        else:
            hasMore = ''
        return f"<DataItem :{name}#{id[:8]} {k}={v}{hasMore}>"
    
    def __hash__(self):
        return hash(self.id)
    
class DataSet():
    
    schema: Schema
    items: Dict[str, DataItem]
    df: DataFrame
    
    def __init__(self, 
                 schema: Schema,
                 labelF: Optional[Callable[[Dict[str, Any]], str]] = None,
                 dataFrame: DataFrame = None,
                ):
        self.schema = schema
        self.valColumns= list(filter(lambda c: c != schema.idColumn, schema.columns))
        self.colNames = list(map(lambda c: c.name, self.valColumns))

        self.labelF = labelF
        self.items = {}
        self.df = schema.create_dataframe([], addEntityColumn=True)
        if dataFrame is not None:
            self.add_df(dataFrame)
        
    def add(self, **kwargs) -> DataItem:
        data = kwargs
        entityName = self.schema.idColumn.name
        k = data.keys()
        for c in data.keys():
            if c not in self.colNames and c != entityName:
                raise Exception(f"Column name '{c}' not defined in schema")
            
        entity_id = data.get(self.schema.idColumn.name)
        row = []
        hashes = []
        for col in self.valColumns:
            cn = col.name
            if cn not in k:
                if col.required:
                    raise Exception(f"Missing value for required property '{cn}'")
                v = col.default
            else:
                v = data[cn]
            row.append(v)
            if entity_id is None and v is not None:
                hashes.append(col.hash_value(v))
        
        if entity_id is None:
            entity_id = self.schema.create_entity_id(hashes) #str(self.schema.create_uuid(''.join(hashes)))

        # TODO: Maybe we should check a bit more if the existing one is equal
        # or have a instance wide flag to fail on not-equal
        ditem = self.items.get(entity_id, None)
        if ditem:
            return ditem
        if self.labelF:
            label = self.labelF(data)
            ditem = self.items.get(label, None)
            if ditem:
                return ditem
        else:
            label = entity_id
            
        row.insert(0, entity_id)
        self.df.loc[label] = row                
        ditem = DataItem(entity_id, row, self.schema)
        self.items[label] = ditem
        return ditem
    
    def add_df(self, df: DataFrame) -> Dict[str, DataItem]:
        # TODO: this is really inefficient as self.add is making a lot of redundant checks 
        # - but let's worry about that another day
        return df.apply(lambda r: self.add(**(r.to_dict())), axis=1)
    
    def add_data_items(self, items: Series[DataItem]):
        for label, ditem in items.items():
            self.items[label] = ditem
    
    def query_one(self, query: str, local_dict: Dict[str, Any]={}, failQuietly=False) -> DataItem:
        """Try to find a single data item which is returned by `query`.
        
        Args:
            query (str): Query string as defined by panda's DataFrame#query.
            local_dict (Dict[str, Any], optional): Optionally maps '@' variables in `query` to values. Defaults to {}.
            failQuietly (bool, optional): If nothing found and set to true return None, otherwise raise exception. Defaults to False.

        Raises:
            Exception: If none or multiple entities are found and 'failQuietly' is set to False

        Returns:
            DataItem: DataItem found as result of query
        """
        r = self.df.query(query, local_dict=local_dict)
        if len(r) != 1:
            if failQuietly:
                return None
            else:
                raise Exception(f"Found no or too many matches ({len(r)})")
        label = r.iloc[0].name
        return self.items[label]
    
    def query(self, query: str, local_dict: Dict[str, Any]={}) -> Sequence[DataItem]:
        """Returns a sequence pf DataItems which fulfill `query`.
        
        Args:
            query (str): Query string as defined by panda's DataFrame#query
            local_dict (Dict[str, Any], optional): Optionally maps '@' variables in `query` to values. Defaults to {}.

        Returns:
            Sequence[DataItem]: Sequence of data items contained in this set
        """
        def f(r):
            label = r.name
            return self.items[label]

        res = self.df.query(query, local_dict=local_dict).apply(f, axis=1)
        return res.to_list() if len(res) > 0 else []
    
    def isempty(self):
        return len(self.df) == 0
    
    def graph(self, depth=99, digraph:Optional[Digraph]=None, fontSize=12, verbose=False) -> Digraph:
        """Return a Graphviz Digraph showing the dependency graph for all items in this set.

        Args:
            depth (int, optional): Number of levels to expand to. Defaults to 99.
            digraph (Optional[Digraph], optional): Digraph object. If set to None, one is being created. Defaults to None.
            fontSize (int, optional): Font size for node and edge label if digraph is created internally . Defaults to 12.
            verbose (bool, optional): If set report on items visited. Defaults to False.

        Returns:
            Digraph: The digraph nodes and edges have been added
        """
        return DataItem.graph_many(*self.items.values(), depth=depth, digraph=digraph, fontSize=fontSize, verbose=verbose)
    
    def __repr__(self):
        return f"<DataSet schema=:{self.schema.name} items={len(self.df)}>"
