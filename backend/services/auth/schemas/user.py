from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from services.auth.core.roles import UserRole

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[UserRole] = None 

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    is_active: bool
    company_id: Optional[UUID] = None

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None
