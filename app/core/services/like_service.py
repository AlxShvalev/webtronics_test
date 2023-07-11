from typing import Optional
from uuid import UUID

from fastapi import Depends

from app.core import exceptions
from app.core.db.models import Like, Post
from app.core.db.repository.likes_repository import LikeRepository


class LikeService:
    def __init__(self, like_repository: LikeRepository = Depends()) -> None:
        self.__like_repository = like_repository

    async def _get_like(self, user_id: UUID, post_id: UUID) -> Optional[Like]:
        return await self.__like_repository.get_by_user_and_post_ids(user_id, post_id)

    async def like_dislike(self, user_id: UUID, post: Post, like_value: bool) -> Like:
        """Get Like form db.

        If Like exists, check it for vlue and change if different.
        If Like has the same value raise exception. Then save Like.
        """
        if user_id == post.author_id:
            raise exceptions.LikesToSelfPostsError
        like = await self._get_like(user_id, post.id)
        if like is None:
            like = Like(user_id=user_id, post_id=post.id)
        if like.value == like_value:
            like_str = "лайк" if like_value is True else "дизлайк"
            raise exceptions.LikeAlreadyExistsError(like_str)
        like.value = like_value
        return await self.__like_repository.save_like(like)

    async def delete_like(self, user_id: UUID, post_id: UUID) -> Like:
        """Delete like if exists, else raise exception."""
        like = await self._get_like(user_id, post_id)
        if like is None:
            raise exceptions.LikeNotExistsError
        return await self.__like_repository.delete(like)
