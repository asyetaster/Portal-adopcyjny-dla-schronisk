"""Uniwersalny runner CLI dla klas *Command / *Query z pakietu operations.

Uruchamiany przez test.py. Logika jest tutaj, bo moduł o nazwie ``test``
koliduje ze standardowym pakietem ``test`` przy imporcie.
"""

import argparse
import inspect
import json
import sys
from typing import Any, get_type_hints

from sqlalchemy import Engine

from database import create_engine_from_url
from discovery import is_command, is_operation_class, iter_package_modules

SUPPORTED_TYPES = (str, int, float, bool)


class OperationError(Exception):
    """Błąd konfiguracji operacji (duplikat, zła sygnatura, nieobsługiwany typ)."""


def discover_operations(package_name: str = "operations") -> dict[str, type]:
    """Zwraca {nazwa_klasy: klasa} dla wszystkich operacji w pakiecie.

    Skanuje rekurencyjnie, więc operacje można grupować w podkatalogach
    (np. operations/user/). Nazwy klas muszą być unikalne w całym pakiecie.
    """
    found: dict[str, type] = {}
    for module in iter_package_modules(package_name):
        for name, obj in vars(module).items():
            if not is_operation_class(obj):
                continue
            if obj.__module__ != module.__name__:
                continue  # klasa tylko zaimportowana do tego modułu
            if name in found and found[name] is not obj:
                raise OperationError(
                    f"Duplikat nazwy operacji {name!r}: "
                    f"{found[name].__module__}.{name} oraz {module.__name__}.{name}"
                )
            found[name] = obj
    return dict(sorted(found.items()))


def option_name(param_name: str) -> str:
    return "--" + param_name.replace("_", "-")


def execute_parameters(cls: type) -> list[tuple[inspect.Parameter, type]]:
    """Zwraca parametry execute() (bez self) z typami; zgłasza czytelne błędy."""
    signature = inspect.signature(cls.execute)
    try:
        hints = get_type_hints(cls.execute)
    except Exception as exc:
        raise OperationError(
            f"{cls.__name__}.execute: nie można odczytać adnotacji typów ({exc})"
        ) from exc

    params = []
    for param in list(signature.parameters.values())[1:]:  # pomijamy self
        where = f"{cls.__name__}.execute, parametr {param.name!r}"
        if param.kind is inspect.Parameter.VAR_POSITIONAL:
            raise OperationError(f"{where}: *args nie jest obsługiwane")
        if param.kind is inspect.Parameter.VAR_KEYWORD:
            raise OperationError(f"{where}: **kwargs nie jest obsługiwane")
        if param.kind is inspect.Parameter.POSITIONAL_ONLY:
            raise OperationError(f"{where}: parametry positional-only nie są obsługiwane")
        if param.name not in hints:
            raise OperationError(f"{where}: brak adnotacji typu")
        annotation = hints[param.name]
        if annotation not in SUPPORTED_TYPES:
            supported = ", ".join(t.__name__ for t in SUPPORTED_TYPES)
            raise OperationError(
                f"{where}: nieobsługiwany typ {annotation!r} (obsługiwane: {supported})"
            )
        params.append((param, annotation))
    return params


def _add_operation_parser(subparsers, name: str, cls: type) -> None:
    params = execute_parameters(cls)
    doc = inspect.getdoc(cls) or ""
    kind = "Command (commit)" if is_command(cls) else "Query (rollback)"
    sub = subparsers.add_parser(
        name,
        help=f"{kind}{': ' + doc.splitlines()[0] if doc else ''}",
        description=doc or None,
    )
    for param, annotation in params:
        has_default = param.default is not inspect.Parameter.empty
        kwargs: dict[str, Any] = {"dest": param.name}
        if annotation is bool:
            kwargs["action"] = argparse.BooleanOptionalAction
        else:
            kwargs["type"] = annotation
            kwargs["metavar"] = annotation.__name__.upper()
        if has_default:
            kwargs["default"] = param.default
            kwargs["help"] = f"{annotation.__name__}, domyślnie: {param.default!r}"
        else:
            kwargs["required"] = True
            kwargs["help"] = f"{annotation.__name__}, wymagany"
        sub.add_argument(option_name(param.name), **kwargs)
    sub.set_defaults(_params=tuple(p.name for p, _ in params))


def build_parser(operations: dict[str, type]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="test.py",
        description="Uruchamia operacje *Command / *Query z pakietu operations.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="wycofaj transakcję także dla Command (nie cofa efektów spoza bazy)",
    )
    subparsers = parser.add_subparsers(dest="operation", metavar="OPERACJA", required=True)
    for name, cls in operations.items():
        _add_operation_parser(subparsers, name, cls)
    return parser


def run_operation(engine: Engine, cls: type, kwargs: dict[str, Any], *, dry_run: bool = False) -> Any:
    """Jedna Connection + jedna transakcja. Command: commit, Query / dry-run: rollback."""
    with engine.connect() as connection:  # zawsze zamyka połączenie
        transaction = connection.begin()
        try:
            result = cls(connection).execute(**kwargs)
            if is_command(cls) and not dry_run:
                transaction.commit()
            else:
                transaction.rollback()
            return result
        except BaseException:
            if transaction.is_active:
                transaction.rollback()
            raise


def main(argv: list[str] | None = None) -> int:
    try:
        operations = discover_operations()
        parser = build_parser(operations)
    except OperationError as exc:
        print(f"Błąd konfiguracji operacji: {exc}", file=sys.stderr)
        return 2

    args = parser.parse_args(argv)
    cls = operations[args.operation]
    kwargs = {name: getattr(args, name) for name in args._params}

    engine = create_engine_from_url()
    try:
        result = run_operation(engine, cls, kwargs, dry_run=args.dry_run)
    except Exception as exc:
        print(f"Błąd: {type(exc).__name__}: {exc}", file=sys.stderr)
        print("Transakcja została wycofana.", file=sys.stderr)
        return 1
    finally:
        engine.dispose()

    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    if args.dry_run and is_command(cls):
        print("(--dry-run: transakcja wycofana)", file=sys.stderr)
    return 0