from fastapi import APIRouter
from pathlib import Path
import json
import random
from datetime import datetime, timedelta
import uuid

router = APIRouter(
    prefix="/mock",
    tags=["Mock Data"]
)

DATA_DIR = Path("data")
USER_FILE = DATA_DIR / "users.json"
CALENDAR_FILE = DATA_DIR / "calendar.json"

DEPARTMENTS = [
    ("dept_company", "회사", None),
    ("dept_tech", "기술본부", "dept_company"),
    ("dept_dev", "개발팀", "dept_tech"),
    ("dept_design", "디자인팀", "dept_tech"),
    ("dept_hr", "인사팀", "dept_company"),
]

POSITIONS = ["사원", "주임", "대리", "선임", "팀장"]
KOREAN_LAST = [
    "김", "이", "박", "최", "정", "강", "조", "윤", "장", "임",
    "한", "오", "서", "신", "권", "황", "안", "송", "류", "홍",
    "전", "고", "문", "양", "손", "배", "백", "허", "유", "남", 
]

KOREAN_FIRST = [
    "민준", "서준", "도윤", "예준", "시우", "지호", "하준", "우진", "현우", "지훈",
    "준서", "유준", "건우", "서진", "민재", "현준", "선우", "은우", "태윤", "수호",
    "지환", "승현", "재윤", "태현", "동현", "성민", "정우", "준혁", "시윤", "진우",
    "서연", "서윤", "지우", "하은", "하윤", "민서", "지유", "예은", "채원", "소율",
    "지민", "예린", "수아", "다은", "유나", "아린", "나은", "서아", "지아", "윤서",
    "은서", "하린", "소윤", "연우", "채윤", "시은", "가은", "지현", "보민", "유진",
    "하늘", "다온", "로운", "이안", "도현", "태린", "라온", "시온", "지안", "해인"
]

EVENT_TITLES = [
    "팀 회의",
    "1:1 미팅",
    "프로젝트 킥오프",
    "디자인 리뷰",
    "스프린트 회고",
    "전사 미팅"
]


@router.get("/refresh")
def refresh_all():

    DATA_DIR.mkdir(exist_ok=True)

    # =========================
    # 1️⃣ 직원 생성
    # =========================

    employee_count = random.randint(30, 80)

    departments = {}
    employees = {}

    for dept_id, name, parent in DEPARTMENTS:
        departments[dept_id] = {
            "id": dept_id,
            "name": name,
            "parent_id": parent,
            "manager_id": None
        }

    for i in range(1, employee_count + 1):
        emp_id = f"emp_{i:03d}"
        name = random.choice(KOREAN_LAST) + random.choice(KOREAN_FIRST)
        dept_id = random.choice(list(departments.keys()))

        employees[emp_id] = {
            "id": emp_id,
            "name": name,
            "email": f"{emp_id}@company.com",
            "department_id": dept_id,
            "position": random.choice(POSITIONS),
            "phone": f"010-{random.randint(1000,9999)}-{random.randint(1000,9999)}",
            "office_location": f"본관 {random.randint(2,5)}층",
            "manager_id": None,
            "joined_date": f"20{random.randint(18,23)}-0{random.randint(1,9)}-01",
            "profile_image": None
        }

    # 부서별 매니저 지정
    for dept in departments.values():
        dept_members = [
            emp_id for emp_id, emp in employees.items()
            if emp["department_id"] == dept["id"]
        ]
        if dept_members:
            manager_id = random.choice(dept_members)
            dept["manager_id"] = manager_id

    user_data = {
        "meta": {
            "generated_at": datetime.now().isoformat()
        },
        "departments": departments,
        "employees": employees
    }

    USER_FILE.write_text(
        json.dumps(user_data, indent=2, ensure_ascii=False)
    )

    # =========================
    # 2️⃣ 일정 생성 (employees 기반)
    # =========================

    event_count = random.randint(50, 150)
    events = {}

    employee_ids = list(employees.keys())

    for i in range(1, event_count + 1):
        event_id = f"evt_{i:03d}"

        organizer = random.choice(employee_ids)

        attendee_count = random.randint(1, 5)
        attendees_sample = random.sample(employee_ids, attendee_count)

        now = datetime.now()
        start = now + timedelta(days=random.randint(-30, 30),
                                hours=random.randint(8, 18))
        end = start + timedelta(hours=random.randint(1, 2))

        events[event_id] = {
            "id": event_id,
            "title": random.choice(EVENT_TITLES),
            "start": start.isoformat(),
            "end": end.isoformat(),
            "organizer_id": organizer,
            "attendees": [
                {
                    "id": emp_id,
                    "type": random.choice(["required", "optional"]),
                    "response": random.choice(["accepted", "declined", "none"])
                }
                for emp_id in attendees_sample
            ],
            "location": f"회의실 {random.randint(1,5)}",
            "description": None,
            "is_private": random.choice([True, False]),
            "recurrence": None,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }

    calendar_data = {
        "meta": {
            "next_event_id": event_count + 1,
            "generated_at": datetime.now().isoformat()
        },
        "events": events
    }

    CALENDAR_FILE.write_text(
        json.dumps(calendar_data, indent=2, ensure_ascii=False)
    )

    return {
        "status": "ok",
        "employees": employee_count,
        "events": event_count
    }
