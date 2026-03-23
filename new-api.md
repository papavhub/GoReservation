## 1. 회의실 조회 API

회의실 예약 현황 및 회의실 정보를 조회하는 API입니다.

### Endpoint

```
POST /cis/guide/mtroom/restApi/mtroomSch.do
```

### Request Parameters

| 파라미터 | 필수 | 설명 | 포맷 |
|---------|------|------|------|
| searchStartDt | 필수 | 시작일 | yyyymmdd |
| searchEndDt | 필수 | 종료일 | yyyymmdd |
| searchStartTime | 선택 | 시작시간 | hh24mi |
| searchEndTime | 선택 | 종료시간 | hh24mi |
| searchBuildNm | 선택 | 건물명 | - |
| searchFloor | 선택 | 층 | - |

### Request Example

```json
{
    "searchStartDt": "20260303",
    "searchEndDt": "20260303",
    "searchBuildNm": "큐브",
    "searchFloor": "5",
    "searchStartTime": "",
    "searchEndTime": ""
}
```

### Response

```json
{
    "checkResult": true,
    "mteengroomList": [...],
    "mteengroomSchList": [...]
}
```

---

## 2. 회의실 예약 API

회의실을 예약하는 API입니다.

### Endpoint

```
POST /cis/guide/mtroom/restApi/getMtroomSchSave.do
```

### Request Parameters

| 파라미터 | 필수 | 설명 | 비고 |
|---------|------|------|------|
| schDt | 필수 | 회의일자 | yyyymmdd |
| startTime | 필수 | 회의 시작시간 | hh24mi |
| endTime | 필수 | 회의 종료시간 | hh24mi |
| mtroomId | 필수 | 회의실 ID | - |
| title | 필수 | 회의 제목 | - |
| contents | 필수 | 회의 내용 | - |
| reqId | 필수 | 신청자 ID | - |
| ownerId | 필수 | 주관자 ID | - |
| purposeCd | 필수 | 회의목적 | REPORT (고정) |
| pimsOpenCd | 필수 | PIMS 공개범위 | C (고정) |
| importYn | 필수 | 중요회의 여부 | N (고정) |
| mailSendYn | 필수 | 이메일 발송여부 | Y (고정) |
| evalSendYn | 필수 | 평가 발송여부 | N (고정) |
| ownerNm | 필수 | 주관자 이름 | - |
| ownerEmail | 필수 | 주관자 이메일 주소 | - |
| pType | 필수 | 참석자 종류 | 0 (고정) |
| mailContents | 필수 | 참석자 이메일 내용 | - |

### Request Example

```json
{
    "schDt": "20260312",
    "startTime": "1500",
    "endTime": "1600",
    "mtroomId": "AZcgLjraAMDj_MRS",
    "title": "API_TEST",
    "contents": "test",
    "reqId": "M220211140332C108882",
    "ownerId": "M220211140332C108882",
    "purposeCd": "REPORT",
    "pimsOpenCd": "C",
    "importYn": "N",
    "mailSendYn": "Y",
    "evalSendYn": "N",
    "ownerNm": "황한동",
    "ownerEmail": "hoasis.hwang@samsung.com",
    "pType": "0",
    "mailContents": "good"
}
```

### Response

```json
{
    "schId": "AZzfq9FaAU_j_MQe",
    "checkResult": true,
    "checkResultMsg": "회의실 예약이 되었습니다."
}
```

---

## 3. 회의실 예약 취소 API

회의실 예약을 취소하는 API입니다.

### Endpoint

```
POST /cis/guide/mtroom/restApi/mtroomSchDel.do
```

### Request Parameters

| 파라미터 | 필수 | 설명 | 비고 |
|---------|------|------|------|
| schId | 필수 | 회의실 예약번호 | 예약 시 반환된 값 |
| reqId | 필수 | 신청자 ID | - |

### Request Example

```json
{
    "schId": "AZzfnTQ6AT7j_MQe",
    "reqId": "M220211140332C108882"
}
```

### Response Examples

**성공 (취소 완료):**

```json
{
    "checkResult": true
}
```

**실패 (시간 경과로 취소 불가):**

```json
{
    "checkResult": false,
    "checkResultTitle": "알림",
    "checkResultMsg": "회의예약시간이 지나서 취소가 불가능 합니다.<br/> 예약일 : 2026-03-12<br/>예약시간 : 09:00 ~ 10:00"
}
```