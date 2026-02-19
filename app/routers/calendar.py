from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from datetime import datetime, date
from typing import List, Optional
import json

router = APIRouter(prefix="/calendars", tags=["Calendar"])

DATA_DIR = Path("data")
USER_FILE = DATA_DIR / "users.json"
CALENDAR_FILE = DATA_DIR / "calendar.json"


# ----------------------------
# 유틸
# ----------------------------

def load_users():
    return json.loads(USER_FILE.read_text())

def load_calendar():
    return json.loads(CALENDAR_FILE.read_text())

def save_calendar(data):
    CALENDAR_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False)
    )


def parse_date_range(start_date: str, end_date: str):
    start = datetime.fromisoformat(start_date + "T00:00:00")
    end = datetime.fromisoformat(end_date + "T23:59:59")
    return start, end


# =====================================================
# 1️⃣ 사용자 일정 조회
# =====================================================

@router.get("/{user_id}/events")
def get_user_events(
    user_id: str,
    start_date: str,
    end_date: str,
    include_private: bool = False
):
    users = load_users()
    calendar = load_calendar()

    if user_id not in users["employees"]:
        raise HTTPException(404, "User not found")

    start, end = parse_date_range(start_date, end_date)

    result = []

    for event in calendar["events"].values():
        event_start = datetime.fromisoformat(event["start"])
        event_end = datetime.fromisoformat(event["end"])

        if event_end < start or event_start > end:
            continue

        # 참석 여부 확인
        is_related = (
            event["organizer_id"] == user_id or
            any(a["id"] == user_id for a in event["attendees"])
        )

        if not is_related:
            continue

        if event["is_private"] and not include_private:
            continue

        organizer = users["employees"][event["organizer_id"]]

        attendees = []
        for a in event["attendees"]:
            emp = users["employees"].get(a["id"])
            if emp:
                attendees.append({
                    "id": emp["id"],
                    "name": emp["name"],
                    "response": a["response"]
                })

        result.append({
            "id": event["id"],
            "title": event["title"],
            "start": event["start"],
            "end": event["end"],
            "location": event["location"],
            "is_all_day": False,
            "is_private": event["is_private"],
            "status": "confirmed",
            "organizer": {
                "id": organizer["id"],
                "name": organizer["name"]
            },
            "attendees": attendees
        })

    return {
        "user_id": user_id,
        "events": result
    }


# =====================================================
# 2️⃣ Free/Busy
# =====================================================

@router.post("/freebusy")
def get_freebusy(payload: dict):
    user_ids: List[str] = payload["user_ids"]
    start_date = payload["start_date"]
    end_date = payload["end_date"]

    start, end = parse_date_range(start_date, end_date)
    calendar = load_calendar()

    results = {}

    for uid in user_ids:
        busy = []

        for event in calendar["events"].values():
            event_start = datetime.fromisoformat(event["start"])
            event_end = datetime.fromisoformat(event["end"])

            if event_end < start or event_start > end:
                continue

            if (
                event["organizer_id"] == uid or
                any(a["id"] == uid for a in event["attendees"])
            ):
                busy.append({
                    "start": event["start"],
                    "end": event["end"]
                })

        results[uid] = {"busy": busy}

    return {"results": results}


# =====================================================
# 3️⃣ 일정 생성
# =====================================================

@router.post("/events")
def create_event(payload: dict):

    calendar = load_calendar()

    next_id = calendar["meta"]["next_event_id"]
    event_id = f"evt_{next_id:03d}"
    calendar["meta"]["next_event_id"] += 1

    now = datetime.now().isoformat()

    new_event = {
        "id": event_id,
        "title": payload["title"],
        "description": payload.get("description"),
        "start": payload["start"],
        "end": payload["end"],
        "location": payload.get("location"),
        "organizer_id": payload["organizer_id"],
        "attendees": [
            {
                "id": a["id"],
                "type": a.get("type", "required"),
                "response": "none"
            }
            for a in payload.get("attendees", [])
        ],
        "is_private": False,
        "recurrence": payload.get("recurrence"),
        "created_at": now,
        "updated_at": now
    }

    calendar["events"][event_id] = new_event
    save_calendar(calendar)

    return {
        "id": event_id,
        "title": new_event["title"],
        "start": new_event["start"],
        "end": new_event["end"],
        "location": new_event["location"],
        "status": "confirmed",
        "html_link": f"https://mock.calendar.local/event/{event_id}"
    }


# =====================================================
# 4️⃣ 일정 수정
# =====================================================

@router.put("/events/{event_id}")
def update_event(event_id: str, updates: dict):

    calendar = load_calendar()

    if event_id not in calendar["events"]:
        raise HTTPException(404, "Event not found")

    event = calendar["events"][event_id]

    for key, value in updates.items():
        if key in event:
            event[key] = value

    event["updated_at"] = datetime.now().isoformat()

    save_calendar(calendar)

    return event


# =====================================================
# 5️⃣ 일정 삭제
# =====================================================

@router.delete("/events/{event_id}")
def delete_event(event_id: str):

    calendar = load_calendar()

    if event_id not in calendar["events"]:
        raise HTTPException(404, "Event not found")

    del calendar["events"][event_id]
    save_calendar(calendar)

    return {"deleted": True}
