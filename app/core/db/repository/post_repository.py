from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.db.db import get_async_session
from app.core.db.models import Post
from app.core.db.repository.abstract_repository import AbstractRepository


class PostRepository(AbstractRepository):
    """Repository for Post model."""

    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        super().__init__(session, Post)

    async def get_posts_with_authors(self) -> list[Post]:
        stmt = select(Post).options(selectinload(Post.author))
        posts = await self._session.execute(stmt)
        return posts.scalars().all()

    async def get_post(self, id: UUID) -> Post:
        stmt = (
            select(
                Post.id,
                Post.title,
                Post.text,
                Post.author_id,
                Post.created_at,
                Post.updated_at,
                # func.count(Post.likes).label("likes")
            )
            .where(Post.id == id)
            .outerjoin(Post.likes)
            .group_by(Post.id)
        )
        post = await self._session.execute(stmt)
        return post.first()
