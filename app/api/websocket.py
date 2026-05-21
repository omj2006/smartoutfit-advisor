from __future__ import annotations

import json
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.agent import Agent
from app.tools.base import ToolRegistry

router = APIRouter()

logger = logging.getLogger(__name__)

_agent: Agent | None = None


def get_ws_agent() -> Agent:
    global _agent
    if _agent is None:
        _agent = Agent()
    return _agent


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    agent = get_ws_agent()

    try:
        while True:
            data = await websocket.receive_text()
            try:
                request = json.loads(data)
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "data": "Invalid JSON"})
                continue

            user_message = request.get("message", "")
            provider = request.get("provider")
            model = request.get("model")
            conversation_id = request.get("conversation_id")

            if not user_message:
                await websocket.send_json({"type": "error", "data": "Empty message"})
                continue

            try:
                async for event in agent.run_stream(
                    user_message=user_message,
                    conversation_id=conversation_id,
                    provider_name=provider,
                    model=model,
                ):
                    await websocket.send_json(event.model_dump())
            except Exception as e:
                logger.error(f"Stream error: {e}")
                await websocket.send_json({"type": "error", "data": str(e)})

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
