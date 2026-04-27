from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import os
from ..database import get_db
from ..crawler.models import Novel, Chapter
from .models import ImportJob
from .schemas import ImportJobResponse
from .txt_importer import TxtImporter
from .epub_importer import EpubImporter

router = APIRouter(prefix="/import", tags=["File Import"])


def get_importer(filename: str):
    ext = os.path.splitext(filename)[1].lower()
    if ext == '.txt':
        return TxtImporter()
    elif ext == '.epub':
        return EpubImporter()
    raise HTTPException(status_code=400, detail=f"Unsupported file format: {ext}")


@router.post("", response_model=ImportJobResponse, status_code=status.HTTP_201_CREATED)
async def import_file(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ['.txt', '.epub']:
        raise HTTPException(status_code=400, detail="Unsupported format. Use .txt or .epub")

    job = ImportJob(filename=file.filename, status="running", created_at=datetime.utcnow())
    db.add(job)
    await db.flush()

    try:
        content = await file.read()
        importer = get_importer(file.filename)

        metadata = await importer.parse_metadata(content, file.filename)
        chapters = await importer.parse_chapters(content)

        novel = Novel(
            title=metadata['title'],
            author=metadata.get('author'),
            source_url=f"file://{file.filename}",
            status="ongoing",
        )
        db.add(novel)
        await db.flush()

        for ch_data in chapters:
            chapter = Chapter(
                novel_id=novel.id,
                chapter_number=ch_data['chapter_number'],
                title=ch_data['title'],
                url="",
                content=ch_data['content'],
                status="crawled",
            )
            db.add(chapter)

        job.novel_id = novel.id
        job.status = "completed"
        job.chapters_imported = len(chapters)
        await db.commit()

    except Exception as e:
        await db.rollback()
        job.status = "failed"
        job.error_message = str(e)[:2000]
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")

    return job


@router.get("/jobs", response_model=list[ImportJobResponse])
async def list_import_jobs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ImportJob).order_by(ImportJob.created_at.desc()))
    return result.scalars().all()
