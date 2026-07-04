# API.md

# MakerWorld Scoreboard API

Base URL

```
http://127.0.0.1:8787
```

---

# POST /ingest

Receives a snapshot from the Chrome Extension.

Example request:

```json
{
  "capturedAt": "2026-07-03T20:40:43.732632",
  "source": "makerworld-next-data-script",
  "handle": "@makermatt3D",
  "likes": 32812,
  "collects": 100756,
  "downloads": 88670,
  "prints": 58480,
  "boosts": 2124,
  "followers": 1917
}
```

Example response:

```json
{
  "ok": true,
  "snapshotId": 123,
  "eventIds": [45, 46],
  "eventCount": 2,
  "achievementIds": [8],
  "achievementCount": 1,
  "receivedAt": "2026-07-03T20:40:43.900Z"
}
```

---

# GET /scoreboard

Returns the current totals and calculated deltas.

Example response:

```json
{
  "stats": {
    "likes": {
      "total": 32812,
      "today": 151,
      "lastHour": 8,
      "last7Days": 1050
    },
    "collects": {
      "total": 100756,
      "today": 592,
      "lastHour": 20,
      "last7Days": 3900
    },
    "downloads": {
      "total": 88670,
      "today": 457,
      "lastHour": 14,
      "last7Days": 2700
    },
    "prints": {
      "total": 58480,
      "today": 295,
      "lastHour": 9,
      "last7Days": 1800
    },
    "boosts": {
      "total": 2124,
      "today": 1,
      "lastHour": 0,
      "last7Days": 4
    },
    "followers": {
      "total": 1917,
      "today": 1,
      "lastHour": 0,
      "last7Days": 12
    }
  },
  "capturedAt": "...",
  "updatedAt": "...",
  "handle": "@makermatt3D"
}
```

---

# GET /events

Returns the recent activity stream.

Example response:

```json
[
  {
    "id": 12,
    "created_at": "...",
    "event_type": "LIKES_GAIN",
    "stat": "likes",
    "old_value": 32810,
    "new_value": 32812,
    "delta": 2,
    "message": "❤️ +2 Likes"
  }
]
```

---

# GET /achievements

Returns recently generated achievements.

Example response:

```json
[
  {
    "id": 4,
    "created_at": "...",
    "achievement_type": "BOOST_RECEIVED",
    "stat": "boosts",
    "threshold": 1,
    "current_value": 2124,
    "delta": 1,
    "priority": "takeover",
    "message": "🚀 Boost received!",
    "seen": 0
  }
]
```

---

# GET /history

Returns raw historical snapshots.

Primarily used for debugging and future analytics.

---

# Planned Endpoints

## GET /milestones

Returns lifetime milestone celebrations.

---

## POST /achievements/{id}/seen

Marks an achievement as displayed by the dashboard.

Used so takeover animations are shown only once.

---

# API Philosophy

The backend is responsible for:

* Data collection
* Historical storage
* Delta calculations
* Event generation
* Achievement generation
* Business rules

The frontend is responsible only for presentation.

The frontend should never calculate deltas, derive achievements, or interpret business logic.

---

# Stability

The React dashboard should treat these endpoints as the canonical contract.

Whenever backend behavior changes, this document should be updated to reflect the new API before frontend work begins.
