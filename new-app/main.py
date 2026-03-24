# pip install -r requirements.txt
# uvicorn main:app --reload --port 8000

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import random
import string

app = FastAPI()

# Fake meeting rooms
FAKE_ROOMS = [
    {"mtroomId": "AZcgLjraAMDj_MRS", "mtroomNm": "큐브 5층 회의실A", "buildNm": "큐브", "floor": "5", "capacity": 10},
    {"mtroomId": "AZcgLjraAMDj_MRT", "mtroomNm": "큐브 5층 회의실B", "buildNm": "큐브", "floor": "5", "capacity": 6},
    {"mtroomId": "AZcgLjraAMDj_MRU", "mtroomNm": "큐브 3층 회의실A", "buildNm": "큐브", "floor": "3", "capacity": 8},
    {"mtroomId": "AZcgLjraAMDj_MRV", "mtroomNm": "타워 2층 회의실A", "buildNm": "타워", "floor": "2", "capacity": 12},
]

# In-memory reservation store
reservations: dict = {}


def random_id(length=16):
    return "AZ" + "".join(random.choices(string.ascii_letters + string.digits, k=length))


class MtroomSchRequest(BaseModel):
    searchStartDt: str
    searchEndDt: str
    searchStartTime: Optional[str] = ""
    searchEndTime: Optional[str] = ""
    searchBuildNm: Optional[str] = ""
    searchFloor: Optional[str] = ""


class ReserveRequest(BaseModel):
    schDt: str
    startTime: str
    endTime: str
    mtroomId: str
    title: str
    contents: str
    reqId: str
    ownerId: str
    purposeCd: str
    pimsOpenCd: str
    importYn: str
    mailSendYn: str
    evalSendYn: str
    ownerNm: str
    ownerEmail: str
    pType: str
    mailContents: str


class CancelRequest(BaseModel):
    schId: str
    reqId: str


@app.post("/cis/guide/mtroom/restApi/mtroomSch.do")
def search_rooms(req: MtroomSchRequest):
    rooms = FAKE_ROOMS
    if req.searchBuildNm:
        rooms = [r for r in rooms if req.searchBuildNm in r["buildNm"]]
    if req.searchFloor:
        rooms = [r for r in rooms if r["floor"] == req.searchFloor]

    sch_list = []
    for r in rooms:
        for sch_id, sch in reservations.items():
            if sch["mtroomId"] == r["mtroomId"] and req.searchStartDt <= sch["schDt"] <= req.searchEndDt:
                sch_list.append({**sch, "schId": sch_id})

    return {
        "checkResult": True,
        "mteengroomList": rooms,
        "mteengroomSchList": sch_list,
    }


@app.post("/cis/guide/mtroom/restApi/getMtroomSchSave.do")
def reserve_room(req: ReserveRequest):
    sch_id = random_id()
    reservations[sch_id] = {
        "mtroomId": req.mtroomId,
        "schDt": req.schDt,
        "startTime": req.startTime,
        "endTime": req.endTime,
        "title": req.title,
        "contents": req.contents,
        "reqId": req.reqId,
        "ownerId": req.ownerId,
        "ownerNm": req.ownerNm,
        "ownerEmail": req.ownerEmail,
    }
    return {
        "schId": sch_id,
        "checkResult": True,
        "checkResultMsg": "회의실 예약이 되었습니다.",
    }


@app.post("/cis/guide/mtroom/restApi/mtroomSchDel.do")
def cancel_room(req: CancelRequest):
    if req.schId not in reservations:
        return {
            "checkResult": False,
            "checkResultTitle": "알림",
            "checkResultMsg": "존재하지 않는 예약번호입니다.",
        }
    del reservations[req.schId]
    return {"checkResult": True}
