from pydantic import BaseModel, EmailStr
from typing import Optional

class CompanyCreate(BaseModel):
    name: str
    legal_id: Optional[str] = None
    contact_email: Optional[EmailStr] = None

class CompanyOut(BaseModel):
    id: str
    name: str
    legal_id: Optional[str]
    contact_email: Optional[EmailStr]

    class Config:
        from_attributes = True
