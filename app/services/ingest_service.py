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

    return {
        "ok": True,
        "snapshotId": snapshot_id,
        "eventIds": event_ids,
        "eventCount": len(event_ids),
        "receivedAt": received_at,
    }