"""Filtry Jinja. ``{{ wartość|label("grupa") }}`` - patrz labels.py."""

from flask import Flask

from labels import label


def register(app: Flask) -> None:
    app.add_template_filter(label, "label")
