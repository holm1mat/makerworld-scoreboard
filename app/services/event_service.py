from datetime import datetime

from app.repositories.event_repository import insert_event

STAT_META = {
    "likes": {
        "singular": "Like",
        "plural": "Likes",
        "color": "#FF4D4D",
        "icon": "heart"
    },
    "collects": {
        "singular": "Collect",
        "plural": "Collects",
        "color": "#FFC61A",
        "icon": "folder"
    },
    "downloads": {
        "singular": "Download",
        "plural": "Downloads",
        "color": "#23B5FF",
        "icon": "download"
    },
    "prints": {
        "singular": "Print",
        "plural": "Prints",
        "color": "#39E75F",
        "icon": "printer"
    },
    "boosts": {
        "singular": "Boost",
        "plural": "Boosts",
        "color": "#B05CFF",
        "icon": "rocket"
    },
    "followers": {
        "singular": "Follower",
        "plural": "Followers",
        "color": "#35D8FF",
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

        label = singular if abs(delta) == 1 else plural
        sign = "+" if delta > 0 else ""

        message = f"{sign}{delta} {label}"

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