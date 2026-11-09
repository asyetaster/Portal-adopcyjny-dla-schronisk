"""Globalna obsługa błędów z operacji i strony błędów.

- ``BusinessRuleError`` → flash + powrót na poprzednią stronę,
- ``NotFoundError`` oraz 404 → strona ``errors/404.html``,
- 403 → strona ``errors/403.html``.
"""

from flask import Flask, flash, redirect, render_template, request

from auth import is_safe_redirect_url
from mailer import discard_queued_mails
from operations.errors import BusinessRuleError, NotFoundError


def register(app: Flask) -> None:
    @app.errorhandler(BusinessRuleError)
    def handle_business_rule_error(error: BusinessRuleError):
        # Transakcja została wycofana, więc zakolejkowane maile nie mogą wyjść.
        discard_queued_mails()
        flash(error.message)
        # Wracamy na stronę z formularzem, ale tylko w obrębie serwisu.
        target = request.referrer or "/"
        if target.startswith(request.host_url):
            target = "/" + target[len(request.host_url):]
        if not is_safe_redirect_url(target):
            target = "/"
        return redirect(target, code=303)

    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error: NotFoundError):
        discard_queued_mails()
        return render_template("errors/404.html", message=str(error) or None), 404

    @app.errorhandler(404)
    def handle_404(error):
        return render_template("errors/404.html", message=None), 404

    @app.errorhandler(403)
    def handle_403(error):
        return render_template("errors/403.html"), 403