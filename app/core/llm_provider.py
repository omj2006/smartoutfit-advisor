from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from typing import Any, AsyncIterator

from app.config import settings
from app.models.schemas import Message, Role, ToolCall, ToolCallFunction

logger = logging.getLogger(__name__)


class LLMResponse:
    def __init__(
        self,
        content: str | None = None,
        tool_calls: list[ToolCall] | None = None,
        finish_reason: str = "stop",
    ):
        self.content = content
        self.tool_calls = tool_calls or []
        self.finish_reason = finish_reason

    @property
    def has_tool_calls(self) -> bool:
        return len(self.tool_calls) > 0


class LLMProvider(ABC):
    def __init__(self, config: dict):
        self.config = config
        self.model = config.get("model", "")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 4096)

    @abstractmethod
    async def chat(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,
        **kwargs,
    ) -> LLMResponse:
        pass

    @abstractmethod
    async def chat_stream(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,
        **kwargs,
    ) -> AsyncIterator[str]:
        pass

    def _messages_to_dicts(self, messages: list[Message]) -> list[dict]:
        result = []
        for msg in messages:
            d: dict[str, Any] = {"role": msg.role.value}
            if msg.content is not None:
                d["content"] = msg.content
            if msg.tool_calls:
                d["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in msg.tool_calls
                ]
            if msg.tool_call_id:
                d["tool_call_id"] = msg.tool_call_id
            if msg.name:
                d["name"] = msg.name
            result.append(d)
        return result


class OpenAIProvider(LLMProvider):
    def __init__(self, config: dict):
        super().__init__(config)
        from openai import AsyncOpenAI

        api_key = config.get("api_key", "") or "sk-placeholder"
        base_url = config.get("base_url")
        client_kwargs: dict[str, Any] = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
        self.client = AsyncOpenAI(**client_kwargs)

    async def chat(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,
        **kwargs,
    ) -> LLMResponse:
        msg_dicts = self._messages_to_dicts(messages)
        chat_kwargs: dict[str, Any] = {
            "model": kwargs.get("model") or self.model,
            "messages": msg_dicts,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if tools:
            chat_kwargs["tools"] = tools
            chat_kwargs["tool_choice"] = "auto"

        response = await self.client.chat.completions.create(**chat_kwargs)
        choice = response.choices[0]

        tool_calls = None
        if choice.message.tool_calls:
            tool_calls = [
                ToolCall(
                    id=tc.id,
                    type=tc.type,
                    function=ToolCallFunction(
                        name=tc.function.name,
                        arguments=tc.function.arguments,
                    ),
                )
                for tc in choice.message.tool_calls
            ]

        return LLMResponse(
            content=choice.message.content,
            tool_calls=tool_calls,
            finish_reason=choice.finish_reason or "stop",
        )

    async def chat_stream(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,
        **kwargs,
    ) -> AsyncIterator[str]:
        msg_dicts = self._messages_to_dicts(messages)
        chat_kwargs: dict[str, Any] = {
            "model": kwargs.get("model") or self.model,
            "messages": msg_dicts,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": True,
        }
        if tools:
            chat_kwargs["tools"] = tools
            chat_kwargs["tool_choice"] = "auto"

        stream = await self.client.chat.completions.create(**chat_kwargs)
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class AnthropicProvider(LLMProvider):
    def __init__(self, config: dict):
        super().__init__(config)
        from anthropic import AsyncAnthropic

        api_key = config.get("api_key", "") or "sk-ant-placeholder"
        self.client = AsyncAnthropic(api_key=api_key)

    def _convert_tools_to_anthropic(self, tools: list[dict]) -> list[dict]:
        anthropic_tools = []
        for tool in tools:
            func = tool.get("function", tool)
            anthropic_tools.append(
                {
                    "name": func["name"],
                    "description": func.get("description", ""),
                    "input_schema": func.get("parameters", {"type": "object", "properties": {}}),
                }
            )
        return anthropic_tools

    def _convert_messages_for_anthropic(
        self, messages: list[Message]
    ) -> tuple[str | None, list[dict]]:
        system_prompt = None
        converted = []
        for msg in messages:
            if msg.role == Role.SYSTEM:
                system_prompt = msg.content
                continue
            if msg.role == Role.TOOL:
                converted.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": msg.tool_call_id,
                                "content": msg.content,
                            }
                        ],
                    }
                )
                continue
            d: dict[str, Any] = {"role": msg.role.value}
            if msg.content is not None:
                d["content"] = msg.content
            if msg.tool_calls:
                content_blocks = []
                if msg.content:
                    content_blocks.append({"type": "text", "text": msg.content})
                for tc in msg.tool_calls:
                    content_blocks.append(
                        {
                            "type": "tool_use",
                            "id": tc.id,
                            "name": tc.function.name,
                            "input": json.loads(tc.function.arguments),
                        }
                    )
                d["content"] = content_blocks
            converted.append(d)
        return system_prompt, converted

    async def chat(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,
        **kwargs,
    ) -> LLMResponse:
        system_prompt, msg_dicts = self._convert_messages_for_anthropic(messages)
        chat_kwargs: dict[str, Any] = {
            "model": kwargs.get("model") or self.model,
            "messages": msg_dicts,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if system_prompt:
            chat_kwargs["system"] = system_prompt
        if tools:
            chat_kwargs["tools"] = self._convert_tools_to_anthropic(tools)

        response = await self.client.messages.create(**chat_kwargs)

        content_text = None
        tool_calls = []

        for block in response.content:
            if block.type == "text":
                content_text = block.text
            elif block.type == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=block.id,
                        type="function",
                        function=ToolCallFunction(
                            name=block.name,
                            arguments=json.dumps(block.input),
                        ),
                    )
                )

        return LLMResponse(
            content=content_text,
            tool_calls=tool_calls if tool_calls else None,
            finish_reason=response.stop_reason or "stop",
        )

    async def chat_stream(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,
        **kwargs,
    ) -> AsyncIterator[str]:
        system_prompt, msg_dicts = self._convert_messages_for_anthropic(messages)
        chat_kwargs: dict[str, Any] = {
            "model": kwargs.get("model") or self.model,
            "messages": msg_dicts,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if system_prompt:
            chat_kwargs["system"] = system_prompt

        async with self.client.messages.stream(**chat_kwargs) as stream:
            async for text in stream.text_stream:
                yield text


class DeepSeekProvider(OpenAIProvider):
    pass


class DummyProvider(LLMProvider):
    def __init__(self, config: dict):
        super().__init__(config)
        self._reason = config.get("reason", "No API key configured")

    async def chat(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,
        **kwargs,
    ) -> LLMResponse:
        return LLMResponse(
            content=(
                f"⚠️ 当前无法调用AI模型：{self._reason}\n\n"
                "请在项目根目录创建 `.env` 文件并配置至少一个API Key：\n"
                "```\n"
                "OPENAI_API_KEY=sk-your-key\n"
                "DEEPSEEK_API_KEY=sk-your-key\n"
                "ANTHROPIC_API_KEY=sk-ant-your-key\n"
                "```\n"
                "配置完成后重启服务器即可正常使用。"
            ),
            finish_reason="stop",
        )

    async def chat_stream(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,
        **kwargs,
    ) -> AsyncIterator[str]:
        yield (
            f"⚠️ 当前无法调用AI模型：{self._reason}\n\n"
            "请在项目根目录创建 `.env` 文件并配置至少一个API Key。"
        )


PROVIDER_CLASSES: dict[str, type[LLMProvider]] = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "deepseek": DeepSeekProvider,
}

_providers: dict[str, LLMProvider] = {}


def get_available_providers() -> list[str]:
    return [
        name
        for name, config in settings.providers.items()
        if config.get("api_key")
    ]


def get_provider(name: str | None = None) -> LLMProvider:
    provider_name = name or settings.default_provider
    if provider_name not in _providers:
        if provider_name not in PROVIDER_CLASSES:
            raise ValueError(
                f"Unknown provider: {provider_name}. Available: {list(PROVIDER_CLASSES.keys())}"
            )
        config = settings.get_provider_config(provider_name)
        api_key = config.get("api_key", "")
        if not api_key:
            available = get_available_providers()
            if available:
                fallback_name = available[0]
                logger.warning(f"Provider '{provider_name}' has no API key, falling back to '{fallback_name}'")
                provider_name = fallback_name
                if provider_name in _providers:
                    return _providers[provider_name]
                config = settings.get_provider_config(provider_name)
            else:
                logger.warning("No API key configured for any provider, using DummyProvider")
                return DummyProvider({"reason": "未配置任何API Key"})
        _providers[provider_name] = PROVIDER_CLASSES[provider_name](config)
    return _providers[provider_name]
