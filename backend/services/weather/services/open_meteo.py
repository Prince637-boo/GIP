import httpx
import logging
from pydantic import ValidationError
from services.weather.schemas.weather import WeatherData

logger = logging.getLogger(__name__)

class OpenMeteoService:
    def __init__(self, api_url: str):
        self.api_url = api_url
    
    async def fetch_weather(self, lat: float, lon: float):
        params = {"latitude": lat, "longitude": lon, "current_weather": "true"}
        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(self.api_url, params=params)
                r.raise_for_status()
                data = r.json()
                return WeatherData(
                    temperature=data["current_weather"]["temperature"],
                    wind_speed=data["current_weather"]["windspeed"],
                    condition=data["current_weather"].get("weathercode", "clear")
                )
            except (httpx.HTTPError, ValidationError) as e:
                logger.error(f"Erreur météo: {e}")
                return WeatherData(temperature=20.0, wind_speed=0.0, condition="unknown")
