# services/auth/models/company.py
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from libs.common.base import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False, index=True)
    legal_id = Column(String(128), nullable=True)  
    contact_email = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # relation inverse : une compagnie peut avoir plusieurs users (operators, passagers créés par la compagnie)
    users = relationship("User", back_populates="company", lazy="selectin")
