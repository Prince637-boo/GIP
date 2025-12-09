from pydantic import BaseModel, ConfigDict
from typing import Optional, Union
from datetime import datetime


class WeatherBase(BaseModel):
    location_name: str
    latitude: float
    longitude: float
    temperature: float
    wind_speed: float


class WeatherCreate(WeatherBase):
    """
    Schéma utilisé pour créer un enregistrement météo
    """
    pass


class Weather(WeatherBase):
    """
    Schéma utilisé pour retourner des données depuis l'API
    """
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
