"""Trasy aplikacji, pogrupowane w podkatalogach (np. routes/user/).

Każdy moduł w tym pakiecie (rekurencyjnie), który definiuje funkcję
``register(app)``, jest wykrywany i wywoływany automatycznie przez
``register_routes()``. Dodanie nowego pliku z trasami nie wymaga edycji app.py.
"""

from flask import Flask

from discovery import iter_package_modules


def register_routes(app: Flask, package_name: str = __name__) -> None:
    for module in iter_package_modules(package_name):
        register = getattr(module, "register", None)
        if callable(register) and getattr(register, "__module__", None) == module.__name__:
            register(app)