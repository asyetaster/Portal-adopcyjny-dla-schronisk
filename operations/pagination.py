"""Wspólne stronicowanie list zwracanych przez Query.

Format wyniku: ``{"items": [...], "pagination": {...}}`` — ten sam, którego
oczekuje ``templates/_pagination.html``.
"""

from sqlalchemy import text
from sqlalchemy.engine import Connection


def like_pattern(value: str) -> str:
    """Wzorzec ``%value%`` dla ``LIKE ... ESCAPE '\\'`` z escapowaniem ``\\ % _``."""
    escaped = value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return f"%{escaped}%"


def paginate(
    connection: Connection,
    *,
    count_sql: str,
    rows_sql: str,
    params: dict,
    page: int,
    limit: int,
) -> dict:
    """Wykonuje zapytanie licznikowe i stronę wyników.

    ``rows_sql`` musi kończyć się ``LIMIT :limit OFFSET :offset``.
    """
    if limit < 1 or page < 1:
        raise ValueError("limit i page muszą być większe od 0")

    total = connection.execute(text(count_sql), params).scalar_one()
    rows = connection.execute(
        text(rows_sql),
        {**params, "limit": limit, "offset": (page - 1) * limit},
    ).mappings().all()

    total_pages = (total + limit - 1) // limit
    return {
        "items": [dict(row) for row in rows],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1,
        },
    }
