from fastapi import FastAPI
from app.routers import calendar, employee, mock

app = FastAPI(
    title="My FastAPI Service",
    description="Docker + Compose 기반 FastAPI 기본 템플릿",
    version="1.0.0"
)

app.include_router(calendar.router)
app.include_router(employee.router)
app.include_router(mock.router)

@app.get("/")
def root():
    return {"message": "FastAPI is running"}
