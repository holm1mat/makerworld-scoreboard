from datetime import datetime

from app.database import get_connection
from app.schemas import MakerWorldStats
from app.repositories.snapshot_repository import insert_snapshot


from datetime import datetime

from app.database import get_connection
from app.schemas import MakerWorldStats
from app.repositories.snapshot_repository import (
    get_latest_snapshot,
    insert_snapshot,
)
from app.services.event_service import (
    generate_stat_change_events,
    persist_events,
)
from app.services.achievement_service import generate_achievements, persist_achievements
from app.services.delta_service import build_dashboard_summary

def process_snapshot(stats: MakerWorldStats):
    received_at = datetime.now().isoformat()

    with get_connection() as conn:
        previous_snapshot = get_latest_snapshot(conn)

        snapshot_id = insert_snapshot(conn, stats, received_at)

        latest_snapshot = {
            "id": snapshot_id,
            "captured_at": stats.capturedAt,
            "received_at": received_at,
            "source": stats.source,
            "handle": stats.handle,
            "collects": stats.collects,
            "downloads": stats.downloads,
            "prints": stats.prints,
            "boosts": stats.boosts,
            "followers": stats.followers,
            "likes": stats.likes,
        }

        events = generate_stat_change_events(previous_snapshot, latest_snapshot)
        event_ids = persist_events(conn, events)

        dashboard = build_dashboard_summary(conn)
        today_deltas = dashboard.get("deltas", {}).get("today", {})

        achievements = generate_achievements(
            conn=conn,
            previous_snapshot=previous_snapshot,
            latest_snapshot=latest_snapshot,
            today_deltas=today_deltas,
        )
        achievement_ids = persist_achievements(conn, achievements)

    return {
        "ok": True,
        "snapshotId": snapshot_id,
        "eventIds": event_ids,
        "eventCount": len(event_ids),
        "achievementIds": achievement_ids,
        "achievementCount": len(achievement_ids),
        "receivedAt": received_at,
    }