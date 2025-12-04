from fastapi import APIRouter

router_baggages = APIRouter(prefix="/baggages", tags=["Baggagges"])

@router_baggages.get("/health")
def health_check():
    return {"status": "healthy"}
