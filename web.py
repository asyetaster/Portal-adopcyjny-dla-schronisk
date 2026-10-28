import functools
from typing import Any, Callable, get_type_hints

from flask import current_app, render_template
from werkzeug.wrappers import Response

from discovery import is_command, is_operation_class


def page(template: str, *, write: bool = False) -> Callable:
    """Renderuje `template` z dict zwróconym przez kontroler.

    Kontroler może też zwrócić gotową odpowiedź (np. redirect po zapisie) -
    wtedy szablon nie jest renderowany, a transakcja kończy się tak samo.

    - jedno połączenie i jedna transakcja na wywołanie widoku,
    - write=True: commit dopiero po poprawnym wyrenderowaniu HTML (lub po zwróceniu odpowiedzi),
    - write=False: rollback po renderowaniu,
    - każdy wyjątek (także abort()): rollback i przekazanie wyjątku do Flaska.
    """

    def decorator(view: Callable) -> Callable:
        # Klasy operacji muszą być zaimportowane w module kontrolera,
        # inaczej get_type_hints() nie rozwiąże adnotacji.
        hints = get_type_hints(view)
        dependencies = {
            name: cls
            for name, cls in hints.items()
            if name != "return" and is_operation_class(cls)
        }
        commands = [name for name, cls in dependencies.items() if is_command(cls)]
        if commands and not write:
            raise RuntimeError(
                f"Widok {view.__name__!r} wstrzykuje Command ({', '.join(commands)}), "
                f"ale @page nie ma write=True"
            )

        @functools.wraps(view)
        def wrapper(*args: Any, **kwargs: Any):
            conflicts = sorted(dependencies.keys() & kwargs.keys())
            if conflicts:
                raise RuntimeError(
                    f"Widok {view.__name__!r}: parametr(y) {', '.join(conflicts)} "
                    f"pochodzą z routingu i jednocześnie są zależnościami do wstrzyknięcia"
                )

            engine = current_app.extensions["db_engine"]
            with engine.connect() as connection:  # zawsze zamyka połączenie
                transaction = connection.begin()
                try:
                    for name, cls in dependencies.items():
                        kwargs[name] = cls(connection)  # wspólna Connection i transakcja
                    result = view(*args, **kwargs)
                    if isinstance(result, Response):
                        # Gotowa odpowiedź (np. redirect po zapisie) - bez renderowania.
                        response = result
                    elif isinstance(result, dict):
                        # Renderujemy przed końcem transakcji: błąd szablonu => rollback.
                        response = render_template(template, **result)
                    else:
                        raise TypeError(
                            f"Widok {view.__name__!r} musi zwrócić dict albo Response "
                            f"(np. redirect), zwrócił {type(result).__name__}"
                        )
                    if write:
                        transaction.commit()
                    else:
                        transaction.rollback()
                except BaseException:
                    if transaction.is_active:
                        transaction.rollback()
                    raise
            return response

        return wrapper

    return decorator