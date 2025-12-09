from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from libs.common.base import Base

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String, nullable=False)

    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)

    temperature = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
