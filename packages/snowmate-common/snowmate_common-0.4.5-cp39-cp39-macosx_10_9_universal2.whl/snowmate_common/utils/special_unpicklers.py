from typing import Tuple


def unpickle_requests_json_decode_error(
    exception_obj: Exception, _, exception_dunder_dict
):
    """
    special function for unpickling requests.exceptions.JSONDecodeError.
    This is important because the args of this module are changed.
    JSONDecodeError.__init__() missing 3 required positional arguments: 'msg', 'doc', and 'pos
    """
    msg, doc, pos = (
        exception_dunder_dict.get("msg"),
        exception_dunder_dict.get("doc"),
        exception_dunder_dict.get("pos"),
    )
    return exception_obj(msg, doc, pos)


def default_exception_unpickle_function(
    exception_obj: Exception, exception_args: Tuple, _
):
    """
    default unpickle function for exceptions
    """
    return exception_obj(*exception_args)


def get_special_unpickle_function(full_name: str):
    """
    return the special unpickle function for the given full_name
    """
    return special_objects.get(full_name, default_exception_unpickle_function)


special_objects = {
    "requests.exceptions.JSONDecodeError": unpickle_requests_json_decode_error
}
