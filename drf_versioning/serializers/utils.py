import inspect
from importlib import import_module

from ..transforms import Transform


def import_transforms(path: str) -> tuple[type[Transform]]:
    module = import_module(path)
    transforms = []
    for name, obj in inspect.getmembers(module):
        if isinstance(obj, type) and issubclass(obj, Transform) and getattr(obj, "version", None):
            transforms.append(obj)
    transforms = tuple(sorted(transforms, key=lambda t: t.version))
    return transforms
