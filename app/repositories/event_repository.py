import sqlite3


def insert_event(
    conn: sqlite3.Connection,
    created_at: str,
    event_type: str,
    stat: str | None,
    old_value: int | None,
    new_value: int | None,
    delta: int | None,
    message: str,
) -> int:
    cursor = conn.execute(
        """
        INSERT INTO events (
            created_at, event_type, stat, old_value,
            new_value, delta, message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            created_at,
            event_type,
            stat,
            old_value,
            new_value,
            delta,
            message,
        ),
    )
    return cursor.lastrowid


def get_recent_events(conn: sqlite3.Connection, limit: int = 25) -> list[dict]:
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT *
        FROM events
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    return [dict(row) for row in rows]