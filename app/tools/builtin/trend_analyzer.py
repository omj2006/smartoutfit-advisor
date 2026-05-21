from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus

import httpx

from app.tools.base import BaseTool, register_tool

logger = logging.getLogger(__name__)

TREND_SOURCES = {
    "vogue": {
        "name": "Vogue中国",
        "search_terms": ["vogue时尚趋势", "vogue潮流", "vogue穿搭"],
        "url_patterns": ["vogue.com.cn", "vogue.com"],
    },
    "elle": {
        "name": "ELLE中国",
        "search_terms": ["elle时尚趋势", "elle潮流穿搭"],
        "url_patterns": ["ellechina.com", "elle.com"],
    },
    "harpersbazaar": {
        "name": "时尚芭莎",
        "search_terms": ["时尚芭莎趋势", "芭莎潮流"],
        "url_patterns": ["harpersbazaar.com.cn"],
    },
    "gq": {
        "name": "GQ中国",
        "search_terms": ["GQ时尚趋势", "GQ男士穿搭"],
        "url_patterns": ["gq.com.cn"],
    },
    "xiaohongshu": {
        "name": "小红书",
        "search_terms": ["小红书穿搭趋势", "小红书流行穿搭"],
        "url_patterns": ["xiaohongshu.com"],
    },
    "weibo": {
        "name": "微博时尚",
        "search_terms": ["微博时尚趋势", "微博穿搭热搜"],
        "url_patterns": ["weibo.com"],
    },
}

SEASON_KEYWORDS = {
    "春": ["春季穿搭", "春装趋势", "早春流行"],
    "夏": ["夏季穿搭", "夏装趋势", "夏日流行"],
    "秋": ["秋季穿搭", "秋装趋势", "早秋流行"],
    "冬": ["冬季穿搭", "冬装趋势", "冬日流行"],
}

OCCASION_KEYWORDS = {
    "商务": ["职场穿搭趋势", "通勤时尚", "商务穿搭流行"],
    "约会": ["约会穿搭趋势", "约会时尚", "约会流行"],
    "休闲": ["休闲穿搭趋势", "日常时尚", "休闲流行"],
    "运动": ["运动穿搭趋势", "运动时尚", "athleisure趋势"],
    "正式": ["正式穿搭趋势", "晚宴时尚", "正装流行"],
}

STYLE_KEYWORDS = {
    "简约": ["极简主义穿搭", "minimalist fashion", "简约风趋势"],
    "街头": ["街头穿搭趋势", "streetwear", "街头风流行"],
    "复古": ["复古穿搭趋势", "vintage fashion", "复古风流行"],
    "优雅": ["优雅穿搭趋势", "elegant fashion", "优雅风流行"],
    "国潮": ["国潮穿搭", "国风时尚", "中国风趋势"],
}


def _extract_text_from_html(html: str) -> str:
    html = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", html)
    html = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", html)
    html = re.sub(r"<nav[^>]*>[\s\S]*?</nav>", "", html)
    html = re.sub(r"<footer[^>]*>[\s\S]*?</footer>", "", html)
    html = re.sub(r"<header[^>]*>[\s\S]*?</header>", "", html)
    html = re.sub(r"<[^>]+>", " ", html)
    html = re.sub(r"&nbsp;", " ", html)
    html = re.sub(r"&amp;", "&", html)
    html = re.sub(r"&lt;", "<", html)
    html = re.sub(r"&gt;", ">", html)
    html = re.sub(r"&quot;", '"', html)
    html = re.sub(r"&#\d+;", "", html)
    html = re.sub(r"\s+", " ", html)
    return html.strip()


def _extract_fashion_insights(text: str, max_length: int = 2000) -> str:
    fashion_keywords = [
        "趋势", "流行", "时尚", "穿搭", "潮流", "风格", "元素", "配色",
        "面料", "设计", "系列", "秀场", "品牌", "搭配", "单品", "造型",
        "色彩", "图案", "剪裁", "复古", "极简", "街头", "优雅", "运动",
        "trend", "fashion", "style", "outfit", "collection", "runway",
        "春夏", "秋冬", "早春", "早秋", "度假", "胶囊", "必备",
    ]

    sentences = re.split(r"[。！？\n.!?]", text)
    relevant = []
    for s in sentences:
        s = s.strip()
        if len(s) < 10:
            continue
        keyword_count = sum(1 for kw in fashion_keywords if kw.lower() in s.lower())
        if keyword_count >= 1:
            relevant.append((keyword_count, s))

    relevant.sort(key=lambda x: x[0], reverse=True)

    result = []
    total_len = 0
    for _, s in relevant:
        if total_len + len(s) > max_length:
            break
        result.append(s)
        total_len += len(s)

    return "。".join(result) if result else ""


async def _search_with_duckduckgo(query: str, max_results: int = 8) -> List[Dict[str, str]]:
    results = []
    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            resp = await client.get(
                "https://html.duckduckgo.com/html/",
                params={"q": query, "kl": "cn-zh"},
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                },
            )

            if resp.status_code != 200:
                return results

            html = resp.text

            link_pattern = re.compile(r'<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)</a>', re.DOTALL)
            snippet_pattern = re.compile(r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>', re.DOTALL)

            links = link_pattern.findall(html)
            snippets = snippet_pattern.findall(html)

            for i, (url, title) in enumerate(links[:max_results]):
                title = _extract_text_from_html(title).strip()
                snippet = _extract_text_from_html(snippets[i]).strip() if i < len(snippets) else ""
                if title and url:
                    results.append({"title": title, "url": url, "snippet": snippet})

    except Exception as e:
        logger.error(f"DuckDuckGo search failed: {e}")

    return results


async def _scrape_page(url: str) -> Optional[str]:
    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            resp = await client.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                },
            )

            if resp.status_code != 200:
                return None

            content_type = resp.headers.get("content-type", "")
            if "text/html" not in content_type and "text/plain" not in content_type:
                return None

            text = _extract_text_from_html(resp.text)
            insights = _extract_fashion_insights(text)
            return insights if insights else None

    except Exception as e:
        logger.error(f"Scraping {url} failed: {e}")
        return None


@register_tool
class TrendAnalyzerTool(BaseTool):
    name = "trend_analyzer"
    description = "分析当前时尚潮流趋势。通过搜索引擎和网页抓取获取最新的穿搭趋势、流行元素、热门风格等信息。支持按季节、场合、风格维度分析趋势。"
    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "趋势分析主题，如'2025春夏穿搭趋势'、'街头风格流行'、'职场穿搭趋势'",
            },
            "season": {
                "type": "string",
                "description": "季节：春/夏/秋/冬",
            },
            "occasion": {
                "type": "string",
                "description": "场合：商务/休闲/约会/运动/正式",
            },
            "style": {
                "type": "string",
                "description": "风格：简约/街头/复古/优雅/国潮",
            },
            "depth": {
                "type": "string",
                "description": "分析深度：quick(快速搜索) 或 deep(深度抓取)，默认quick",
                "default": "quick",
            },
        },
        "required": ["query"],
    }

    async def execute(
        self,
        query: str = "",
        season: str = "",
        occasion: str = "",
        style: str = "",
        depth: str = "quick",
        **kwargs,
    ) -> str:
        search_queries = self._build_search_queries(query, season, occasion, style)

        all_results = []
        for sq in search_queries[:3]:
            results = await _search_with_duckduckgo(sq, max_results=5)
            all_results.extend(results)

        seen_urls = set()
        unique_results = []
        for r in all_results:
            if r["url"] not in seen_urls:
                seen_urls.add(r["url"])
                unique_results.append(r)

        if not unique_results:
            return self._fallback_trend_analysis(query, season, occasion, style)

        trend_summary_parts = [
            f"📊 潮流趋势分析: {query}",
        ]

        if season:
            trend_summary_parts.append(f"季节: {season}")
        if occasion:
            trend_summary_parts.append(f"场合: {occasion}")
        if style:
            trend_summary_parts.append(f"风格: {style}")

        trend_summary_parts.append(f"\n🔍 搜索到 {len(unique_results)} 条相关资讯:\n")

        scraped_insights = []
        if depth == "deep":
            scrape_tasks = []
            for r in unique_results[:3]:
                url = r["url"]
                if any(d in url for d in ["vogue", "elle", "harpersbazaar", "gq", "xiaohongshu", "weibo", "zhihu", "bilibili"]):
                    scrape_tasks.append((r, url))

            for r, url in scrape_tasks:
                insights = await _scrape_page(url)
                if insights:
                    scraped_insights.append({"source": r["title"], "insights": insights})

        for i, r in enumerate(unique_results[:8], 1):
            trend_summary_parts.append(f"  {i}. {r['title']}")
            if r.get("snippet"):
                trend_summary_parts.append(f"     {r['snippet'][:120]}")
            trend_summary_parts.append(f"     🔗 {r['url']}")
            trend_summary_parts.append("")

        if scraped_insights:
            trend_summary_parts.append("\n📝 深度趋势解读:")
            for insight in scraped_insights:
                trend_summary_parts.append(f"\n--- {insight['source']} ---")
                trend_summary_parts.append(insight["insights"][:800])

        trend_summary_parts.append(self._generate_trend_summary(query, season, occasion, style, unique_results))

        return "\n".join(trend_summary_parts)

    def _build_search_queries(self, query: str, season: str, occasion: str, style: str) -> List[str]:
        queries = [query]

        year = "2025"
        base_query = f"{year} 穿搭趋势"

        if season and season in SEASON_KEYWORDS:
            for kw in SEASON_KEYWORDS[season][:2]:
                queries.append(f"{kw} {year}")

        if occasion and occasion in OCCASION_KEYWORDS:
            for kw in OCCASION_KEYWORDS[occasion][:2]:
                queries.append(kw)

        if style and style in STYLE_KEYWORDS:
            for kw in STYLE_KEYWORDS[style][:2]:
                queries.append(kw)

        queries.append(f"{base_query} 流行元素")
        queries.append(f"{base_query} 热门单品")

        return queries

    def _generate_trend_summary(
        self,
        query: str,
        season: str,
        occasion: str,
        style: str,
        search_results: List[Dict[str, str]],
    ) -> str:
        summary_parts = ["\n📈 趋势要点总结:"]

        all_text = " ".join(r.get("snippet", "") + " " + r.get("title", "") for r in search_results)

        trend_elements = []
        element_keywords = {
            "极简主义": ["极简", "简约", "minimalist", "less is more"],
            "复古回潮": ["复古", "vintage", "怀旧", "retro"],
            "运动休闲": ["运动", "athleisure", "休闲运动", "运动风"],
            "可持续时尚": ["可持续", "环保", "sustainable", "绿色"],
            "中性风": ["中性", "unisex", "无性别", "genderless"],
            "国潮崛起": ["国潮", "国风", "中国风", "新中式"],
            "大码时尚": ["大码", "包容", "diverse", "多元"],
            "科技面料": ["科技", "机能", "techwear", "功能性"],
            "撞色搭配": ["撞色", "color block", "对比色"],
            "层次叠穿": ["叠穿", "layering", "层次感"],
        }

        for element, keywords in element_keywords.items():
            count = sum(1 for kw in keywords if kw.lower() in all_text.lower())
            if count > 0:
                trend_elements.append((count, element))

        trend_elements.sort(key=lambda x: x[0], reverse=True)

        if trend_elements:
            summary_parts.append("🔥 热门趋势方向:")
            for count, element in trend_elements[:5]:
                bars = "█" * min(count * 2, 10)
                summary_parts.append(f"  {bars} {element}")
        else:
            summary_parts.append("  基于搜索结果，建议关注当前季节的主流穿搭风格")

        if season:
            season_tips = {
                "春": "早春建议关注轻薄外套+叠穿组合，色彩以柔和暖色调为主",
                "夏": "夏季趋势偏向透气面料和清爽配色，防晒单品是重点",
                "秋": "秋季流行层次穿搭，大地色系和格纹元素是经典选择",
                "冬": "冬季注重保暖与时尚兼顾，功能性外套和配饰是关键",
            }
            if season in season_tips:
                summary_parts.append(f"\n🍂 {season}季穿搭建议: {season_tips[season]}")

        if occasion:
            occasion_tips = {
                "商务": "职场趋势偏向smart casual，告别刻板正装，融入时尚元素",
                "约会": "约会穿搭趋势强调个性表达，精致但不刻意",
                "休闲": "休闲风趋势注重舒适与时尚的平衡，基础款+亮点单品",
                "运动": "运动时尚趋势是athleisure风格，运动单品日常化",
                "正式": "正式场合趋势更注重细节和质感，简约但不简单",
            }
            if occasion in occasion_tips:
                summary_parts.append(f"\n👔 {occasion}场合趋势: {occasion_tips[occasion]}")

        return "\n".join(summary_parts)

    def _fallback_trend_analysis(self, query: str, season: str, occasion: str, style: str) -> str:
        parts = [
            f"📊 潮流趋势分析: {query}",
            "",
            "⚠️ 搜索引擎暂时不可用，以下为内置趋势参考：",
            "",
            "🔥 2025年核心趋势方向:",
            "  ██████ 极简主义 — Less is more，回归本质",
            "  █████  复古回潮 — 90年代风格强势回归",
            "  ████   运动休闲 — Athleisure持续流行",
            "  ████   国潮崛起 — 新中式风格成为新宠",
            "  ███    可持续时尚 — 环保面料和二手时尚",
            "",
            "🎨 2025流行色彩:",
            "  · 柔和粉彩色系 — 薰衣草紫、薄荷绿、奶油白",
            "  · 大地色系 — 驼色、焦糖色、橄榄绿",
            "  · 金属色 — 银色回归，未来感十足",
            "",
            "👗 关键单品:",
            "  · Oversize西装外套 — 通勤休闲两相宜",
            "  · 阔腿裤 — 舒适与时尚并存",
            "  · 针织连衣裙 — 优雅慵懒风",
            "  · 功能性冲锋衣 — 户外时尚化",
            "  · 乐福鞋 — 百搭鞋款回归",
        ]

        if season:
            season_data = {
                "春": "\n\n🌸 春季特别趋势:\n  · 薄风衣+针织内搭\n  · 碎花元素回归\n  · 浅色系为主，薄荷绿/薰衣草紫",
                "夏": "\n\n☀️ 夏季特别趋势:\n  · 防晒时尚化 — 防晒衣也能很时髦\n  · 清凉面料 — 亚麻、真丝、棉麻\n  · 亮色系 — 橙色、电光蓝",
                "秋": "\n\n🍂 秋季特别趋势:\n  · 层次叠穿 — 衬衫+针织+外套\n  · 格纹元素 — 经典英伦风\n  · 大地色系 — 驼色、焦糖、酒红",
                "冬": "\n\n❄️ 冬季特别趋势:\n  · 功能性保暖 — 科技面料羽绒服\n  · 配饰升级 — 围巾/帽子成焦点\n  · 深色系+亮色点缀",
            }
            if season in season_data:
                parts.append(season_data[season])

        return "\n".join(parts)
