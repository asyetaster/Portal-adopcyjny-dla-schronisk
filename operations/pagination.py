"""Wspólny helper stronicowania.

Zwraca strukturę w tym samym formacie, który zwracał ``ListUsersQuery``:
``{"items": [...], "pagination": {...}}``.
"""

from sqlalchemy import text
from sqlalchemy.engine import Connection


def build_pagination(*, page: int, limit: int, total: int) -> dict:
    total_pages = (total + limit - 1) // limit
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
    }


def paginate(
    connection: Connection,
    *,
    count_sql: str,
    items_sql: str,
    params: dict | None = None,
    page: int = 1,
    limit: int = 20,
) -> dict:
    """Wykonuje zapytanie z licznikiem i jedną stroną wyników.

    ``items_sql`` musi mieć własne ``ORDER BY`` i **nie** może mieć ``LIMIT``;
    helper dopisuje ``LIMIT :limit OFFSET :offset``. Nazwy parametrów ``limit``
    i ``offset`` są zarezerwowane.
    """
    if limit < 1 or page < 1:
        raise ValueError("limit i page muszą być większe od 0")

    params = dict(params or {})
    if "limit" in params or "offset" in params:
        raise ValueError("Parametry 'limit' i 'offset' są zarezerwowane")

    total = connection.execute(text(count_sql), params).scalar_one()

    rows = connection.execute(
        text(f"{items_sql}\nLIMIT :limit OFFSET :offset"),
        {**params, "limit": limit, "offset": (page - 1) * limit},
    ).mappings().all()

    return {
        "items": [dict(row) for row in rows],
        "pagination": build_pagination(page=page, limit=limit, total=total),
    }
