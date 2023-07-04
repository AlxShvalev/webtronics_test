from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_restful.cbv import cbv

from app.api.request_models.post_requests import PostCreateRequest, PostUpdateRequest
from app.api.response_models.post_response import PostResponse, PostWithAuthorResponse
from app.core.services.post_service import PostService
from app.core.services.user_service import UserService

router = APIRouter(prefix="/posts", tags=["Posts"])


@cbv(router)
class PostCBV:
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

    @router.patch("/{post_id}", response_model=PostResponse, status_code=HTTPStatus.OK, summary="Update post.")
    async def update_post(
        self, post_id: UUID, post_data: PostUpdateRequest, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> PostResponse:
        user = await self.user_service.get_user_by_token(token.credentials)
        return await self.post_service.update_post(post_id, post_data, user)
