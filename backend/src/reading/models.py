from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from ..database import Base
import uuid


class ReadingProgress(Base):
    __tablename__ = "reading_progress"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False, index=True)
    novel_id = Column(String(36), nullable=False, index=True)
    chapter_id = Column(String(36), nullable=False)
    scroll_position = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False, index=True)
    novel_id = Column(String(36), nullable=False, index=True)
    chapter_id = Column(String(36), nullable=False)
    note = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ReadingHistory(Base):
    __tablename__ = "reading_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False, index=True)
    novel_id = Column(String(36), nullable=False, index=True)
    chapter_id = Column(String(36), nullable=False)
    read_at = Column(DateTime(timezone=True), server_default=func.now())
