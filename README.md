# GoReservation

Docker + Compose 기반 FastAPI 백엔드 서비스. 사내 직원 정보 및 일정 관리를 위한 Mock API 서버입니다.

## 기술 스택

- **Python 3.11**
- **FastAPI**
- **Uvicorn**
- **Docker / Docker Compose**
- JSON 파일 기반 Mock DB (`data/users.json`, `data/calendar.json`)

## 프로젝트 구조

```
GoReservation/
├── app/
│   ├── main.py               # FastAPI 앱 진입점
│   └── routers/
│       ├── employee.py       # 직원 / 조직도 API
│       ├── calendar.py       # 일정 API
│       └── mock.py           # Mock 데이터 생성 API
├── data/
│   ├── users.json            # 직원 / 부서 데이터 (자동 생성)
│   └── calendar.json         # 일정 데이터 (자동 생성)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 실행 방법

### Docker Compose (권장)

```bash
docker compose up --build
```

서버가 `http://localhost:8000` 에서 실행됩니다.

### 로컬 실행

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API 목록

### Mock 데이터 생성

| Method | Path | 설명 |
|--------|------|------|
| GET | `/mock/refresh` | 직원 및 일정 Mock 데이터 전체 재생성 |

> **주의:** 다른 API를 사용하기 전에 반드시 `/mock/refresh`를 먼저 호출해야 합니다.

---

### 직원 (Employees)

| Method | Path | 설명 |
|--------|------|------|
| GET | `/employees/search?q={검색어}` | 이름 / 이메일 / 부서명으로 직원 검색 |
| GET | `/employees/{employee_id}` | 직원 상세 정보 조회 |
| GET | `/departments/{department_id}/members` | 부서 멤버 조회 (`include_sub=true`로 하위 부서 포함) |
| GET | `/organization` | 전체 조직도 조회 |

#### 직원 검색 파라미터

| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|--------|------|
| `q` | string | 필수 | 검색 키워드 |
| `limit` | int | 20 | 최대 반환 수 |
| `offset` | int | 0 | 페이징 오프셋 |

---

### 일정 (Calendar)

| Method | Path | 설명 |
|--------|------|------|
| GET | `/calendars/{user_id}/events` | 특정 사용자의 일정 조회 |
| POST | `/calendars/freebusy` | 여러 사용자의 Free/Busy 조회 |
| POST | `/calendars/events` | 일정 생성 |
| PUT | `/calendars/events/{event_id}` | 일정 수정 |
| DELETE | `/calendars/events/{event_id}` | 일정 삭제 |

#### 사용자 일정 조회 파라미터

| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|--------|------|
| `start_date` | string | 필수 | 조회 시작일 (YYYY-MM-DD) |
| `end_date` | string | 필수 | 조회 종료일 (YYYY-MM-DD) |
| `include_private` | bool | false | 비공개 일정 포함 여부 |

## API 문서

서버 실행 후 아래 주소에서 Swagger UI를 확인할 수 있습니다.

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 조직 구조 (Mock 데이터)

```
회사
└── 기술본부
    ├── 개발팀
    └── 디자인팀
└── 인사팀
```

직원 수는 매 갱신 시 30~80명, 일정은 50~150개가 랜덤 생성됩니다.
