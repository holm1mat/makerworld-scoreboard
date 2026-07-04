from datetime import datetime
import sqlite3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import get_connection
from app.schema import init_db
from app.schemas import MakerWorldStats
from app.services.delta_service import build_dashboard_summary, build_scoreboard_response
from app.services.ingest_service import process_snapshot
from app.repositories.snapshot_repository import get_recent_snapshots
from app.repositories.event_repository import get_recent_events
from app.repositories.achievement_repository import get_recent_achievements

app = FastAPI(title="MakerWorld Scoreboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "https://makerworld.com",
    "http://localhost:8787",
    "http://127.0.0.1:8787",
    ],
    allow_origin_regex=r"chrome-extension://.*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.post("/ingest")
def ingest(stats: MakerWorldStats):
    return process_snapshot(stats)


@app.get("/stats")
def latest_stats():
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            """
            SELECT *
            FROM stat_snapshots
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()

    if not row:
        return {"error": "No stats received yet"}

    return dict(row)


@app.get("/history")
def history(limit: int = 50):
    with get_connection() as conn:
        return get_recent_snapshots(conn, limit)


@app.get("/events")
def events(limit: int = 25):
    with get_connection() as conn:
        return get_recent_events(conn, limit)


@app.get("/dashboard")
def dashboard():
    with get_connection() as conn:
        return build_dashboard_summary(conn)
    

@app.get("/scoreboard")
def scoreboard():
    with get_connection() as conn:
        return build_scoreboard_response(conn)


@app.get("/achievements")
def achievements(limit: int = 25):
    with get_connection() as conn:
        return get_recent_achievements(conn, limit)