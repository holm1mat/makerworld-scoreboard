from datetime import datetime

from app.repositories.achievement_repository import (
    achievement_exists_today,
    insert_achievement,
)

ACHIEVEMENT_RULES = [
    {
        "id": "BOOST_RECEIVED",
        "stat": "boosts",
        "trigger": "gain",
        "threshold": 1,
        "priority": "takeover",
        "message": "🚀 Boost received!",
    },
    {
        "id": "FOLLOWER_GAIN",
        "stat": "followers",
        "trigger": "gain",
        "threshold": 1,
        "priority": "takeover",
        "message": "👤 New follower!",
    },
    {
        "id": "DAILY_LIKES_100",
        "stat": "likes",
        "trigger": "daily_total",
        "threshold": 100,
        "priority": "takeover",
        "message": "❤️ 100 likes today!",
    },
    {
        "id": "DAILY_COLLECTS_200",
        "stat": "collects",
        "trigger": "daily_total",
        "threshold": 500,
        "priority": "takeover",
        "message": "📁 500 collects today!",
    },
    {
        "id": "DAILY_DOWNLOADS_250",
        "stat": "downloads",
        "trigger": "daily_total",
        "threshold": 400,
        "priority": "takeover",
        "message": "⬇️ 400 downloads today!",
    },
    {
        "id": "DAILY_PRINTS_50",
        "stat": "prints",
        "trigger": "daily_total",
        "threshold": 200,
        "priority": "takeover",
        "message": "🖨️ 200 prints today!",
    },
]


def generate_achievements(
    conn,
    previous_snapshot: dict | None,
    latest_snapshot: dict,
    today_deltas: dict,
) -> list[dict]:
    now = datetime.now()
    created_at = now.isoformat()
    day_prefix = now.date().isoformat()

    achievements = []

    for rule in ACHIEVEMENT_RULES:
        rule_id = rule["id"]
        stat = rule["stat"]
        trigger = rule["trigger"]
        threshold = rule["threshold"]

        if trigger == "gain":
            if not previous_snapshot:
                continue

            previous_value = previous_snapshot.get(stat) or 0
            current_value = latest_snapshot.get(stat) or 0
            delta = current_value - previous_value

            if delta < threshold:
                continue

            achievements.append(
                {
                    "created_at": created_at,
                    "achievement_type": rule_id,
                    "stat": stat,
                    "threshold": threshold,
                    "current_value": current_value,
                    "delta": delta,
                    "priority": rule["priority"],
                    "message": rule["message"],
                }
            )

        elif trigger == "daily_total":
            daily_total = today_deltas.get(stat) or 0

            if daily_total < threshold:
                continue

            # Only fire each daily achievement once per day.
            if achievement_exists_today(conn, rule_id, day_prefix):
                continue

            achievements.append(
                {
                    "created_at": created_at,
                    "achievement_type": rule_id,
                    "stat": stat,
                    "threshold": threshold,
                    "current_value": latest_snapshot.get(stat) or 0,
                    "delta": daily_total,
                    "priority": rule["priority"],
                    "message": rule["message"],
                }
            )

    return achievements


def persist_achievements(conn, achievements: list[dict]) -> list[int]:
    achievement_ids = []

    for achievement in achievements:
        achievement_id = insert_achievement(
            conn=conn,
            created_at=achievement["created_at"],
            achievement_type=achievement["achievement_type"],
            stat=achievement["stat"],
            threshold=achievement["threshold"],
            current_value=achievement["current_value"],
            delta=achievement["delta"],
            priority=achievement["priority"],
            message=achievement["message"],
        )
        achievement_ids.append(achievement_id)

    return achievement_ids