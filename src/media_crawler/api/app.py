from __future__ import annotations

from contextlib import AsyncExitStack, asynccontextmanager

from fastapi import FastAPI, Request

from pythonprojecttemplate.api.auth.token_registry import token_registry
from pythonprojecttemplate.api.http_status import HTTPStatus
from pythonprojecttemplate.api.models.result_vo import ResultVO

from pythonprojecttemplate.config.settings import settings
from pythonprojecttemplate.log.logHelper import get_logger
from pythonprojecttemplate.modules.loader import module_lifespan
from pythonprojecttemplate.monitoring.main import monitoring_center
from pythonprojecttemplate.scheduler.scheduler_center import scheduler_center

from .api_router import api_router

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting scheduler and monitoring centers")
    await token_registry.startup()
    scheduler_center.start()
    await monitoring_center.start()

    async with AsyncExitStack() as stack:
        await stack.enter_async_context(module_lifespan(app))
        try:
            yield
        finally:
            logger.info("Shutting down background services")
            scheduler_center.shutdown()
            await monitoring_center.shutdown()
            await token_registry.shutdown()


def create_application() -> FastAPI:
    origin = getattr(settings, "load_origin", {})
    logger.info(
        "Configuration version %s loaded from %s (env=%s, env_file=%s, config_file=%s)",
        settings.config_version,
        origin.get("source", "unknown"),
        origin.get("env_name", settings.env),
        origin.get("env_file", "n/a"),
        origin.get("config_file", "n/a"),
    )
    app = FastAPI(
        title=settings.api.title,
        description=settings.api.description,
        version=settings.api.version,
        lifespan=lifespan,
        docs_url=settings.api.docs_url,
    )
    app.include_router(api_router)

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return ResultVO.error(
            code=HTTPStatus.INTERNAL_SERVER_ERROR.code,
            message=str(exc),
        )

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": settings.api.title, "version": settings.api.version}

    @app.get("/")
    async def root():
        return {
            "message": "Welcome to Python Project Template API",
            "version": settings.api.version,
            "docs": settings.api.docs_url,
            "health": "/health",
        }

    return app


app = create_application()

__all__ = ["app", "create_application"]
