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
        """Create new Post."""
        post = Post(title=post_data.title, text=post_data.text, author=author)
        return await self.__post_repository.create(post)

    async def get_posts(self) -> list[Post]:
        """Get Posts with authors."""
        return await self.__post_repository.get_posts_with_authors()

    async def get_post_simple(self, post_id: UUID) -> Post:
        """Get post by id."""
        return await self.__post_repository.get_post_author(post_id)

    async def get_post_extended(self, post_id: UUID) -> Post:
        """Get post by id with extra fields."""
        post = await self.__post_repository.get_post_extended(post_id)
        if post is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Пост не найден.")
        return post

    async def update_post(self, post_id: UUID, post_data: PostUpdateRequest, user: User) -> Post:
        """Update Post."""
        post = await self.__post_repository.get(post_id)
        if post.author_id != user.id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="У вас нет прав на редактирование этого поста."
            )
        post.title = post_data.title or post.title
        post.text = post_data.text or post.text
        return await self.__post_repository.update(post)

    async def delete_post(self, post_id: UUID, user: User) -> Post:
        """Delete Post."""
        post = await self.__post_repository.get(post_id)
        if post.author_id != user.id:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="У вас нет прав на удаление этого поста.")
        return await self.__post_repository.delete(post)
