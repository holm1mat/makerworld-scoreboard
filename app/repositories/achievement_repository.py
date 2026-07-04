import sqlite3


def insert_achievement(
    conn: sqlite3.Connection,
    created_at: str,
    achievement_type: str,
    stat: str,
    threshold: int | None,
    current_value: int,
    delta: int | None,
    priority: str,
    message: str,
) -> int:
    cursor = conn.execute(
        """
        INSERT INTO achievements (
            created_at, achievement_type, stat, threshold,
            current_value, delta, priority, message, seen_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL)
        """,
        (
            created_at,
            achievement_type,
            stat,
            threshold,
            current_value,
            delta,
            priority,
            message,
        ),
    )
    return cursor.lastrowid


def get_recent_achievements(conn: sqlite3.Connection, limit: int = 25) -> list[dict]:
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT *
        FROM achievements
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    return [dict(row) for row in rows]


def achievement_exists_today(conn: sqlite3.Connection, achievement_type: str, day_prefix: str) -> bool:
    row = conn.execute(
        """
        SELECT id
        FROM achievements
        WHERE achievement_type = ?
          AND created_at LIKE ?
        LIMIT 1
        """,
        (achievement_type, f"{day_prefix}%"),
    ).fetchone()

    return row is not None