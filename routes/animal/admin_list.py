from flask import Flask, request

from auth import admin_required
from operations.animal.ListAnimalsForModerationQuery import ListAnimalsForModerationQuery
from web import page


def register(app: Flask) -> None:
    @app.get("/admin/animals")
    @admin_required
    @page("admin/animals/list.html")
    def admin_animal_list(list_animals: ListAnimalsForModerationQuery):
        search = request.args.get("search", "").strip()
        hidden_only = request.args.get("hidden") == "1"
        page_num = max(request.args.get("page", 1, type=int), 1)
        result = list_animals.execute(search=search, hidden_only=hidden_only, page=page_num)
        return {
            "animals": result["items"],
            "pagination": result["pagination"],
            "search": search,
            "hidden_only": hidden_only,
        }