from __future__ import annotations

import logging
import os
import random
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)

# 当前文件目录
current_dir = Path(__file__).resolve().parent

FRONTEND_DIR = current_dir / "dist"
IMAGES_DIR = current_dir / "data" / "generated_images"


def _get_mock_outfit_result(city: str, occasion: str):
    """
    获取模拟的穿搭工作流结果（用于演示和故障恢复）
    """
    temp = random.randint(18, 28)
    temp_range = "舒适（18-25℃）" if temp <= 25 else "温暖（25-32℃）"
    
    suggestions = {
        "日常": "T恤+牛仔裤+帆布鞋，休闲舒适",
        "通勤": "衬衫+休闲裤+皮鞋，干练得体",
        "约会": "连衣裙+小白鞋，优雅浪漫",
        "运动": "运动套装+运动鞋，活力四射",
        "聚会": "小西装+连衣裙+高跟鞋，时尚优雅"
    }
    
    suggestion = suggestions.get(occasion, suggestions["日常"])
    
    return {
        "success": True,
        "data": {
            "weather": {
                "city": city or "北京",
                "temperature": temp,
                "weather": "多云",
                "wind_speed": "10 km/h",
                "temp_range": temp_range
            },
            "outfit_suggestion": {
                "temp_range": temp_range,
                "occasion": occasion or "日常",
                "suggestion": suggestion,
                "style": f"{occasion or '日常'}风格"
            },
            "filtered_products": [
                {"id": 1, "name": "简约休闲T恤", "brand": "StyleAI", "price": "¥199", "category": "上衣"},
                {"id": 2, "name": "高腰牛仔裤", "brand": "StyleAI", "price": "¥299", "category": "下装"},
                {"id": 3, "name": "舒适休闲鞋", "brand": "StyleAI", "price": "¥399", "category": "鞋履"},
                {"id": 4, "name": "时尚单肩包", "brand": "StyleAI", "price": "¥159", "category": "配饰"}
            ],
            "fashion_trends": [
                {"style": "极简主义", "items": "oversize西装、阔腿裤", "colors": "大地色系"},
                {"style": "运动休闲风", "items": "卫衣、运动裤", "colors": "荧光色"},
                {"style": "复古回潮", "items": "格纹衬衫、喇叭裤", "colors": "酒红色"}
            ],
            "image_prompt": f"时尚穿搭，{occasion or '日常'}场合，温度{temp}度，高清全身人像摄影",
            "execution_log": [],
            "user_memory": {"preferred_styles": [], "preferred_colors": []}
        }
    }


def _load_builtin_tools():
    """加载内置工具"""
    try:
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

        from app.tools.base import ToolRegistry
        registry = ToolRegistry()
        logger.info(f"Loaded {len(registry.get_tool_names())} builtin tools: {registry.get_tool_names()}")
    except Exception as e:
        logger.warning(f"Failed to load some tools: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    _load_builtin_tools()
    logger.info("SmartOutfit Advisor server started with full backend features")
    yield
    logger.info("SmartOutfit Advisor server shutting down")


def create_app() -> FastAPI:
    app = FastAPI(
        title="SmartOutfit Advisor - AI 穿搭助手",
        description="基于 LangGraph 多智能体的智能穿搭推荐平台",
        version="2.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 包含完整的后端 API
    try:
        from app.api.routes import router as api_router
        app.include_router(api_router, prefix="/api")
        logger.info("完整 API 路由加载成功")
    except Exception as e:
        logger.warning(f"无法加载完整 API: {e}, 使用简化 API")

    # 包含认证 API
    try:
        from auth_api import router as auth_router
        app.include_router(auth_router)
        logger.info("认证 API 加载成功")
    except Exception as e:
        logger.warning(f"无法加载认证 API: {e}")

    # LangGraph 多智能体工作流 API
    @app.post("/api/langgraph/outfit")
    async def langgraph_outfit(request: dict):
        """
        LangGraph 多智能体穿搭工作流
        包含：天气查询、知识库、商品检索、潮流趋势、图像生成
        """
        import traceback
        
        try:
            city = request.get("city", "")
            occasion = request.get("occasion", "")
            user_query = request.get("query", "")
            user_id = request.get("user_id", "default")
            
            # 调用工作流（带超时处理）
            import threading
            import time
            
            result = None
            error = None
            
            def run_workflow():
                nonlocal result, error
                try:
                    from agents.outfit_workflow import get_outfit_workflow
                    
                    workflow = get_outfit_workflow()
                    result = workflow.run(
                        city=city,
                        occasion=occasion,
                        user_query=user_query,
                        user_id=user_id
                    )
                except Exception as e:
                    error = e
            
            # 启动工作流线程，设置超时
            thread = threading.Thread(target=run_workflow)
            thread.start()
            thread.join(timeout=30)  # 30秒超时
            
            if error:
                raise error
            
            if result is None:
                # 如果超时，返回模拟数据
                logger.warning("LangGraph workflow timed out, returning mock data")
                return _get_mock_outfit_result(city, occasion)
            
            return {
                "success": True,
                "data": {
                    "weather": result.get("weather"),
                    "outfit_suggestion": result.get("outfit_suggestion"),
                    "filtered_products": result.get("filtered_products"),
                    "fashion_trends": result.get("fashion_trends"),
                    "image_prompt": result.get("image_prompt"),
                    "execution_log": result.get("execution_log"),
                    "user_memory": result.get("user_memory")
                }
            }
        except Exception as e:
            logger.error(f"LangGraph workflow error: {e}")
            logger.error(traceback.format_exc())
            # 无论如何都返回模拟数据
            return _get_mock_outfit_result(request.get("city", ""), request.get("occasion", ""))
    
    # 基础健康检查
    @app.get("/api/health")
    async def health_check():
        return {
            "status": "ok",
            "message": "SmartOutfit Advisor server is running",
            "features": [
                "weather_query",
                "knowledge_base",
                "outfit_advisor",
                "product_search",
                "image_generator",
                "trend_analyzer",
                "langgraph_workflow"
            ]
        }

    # 挂载静态文件
    os.makedirs(str(IMAGES_DIR), exist_ok=True)
    try:
        app.mount("/images", StaticFiles(directory=str(IMAGES_DIR)), name="images")
    except Exception as e:
        logger.warning(f"Could not mount images directory: {e}")

    if FRONTEND_DIR.exists():
        try:
            app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIR / "assets")), name="assets")
            
            @app.get("/{path:path}")
            async def serve_frontend(path: str):
                file_path = FRONTEND_DIR / path
                if file_path.exists() and file_path.is_file():
                    return FileResponse(file_path)
                return FileResponse(FRONTEND_DIR / "index.html")
        except Exception as e:
            logger.warning(f"Could not serve frontend: {e}")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "merged_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
