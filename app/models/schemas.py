from __future__ import annotations

from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, Field


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ToolCallFunction(BaseModel):
    name: str
    arguments: str


class ToolCall(BaseModel):
    id: str
    type: str = "function"
    function: ToolCallFunction


class Message(BaseModel):
    role: Role
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None


class ToolParameter(BaseModel):
    type: str
    description: str = ""
    enum: Optional[List[str]] = None


class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: dict = Field(default_factory=dict)


class ChatRequest(BaseModel):
    message: str
    provider: Optional[str] = None
    model: Optional[str] = None
    conversation_id: Optional[str] = None


class ToolResultMessage(BaseModel):
    tool_name: str
    tool_call_id: str
    result: str
    success: bool


class AgentStep(BaseModel):
    thought: Optional[str] = None
    tool_name: Optional[str] = None
    tool_args: Optional[dict] = None
    tool_result: Optional[str] = None
    is_final: bool = False


class ChatResponse(BaseModel):
    message: str
    steps: List[AgentStep] = Field(default_factory=list)
    provider: str = ""
    model: str = ""


class StreamEvent(BaseModel):
    type: str
    data: Any = None
