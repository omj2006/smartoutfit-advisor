from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Callable

from app.models.schemas import ToolDefinition

logger = logging.getLogger(__name__)


class BaseTool(ABC):
    name: str = ""
    description: str = ""
    parameters: dict[str, Any] = {}

    @abstractmethod
    async def execute(self, **kwargs) -> str:
        pass

    def get_definition(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def get_tool_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters=self.parameters,
        )


class ToolRegistry:
    _instance: ToolRegistry | None = None
    _tools: dict[str, BaseTool]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools = {}
        return cls._instance

    def register(self, tool: BaseTool) -> None:
        if tool.name in self._tools:
            logger.warning(f"Tool '{tool.name}' already registered, overwriting")
        self._tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def unregister(self, name: str) -> None:
        if name in self._tools:
            del self._tools[name]
            logger.info(f"Unregistered tool: {name}")

    def get(self, name: str) -> BaseTool | None:
        return self._tools.get(name)

    def get_all(self) -> dict[str, BaseTool]:
        return dict(self._tools)

    def get_tool_definitions(self) -> list[dict]:
        return [tool.get_definition() for tool in self._tools.values()]

    def get_tool_names(self) -> list[str]:
        return list(self._tools.keys())

    def has_tool(self, name: str) -> bool:
        return name in self._tools

    async def execute_tool(self, name: str, **kwargs) -> str:
        tool = self._tools.get(name)
        if not tool:
            return f"Error: Tool '{name}' not found"
        try:
            result = await tool.execute(**kwargs)
            return result
        except Exception as e:
            logger.error(f"Tool '{name}' execution failed: {e}")
            return f"Error executing tool '{name}': {str(e)}"


def register_tool(cls: type[BaseTool]) -> type[BaseTool]:
    registry = ToolRegistry()
    instance = cls()
    registry.register(instance)
    return cls


def tool(
    name: str, description: str, parameters: dict[str, Any]
) -> Callable[[Callable], type[BaseTool]]:
    def decorator(func: Callable) -> type[BaseTool]:
        class FuncTool(BaseTool):
            pass

        FuncTool.name = name
        FuncTool.description = description
        FuncTool.parameters = parameters

        async def execute(self, **kwargs):
            import asyncio
            import inspect

            if inspect.iscoroutinefunction(func):
                return await func(**kwargs)
            return await asyncio.to_thread(func, **kwargs)

        FuncTool.execute = execute
        registry = ToolRegistry()
        registry.register(FuncTool())
        return FuncTool

    return decorator
