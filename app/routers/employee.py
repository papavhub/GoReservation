from fastapi import APIRouter
from pathlib import Path
import json
import random
from datetime import datetime

router = APIRouter(
    prefix="",
    tags=["Employees"]
)

DATA_DIR = Path("data")
USER_FILE = DATA_DIR / "users.json"

from fastapi import Query, Path, HTTPException

def load_data():
    if not USER_FILE.exists():
        raise HTTPException(status_code=404, detail="Data not generated. Call /refresh first.")
    return json.loads(USER_FILE.read_text(encoding="utf-8"))


def build_department_path(departments, dept_id):
    path = []
    current = departments.get(dept_id)

    while current:
        path.insert(0, current["name"])
        parent_id = current["parent_id"]
        current = departments.get(parent_id) if parent_id else None

    return path


# 1. 직원 검색
@router.get("/employees/search")
def employee_search(
    q: str = Query(...),
    limit: int = Query(20),
    offset: int = Query(0)
):
    data = load_data()
    departments = data["departments"]
    employees = data["employees"]

    results = []

    for emp in employees.values():
        dept = departments.get(emp["department_id"])

        if (
            q.lower() in emp["name"].lower()
            or q.lower() in emp["email"].lower()
            or (dept and q.lower() in dept["name"].lower())
        ):
            results.append({
                "id": emp["id"],
                "name": emp["name"],
                "email": emp["email"],
                "department": {
                    "id": dept["id"],
                    "name": dept["name"]
                },
                "position": emp["position"],
                "phone": emp["phone"],
                "profile_image": emp["profile_image"]
            })

    total = len(results)

    return {
        "total": total,
        "employees": results[offset:offset + limit]
    }


# 2. 직원 상세 조회
@router.get("/employees/{employee_id}")
def employee_detail(
    employee_id: str = Path(...)
):
    data = load_data()
    departments = data["departments"]
    employees = data["employees"]

    emp = employees.get(employee_id)

    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    dept = departments.get(emp["department_id"])

    manager = None
    if dept and dept.get("manager_id"):
        manager_emp = employees.get(dept["manager_id"])
        if manager_emp:
            manager = {
                "id": manager_emp["id"],
                "name": manager_emp["name"]
            }

    return {
        "id": emp["id"],
        "name": emp["name"],
        "email": emp["email"],
        "department": {
            "id": dept["id"],
            "name": dept["name"],
            "path": build_department_path(departments, dept["id"])
        },
        "position": emp["position"],
        "phone": emp["phone"],
        "office_location": emp["office_location"],
        "manager": manager,
        "profile_image": emp["profile_image"],
        "joined_date": emp["joined_date"]
    }


# 3. 팀/부서 멤버 조회
@router.get("/departments/{department_id}/members")
def department_members(
    department_id: str,
    include_sub: bool = Query(False)
):
    data = load_data()
    departments = data["departments"]
    employees = data["employees"]

    dept = departments.get(department_id)

    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    target_depts = {department_id}

    if include_sub:
        for d in departments.values():
            if d["parent_id"] == department_id:
                target_depts.add(d["id"])

    members = [
        {
            "id": emp["id"],
            "name": emp["name"],
            "email": emp["email"],
            "position": emp["position"]
        }
        for emp in employees.values()
        if emp["department_id"] in target_depts
    ]

    return {
        "department": {
            "id": dept["id"],
            "name": dept["name"]
        },
        "members": members,
        "total": len(members)
    }


# 4. 조직도 조회
@router.get("/organization")
def organization():
    data = load_data()
    departments = data["departments"]
    employees = data["employees"]

    result = []

    for dept in departments.values():
        member_count = len([
            emp for emp in employees.values()
            if emp["department_id"] == dept["id"]
        ])

        manager = None
        if dept.get("manager_id"):
            manager_emp = employees.get(dept["manager_id"])
            if manager_emp:
                manager = {
                    "id": manager_emp["id"],
                    "name": manager_emp["name"]
                }

        result.append({
            "id": dept["id"],
            "name": dept["name"],
            "parent_id": dept["parent_id"],
            "member_count": member_count,
            "manager": manager
        })

    return {"departments": result}
