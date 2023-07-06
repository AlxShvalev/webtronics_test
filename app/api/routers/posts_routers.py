from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_restful.cbv import cbv

from app.api.request_models.post_requests import PostCreateRequest, PostUpdateRequest
from app.api.response_models.post_response import PostResponse, PostWithAuthorResponse
from app.core.services.like_service import LikeService
from app.core.services.post_service import PostService
from app.core.services.user_service import UserService

router = APIRouter(prefix="/posts", tags=["Posts"])


@cbv(router)
class PostCBV:
    """Class for Post routing."""

    like_service: LikeService = Depends()
    post_service: PostService = Depends()
    user_service: UserService = Depends()

    @router.post("/", response_model=PostResponse, status_code=HTTPStatus.CREATED, summary="Create post.")
    async def create_post(
        self,
        post_data: PostCreateRequest,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    ) -> PostResponse:
        user = await self.user_service.get_user_by_token(token.credentials)
        return await self.post_service.create_post(post_data=post_data, author=user)

    @router.get("/", response_model=list[PostWithAuthorResponse], status_code=HTTPStatus.OK, summary="Get all posts.")
    async def get_posts(self) -> list[PostWithAuthorResponse]:
        return await self.post_service.get_posts()

    @router.get("/{post_id}", response_model=PostResponse, status_code=HTTPStatus.OK, summary="Get post by id.")
    async def get_post(self, post_id: UUID) -> PostResponse:
        """Get post by id."""
        return await self.post_service.get_post(post_id)

    @router.patch("/{post_id}", response_model=PostResponse, status_code=HTTPStatus.OK, summary="Update post.")
    async def update_post(
        self, post_id: UUID, post_data: PostUpdateRequest, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> PostResponse:
        user = await self.user_service.get_user_by_token(token.credentials)
        return await self.post_service.update_post(post_id, post_data, user)

    @router.delete("/{post_id}", response_model=PostResponse, status_code=HTTPStatus.OK)
    async def delete_post(
        self, post_id: UUID, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> PostResponse:
        user = await self.user_service.get_user_by_token(token.credentials)
        return await self.post_service.delete_post(post_id, user)

    @router.post("/{post_id}/like", response_model=PostResponse, status_code=HTTPStatus.OK)
    async def like_post(
        self, post_id: UUID, value: bool, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> PostResponse:
        user = await self.user_service.get_user_by_token(token.credentials)
        post = await self.post_service.get_post(post_id)
        await self.like_service.like_dislike(user_id=user.id, post=post, like_value=value)
        return post

    @router.delete("/{post_id}/like", response_model=PostResponse, status_code=HTTPStatus.OK)
    async def delete_like(
        self, post_id: UUID, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> PostResponse:
        user = await self.user_service.get_user_by_token(token.credentials)
        post = await self.post_service.get_post(post_id)
        await self.like_service.delete_like(user.id, post.id)
        return post
