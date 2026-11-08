"""Funkcje autoryzacji: ładowanie zalogowanego użytkownika i ochrona /admin.

Funkcje ``load_logged_in_user()`` i ``require_admin_access()`` są rejestrowane
jako ``before_request`` w ``routes/auth/__init__.py`` (Task 4).
"""

import functools

from flask import abort, current_app, g, redirect, request, session, url_for

from operations.user.GetCurrentUserQuery import GetCurrentUserQuery


def load_logged_in_user():
    """before_request: ładuje ``g.user`` z sesji.

    Otwiera własne, krótkie połączenie tylko do odczytu (nie współdzieli
    transakcji z ``@page``). Przy braku sesji lub koncie o statusie innym niż
    ``Active`` czyści sesję.
    """
    g.user = None

    if request.endpoint == "static":
        return

    user_id = session.get("user_id")
    if user_id is None:
        return

    engine = current_app.extensions["db_engine"]
    with engine.connect() as conn:
        user = GetCurrentUserQuery(conn).execute(user_id)

    if user is None or user["status"] != "Active":
        session.clear()
        g.user = None
        return

    g.user = user


def require_admin_access():
    """before_request: chroni całe ``/admin/*``.

    - brak zalogowanego użytkownika → przekierowanie na ``/login?next=...``,
    - zalogowany bez ``is_admin`` → ``abort(403)``,
    - pozostałe ścieżki (poza ``/admin``) → przepuszcza.
    """
    if not request.path.startswith("/admin"):
        return

    if g.user is None:
        return redirect(url_for("login", next=request.path))

    if not g.user["is_admin"]:
        abort(403)


def is_safe_redirect_url(target: str) -> bool:
    """True tylko dla względnych ścieżek (zapobiega atakom open redirect)."""
    return bool(target) and target.startswith("/") and not target.startswith("//")


def login_required(view):
    """Dekorator widoku: bez zalogowania → ``/login?next=...``.

    Stoi między ``@app.get/post`` a ``@page``, więc odmowa następuje przed
    otwarciem transakcji.
    """

    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)

    return wrapper


def admin_required(view):
    """Dekorator widoku: bez zalogowania → ``/login``, bez ``is_admin`` → 403."""

    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.path))
        if not g.user["is_admin"]:
            abort(403)
        return view(*args, **kwargs)

    return wrapper
