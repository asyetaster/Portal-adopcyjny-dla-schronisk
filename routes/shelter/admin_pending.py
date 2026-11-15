from flask import Flask, request

from auth import admin_required
from operations.shelter.ListPendingShelterRegistrationsQuery import (
    ListPendingShelterRegistrationsQuery,
)
from web import page


def register(app: Flask) -> None:
    @app.get("/admin/shelters/pending")
    @admin_required
    @page("admin/shelters/pending.html")
    def admin_shelter_pending(list_pending: ListPendingShelterRegistrationsQuery):
        page_num = max(request.args.get("page", 1, type=int), 1)
        result = list_pending.execute(page=page_num)
        return {"shelters": result["items"], "pagination": result["pagination"]}
