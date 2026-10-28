"""Wspólne funkcje wykrywania: moduły w pakiecie i klasy operacji.

Używane przez runner CLI (cli.py), dekorator @page (web.py) i rejestrację tras (routes/).

Szukanie komen i query do testów.
"""

import importlib
import inspect
import pkgutil
from types import ModuleType
from typing import Any

OPERATION_SUFFIXES = ("Command", "Query")


def iter_package_modules(package_name: str) -> list[ModuleType]:
    """Importuje pakiet i rekurencyjnie wszystkie jego moduły i podpakiety.

    Zwraca też sam pakiet (klasy z __init__.py też się liczą).
    """
    package = importlib.import_module(package_name)
    modules = [package]
    for info in pkgutil.walk_packages(package.__path__, prefix=f"{package_name}."):
        modules.append(importlib.import_module(info.name))
    return modules


def is_operation_class(obj: Any) -> bool:
    return (
        inspect.isclass(obj)
        and obj.__name__.endswith(OPERATION_SUFFIXES)
        and callable(getattr(obj, "execute", None))
    )


def is_command(cls: type) -> bool:
    return cls.__name__.endswith("Command")