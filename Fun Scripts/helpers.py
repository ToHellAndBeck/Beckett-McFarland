import requests
from typing import Literal
from constants import random_json_urls
from random import choice

def hit_api(url, method:Literal["get", "post"]="get", return_type:Literal["json","content"]|None="json"):
    hit_method = requests.get if method == 'get' else requests.post
    return hit_method(url).json() if return_type == 'json' else hit_method(url).content.decode()

def iter_dict(d:dict, parent=""):
    for dict_key, dict_value in d.items():
        if isinstance(dict_value, dict):
            for dict_parent, dict_data in iter_dict(dict_value, parent=parent+'.'+dict_key):
                yield dict_parent, dict_data
        elif isinstance(dict_value, list):
            for list_parent, list_data in iter_list(dict_value, parent=parent+'.'+dict_key):
                yield list_parent, list_data
        else:
            yield parent+'.'+dict_key, str(dict_value)

def iter_list(l:list, parent=""):
    for list_data in l:
        if isinstance(list_data, dict):
            for dict_parent, dict_data in iter_dict(list_data, parent=parent+"L"):
                yield dict_parent, dict_data

        elif isinstance(list_data, list):
            for list_parent, list_data2 in iter_list(list_data, parent=parent+"L"):
                yield list_parent, list_data2
        
        else:
            yield parent, str(list_data)


def iter_data(data, parent=""):
    if isinstance(data, dict):
        for dict_parent, dict_data in iter_dict(data, parent=parent):
            yield dict_parent, dict_data

    elif isinstance(data, list):
        for list_parent, list_data in iter_list(data, parent=parent+'-'):
            yield list_parent, list_data
    else:
        yield parent, str(data)


