from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import uuid


class Source(Base):
    __tablename__ = "sources"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    base_url = Column(String(500), nullable=False)
    config = Column(JSON, default={})
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_crawled_at = Column(DateTime(timezone=True))

    novels = relationship("Novel", back_populates="source")
    crawl_jobs = relationship("CrawlJob", back_populates="source")


class Novel(Base):
    __tablename__ = "novels"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String(36), ForeignKey("sources.id"), nullable=False)
    title = Column(String(500), nullable=False, index=True)
    author = Column(String(255), index=True)
    description = Column(Text)
    source_url = Column(String(500), unique=True, nullable=False)
    cover_image = Column(String(500))
    status = Column(String(50), default="ongoing")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    source = relationship("Source", back_populates="novels")
    chapters = relationship("Chapter", back_populates="novel", cascade="all, delete-orphan")


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    novel_id = Column(String(36), ForeignKey("novels.id"), nullable=False)
    chapter_number = Column(Integer, nullable=False)
    title = Column(String(500), nullable=False)
    url = Column(String(500), unique=True, nullable=False)
    content = Column(Text)
    crawled_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default="pending")

    novel = relationship("Novel", back_populates="chapters")


class CrawlJob(Base):
    __tablename__ = "crawl_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String(36), ForeignKey("sources.id"), nullable=False)
    status = Column(String(50), default="pending")
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    chapters_crawled = Column(Integer, default=0)
    chapters_total = Column(Integer, default=0)
    error_message = Column(Text)

    source = relationship("Source", back_populates="crawl_jobs")
