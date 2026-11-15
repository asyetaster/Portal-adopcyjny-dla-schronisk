from flask import Flask, request

from auth import shelter_required
from operations.shelter.ListShelterEmployeesQuery import ListShelterEmployeesQuery
from web import page


def register(app: Flask) -> None:
    @app.get("/panel/shelters/<int:shelter_id>/employees")
    @shelter_required()
    @page("panel/employees/list.html")
    def panel_employees(shelter_id: int, list_employees: ListShelterEmployeesQuery):
        page_num = max(request.args.get("page", 1, type=int), 1)
        result = list_employees.execute(shelter_id=shelter_id, page=page_num)
        return {"employees": result["items"], "pagination": result["pagination"]}
