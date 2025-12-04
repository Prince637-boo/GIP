from fastapi import APIRouter

router_auth = APIRouter(prefix="/auth", tags=["Authentication"])

@router_auth.get("/health")
def health_check():
    return {"status": "healthy"}
