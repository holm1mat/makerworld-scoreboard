from datetime import datetime, timedelta

from app.repositories.snapshot_repository import (
    get_latest_snapshot,
    get_first_snapshot_after,
)

STAT_KEYS = ["collects", "downloads", "prints", "boosts", "followers", "likes"]


def calculate_delta(latest: dict, baseline: dict | None):
    if not latest or not baseline:
        return {key: 0 for key in STAT_KEYS}

    return {
        key: (latest.get(key) or 0) - (baseline.get(key) or 0)
        for key in STAT_KEYS
    }


def build_dashboard_summary(conn):
    latest = get_latest_snapshot(conn)

    if not latest:
        return {"error": "No stats received yet"}

    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    hour_start = now - timedelta(hours=1)
    week_start = now - timedelta(days=7)

    today_baseline = get_first_snapshot_after(conn, today_start.isoformat())
    hour_baseline = get_first_snapshot_after(conn, hour_start.isoformat())
    week_baseline = get_first_snapshot_after(conn, week_start.isoformat())

    return {
        "latest": latest,
        "deltas": {
            "today": calculate_delta(latest, today_baseline),
            "lastHour": calculate_delta(latest, hour_baseline),
            "last7Days": calculate_delta(latest, week_baseline),
        },
    }


def build_scoreboard_response(conn):
    dashboard = build_dashboard_summary(conn)

    if "error" in dashboard:
        return dashboard

    latest = dashboard["latest"]
    today = dashboard["deltas"]["today"]

    return {
        "stats": {
            key: {
                "total": latest.get(key),
                "today": today.get(key, 0),
                "lastHour": dashboard["deltas"]["lastHour"].get(key, 0),
                "last7Days": dashboard["deltas"]["last7Days"].get(key, 0),
            }
            for key in STAT_KEYS
        },
        "updatedAt": latest.get("received_at"),
        "capturedAt": latest.get("captured_at"),
        "handle": latest.get("handle"),
    }