from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.response_models.post_response import PostWithAuthorResponse
from app.core.db.db import get_async_session
from app.core.db.models import Post
from app.core.db.repository.abstract_repository import AbstractRepository


class PostRepository(AbstractRepository):
    """Repository for Post model."""

    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        super().__init__(session, Post)

    async def get_posts_with_authors(self) -> list[PostWithAuthorResponse]:
        stmt = select(Post).options(selectinload(Post.author))
        posts = await self._session.execute(stmt)
        return posts.scalars().all()
