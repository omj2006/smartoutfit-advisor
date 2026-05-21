from __future__ import annotations

import json
import logging
import re
import uuid
from typing import Any, AsyncIterator, Dict, List, Optional

from app.config import settings
from app.core.llm_provider import LLMProvider, LLMResponse, get_provider
from app.models.schemas import (
    AgentStep,
    ChatResponse,
    Message,
    Role,
    StreamEvent,
)
from app.tools.base import ToolRegistry

logger = logging.getLogger(__name__)

LANGGRAPH_AVAILABLE = False

try:
    from langgraph.graph import END, StateGraph

    LANGGRAPH_AVAILABLE = True
except ImportError:
    logger.warning("langgraph not installed, langgraph_agent will fallback to regular Agent")

from typing import TypedDict


class AgentState(TypedDict):
    messages: List[str]
    user_query: str
    city: str
    occasion: str
    gender: str
    style: str
    weather_data: str
    knowledge_data: str
    product_data: str
    trend_data: str
    outfit_plan: str
    image_url: str
    final_response: str
    error: str


def _initial_state(user_query: str) -> AgentState:
    return AgentState(
        messages=[],
        user_query=user_query,
        city="",
        occasion="",
        gender="",
        style="",
        weather_data="",
        knowledge_data="",
        product_data="",
        trend_data="",
        outfit_plan="",
        image_url="",
        final_response="",
        error="",
    )


async def _llm_parse(prompt: str, system: str = "") -> str:
    provider = get_provider()
    messages: List[Message] = []
    if system:
        messages.append(Message(role=Role.SYSTEM, content=system))
    messages.append(Message(role=Role.USER, content=prompt))
    try:
        response: LLMResponse = await provider.chat(messages=messages)
        return response.content or ""
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return ""


async def coordinator_node(state: AgentState) -> AgentState:
    user_query = state["user_query"]
    system_prompt = (
        "你是一个穿搭意图解析器。根据用户输入，提取以下参数并以JSON格式返回：\n"
        "- city: 城市（如'北京'、'上海'），如果用户没有指定则返回空字符串\n"
        "- occasion: 场合（如'上班'、'约会'、'休闲'、'运动'、'正式晚宴'），如果用户没有指定则返回'休闲'\n"
        "- gender: 性别（'男'或'女'），如果用户没有指定则返回空字符串\n"
        "- style: 风格偏好（如'简约'、'文艺'、'街头'、'优雅'），如果用户没有指定则返回空字符串\n"
        "只返回JSON，不要其他内容。"
    )
    result = await _llm_parse(user_query, system_prompt)
    try:
        cleaned = re.sub(r"```json\s*|```\s*", "", result).strip()
        params = json.loads(cleaned)
        state["city"] = params.get("city", "") or ""
        state["occasion"] = params.get("occasion", "") or "休闲"
        state["gender"] = params.get("gender", "") or ""
        state["style"] = params.get("style", "") or ""
    except (json.JSONDecodeError, AttributeError):
        state["city"] = ""
        state["occasion"] = "休闲"
        state["gender"] = ""
        state["style"] = ""
    state["messages"] = state.get("messages", []) + [f"[coordinator] 解析结果: city={state['city']}, occasion={state['occasion']}, gender={state['gender']}, style={state['style']}"]
    return state


async def weather_agent_node(state: AgentState) -> AgentState:
    registry = ToolRegistry()
    city = state.get("city", "")
    if not city:
        state["weather_data"] = "未指定城市，跳过天气查询"
        state["messages"] = state.get("messages", []) + ["[weather_agent] 未指定城市，跳过天气查询"]
        return state
    try:
        result = await registry.execute_tool("weather_query", city=city)
        state["weather_data"] = result
    except Exception as e:
        state["weather_data"] = f"天气查询失败: {str(e)}"
    state["messages"] = state.get("messages", []) + [f"[weather_agent] 天气数据已获取"]
    return state


async def fashion_agent_node(state: AgentState) -> AgentState:
    registry = ToolRegistry()
    user_query = state.get("user_query", "")
    occasion = state.get("occasion", "休闲")
    style = state.get("style", "")
    gender = state.get("gender", "")
    weather_data = state.get("weather_data", "")

    knowledge_query = user_query
    if occasion:
        knowledge_query += f" {occasion}穿搭"
    if style:
        knowledge_query += f" {style}风格"

    try:
        knowledge_result = await registry.execute_tool("knowledge_base", query=knowledge_query)
        state["knowledge_data"] = knowledge_result
    except Exception as e:
        state["knowledge_data"] = f"知识库查询失败: {str(e)}"

    product_kwargs: Dict[str, Any] = {"query": user_query}
    if occasion:
        product_kwargs["occasion"] = occasion
    if style:
        product_kwargs["style"] = style
    if gender:
        if gender == "女":
            product_kwargs["category"] = "连衣裙"
        else:
            product_kwargs["category"] = "上装"

    try:
        product_result = await registry.execute_tool("product_search", **product_kwargs)
        state["product_data"] = product_result
    except Exception as e:
        state["product_data"] = f"商品搜索失败: {str(e)}"

    try:
        trend_kwargs: Dict[str, Any] = {"query": f"{occasion or '日常'}穿搭趋势"}
        if style:
            trend_kwargs["style"] = style
        trend_result = await registry.execute_tool("trend_analyzer", **trend_kwargs)
        state["trend_data"] = trend_result
    except Exception as e:
        state["trend_data"] = f"趋势分析失败: {str(e)}"

    state["messages"] = state.get("messages", []) + ["[fashion_agent] 穿搭知识、商品、趋势数据已获取"]
    return state


async def image_agent_node(state: AgentState) -> AgentState:
    registry = ToolRegistry()
    product_data = state.get("product_data", "")
    occasion = state.get("occasion", "休闲")
    style = state.get("style", "")
    gender = state.get("gender", "女") or "女"
    weather_data = state.get("weather_data", "")

    weather_desc = ""
    if weather_data and "天气" in weather_data:
        for keyword in ["晴", "多云", "阴", "雨", "雪", "雾"]:
            if keyword in weather_data:
                weather_desc = keyword
                break

    top = ""
    bottom = ""
    dress = ""
    shoes = ""
    accessory = ""

    if product_data:
        lines = product_data.split("\n")
        for line in lines:
            lower = line.lower()
            if any(kw in lower for kw in ["上装", "衬衫", "t恤", "卫衣", "外套", "毛衣", "针织"]):
                if not top:
                    top = line.strip()[:50]
            elif any(kw in lower for kw in ["下装", "裤", "裙"]):
                if not bottom:
                    bottom = line.strip()[:50]
            elif any(kw in lower for kw in ["连衣裙"]):
                if not dress:
                    dress = line.strip()[:50]
            elif any(kw in lower for kw in ["鞋", "靴", "运动鞋"]):
                if not shoes:
                    shoes = line.strip()[:50]
            elif any(kw in lower for kw in ["配饰", "包", "帽", "围巾"]):
                if not accessory:
                    accessory = line.strip()[:50]

    image_kwargs: Dict[str, Any] = {}
    if dress:
        image_kwargs["dress"] = dress
    else:
        if top:
            image_kwargs["top"] = top
        if bottom:
            image_kwargs["bottom"] = bottom
    if shoes:
        image_kwargs["shoes"] = shoes
    if accessory:
        image_kwargs["accessory"] = accessory
    if style:
        image_kwargs["style"] = style
    if occasion:
        image_kwargs["occasion"] = occasion
    image_kwargs["gender"] = gender
    if weather_desc:
        image_kwargs["weather"] = weather_desc

    try:
        image_result = await registry.execute_tool("image_generator", **image_kwargs)
        urls = re.findall(r"\[IMAGE_URL\](.*?)\[/IMAGE_URL\]", image_result)
        if urls:
            state["image_url"] = urls[0]
        state["outfit_plan"] = image_result
    except Exception as e:
        state["outfit_plan"] = f"效果图生成失败: {str(e)}"
        state["image_url"] = ""

    state["messages"] = state.get("messages", []) + ["[image_agent] 穿搭效果图已生成"]
    return state


async def response_agent_node(state: AgentState) -> AgentState:
    user_query = state.get("user_query", "")
    city = state.get("city", "")
    occasion = state.get("occasion", "休闲")
    gender = state.get("gender", "")
    style = state.get("style", "")
    weather_data = state.get("weather_data", "")
    knowledge_data = state.get("knowledge_data", "")
    product_data = state.get("product_data", "")
    trend_data = state.get("trend_data", "")
    outfit_plan = state.get("outfit_plan", "")
    image_url = state.get("image_url", "")

    system_prompt = (
        "你是一位专业的穿搭顾问。请根据以下信息，为用户提供一份完整的穿搭推荐方案。\n"
        "方案应包含：天气分析、穿搭建议、推荐单品、搭配技巧、潮流趋势参考。\n"
        "请用友好、专业的语气回答，使用中文。"
    )

    context_parts = [f"用户需求: {user_query}"]
    if city:
        context_parts.append(f"城市: {city}")
    if occasion:
        context_parts.append(f"场合: {occasion}")
    if gender:
        context_parts.append(f"性别: {gender}")
    if style:
        context_parts.append(f"风格偏好: {style}")
    if weather_data:
        context_parts.append(f"\n天气信息:\n{weather_data[:500]}")
    if knowledge_data:
        context_parts.append(f"\n穿搭知识:\n{knowledge_data[:800]}")
    if product_data:
        context_parts.append(f"\n推荐商品:\n{product_data[:800]}")
    if trend_data:
        context_parts.append(f"\n潮流趋势:\n{trend_data[:500]}")
    if outfit_plan:
        context_parts.append(f"\n穿搭效果图:\n{outfit_plan[:300]}")

    prompt = "\n".join(context_parts)

    result = await _llm_parse(prompt, system_prompt)

    if image_url and "[IMAGE_URL]" not in result:
        result = result + "\n" + f"[IMAGE_URL]{image_url}[/IMAGE_URL]"

    state["final_response"] = result
    state["messages"] = state.get("messages", []) + ["[response_agent] 最终推荐已生成"]
    return state


def _build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("coordinator", coordinator_node)
    graph.add_node("weather_agent", weather_agent_node)
    graph.add_node("fashion_agent", fashion_agent_node)
    graph.add_node("image_agent", image_agent_node)
    graph.add_node("response_agent", response_agent_node)

    graph.set_entry_point("coordinator")
    graph.add_edge("coordinator", "weather_agent")
    graph.add_edge("weather_agent", "fashion_agent")
    graph.add_edge("fashion_agent", "image_agent")
    graph.add_edge("image_agent", "response_agent")
    graph.add_edge("response_agent", END)

    return graph.compile()


_compiled_graph = None


def _get_compiled_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = _build_graph()
    return _compiled_graph


async def run_langgraph_agent(
    user_query: str,
    conversation_id: Optional[str] = None,
) -> ChatResponse:
    if not LANGGRAPH_AVAILABLE:
        from app.core.agent import Agent

        agent = Agent()
        return await agent.run(
            user_message=user_query,
            conversation_id=conversation_id,
        )

    try:
        graph = _get_compiled_graph()
        state = _initial_state(user_query)
        result_state = await graph.ainvoke(state)

        steps: List[AgentStep] = []
        for msg in result_state.get("messages", []):
            steps.append(AgentStep(thought=msg, is_final=False))
        steps.append(AgentStep(thought=result_state.get("final_response", ""), is_final=True))

        provider = get_provider()
        return ChatResponse(
            message=result_state.get("final_response", "未能生成推荐"),
            steps=steps,
            provider=settings.default_provider,
            model=provider.model,
        )
    except Exception as e:
        logger.error(f"LangGraph agent failed: {e}, falling back to regular Agent")
        from app.core.agent import Agent

        agent = Agent()
        return await agent.run(
            user_message=user_query,
            conversation_id=conversation_id,
        )


async def run_langgraph_agent_stream(
    user_query: str,
    conversation_id: Optional[str] = None,
) -> AsyncIterator[StreamEvent]:
    if not LANGGRAPH_AVAILABLE:
        from app.core.agent import Agent

        agent = Agent()
        async for event in agent.run_stream(
            user_message=user_query,
            conversation_id=conversation_id,
        ):
            yield event
        return

    conv_id = conversation_id or str(uuid.uuid4())
    yield StreamEvent(type="conversation_id", data=conv_id)

    try:
        graph = _get_compiled_graph()
        state = _initial_state(user_query)

        node_names = [
            ("coordinator", "coordinator"),
            ("weather_agent", "weather_agent"),
            ("fashion_agent", "fashion_agent"),
            ("image_agent", "image_agent"),
            ("response_agent", "response_agent"),
        ]

        current_state = state
        for node_key, node_name in node_names:
            yield StreamEvent(
                type="agent_step",
                data={"node": node_name, "status": "running"},
            )

            try:
                node_func = {
                    "coordinator": coordinator_node,
                    "weather_agent": weather_agent_node,
                    "fashion_agent": fashion_agent_node,
                    "image_agent": image_agent_node,
                    "response_agent": response_agent_node,
                }[node_key]

                current_state = await node_func(current_state)

                step_data: Dict[str, Any] = {"node": node_name, "status": "completed"}

                if node_name == "coordinator":
                    step_data["city"] = current_state.get("city", "")
                    step_data["occasion"] = current_state.get("occasion", "")
                    step_data["gender"] = current_state.get("gender", "")
                    step_data["style"] = current_state.get("style", "")
                elif node_name == "weather_agent":
                    step_data["weather_data"] = current_state.get("weather_data", "")[:200]
                elif node_name == "fashion_agent":
                    step_data["knowledge_data"] = current_state.get("knowledge_data", "")[:200]
                    step_data["product_data"] = current_state.get("product_data", "")[:200]
                    step_data["trend_data"] = current_state.get("trend_data", "")[:200]
                elif node_name == "image_agent":
                    step_data["image_url"] = current_state.get("image_url", "")
                elif node_name == "response_agent":
                    step_data["final_response"] = current_state.get("final_response", "")[:200]

                yield StreamEvent(type="agent_step", data=step_data)
            except Exception as e:
                yield StreamEvent(
                    type="agent_step",
                    data={"node": node_name, "status": "error", "error": str(e)},
                )
                current_state["error"] = f"{node_name} failed: {str(e)}"

        final_response = current_state.get("final_response", "")
        if not final_response and current_state.get("error"):
            final_response = f"抱歉，生成推荐时遇到问题: {current_state['error']}"

        yield StreamEvent(type="final_answer", data=final_response)

    except Exception as e:
        logger.error(f"LangGraph stream failed: {e}, falling back to regular Agent stream")
        from app.core.agent import Agent

        agent = Agent()
        async for event in agent.run_stream(
            user_message=user_query,
            conversation_id=conversation_id,
        ):
            yield event
