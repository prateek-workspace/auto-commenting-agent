from fastapi import FastAPI

from app.core.config import settings
from app.core.database import init_db
from app.core.logging import setup_logging

from app.posts.router import router as posts_router
from app.generation.router import router as generation_router
from app.review.router import router as review_router
from app.posting.router import router as posting_router
from app.feedback.router import router as feedback_router


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
    )
    app.include_router(posts_router)
    app.include_router(generation_router)
    app.include_router(review_router, prefix="/review")
    app.include_router(posting_router)
    app.include_router(feedback_router)

    @app.on_event("startup")
    def on_startup():
        init_db()

    @app.get("/health", tags=["health"])
    def health():
        return {
            "status": "ok",
            "app": settings.APP_NAME,
            "env": settings.ENV,
            "auto_posting_enabled": settings.AUTO_POSTING_ENABLED,
        }

    return app


app = create_app()
