from fastapi import APIRouter
from pathlib import Path
import json
import random
from datetime import datetime

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

DATA_DIR = Path("data")
USER_FILE = DATA_DIR / "users.json"

DEPARTMENTS = [
    ("dept_company", "회사", None),
    ("dept_tech", "기술본부", "dept_company"),
    ("dept_dev", "개발팀", "dept_tech"),
    ("dept_design", "디자인팀", "dept_tech"),
    ("dept_hr", "인사팀", "dept_company"),
]

POSITIONS = ["사원", "주임", "대리", "선임", "팀장"]
KOREAN_LAST = ["김", "이", "박", "최", "정", "강"]
KOREAN_FIRST = ["민수", "서연", "지훈", "지민", "하늘", "수빈"]


@router.get("/refresh")
def refresh_users():

    DATA_DIR.mkdir(exist_ok=True)

    employee_count = random.randint(30, 80)

    departments = {}
    employees = {}

    # 부서 생성
    for dept_id, name, parent in DEPARTMENTS:
        departments[dept_id] = {
            "id": dept_id,
            "name": name,
            "parent_id": parent,
            "manager_id": None
        }

    # 직원 생성
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

    # 각 부서에 랜덤 매니저 지정
    for dept in departments.values():
        dept_members = [
            emp_id for emp_id, emp in employees.items()
            if emp["department_id"] == dept["id"]
        ]
        if dept_members:
            manager_id = random.choice(dept_members)
            dept["manager_id"] = manager_id

    data = {
        "meta": {
            "generated_at": datetime.now().isoformat()
        },
        "departments": departments,
        "employees": employees
    }

    USER_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False)
    )

    return {
        "status": "ok",
        "generated_employees": employee_count,
        "generated_departments": len(departments)
    }
