from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from ..database import get_db
from .models import Source, Novel, CrawlJob
from .schemas import SourceCreate, SourceResponse, CrawlJobResponse, NovelResponse
from .engine.factory import get_crawler

router = APIRouter(prefix="/sources", tags=["Crawler Management"])


@router.get("", response_model=list[SourceResponse])
async def list_sources(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Source))
    return result.scalars().all()


@router.post("", response_model=SourceResponse, status_code=status.HTTP_201_CREATED)
async def create_source(source_data: SourceCreate, db: AsyncSession = Depends(get_db)):
    source = Source(**source_data.model_dump())
    db.add(source)
    await db.flush()
    await db.refresh(source)
    return source


@router.get("/{source_id}", response_model=SourceResponse)
async def get_source(source_id: str, db: AsyncSession = Depends(get_db)):
    source = (await db.execute(select(Source).where(Source.id == source_id))).scalar_one_or_none()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.put("/{source_id}", response_model=SourceResponse)
async def update_source(source_id: str, source_data: SourceCreate, db: AsyncSession = Depends(get_db)):
    source = (await db.execute(select(Source).where(Source.id == source_id))).scalar_one_or_none()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    for key, value in source_data.model_dump().items():
        setattr(source, key, value)
    await db.flush()
    await db.refresh(source)
    return source


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_source(source_id: str, db: AsyncSession = Depends(get_db)):
    source = (await db.execute(select(Source).where(Source.id == source_id))).scalar_one_or_none()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    await db.delete(source)
    await db.flush()


@router.post("/{source_id}/crawl", response_model=CrawlJobResponse)
async def trigger_crawl(source_id: str, db: AsyncSession = Depends(get_db)):
    source = (await db.execute(select(Source).where(Source.id == source_id))).scalar_one_or_none()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    if not source.enabled:
        raise HTTPException(status_code=400, detail="Source is disabled")

    crawler = get_crawler(source, db)
    if not crawler:
        raise HTTPException(status_code=400, detail="No crawler configured for this source")

    job = CrawlJob(source_id=source_id, status="running", started_at=datetime.utcnow())
    db.add(job)
    await db.flush()

    try:
        novels = (await db.execute(select(Novel).where(Novel.source_id == source_id))).scalars().all()
        total_crawled = 0
        for novel in novels:
            crawled = await crawler.crawl_chapters(novel)
            total_crawled += crawled

        source.last_crawled_at = datetime.utcnow()
        job.status = "completed"
        job.completed_at = datetime.utcnow()
        job.chapters_crawled = total_crawled
        await db.commit()
    except Exception as e:
        await db.rollback()
        job.status = "failed"
        job.error_message = str(e)[:2000]
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Crawl failed: {str(e)}")

    return job


@router.get("/{source_id}/jobs", response_model=list[CrawlJobResponse])
async def list_jobs(source_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CrawlJob).where(CrawlJob.source_id == source_id).order_by(CrawlJob.started_at.desc())
    )
    return result.scalars().all()


@router.get("/{source_id}/novels", response_model=list[NovelResponse])
async def list_novels(source_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Novel).where(Novel.source_id == source_id))
    return result.scalars().all()
