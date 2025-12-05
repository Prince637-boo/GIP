import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from libs.common.base import Base

class ScanLog(Base):
    __tablename__ = "scan_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    baggage_id = Column(UUID(as_uuid=True), ForeignKey("baggages.id"), nullable=False)
    scanned_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    location = Column(String(255), nullable=False)
    device_info = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    baggage = relationship("Baggage", lazy="selectin")
