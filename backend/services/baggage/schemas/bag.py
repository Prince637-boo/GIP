from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import Optional
from ..core.enums import BaggageStatus

class BaggageCreate(BaseModel):
    owner_id: UUID
    company_id: UUID
    description: Optional[str] = None
    weight: Optional[str] = None

class BaggageOut(BaseModel):
    id: UUID
    tag: str
    qr_code_path: str | None
    description: Optional[str]
    weight: Optional[str]
    status: BaggageStatus

    model_config = ConfigDict(from_attributes=True)

