from typing import (
    Dict,
    List,
    Literal,
    Iterable
)

import copy
import keyword
import datetime
import json
from collections import UserDict

from xmlrpc.client import boolean
from pandas.core.frame import DataFrame
import pandas as pd

from ..utility import all_dict_values_in_target_types
from ..watcher import get_obj_size
from .dtypes import dtype_auto_refine
from ..string.convert_functions import upper_and_replace_space_with_underscore
_export_mode = Literal["stacked","multi-column"]


class liamDict(UserDict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("liamDict object has no attribute '%s'" % key)
    
    def __setattr__(self, key, value):
        if key == 'data':   # <1>
            super().__setattr__(key, value)
            return
        self[key] = value
    
    def __setitem__(self, key, value):
        key = self._get_key(key) # <2>
        value = self.handle_value(value) # <3>
        super().__setitem__(key, value) # <4>
    
    def __getitem__(self, key):
        key = self._get_key(key)
        return super().__getitem__(key) # <5>
    
    def _get_key(self, key):
        if hasattr(self.__class__, key) or keyword.iskeyword(key): # <6>
            key += '_'
        return key

    def handle_value(self, value):
        if isinstance(value, dict):
            value = liamDict(value)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                value[i] = self.handle_value(item)
        return value

class attrDict(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("attrDict object has no attribute '%s'" % key)
            
    def __setattr__(self, key, value):
        self[key] = value
    
    def __str__(self):
        temp_dict = {"avaliable keys":[k for k in self.keys() if not k.startswith('_')]}
        temp_dict.update({k:self[k] for k in self.keys() if k[0]=='_' and k[1]!='_' and (not k.startswith('_logger'))} )
        temp_json = json.dumps(temp_dict,indent=2)
        return temp_json

    def __repr__(self):
        return self.__str__()


    def export(self,key_list:Iterable):
        """export an attrDict by given list of keys

        Args:
            key_list (Iterable): list of some existing keys

        Returns:
            attrDict: result
        """
        result = {k: self[k] for k in self.keys() if k in key_list}
        return attrDict(result)

    def df_dtype_refine(self, inplace: bool = False, ignored_dfs:list=[])->object:
        """batch refine all Pandas dataframes by data types which save more memory

        Args:
            inplace (bool, optional): affects original data or not. Defaults to False.
            ignored_dfs (list, optional): list of keys that will be ignored by this method.

        Returns:
            object: copy of effective instance
        """
        if inplace:
            new_one = self
        else:
            new_one = copy.deepcopy(self)

        for k,v in self.items():
            if isinstance(v,DataFrame) and (k not in ignored_dfs):
                new_one[k] = dtype_auto_refine(v)
        return new_one

    def key_standardization(
        self, 
        standardize_func:callable = upper_and_replace_space_with_underscore
    ):
        """standardize the dictionary key by standardize_func

        Args:
            standardize_func (callable, optional): string conversion function. Defaults to toolbox.string.convert_functions.upper_and_replace_space_with_underscore.
        """
        original_keys = list(self.keys())
        for k in original_keys:
            self[standardize_func(k)]=self.pop(k)

    @property
    def size_summary(self)->dict:
        """iteratively approximate the size of each item in an attrDict instance

        Returns:
            Dict: result
        """
        rs = {k:get_obj_size(v) for k,v in self.items() if not k.startswith('_')}
        return rs

class JSE_4df(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DataFrame):
            return obj.to_dict(orient='records')
        return json.JSONEncoder.default(self, obj)


class Property4DataSet(attrDict):
    def __init__(self, value_type:type, input_dict:dict = None):
        _target_types = (
            datetime.date,
            datetime.datetime,
            datetime.time,
            str, 
            int, 
            float, 
            bool
            )

        if input_dict is None:
            pass
        elif value_type is None:
            
            if all_dict_values_in_target_types(input_dict, _target_types, visible_key_only=True):
                _ = [self.add(v, i) for i,v in input_dict.items() if not i.startswith('_')]
        elif isinstance(input_dict, Dict):
            if all_dict_values_in_target_types(input_dict, [List,], visible_key_only=True):
                input_dict = {i:v[0] for i,v in input_dict.items() if not i.startswith('_')}
            if all_dict_values_in_target_types(input_dict, [value_type,], visible_key_only=True):
                _ = [self.add(v, i) for i,v in input_dict.items() if not i.startswith('_')]
            else:
                raise TypeError(f'Not all values in attrDict are {value_type}')

    def add(self,var, property_name):
        setattr(self,property_name, var)
    def delete(self,property_name):
        del self[property_name]
        
    @property    
    def allitems(self):
        return [x for x in list(self.keys()) if (x !=__name__) and (not x.startswith('_')) ] 
        #return [x for x in list(self.__dict__.keys()) if (x !=__name__) and (not x.startswith('_')) ] 

class DataSet:
    __slots__ = (
        "DF",
        "PAR",
        "MAP"
    )
    def __init__(self, dict_PAR=None, dict_DF=None, dict_MAP=None):
        self.DF = self._DF(value_type = DataFrame, input_dict = dict_DF)
        self.PAR = self._PAR(value_type = None, input_dict = dict_PAR)
        self.MAP = Property4DataSet(value_type = dict, input_dict = dict_MAP)

    def set(self, dict_PAR:DataFrame=None, dict_DF:DataFrame=None, dict_MAP:DataFrame=None)->None:
        """assign dataframes to DataSet

        Args:
            dict_PAR (DataFrame, optional): DataFrame for PAR. Defaults to None.
            dict_DF (DataFrame, optional): DataFrame for Df. Defaults to None.
            dict_MAP (DataFrame, optional): DataFrame for MAP. Defaults to None.

        Raises:
            ValueError: when all Args are None
        """
        if all({(dict_PAR is None),(dict_DF is None),(dict_MAP is None)}): 
            raise ValueError("No attrDict instance has been assigned")
        if dict_DF:
            self.DF = self._DF(value_type = DataFrame, input_dict = dict_DF)
        if dict_PAR:
            self.PAR = self._PAR(value_type = None, input_dict = dict_PAR)
        if dict_MAP:
            self.MAP = Property4DataSet(value_type = dict, input_dict = dict_MAP)


    class _DF(Property4DataSet):

        def dump2json(self, output_path: str = None):
            if not output_path:
                output_path = 'feed.DF.json'

            with open(output_path, 'w') as fp:
                json.dump(self, fp, cls=JSE_4df, indent = 2)

        def column_standardization(
                self,
                standardize_func:callable = upper_and_replace_space_with_underscore,
                inplace: bool = False
            ):
            """standardize the column name for each dataframe under DF by standardize_func

            Args:
                standardize_func (callable, optional): string conversion function. Defaults to upper_and_replace_space_with_underscore.
                inplace (bool, optional): Whether to modify the DataFrame rather than creating a new one. Defaults to False.

            Returns:
                Dataframe: it would be different than original DF property if `inplace=False`
            """
            if inplace:
                new_one = self
            else:
                new_one = copy.deepcopy(self)
           
            for df_name in new_one.allitems:
                col_names = list(new_one[df_name].columns)
                new_one[df_name].rename(
                    {col:standardize_func(col) for col in col_names},
                    axis='columns',
                    inplace=True
                )

            return new_one

    class _PAR(Property4DataSet):   
        def export_df(self, format: _export_mode = "multi-column"):
            """return a DataFrame by gathering all parameter:value within PAR  

            Args:
                format (_export_mode, optional): Literal["stacked","multi-column"]. Defaults to "multi-column".

            Returns:
                DataFrame
            """
            if format=="multi-column":
                df = pd.DataFrame(
                    [
                        [getattr(self,x) for x in self.allitems]
                    ],
                    columns = self.allitems
                    )
            if format=="stacked":
                df = pd.DataFrame(
                                zip(
                                    self.allitems,
                                    [getattr(self,x) for x in self.allitems]
                                ),
                                columns = ["parameter","value"]
                            )
            return df
    

class Feed(DataSet):
    def __init__(self, multi_group = False, **kwargs):
        """Feed has a simple but organized structure to store the data

        Args:
            multi_group (bool, optional): Allows a hierarchical stucture. Defaults to False.
        """
        self.__multi_group = multi_group
        if multi_group:
            self.add_new_group = self.__add_new_group
        else:
            super().__init__(**kwargs)

    def __add_new_group(self,group_name, **kwargs):
        setattr(self, group_name, DataSet(**kwargs))

    def __get_group_names(self):
        if self.__multi_group:
            return [g for g in list(self.__dict__.keys()) if g not in ('add_new_group','__add_new_group','__get_group_names','_Feed__multi_group')]
        else:
            return None

    def __str__(self):
        if self.__multi_group:
            temp_dict = {
                g:[{x:[s for s in getattr(getattr(self,g),x).allitems]} for x in getattr(self,g).__slots__] 
                for g in self.__get_group_names()
            }
        else:
            temp_dict = {
                k:[x for x in getattr(self,k).allitems] 
                for k in self.__slots__
            }

        temp_json = json.dumps(temp_dict,indent=2)
        return "data attributes: \n" + temp_json

    def __repr__(self):
        return self.__str__()
        # if self.__multi_group:
        #     temp_dict = {
        #         g:[{x:[s for s in getattr(getattr(self,g),x).allitems]} for x in getattr(self,g).__slots__] 
        #         for g in self.__get_group_names()
        #     }
        # else:
        #     temp_dict = {
        #         k:[x for x in getattr(self,k).allitems] 
        #         for k in dir(self) if not k.startswith('_')
        #     }

        # temp_json = json.dumps(temp_dict,indent=2)
        # return "data attributes: \n" + temp_json


