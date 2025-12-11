import json
from datetime import datetime, timedelta
from services.weather.redis_client import redis_client
from services.weather.services.open_meteo import OpenMeteoService
from services.weather.schemas.weather import WeatherResponse

CACHE_TTL = 300  # 5 minutes

class WeatherService:
    def __init__(self, open_meteo: OpenMeteoService):
        self.open_meteo = open_meteo
    
    async def get_weather(self, lat: float, lon: float):
        key = f"weather:{lat}:{lon}"
        cached = await redis_client.get(key)
        if cached:
            return WeatherResponse.parse_raw(cached)

        current_weather = await self.open_meteo.fetch_weather(lat, lon)

        # Analyse simple des prévisions ou tendances
        alert = None
        if current_weather.wind_speed > 20:
            alert = "Vents forts prévus, retards possibles"
        elif current_weather.temperature < 0:
            alert = "Températures négatives, conditions hivernales"

        response = WeatherResponse(
            latitude=lat,
            longitude=lon,
            current=current_weather,
            alert=alert
        )

        await redis_client.set(key, response.json(), ex=CACHE_TTL)

        # Notification automatique via Redis Pub/Sub
        if alert:
            await redis_client.publish("weather.alerts", json.dumps({
                "lat": lat,
                "lon": lon,
                "alert": alert,
                "timestamp": datetime.utcnow().isoformat()
            }))

        return response
