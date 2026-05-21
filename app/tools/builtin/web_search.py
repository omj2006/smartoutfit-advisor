from __future__ import annotations

import httpx

from app.tools.base import BaseTool, register_tool


@register_tool
class WebSearchTool(BaseTool):
    name = "web_search"
    description = "搜索互联网获取信息。返回搜索结果摘要。"
    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "搜索关键词",
            },
            "num_results": {
                "type": "integer",
                "description": "返回结果数量，默认5",
                "default": 5,
            },
        },
        "required": ["query"],
    }

    async def execute(self, query: str = "", num_results: int = 5, **kwargs) -> str:
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(
                    "https://www.googleapis.com/customsearch/v1",
                    params={
                        "key": "",
                        "cx": "",
                        "q": query,
                        "num": min(num_results, 10),
                    },
                )
                if resp.status_code == 200:
                    data = resp.json()
                    items = data.get("items", [])
                    if not items:
                        return f"未找到关于 '{query}' 的搜索结果"
                    results = []
                    for i, item in enumerate(items, 1):
                        results.append(
                            f"{i}. {item.get('title', 'No Title')}\n"
                            f"   {item.get('snippet', '')}\n"
                            f"   URL: {item.get('link', '')}"
                        )
                    return "\n\n".join(results)
                else:
                    return self._fallback_search(query)
        except Exception:
            return self._fallback_search(query)

    def _fallback_search(self, query: str) -> str:
        return (
            f"网络搜索工具需要配置 Google Custom Search API 密钥。\n"
            f"搜索关键词: '{query}'\n"
            f"请在 config.yaml 或 .env 中配置搜索 API 密钥以启用此功能。\n"
            f"或者你可以通过注册自定义搜索工具来替换此实现。"
        )
