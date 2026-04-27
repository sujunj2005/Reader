from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ImportJobResponse(BaseModel):
    id: str
    filename: str
    status: str
    novel_id: Optional[str] = None
    chapters_imported: int = 0
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
