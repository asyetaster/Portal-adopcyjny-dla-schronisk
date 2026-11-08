from flask import Flask, abort, g

from auth import login_required
from operations.user.GetMyProfileQuery import GetMyProfileQuery
from web import page


def register(app: Flask) -> None:
    @app.get("/account/profile")
    @login_required
    @page("account/profile.html")
    def account_profile(get_profile: GetMyProfileQuery):
        profile = get_profile.execute(g.user["id"])

        if profile is None:
            abort(404)

        return {"profile": profile}
