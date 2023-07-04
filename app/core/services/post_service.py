from fastapi import Depends

from app.api.request_models.post_requests import PostCreateRequest
from app.api.response_models.post_response import PostResponse
from app.core.db.models import Post, User
from app.core.db.repository.post_repository import PostRepository


class PostService:
    def __init__(
        self,
        post_repository: PostRepository = Depends(),
    ) -> None:
        self.__post_repository = post_repository

    async def create_post(self, post_data: PostCreateRequest, author: User) -> PostResponse:
        post = Post(title=post_data.title, text=post_data.text, author=author)
        return await self.__post_repository.create(post)
