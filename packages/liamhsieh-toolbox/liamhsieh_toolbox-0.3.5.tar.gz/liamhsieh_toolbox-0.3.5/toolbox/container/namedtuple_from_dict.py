from collections import namedtuple

def namedtuple_from_dict(source_dict:dict,name:str)->namedtuple:
    """return an instance of namedtuple from dictionary named name

    Args:
        source_dict (dict): data source
        name (str): name of namedtuple class

    Returns:
        namedtuple: converted from dictionary
    """

    return namedtuple(
        name,
        source_dict.keys()
    )(
        **source_dict
    )