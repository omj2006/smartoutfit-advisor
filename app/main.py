from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as api_router
from app.api.websocket import router as ws_router
from app.tools.base import ToolRegistry

logger = logging.getLogger(__name__)

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
IMAGES_DIR = Path(__file__).parent.parent / "data" / "generated_images"


def _load_builtin_tools():
    import app.tools.builtin.calculator
    import app.tools.builtin.web_search
    import app.tools.builtin.code_runner
    import app.tools.builtin.file_ops
    import app.tools.builtin.weather_query
    import app.tools.builtin.knowledge_base
    import app.tools.builtin.outfit_advisor
    import app.tools.builtin.product_search
    import app.tools.builtin.image_generator
    import app.tools.builtin.trend_analyzer
    import app.tools.builtin.ecommerce_api
    import app.tools.builtin.product_sync

    registry = ToolRegistry()
    logger.info(f"Loaded {len(registry.get_tool_names())} builtin tools: {registry.get_tool_names()}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    _load_builtin_tools()
    logger.info("Agent server started")
    yield
    logger.info("Agent server shutting down")


def create_app() -> FastAPI:
    app = FastAPI(
        title="穿搭顾问 - 智能穿搭助手",
        description="基于天气和场合的智能穿搭推荐平台，支持商品搜索和效果图生成",
        version="0.2.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api")
    app.include_router(ws_router)

    os.makedirs(str(IMAGES_DIR), exist_ok=True)
    app.mount("/images", StaticFiles(directory=str(IMAGES_DIR)), name="images")

    if FRONTEND_DIR.exists():
        app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    from app.config import settings

    uvicorn.run(
        "app.main:app",
        host=settings.server.get("host", "0.0.0.0"),
        port=settings.server.get("port", 8000),
        reload=True,
    )
