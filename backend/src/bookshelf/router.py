from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from ..database import get_db
from ..auth.dependencies import get_current_user
from ..auth.models import User
from ..crawler.models import Novel
from .models import Tag, UserNovel, novel_tags
from .schemas import (
    TagResponse, NovelSearchResult,
    UserNovelCreate, UserNovelUpdate, UserNovelResponse
)

router = APIRouter(tags=["Bookshelf"])


@router.get("/novels/search", response_model=list[NovelSearchResult])
async def search_novels(
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db)
):
    search_pattern = f"%{q}%"
    result = await db.execute(
        select(Novel).where(
            or_(
                Novel.title.ilike(search_pattern),
                Novel.author.ilike(search_pattern),
            )
        ).limit(50)
    )
    novels = result.scalars().all()
    return [NovelSearchResult.model_validate(n) for n in novels]


@router.get("/novels/tags/{tag_name}", response_model=list[NovelSearchResult])
async def get_novels_by_tag(
    tag_name: str,
    db: AsyncSession = Depends(get_db)
):
    tag = (await db.execute(select(Tag).where(Tag.name == tag_name))).scalar_one_or_none()
    if not tag:
        return []

    result = await db.execute(
        select(Novel).join(novel_tags).where(novel_tags.c.tag_id == tag.id)
    )
    novels = result.scalars().all()
    return [NovelSearchResult.model_validate(n) for n in novels]


@router.get("/bookshelf", response_model=list[dict])
async def get_bookshelf(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    from sqlalchemy.orm import selectinload
    result = await db.execute(
        select(UserNovel).where(UserNovel.user_id == current_user.id)
    )
    user_novels = result.scalars().all()

    response = []
    for un in user_novels:
        novel = (await db.execute(select(Novel).where(Novel.id == un.novel_id))).scalar_one_or_none()
        if novel:
            response.append({
                "user_novel_id": un.id,
                "novel_id": novel.id,
                "title": novel.title,
                "author": novel.author,
                "cover_image": novel.cover_image,
                "status": un.status,
                "added_at": un.added_at,
            })
    return response


@router.post("/bookshelf", response_model=UserNovelResponse, status_code=status.HTTP_201_CREATED)
async def add_to_bookshelf(
    data: UserNovelCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    existing = (await db.execute(
        select(UserNovel).where(UserNovel.user_id == current_user.id, UserNovel.novel_id == data.novel_id)
    )).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Novel already in bookshelf")

    novel = (await db.execute(select(Novel).where(Novel.id == data.novel_id))).scalar_one_or_none()
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found")

    user_novel = UserNovel(user_id=current_user.id, novel_id=data.novel_id, status=data.status)
    db.add(user_novel)
    await db.flush()
    await db.refresh(user_novel)
    return user_novel


@router.put("/bookshelf/{user_novel_id}", response_model=UserNovelResponse)
async def update_bookshelf_status(
    user_novel_id: str,
    data: UserNovelUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_novel = (await db.execute(
        select(UserNovel).where(UserNovel.id == user_novel_id, UserNovel.user_id == current_user.id)
    )).scalar_one_or_none()
    if not user_novel:
        raise HTTPException(status_code=404, detail="Bookshelf entry not found")

    user_novel.status = data.status
    await db.flush()
    await db.refresh(user_novel)
    return user_novel


@router.delete("/bookshelf/{user_novel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_bookshelf(
    user_novel_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_novel = (await db.execute(
        select(UserNovel).where(UserNovel.id == user_novel_id, UserNovel.user_id == current_user.id)
    )).scalar_one_or_none()
    if not user_novel:
        raise HTTPException(status_code=404, detail="Bookshelf entry not found")
    await db.delete(user_novel)
    await db.flush()


@router.get("/tags", response_model=list[TagResponse])
async def list_tags(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).order_by(Tag.name))
    return result.scalars().all()
