# services/auth/models/user.py
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from libs.common.base import Base
from services.auth.core.roles import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    role = Column(Enum(UserRole), default=UserRole.PASSAGER, nullable=False)

    # Optionnel : si l'utilisateur est associé à une compagnie
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True)
    company = relationship("Company", back_populates="users", lazy="selectin")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
