from fastapi import APIRouter

router = APIRouter()
@router.get("/health")
def fnc():
    return {
        "status": "ok",
        "service": "inventory"
    }