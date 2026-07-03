import sqlite3
from app.schemas import MakerWorldStats


def insert_snapshot(conn: sqlite3.Connection, stats: MakerWorldStats, received_at: str) -> int:
    cursor = conn.execute(
        """
        INSERT INTO stat_snapshots (
            captured_at, received_at, source, handle,
            collects, downloads, prints, boosts, followers, likes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            stats.capturedAt,
            received_at,
            stats.source,
            stats.handle,
            stats.collects,
            stats.downloads,
            stats.prints,
            stats.boosts,
            stats.followers,
            stats.likes,
        ),
    )
    return cursor.lastrowid


def get_latest_snapshot(conn: sqlite3.Connection) -> dict | None:
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        """
        SELECT *
        FROM stat_snapshots
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    return dict(row) if row else None


def get_previous_snapshot(conn: sqlite3.Connection, current_snapshot_id: int) -> dict | None:
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        """
        SELECT *
        FROM stat_snapshots
        WHERE id < ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (current_snapshot_id,),
    ).fetchone()

    return dict(row) if row else None


def get_recent_snapshots(conn: sqlite3.Connection, limit: int = 50) -> list[dict]:
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT *
        FROM stat_snapshots
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    return [dict(row) for row in rows]


def get_first_snapshot_after(conn: sqlite3.Connection, cutoff_iso: str) -> dict | None:
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        """
        SELECT *
        FROM stat_snapshots
        WHERE received_at >= ?
        ORDER BY received_at ASC
        LIMIT 1
        """,
        (cutoff_iso,),
    ).fetchone()

    return dict(row) if row else None