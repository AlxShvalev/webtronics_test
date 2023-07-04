from fastapi import FastAPI

from app.api.routers import post_router, user_router
from app.core.settings import settings


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(title=settings.TITLE, debug=settings.DEBUG, root_path=settings.ROOT_PATH)
    app.include_router(post_router)
    app.include_router(user_router)

    return app
