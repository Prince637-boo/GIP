from fastapi import APIRouter

router_meteo_ia = APIRouter(prefix="/meteo", tags=["Météo IA"])

@router_meteo_ia.get("/health")
def health_check():
    return {"status": "healthy"}
