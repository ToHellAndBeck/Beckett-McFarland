import requests
from typing import Literal

from random import choice

import requests
from typing import Literal

def hit_api(url, method: Literal["get", "post"] = "get", return_type: Literal["json", "content"] | None = "json", timeout: int = 5):
    hit_method = requests.get if method == 'get' else requests.post
    try:
        response = hit_method(url, timeout=timeout)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json() if return_type == 'json' else response.content.decode()
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None

# Rest of your code remains unchanged


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


