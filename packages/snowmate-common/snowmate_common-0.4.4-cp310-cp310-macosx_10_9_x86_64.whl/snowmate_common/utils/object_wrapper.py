import copy
from typing import Any, AnyStr
from snowmate_common.utils import special_unpicklers

JSONPICKLE_EXTERNAL_TYPE_KEY = "py/snow/external/type"
FUNCS_INDEX = 1
CLS_INDEX = 0


def get_attribute_full_name(cls: Any) -> AnyStr:
    mod = cls.__module__
    if hasattr(cls, "__qualname__"):
        return f"{mod}.{cls.__qualname__}"
    return f"{mod}.{cls.__name__}"


def import_by_full_name(full_name):
    # pylint: disable=import-outside-toplevel
    from jsonpickle.unpickler import loadclass
    import importlib

    try:
        return importlib.import_module(full_name)
    except Exception:
        return loadclass(full_name)


class SpecialWrapper:
    def __new__(cls, *args, **kwargs):
        # pylint: disable=import-outside-toplevel
        from jsonpickle.unpickler import loadclass

        full_name = args[0]
        function_to_run = loadclass(full_name)
        return function_to_run(*args[1:], **kwargs)


class ModuleWrapper:
    def __new__(cls, *args):
        # pylint: disable=import-outside-toplevel
        module_full_name = args[0]
        return import_by_full_name(module_full_name)

    def __init__(self, module_full_name) -> None:
        self.module_full_name = str(module_full_name)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return ModuleWrapper(*args)


class ExceptionWrapper:
    def __new__(cls, *args):
        exception_full_name = args[0]
        exception_args, exception_dunder_dict = args[1], args[2]
        exception_object = import_by_full_name(exception_full_name)
        unpickle_function = special_unpicklers.get_special_unpickle_function(
            exception_full_name
        )
        return unpickle_function(
            exception_object, exception_args, exception_dunder_dict
        )

    def __init__(self, *args):
        self.args = args

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return ExceptionWrapper(*args)


class FunctionWrapper:
    def __init__(self, fullname) -> None:
        self.fullname = str(fullname)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return FunctionWrapper(*args)

    def __reduce__(self):
        # pylint: disable=import-outside-toplevel
        from jsonpickle.unpickler import loadclass

        return loadclass, (self.fullname,)


class ObjectWrapperBase:
    def __new__(cls, *args):
        new_cls = copy.copy(cls)
        new_obj = object.__new__(new_cls)  # needed in case of set attr failure
        new_obj.funcs = {}
        new_obj.cls = ""
        try:
            try:
                for func in args[FUNCS_INDEX]:
                    setattr(new_cls, func, args[FUNCS_INDEX][func])
            except Exception:
                pass
            new_obj.__dict__ = args[FUNCS_INDEX]
            new_obj = object.__new__(new_cls)
            new_obj.funcs = args[FUNCS_INDEX]
            new_obj.cls = args[CLS_INDEX]
        except Exception:
            pass
        return new_obj


class ObjectWrapper(ObjectWrapperBase):
    def __new__(cls, *args):
        return super().__new__(cls, *args)

    def __init__(self, cls: Any, *_args):
        """
        This object wraps extranl types.
        """
        self.__setattr__(JSONPICKLE_EXTERNAL_TYPE_KEY, get_attribute_full_name(cls))

    def __reduce__(self):
        if not hasattr(self, "funcs"):
            # pylint: disable=attribute-defined-outside-init
            self.funcs = {}
        if not hasattr(self, "cls"):
            # pylint: disable=attribute-defined-outside-init
            self.cls = ""
        funcs = self.funcs
        cls = self.cls
        del self.funcs
        del self.cls
        return ObjectWrapper, (cls, funcs), self.__dict__


class UnpicklableObject(ObjectWrapperBase):
    def __new__(cls, *args):
        return super().__new__(cls, *args)

    def __reduce__(self):
        return UnpicklableObject, (str(self.cls), self.funcs), self.__dict__
