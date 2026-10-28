from flask import Flask, request

from operations.user.ListUsersQuery import ListUsersQuery
from web import page


def register(app: Flask) -> None:
    @app.get("/admin/users")
    @page("admin/users/list.html")
    def user_list(list_users: ListUsersQuery):
        # `page` z query stringa; chronimy przed wartościami < 1,
        # których query by nie przyjęło (ValueError => 500).
        page_num = max(request.args.get("page", 1, type=int), 1)
        result = list_users.execute(page=page_num)
        return {"users": result["items"], "pagination": result["pagination"]}