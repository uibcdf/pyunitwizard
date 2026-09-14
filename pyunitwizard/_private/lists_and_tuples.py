def is_list_or_tuple(obj) -> bool:
    """Checks whether an object is a list or a tuple"""
    if isinstance(obj, (list, tuple)):
        return True
    else:
        return False


def list_to_csv_string(obj):

    return ",".join([str(ii) for ii in obj])


def list_to_ssv_string(obj):

    return " ".join([str(ii) for ii in obj])
