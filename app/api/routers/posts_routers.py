from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_restful.cbv import cbv

from app.api.request_models.post_requests import PostCreateRequest
from app.api.response_models.post_response import PostResponse
from app.core.services.post_service import PostService
from app.core.services.user_service import UserService

router = APIRouter(prefix="/posts", tags=["Posts"])


@cbv(router)
class PostCBV:
    post_service: PostService = Depends()
    user_service: UserService = Depends()

    @router.post("/")
    async def create_post(
        self,
        post_data: PostCreateRequest,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    ) -> PostResponse:
        user = await self.user_service.get_user_by_token(token.credentials)
        return await self.post_service.create_post(post_data=post_data, author=user)
