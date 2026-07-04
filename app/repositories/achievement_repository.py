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
            current_value, delta, priority, message, seen
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
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


def get_recent_achievements(
    conn: sqlite3.Connection,
    limit: int = 25,
) -> list[dict]:
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

    achievements = []

    for row in rows:
        achievement = dict(row)
        achievement["seen"] = bool(achievement["seen"])
        achievements.append(achievement)

    return achievements


def get_pending_achievements(
    conn: sqlite3.Connection,
    limit: int = 10,
):
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        """
        SELECT *
        FROM achievements
        WHERE seen = 0
        ORDER BY id
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    return [
        {
            **dict(row),
            "seen": bool(row["seen"])
        }
        for row in rows
    ]


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


def mark_achievement_seen(
    conn: sqlite3.Connection,
    achievement_id: int,
) -> None:
    conn.execute(
        """
        UPDATE achievements
        SET seen = 1
        WHERE id = ?
        """,
        (achievement_id,),
    )