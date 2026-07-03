from app.database import get_connection


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stat_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                captured_at TEXT NOT NULL,
                received_at TEXT NOT NULL,
                source TEXT NOT NULL,
                handle TEXT NOT NULL,
                collects INTEGER,
                downloads INTEGER,
                prints INTEGER,
                boosts INTEGER,
                followers INTEGER,
                likes INTEGER
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                event_type TEXT NOT NULL,
                stat TEXT,
                old_value INTEGER,
                new_value INTEGER,
                delta INTEGER,
                message TEXT
            )
        """)