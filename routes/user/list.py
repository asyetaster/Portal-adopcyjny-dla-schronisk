from flask import Flask, request

from operations.user import USER_STATUS_LABELS
from operations.user.ListUsersQuery import ListUsersQuery
from web import page


def register(app: Flask) -> None:
    @app.get("/admin/users")
    @page("admin/users/list.html")
    def user_list(list_users: ListUsersQuery):
        page_num = max(request.args.get("page", 1, type=int), 1)
        search = request.args.get("search", "").strip()
        status = request.args.get("status", "")
        if status not in USER_STATUS_LABELS:
            status = ""

        result = list_users.execute(search=search, status=status, page=page_num)

        return {
            "users": result["items"],
            "pagination": result["pagination"],
            "status_labels": USER_STATUS_LABELS,
            "search": search,
            "status": status,
        }
