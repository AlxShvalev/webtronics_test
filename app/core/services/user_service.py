import datetime as dt
from http import HTTPStatus
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.api.request_models.user_requests import LoginRequest, UserCreateRequest
from app.api.response_models.user_response import UserLoginResponse
from app.core.db.models import User
from app.core.db.repository.user_repository import UserRepository
from app.core.settings import settings

PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="user/login", scheme_name="JWT")

ALGORITHM = "HS256"


class UserService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.__user_repository = user_repository

    def _get_hashed_password(self, password: str) -> str:
        """Get password hash."""
        return PASSWORD_CONTEXT.hash(password)

    def _verify_hashed_password(self, password: str, hashed_password: str) -> bool:
        return PASSWORD_CONTEXT.verify(password, hashed_password)

    async def __authenticate_user(self, auth_data: LoginRequest) -> User:
        """Authenticate User by username and password."""
        user = await self.__user_repository.get_by_username(auth_data.username)
        password = auth_data.password.get_secret_value()
        if not self._verify_hashed_password(password, user.hashed_password):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Неверный email или пароль")
        return user

    def __create_jwt_token(self, username: str, expires_delta: int) -> str:
        """
        Create JWT token.

        Arguments:
            username (str) - unique username,
            expires_delta (int) - token lifetime.
        """
        expire = dt.datetime.utcnow() + dt.timedelta(minutes=expires_delta)
        to_encode = {"username": username, "exp": expire}
        return jwt.encode(to_encode, settings.SECRET_KEY, ALGORITHM)

    def __get_username_from_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="У вас нeт прав для просмотра данной страницы"
            )
        username = payload.get("username")
        if not username:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="У вас нeт прав для просмотра данной страницы"
            )
        return username

    async def login(self, auth_data: LoginRequest) -> UserLoginResponse:
        """Get access- and refresh- tokens."""
        user = await self.__authenticate_user(auth_data)
        return UserLoginResponse(
            access_token=self.__create_jwt_token(user.username, settings.ACCESS_TOKEN_EXPIRES_MINUTES),
            refresh_token=self.__create_jwt_token(user.username, settings.REFRESH_TOKEN_EXPIRES_MINUTES),
        )

    async def register_new_user(self, schema: UserCreateRequest) -> User:
        """User register."""
        user = User(
            username=schema.username,
            email=schema.email,
            name=schema.name,
            surname=schema.surname,
            hashed_password=self._get_hashed_password(schema.password.get_secret_value()),
        )
        return await self.__user_repository.create(user)

    async def get_user_by_id(self, id: UUID) -> User:
        """Get user."""
        return await self.__user_repository.get(id)

    async def get_user_by_username(self, username: str) -> User:
        """Get User by username."""
        user = await self.__user_repository.get_by_username(username)
        return user

    async def get_user_by_token(self, token: str) -> User:
        """Get User by jwt token."""
        username = self.__get_username_from_token(token)
        return await self.get_user_by_username(username)
