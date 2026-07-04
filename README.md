# README.md

# MakerWorld Scoreboard Architecture

## Vision

MakerWorld Scoreboard is a self-hosted dashboard and Raspberry Pi appliance that displays live MakerWorld statistics, recent activity, achievements, and milestones in a clean, retro-inspired interface.

The project is intentionally divided into small services with clear responsibilities so that it can evolve over time without becoming tightly coupled.

---

# High Level Architecture

```
                MakerWorld
                     │
                     ▼
           Chrome Extension Collector
                     │
              Reads __NEXT_DATA__
                     │
                     ▼
                POST /ingest
                     │
                     ▼
              Ingest Service
                     │
      ┌──────────────┴──────────────┐
      ▼                             ▼
 Snapshot Repository          Snapshot Service
      │
      ▼
    SQLite
      │
      ▼
 Delta Service
      │
 ┌────┴───────────────┐
 ▼                    ▼
Event Service   Achievement Service
                     │
             (Future)
                     ▼
             Milestone Service
                     │
                     ▼
                  FastAPI
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
      React Dashboard      Raspberry Pi UI
```

---

# Backend Responsibilities

## Snapshot Service

Purpose:

Persist the raw truth reported by MakerWorld.

Responsibilities:

* Store every snapshot.
* Never modify or interpret data.
* Act as the historical source of truth.

---

## Delta Service

Purpose:

Compare snapshots over time.

Produces:

* Today
* Last Hour
* Last 7 Days

The Delta Service is intentionally stateless and derives all calculations from snapshot history.

---

## Event Service

Purpose:

Generate an activity stream from snapshot differences.

Examples:

* ❤️ +3 Likes
* 📁 +5 Collects
* ⬇️ +2 Downloads
* 🖨️ +1 Print

Events represent factual changes and are shown in the Recent Activity feed.

---

## Achievement Service

Purpose:

Recognize meaningful accomplishments that deserve celebration.

Current achievement rules:

* 🚀 Boost Received
* 👤 New Follower
* ❤️ 100 Likes Today
* 📁 500 Collects Today
* ⬇️ 400 Downloads Today
* 🖨️ 200 Prints Today

Achievements are intended to drive temporary full-screen UI takeovers.

Unlike Events, Achievements are not part of the permanent dashboard.

---

# Repository Layer

Repositories are responsible only for persistence.

Current repositories:

* snapshot_repository.py
* event_repository.py
* achievement_repository.py

Repositories should never contain business logic.

---

# Database

SQLite is the project's primary datastore.

Current tables:

* snapshots
* events
* achievements

Future tables may include:

* milestones
* settings
* models

---

# Collector

The Chrome Extension is currently the only collector.

Responsibilities:

* Read MakerWorld's `window.__NEXT_DATA__`
* Refresh the MakerWorld page periodically
* POST snapshots to the backend

The backend intentionally does not know or care how data is collected.

Future collectors could include:

* Firefox Extension
* Official API (if one becomes available)

---

# Frontend Responsibilities

The React application owns:

* Dashboard layout
* Theme
* Animations
* Recent Activity feed
* Achievement takeovers
* Navigation
* Settings

The frontend should never calculate statistics.

All business logic belongs in the backend.

---

# Design Philosophy

The backend answers:

* What happened?
* What changed?
* What deserves celebration?

The frontend answers:

* How should it look?
* How should it animate?
* How should it be presented?

Keeping these responsibilities separate allows the dashboard to remain simple while the backend continues to grow.

---

# Long-Term Roadmap

## Backend

* Snapshot Service ✅
* Delta Service ✅
* Event Service ✅
* Achievement Service ✅
* Milestone Service (planned)
* Per-model analytics
* Configuration system

## Frontend

* React dashboard
* Achievement animations
* Theme system
* Settings page

## Hardware

* Raspberry Pi appliance
* Chromium kiosk mode
* 3D printed enclosure
* Optional LEDs / audio for celebrations
