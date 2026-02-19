from fastapi import APIRouter
from pathlib import Path
import json
import random
from datetime import datetime, timedelta, timezone

router = APIRouter(
    prefix="/calendar",
    tags=["Calendar"]
)

DATA_DIR = Path("data")
CALENDAR_FILE = DATA_DIR / "calendar.json"

USER_IDS = ["emp_001", "emp_002", "emp_003", "emp_004", "emp_005"]
LOCATIONS = ["본관 대회의실", "온라인 Zoom", "회의실 A", "회의실 B"]
TITLES = ["팀 회의", "기획 미팅", "1:1 면담", "프로젝트 점검", "디자인 리뷰"]


@router.get("/refresh")
def refresh_calendar():

    DATA_DIR.mkdir(exist_ok=True)

    event_count = random.randint(5, 20)

    events = {}
    base_date = datetime(2024, 1, 1, tzinfo=timezone(timedelta(hours=9)))

    for i in range(1, event_count + 1):
        event_id = f"evt_{i:03d}"

        start_offset_days = random.randint(0, 30)
        start_hour = random.randint(9, 17)

        start_time = base_date + timedelta(days=start_offset_days, hours=start_hour)
        end_time = start_time + timedelta(hours=1)

        organizer = random.choice(USER_IDS)

        attendee_pool = [u for u in USER_IDS if u != organizer]
        random.shuffle(attendee_pool)

        attendee_count = random.randint(1, len(attendee_pool))
        attendees = []

        for uid in attendee_pool[:attendee_count]:
            attendees.append({
                "id": uid,
                "type": random.choice(["required", "optional"]),
                "response": random.choice(["accepted", "declined", "tentative", "none"])
            })

        events[event_id] = {
            "id": event_id,
            "title": random.choice(TITLES),
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "organizer_id": organizer,
            "attendees": attendees,
            "location": random.choice(LOCATIONS),
            "description": None,
            "is_private": random.choice([True, False]),
            "recurrence": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

    data = {
        "meta": {
            "next_event_id": event_count + 1
        },
        "events": events
    }

    CALENDAR_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False)
    )

    return {
        "status": "ok",
        "generated_events": event_count
    }
