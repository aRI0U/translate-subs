import importlib.resources
import inspect
import warnings
from typing import Dict, Optional, Sequence, TypeVar


T = TypeVar('T')


def is_valid_module(module_name: str) -> bool:
    return not module_name.startswith("_") and module_name.endswith(".py")


def import_one(
        module_name: str,
        package: str,
        base_class: Optional[T] = None,
        invalid_modules: Sequence = ()
) -> T:
    module = importlib.import_module(package + '.' + module_name)
    for name, cls in inspect.getmembers(module, inspect.isclass):
        if base_class is None or issubclass(cls, base_class):
            return cls

    # raise error
    valid_modules = [
        m[:-3] for m in importlib.resources.contents(package)
        if is_valid_module(m) and m not in invalid_modules
    ]
    raise ImportError("Invalid module selected. "
                      f"Valid choices are {', '.join(valid_modules)}, "
                      f"but found `{module_name}`.")


def import_all(package: str, base_class: Optional[T] = None) -> Dict[str, T]:
    classes = {}
    for module_file in importlib.resources.contents(package):
        if not is_valid_module(module_file):
            continue
        try:
            module = importlib.import_module(f"{__package__}.{module_file[:-3]}")
        except ModuleNotFoundError:
            warnings.warn(f"Could not import callback implemented in {__file__.replace('__init__.py', module_file)}`. "
                          f"If you really want to use it, please first install the required dependencies.")
            continue

        for name, cls in inspect.getmembers(module, inspect.isclass):
            if base_class is None or issubclass(cls, base_class):
                classes[name] = cls

        return classes
