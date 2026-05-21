from __future__ import annotations

import json
import logging
import re
import uuid
from typing import Any, AsyncIterator, Callable

from app.config import settings
from app.core.llm_provider import LLMProvider, LLMResponse, get_provider
from app.models.schemas import (
    AgentStep,
    ChatResponse,
    Message,
    Role,
    StreamEvent,
    ToolCall,
)
from app.tools.base import ToolRegistry

logger = logging.getLogger(__name__)


class Conversation:
    def __init__(self, conversation_id: str | None = None):
        self.id = conversation_id or str(uuid.uuid4())
        self.messages: list[Message] = []

    def add_message(self, message: Message) -> None:
        self.messages.append(message)

    def add_user_message(self, content: str) -> None:
        self.add_message(Message(role=Role.USER, content=content))

    def add_assistant_message(
        self, content: str | None = None, tool_calls: list[ToolCall] | None = None
    ) -> None:
        self.add_message(
            Message(role=Role.ASSISTANT, content=content, tool_calls=tool_calls)
        )

    def add_tool_message(
        self, content: str, tool_call_id: str, name: str
    ) -> None:
        self.add_message(
            Message(
                role=Role.TOOL,
                content=content,
                tool_call_id=tool_call_id,
                name=name,
            )
        )

    def get_messages(self) -> list[Message]:
        return list(self.messages)

    def clear(self) -> None:
        self.messages.clear()


class Agent:
    def __init__(
        self,
        provider: LLMProvider | None = None,
        tool_registry: ToolRegistry | None = None,
        max_iterations: int | None = None,
        system_prompt: str | None = None,
        on_step: Callable[[AgentStep], Any] | None = None,
    ):
        self.provider = provider or get_provider()
        self.tool_registry = tool_registry or ToolRegistry()
        self.max_iterations = max_iterations or settings.max_iterations
        self.system_prompt = system_prompt or settings.system_prompt
        self.on_step = on_step
        self._conversations: dict[str, Conversation] = {}

    def get_or_create_conversation(self, conversation_id: str | None = None) -> Conversation:
        if conversation_id and conversation_id in self._conversations:
            return self._conversations[conversation_id]
        conv = Conversation(conversation_id)
        self._conversations[conv.id] = conv
        return conv

    def _build_system_message(self) -> Message:
        tool_names = self.tool_registry.get_tool_names()
        tools_desc = ""
        if tool_names:
            tools_desc = f"\n\n你可以使用以下工具: {', '.join(tool_names)}\n当需要使用工具时，请调用相应的工具函数。"

        return Message(
            role=Role.SYSTEM,
            content=self.system_prompt + tools_desc,
        )

    async def run(
        self,
        user_message: str,
        conversation_id: str | None = None,
        provider_name: str | None = None,
        model: str | None = None,
    ) -> ChatResponse:
        if provider_name:
            self.provider = get_provider(provider_name)

        conv = self.get_or_create_conversation(conversation_id)
        conv.add_user_message(user_message)

        steps: list[AgentStep] = []
        messages = [self._build_system_message()] + conv.get_messages()
        tools = self.tool_registry.get_tool_definitions()

        for iteration in range(self.max_iterations):
            logger.info(f"Agent iteration {iteration + 1}/{self.max_iterations}")

            try:
                response: LLMResponse = await self.provider.chat(
                    messages=messages,
                    tools=tools if tools else None,
                    model=model,
                )
            except Exception as e:
                logger.error(f"LLM call failed: {e}")
                step = AgentStep(
                    thought=f"LLM调用失败: {str(e)}",
                    is_final=True,
                )
                steps.append(step)
                return ChatResponse(
                    message=f"抱歉，AI模型调用失败: {str(e)}",
                    steps=steps,
                    provider=provider_name or settings.default_provider,
                    model=model or self.provider.model,
                )

            if response.has_tool_calls:
                conv.add_assistant_message(
                    content=response.content, tool_calls=response.tool_calls
                )
                messages.append(conv.messages[-1])

                for tool_call in response.tool_calls:
                    func_name = tool_call.function.name
                    try:
                        func_args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        func_args = {}

                    step = AgentStep(
                        thought=response.content,
                        tool_name=func_name,
                        tool_args=func_args,
                    )

                    if self.on_step:
                        self.on_step(step)

                    result = await self.tool_registry.execute_tool(
                        func_name, **func_args
                    )

                    step.tool_result = result
                    steps.append(step)

                    conv.add_tool_message(
                        content=result,
                        tool_call_id=tool_call.id,
                        name=func_name,
                    )
                    messages.append(conv.messages[-1])

                    logger.info(f"Tool {func_name} executed: {result[:200]}")
            else:
                final_content = response.content or ""
                conv.add_assistant_message(content=final_content)

                image_urls = []
                for step in steps:
                    if step.tool_result and "[IMAGE_URL]" in (step.tool_result or ""):
                        urls = re.findall(r'\[IMAGE_URL\](.*?)\[/IMAGE_URL\]', step.tool_result)
                        image_urls.extend(urls)

                if image_urls and "[IMAGE_URL]" not in final_content:
                    image_tags = "".join(f"[IMAGE_URL]{url}[/IMAGE_URL]" for url in image_urls)
                    final_content = final_content + "\n" + image_tags

                step = AgentStep(
                    thought=final_content,
                    is_final=True,
                )
                steps.append(step)

                if self.on_step:
                    self.on_step(step)

                return ChatResponse(
                    message=final_content,
                    steps=steps,
                    provider=provider_name or settings.default_provider,
                    model=model or self.provider.model,
                )

        conv.add_assistant_message(content="达到最大迭代次数，停止执行。")
        return ChatResponse(
            message="达到最大迭代次数，未能完成任务。请尝试简化你的问题。",
            steps=steps,
            provider=provider_name or settings.default_provider,
            model=model or self.provider.model,
        )

    async def run_stream(
        self,
        user_message: str,
        conversation_id: str | None = None,
        provider_name: str | None = None,
        model: str | None = None,
    ) -> AsyncIterator[StreamEvent]:
        if provider_name:
            self.provider = get_provider(provider_name)

        conv = self.get_or_create_conversation(conversation_id)

        yield StreamEvent(type="conversation_id", data=conv.id)

        conv.add_user_message(user_message)

        messages = [self._build_system_message()] + conv.get_messages()
        tools = self.tool_registry.get_tool_definitions()

        collected_image_urls = []

        for iteration in range(self.max_iterations):
            try:
                response = await self.provider.chat(
                    messages=messages,
                    tools=tools if tools else None,
                    model=model,
                )
            except Exception as e:
                yield StreamEvent(type="error", data=str(e))
                return

            if response.has_tool_calls:
                conv.add_assistant_message(
                    content=response.content, tool_calls=response.tool_calls
                )
                messages.append(conv.messages[-1])

                for tool_call in response.tool_calls:
                    func_name = tool_call.function.name
                    try:
                        func_args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        func_args = {}

                    yield StreamEvent(
                        type="tool_call",
                        data={
                            "name": func_name,
                            "args": func_args,
                            "thought": response.content,
                        },
                    )

                    result = await self.tool_registry.execute_tool(
                        func_name, **func_args
                    )

                    if "[IMAGE_URL]" in result:
                        urls = re.findall(r'\[IMAGE_URL\](.*?)\[/IMAGE_URL\]', result)
                        collected_image_urls.extend(urls)

                    yield StreamEvent(
                        type="tool_result",
                        data={"name": func_name, "result": result},
                    )

                    conv.add_tool_message(
                        content=result,
                        tool_call_id=tool_call.id,
                        name=func_name,
                    )
                    messages.append(conv.messages[-1])
            else:
                final_content = response.content or ""
                conv.add_assistant_message(content=final_content)

                if collected_image_urls and "[IMAGE_URL]" not in final_content:
                    image_tags = "".join(f"[IMAGE_URL]{url}[/IMAGE_URL]" for url in collected_image_urls)
                    final_content = final_content + "\n" + image_tags

                yield StreamEvent(type="final_answer", data=final_content)
                return

        yield StreamEvent(
            type="error",
            data="达到最大迭代次数，未能完成任务。",
        )
