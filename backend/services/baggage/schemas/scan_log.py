from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class ScanLogCreate(BaseModel):
    location: str
    device_info: str | None = None

class ScanLogOut(BaseModel):
    id: UUID
    location: str
    device_info: str | None
    timestamp: datetime

    
    model_config = ConfigDict(from_attributes=True)
