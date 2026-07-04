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

        conn.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                achievement_type TEXT NOT NULL,
                stat TEXT NOT NULL,
                threshold INTEGER,
                current_value INTEGER,
                delta INTEGER,
                priority TEXT NOT NULL,
                message TEXT NOT NULL,
                seen INTEGER NOT NULL DEFAULT 0
            )
        """)