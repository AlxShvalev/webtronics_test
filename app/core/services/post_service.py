from http import HTTPStatus
from uuid import UUID

from fastapi import Depends, HTTPException

from app.api.request_models.post_requests import PostCreateRequest, PostUpdateRequest
from app.core.db.models import Post, User
from app.core.db.repository.post_repository import PostRepository


class PostService:
    def __init__(
        self,
        post_repository: PostRepository = Depends(),
    ) -> None:
        self.__post_repository = post_repository

    async def create_post(self, post_data: PostCreateRequest, author: User) -> Post:
        post = Post(title=post_data.title, text=post_data.text, author=author)
        return await self.__post_repository.create(post)

    async def get_posts(self) -> list[Post]:
        return await self.__post_repository.get_posts_with_authors()

    async def update_post(self, post_id: UUID, post_data: PostUpdateRequest, user: User) -> Post:
        post = await self.__post_repository.get(post_id)
        if post.author_id != user.id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="У вас нет прав на редактирование этого поста."
            )
        post.title = post_data.title or post.title
        post.text = post_data.text or post.text
        return await self.__post_repository.update(post)
