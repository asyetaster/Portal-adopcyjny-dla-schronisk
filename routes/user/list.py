from flask import Flask

from operations.user.ListUsersQuery import ListUsersQuery
from web import page


def register(app: Flask) -> None:
    @app.get("/admin/users")
    @page("admin/users/list.html")
    def user_list(list_users: ListUsersQuery):
        return {"users": list_users.execute()}