from __future__ import annotations

import json
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.core.agent import Agent
from app.core.llm_provider import get_available_providers
from app.models.schemas import ChatRequest, ChatResponse
from app.tools.base import ToolRegistry
from app.tools.builtin.product_db import get_all_products, get_categories, init_db, query_products

router = APIRouter()

agent: Agent | None = None


def get_agent() -> Agent:
    global agent
    if agent is None:
        agent = Agent()
    return agent


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        a = get_agent()
        response = await a.run(
            user_message=request.message,
            conversation_id=request.conversation_id,
            provider_name=request.provider,
            model=request.model,
        )
        response.provider = request.provider or response.provider
        response.model = request.model or response.model
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    use_langgraph = request.model == "langgraph" if request.model else False

    async def event_generator():
        try:
            if use_langgraph:
                from app.core.langgraph_agent import run_langgraph_agent_stream
                async for event in run_langgraph_agent_stream(
                    user_query=request.message,
                    conversation_id=request.conversation_id,
                ):
                    yield f"data: {json.dumps(event.model_dump(), ensure_ascii=False)}\n\n"
            else:
                a = get_agent()
                async for event in a.run_stream(
                    user_message=request.message,
                    conversation_id=request.conversation_id,
                    provider_name=request.provider,
                    model=request.model,
                ):
                    yield f"data: {json.dumps(event.model_dump(), ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            error_event = {"type": "error", "data": str(e)}
            yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/tools")
async def list_tools():
    registry = ToolRegistry()
    tools = []
    for name, tool in registry.get_all().items():
        tools.append(tool.get_tool_definition().model_dump())
    return {"tools": tools}


@router.get("/providers")
async def list_providers():
    return {"providers": get_available_providers()}


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    a = get_agent()
    conv = a._conversations.get(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {
        "id": conv.id,
        "messages": [m.model_dump() for m in conv.messages],
    }


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    a = get_agent()
    if conversation_id in a._conversations:
        del a._conversations[conversation_id]
    return {"status": "ok"}


@router.get("/products")
async def list_products(
    category: Optional[str] = None,
    season: Optional[str] = None,
    occasion: Optional[str] = None,
    gender: Optional[str] = None,
    max_price: Optional[float] = None,
    limit: int = 20,
):
    init_db()
    products = query_products(
        category=category,
        season=season,
        occasion=occasion,
        gender=gender,
        max_price=max_price,
        limit=limit,
    )
    return {"products": products, "total": len(products)}


@router.post("/generate-outfit-image")
async def generate_outfit_image(request: dict):
    from app.tools.builtin.image_generator import ImageGeneratorTool

    tool = ImageGeneratorTool()
    try:
        result = await tool.execute(**request)
        image_url = None
        if "[IMAGE_URL]" in result:
            start = result.index("[IMAGE_URL]") + len("[IMAGE_URL]")
            end = result.index("[/IMAGE_URL]")
            image_url = result[start:end]

        return {
            "success": image_url is not None,
            "image_url": image_url,
            "message": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products/categories")
async def list_product_categories():
    init_db()
    return {"categories": get_categories()}


@router.get("/products/search")
async def search_products(
    q: str = "",
    category: Optional[str] = None,
    season: Optional[str] = None,
    occasion: Optional[str] = None,
    style: Optional[str] = None,
    gender: Optional[str] = None,
    max_price: Optional[float] = None,
    top_k: int = 5,
):
    from app.tools.builtin.product_search import get_search_engine

    init_db()
    engine = get_search_engine()

    filters = {}
    if category:
        filters["category"] = category
    if season:
        filters["season"] = season
    if occasion:
        filters["occasion"] = occasion
    if style:
        filters["style"] = style
    if gender:
        filters["gender"] = gender

    results = engine.search(
        query=q,
        top_k=top_k,
        filters=filters if filters else None,
    )

    products = []
    for score, product in results:
        if max_price and product.get("price", 0) > max_price:
            continue
        product["match_score"] = round(score, 3)
        products.append(product)

    return {"products": products, "total": len(products)}


@router.post("/ecommerce/sync")
async def sync_ecommerce_products(platforms: Optional[str] = None):
    from app.tools.builtin.product_sync import ProductSync
    try:
        sync = ProductSync()
        platform_list = platforms.split(",") if platforms else None
        result = sync.sync_from_platforms(platform_list)
        return {"status": "ok", "synced": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ecommerce/stats")
async def ecommerce_stats():
    from app.tools.builtin.product_sync import ProductSync
    try:
        sync = ProductSync()
        return sync.get_sync_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
