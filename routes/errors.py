"""Globalna obsługa błędów z operacji."""

from flask import Flask, flash, redirect, request
from werkzeug.exceptions import NotFound

from auth import is_safe_redirect_url
from operations.errors import BusinessRuleError, NotFoundError


def register(app: Flask) -> None:
    @app.errorhandler(BusinessRuleError)
    def handle_business_rule_error(error: BusinessRuleError):
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
        return NotFound()
