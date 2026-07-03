from datetime import datetime

from app.repositories.event_repository import insert_event

STAT_META = {
    "likes": {
        "singular": "Like",
        "plural": "Likes",
        "emoji": "❤️",
        "color": "#E74C3C",
        "icon": "heart"
    },
    "collects": {
        "singular": "Collect",
        "plural": "Collects",
        "emoji": "📁",
        "color": "#F39C12",
        "icon": "folder"
    },
    "downloads": {
        "singular": "Download",
        "plural": "Downloads",
        "emoji": "⬇️",
        "color": "#3498DB",
        "icon": "download"
    },
    "prints": {
        "singular": "Print",
        "plural": "Prints",
        "emoji": "🖨️",
        "color": "#9B59B6",
        "icon": "printer"
    },
    "boosts": {
        "singular": "Boost",
        "plural": "Boosts",
        "emoji": "🚀",
        "color": "#2ECC71",
        "icon": "rocket"
    },
    "followers": {
        "singular": "Follower",
        "plural": "Followers",
        "emoji": "👥",
        "color": "#1ABC9C",
        "icon": "users"
    }
}

STAT_KEYS = list(STAT_META.keys())


def generate_stat_change_events(previous: dict | None, latest: dict) -> list[dict]:
    if not previous:
        return []

    events = []

    for key in STAT_KEYS:
        old_value = previous.get(key) or 0
        new_value = latest.get(key) or 0
        delta = new_value - old_value

        if delta == 0:
            continue

        direction = "GAIN" if delta > 0 else "LOSS"
        event_type = f"{key.upper()}_{direction}"

        meta = STAT_META[key]

        singular = meta["singular"]
        plural = meta["plural"]
        emoji = meta["emoji"]

        label = singular if abs(delta) == 1 else plural
        sign = "+" if delta > 0 else ""

        message = f"{emoji} {sign}{delta} {label}"

        events.append(
            {
                "created_at": datetime.now().isoformat(),
                "event_type": event_type,
                "stat": key,
                "old_value": old_value,
                "new_value": new_value,
                "delta": delta,
                "message": message,
            }
        )

    return events


def persist_events(conn, events: list[dict]) -> list[int]:
    event_ids = []

    for event in events:
        event_id = insert_event(
            conn=conn,
            created_at=event["created_at"],
            event_type=event["event_type"],
            stat=event["stat"],
            old_value=event["old_value"],
            new_value=event["new_value"],
            delta=event["delta"],
            message=event["message"],
        )
        event_ids.append(event_id)

    return event_ids