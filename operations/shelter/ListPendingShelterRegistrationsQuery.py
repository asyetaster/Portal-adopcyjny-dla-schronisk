from sqlalchemy.engine import Connection

from operations.pagination import paginate


class ListPendingShelterRegistrationsQuery:
    """Admin: zgłoszenia placówek do decyzji, najstarsze najpierw."""

    def __init__(self, connection: Connection):
        self.connection = connection

    def execute(self, page: int = 1, limit: int = 20) -> dict:
        return paginate(
            self.connection,
            count_sql="SELECT COUNT(*) FROM shelters WHERE status = 'Pending'",
            rows_sql="""
                SELECT
                    s.id,
                    s.name,
                    s.city,
                    s.voivodeship,
                    s.contact_email,
                    s.submitted_at,
                    u.first_name AS submitter_first_name,
                    u.last_name AS submitter_last_name,
                    u.email AS submitter_email
                FROM shelters s
                JOIN users u ON u.id = s.submitted_by
                WHERE s.status = 'Pending'
                ORDER BY s.submitted_at ASC, s.id ASC
                LIMIT :limit OFFSET :offset
            """,
            params={},
            page=page,
            limit=limit,
        )
