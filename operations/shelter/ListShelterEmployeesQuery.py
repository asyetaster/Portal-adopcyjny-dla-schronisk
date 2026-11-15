from sqlalchemy.engine import Connection

from operations.pagination import paginate


class ListShelterEmployeesQuery:
    """Pracownicy placówki, sortowani po nazwisku."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, shelter_id: int, page: int = 1, limit: int = 20) -> dict:
        return paginate(
            self.connection,
            count_sql="SELECT COUNT(*) FROM shelter_employees WHERE shelter_id = :shelter_id",
            rows_sql="""
                SELECT
                    u.id,
                    u.first_name,
                    u.last_name,
                    u.email,
                    u.status,
                    e.is_manager,
                    e.assigned_at
                FROM shelter_employees e
                JOIN users u ON u.id = e.user_id
                WHERE e.shelter_id = :shelter_id
                ORDER BY u.last_name, u.first_name, u.id
                LIMIT :limit OFFSET :offset
            """,
            params={"shelter_id": shelter_id},
            page=page,
            limit=limit,
        )
