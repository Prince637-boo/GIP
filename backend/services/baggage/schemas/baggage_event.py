from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import Optional
from ..core.enums import BaggageStatus

class BaggageEventCreate(BaseModel):
    status: BaggageStatus
    location: str

class BaggageEventOut(BaseModel):
    id: UUID
    status: BaggageStatus
    location: str
    timestamp: str

    
    model_config = ConfigDict(from_attributes=True)
