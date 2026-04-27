from sqlalchemy import Column, String, DateTime, ForeignKey, Table
from sqlalchemy.sql import func
from ..database import Base
import uuid

novel_tags = Table(
    "novel_tags",
    Base.metadata,
    Column("novel_id", String(36), ForeignKey("novels.id"), primary_key=True),
    Column("tag_id", String(36), ForeignKey("tags.id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserNovel(Base):
    __tablename__ = "user_novels"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False, index=True)
    novel_id = Column(String(36), nullable=False, index=True)
    status = Column(String(50), default="reading")
    added_at = Column(DateTime(timezone=True), server_default=func.now())
