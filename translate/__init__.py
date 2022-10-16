from typing import Type

from utils.imports import import_one as _import_one
from .base import Translator


def import_translator(backend: str) -> Type[Translator]:
    return _import_one(backend, __package__, Translator, exclude_modules=["base"])
