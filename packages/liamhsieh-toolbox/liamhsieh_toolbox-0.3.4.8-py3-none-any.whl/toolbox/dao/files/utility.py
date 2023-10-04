import pathlib
from collections.abc import KeysView

def all_equal(iterator):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == x for x in iterator)

    
def count_folder_number(contents:list) -> int:
    #return sum(os.path.isdir(c) for c in contents)
    return sum(pathlib.Path(c).is_dir() for c in contents)

def count_file_number(contents:list) -> int:
    return sum(pathlib.Path(c).is_file() for c in contents)

def create_nonduplicated_dict_key(dict_key:str,keys:KeysView, addition = "_") -> str:
    """If dict_key has not existed in keys, directly return, otherwise, keep adding additional string as suffix until no duplication is confirmed

    Args:
        dict_key (str): dictionary key that plans to add
        keys (KeysView): keys of target dictionary
        addition (str, optional): aditional string as suffix to avoid duplication. Defaults to "_".

    Raises:
        TypeError: keys needs to be a dict_keys

    Returns:
        str: confirmed key for futher insert 
    """
    if not isinstance(d.keys(),KeysView):
        raise TypeError('keys needs to be a dict_keys')

    if dict_key not in list(keys):
        return dict_key
    else:
        return create_nonduplicated_dict_key(''.join((dict_key,addition)),keys)

