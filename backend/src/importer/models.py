from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.sql import func
from ..database import Base
import uuid


class ImportJob(Base):
    __tablename__ = "import_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String(500), nullable=False)
    status = Column(String(50), default="pending")
    novel_id = Column(String(36))
    chapters_imported = Column(Integer, default=0)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
