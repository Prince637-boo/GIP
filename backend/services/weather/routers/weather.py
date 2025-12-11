from fastapi import APIRouter, Query, Depends
from services.weather.services.open_meteo import OpenMeteoService
from services.weather.service_weather import WeatherService

router = APIRouter(prefix="/weather", tags=["Weather"])

# Dépendances
open_meteo_service = OpenMeteoService(api_url="https://api.open-meteo.com/v1/forecast")
weather_service = WeatherService(open_meteo=open_meteo_service)

@router.get("/", response_model=None)
async def get_weather(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180)
):
    """
    Obtenir la météo actuelle + alertes.  
    Alertes automatiques envoyées via Redis Pub/Sub si conditions critiques détectées.
    """
    return await weather_service.get_weather(lat, lon)
