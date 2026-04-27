from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from ..database import get_db
from ..auth.dependencies import get_current_user
from ..auth.models import User
from ..crawler.models import Novel, Chapter
from .models import ReadingProgress, Bookmark, ReadingHistory
from .schemas import (
    ReadingProgressUpdate, ReadingProgressResponse,
    BookmarkCreate, BookmarkResponse,
    ChapterResponse, NovelChaptersResponse
)

router = APIRouter(prefix="/reading", tags=["Reading"])


@router.get("/novels/{novel_id}/chapters", response_model=NovelChaptersResponse)
async def get_novel_chapters(novel_id: str, db: AsyncSession = Depends(get_db)):
    novel = (await db.execute(select(Novel).where(Novel.id == novel_id))).scalar_one_or_none()
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found")

    chapters = (await db.execute(
        select(Chapter).where(Chapter.novel_id == novel_id).order_by(Chapter.chapter_number)
    )).scalars().all()

    return NovelChaptersResponse(
        id=novel.id,
        title=novel.title,
        author=novel.author,
        chapters=[ChapterResponse.model_validate(ch) for ch in chapters],
    )


@router.get("/progress/{novel_id}", response_model=ReadingProgressResponse)
async def get_reading_progress(
    novel_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    progress = (await db.execute(
        select(ReadingProgress).where(
            ReadingProgress.user_id == current_user.id,
            ReadingProgress.novel_id == novel_id
        )
    )).scalar_one_or_none()
    if not progress:
        raise HTTPException(status_code=404, detail="No reading progress found")
    return progress


@router.post("/progress", response_model=ReadingProgressResponse)
async def save_reading_progress(
    data: ReadingProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    progress = (await db.execute(
        select(ReadingProgress).where(
            ReadingProgress.user_id == current_user.id,
            ReadingProgress.novel_id == data.novel_id
        )
    )).scalar_one_or_none()

    if progress:
        progress.chapter_id = data.chapter_id
        progress.scroll_position = data.scroll_position
    else:
        progress = ReadingProgress(
            user_id=current_user.id,
            novel_id=data.novel_id,
            chapter_id=data.chapter_id,
            scroll_position=data.scroll_position,
        )
        db.add(progress)

    await db.flush()
    await db.refresh(progress)
    return progress


@router.get("/bookmarks", response_model=list[BookmarkResponse])
async def list_bookmarks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Bookmark).where(Bookmark.user_id == current_user.id).order_by(Bookmark.created_at.desc())
    )
    return result.scalars().all()


@router.post("/bookmarks", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED)
async def create_bookmark(
    data: BookmarkCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    bookmark = Bookmark(
        user_id=current_user.id,
        novel_id=data.novel_id,
        chapter_id=data.chapter_id,
        note=data.note,
    )
    db.add(bookmark)
    await db.flush()
    await db.refresh(bookmark)
    return bookmark


@router.delete("/bookmarks/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bookmark(
    bookmark_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    bookmark = (await db.execute(
        select(Bookmark).where(Bookmark.id == bookmark_id, Bookmark.user_id == current_user.id)
    )).scalar_one_or_none()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    await db.delete(bookmark)
    await db.flush()


@router.get("/history", response_model=list[dict])
async def get_reading_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ReadingHistory).where(ReadingHistory.user_id == current_user.id)
        .order_by(ReadingHistory.read_at.desc()).limit(50)
    )
    return result.scalars().all()
