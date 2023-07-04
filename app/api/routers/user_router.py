from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from app.api.request_models.user_requests import LoginRequest, UserCreateRequest
from app.api.response_models.user_response import UserLoginResponse, UserResponse
from app.core.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Пользователи"])


@cbv(router)
class UserCBV:
    """Base class for User routing."""

    user_service: UserService = Depends()

    @router.post(
        "/",
        response_model=UserResponse,
        response_model_exclude_none=True,
        status_code=HTTPStatus.CREATED,
        summary="Регистрация нового пользователя.",
        response_description="Регистрация нового пользователя.",
    )
    async def create_user(self, schema: UserCreateRequest) -> UserResponse:
        """Register new User."""
        return await self.user_service.register_new_user(schema)

    @router.get(
        "/{user_id}",
        response_model=UserResponse,
        response_model_exclude_none=True,
        status_code=HTTPStatus.OK,
        summary="Получить пользователя",
        response_description="Получить пользователя по его id.",
    )
    async def get_user(self, user_id: UUID) -> UserResponse:
        """Get user by id."""
        return await self.user_service.get_user_by_id(user_id)

    @router.post("/login", response_model=UserLoginResponse, status_code=HTTPStatus.OK)
    async def login(self, auth_data: LoginRequest) -> UserLoginResponse:
        """User authenticate by username and password."""
        return await self.user_service.login(auth_data)
