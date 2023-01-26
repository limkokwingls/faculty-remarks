from types import NoneType
from rich import print


def convert_list_to_dict(data: dict[int, list[dict]]):
    new_dict = {}
    for std_no, results in data.items():
        values = {}
        for it in results:
            for key, value in it.items():
                values[key] = value
        new_dict[std_no] = values
    return new_dict


def to_int(value): return int(float(value))


def is_number(s):
    if type(s) == NoneType:
        return False
    try:
        float(s)
    except ValueError:
        return False
    return True
