from flask import Flask

from auth import shelter_required
from operations.shelter import SHELTER_STATUS_LABELS
from operations.shelter.GetShelterForManagementQuery import GetShelterForManagementQuery
from web import page


def register(app: Flask) -> None:
    @app.get("/panel/shelters/<int:shelter_id>")
    @shelter_required()
    @page("panel/dashboard.html")
    def panel_dashboard(shelter_id: int, get_shelter: GetShelterForManagementQuery):
        return {
            "shelter": get_shelter.execute(shelter_id),
            "status_labels": SHELTER_STATUS_LABELS,
        }
