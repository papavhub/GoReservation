from fastapi import APIRouter

router = APIRouter(
    prefix="/calendar",
    tags=["Health Check"]
)

@router.get("/")
def health_check():
    return {"status": "ok"}


@router.get("/refresh")
def health_check():
    
    
    
    
    return {"status": "ok"}