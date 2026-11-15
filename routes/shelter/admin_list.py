from flask import Flask, request

from auth import admin_required
from operations.shelter import SHELTER_STATUS_LABELS
from operations.shelter.ListSheltersQuery import ListSheltersQuery
from web import page


def register(app: Flask) -> None:
    @app.get("/admin/shelters")
    @admin_required
    @page("admin/shelters/list.html")
    def admin_shelter_list(list_shelters: ListSheltersQuery):
        search = request.args.get("search", "").strip()
        status = request.args.get("status", "")
        if status not in SHELTER_STATUS_LABELS:
            status = ""
        page_num = max(request.args.get("page", 1, type=int), 1)

        result = list_shelters.execute(status=status, search=search, page=page_num)
        return {
            "shelters": result["items"],
            "pagination": result["pagination"],
            "status_labels": SHELTER_STATUS_LABELS,
            "search": search,
            "status": status,
        }
