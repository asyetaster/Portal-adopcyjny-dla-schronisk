"""Filtry Jinja. ``{{ wartość|label("grupa") }}`` - patrz labels.py."""

from flask import Flask

from labels import format_age, label


def register(app: Flask) -> None:
    app.add_template_filter(label, "label")
    # {{ animal.age_min_months|age(animal.age_max_months) }}
    app.add_template_filter(format_age, "age")
