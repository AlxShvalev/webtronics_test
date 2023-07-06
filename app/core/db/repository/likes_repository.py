from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models import Like
from app.core.db.repository.abstract_repository import AbstractRepository


class LikeRepository(AbstractRepository):
    """Repository for Like model."""

    def __init__(self, session: AsyncSession = Depends()) -> None:
        super().__init__(session, Like)

    async def get_by_user_and_post_ids(self, user_id: UUID, post_id: UUID) -> Like:
        stmt = select(Like).where(Like.user_id == user_id, Like.post_id == post_id)
        like = await self._session.execute(stmt)
        return like.scalars().first()

    async def save_like(self, like: Like) -> Like:
        self._session.add(like)
        await self._session.commit()
        await self._session.refresh(like)
        return like
