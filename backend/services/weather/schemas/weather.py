from pydantic import BaseModel
from typing import List, Optional

class WeatherData(BaseModel):
    temperature: float
    wind_speed: float
    condition: str

class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    current: WeatherData
    forecast: Optional[List[WeatherData]] = None
    alert: Optional[str] = None
