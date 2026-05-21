from __future__ import annotations

import json
import math
import os
from typing import Any, Dict, List

from app.tools.base import BaseTool, register_tool

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "outfit_kb")
KNOWLEDGE_DIR = os.path.abspath(KNOWLEDGE_DIR)


OUTFIT_KNOWLEDGE = [
    {
        "id": "temp_hot",
        "category": "温度穿搭",
        "condition": "温度 >= 30°C",
        "temperature_range": [30, 50],
        "title": "高温天气穿搭指南",
        "advice": "选择轻薄透气的面料，如棉麻、真丝、雪纺。颜色以浅色系为主（白色、浅蓝、浅粉），避免深色吸热。上衣可选短袖T恤、吊带、背心；下装选短裤、短裙、阔腿裤。配饰搭配遮阳帽、墨镜、防晒衣。",
        "items": ["棉麻短袖", "吊带背心", "短裤", "凉鞋", "遮阳帽", "墨镜", "防晒衣"],
        "style_tips": "高温天穿搭以清凉为主，可适当露肤但注意防晒。选择A字版型的下装更透气。",
    },
    {
        "id": "temp_warm",
        "category": "温度穿搭",
        "condition": "25°C <= 温度 < 30°C",
        "temperature_range": [25, 30],
        "title": "温暖天气穿搭指南",
        "advice": "适合穿短袖搭配薄外套或开衫，方便早晚温差调节。面料选择棉质、亚麻等透气材质。可以尝试层次穿搭，内搭短袖外搭薄款衬衫或针织开衫。",
        "items": ["短袖T恤", "薄款衬衫", "针织开衫", "九分裤", "休闲鞋", "帆布鞋"],
        "style_tips": "温暖天气是层次穿搭的好时机，薄外套既实用又增添时尚感。",
    },
    {
        "id": "temp_mild",
        "category": "温度穿搭",
        "condition": "18°C <= 温度 < 25°C",
        "temperature_range": [18, 25],
        "title": "舒适天气穿搭指南",
        "advice": "最舒适的穿搭温度，长袖薄衫、卫衣、牛仔外套都是好选择。可穿长裤或中长裙。这个温度适合各种风格尝试，休闲、商务休闲、轻复古都可以。",
        "items": ["长袖衬衫", "卫衣", "牛仔外套", "风衣", "直筒裤", "乐福鞋"],
        "style_tips": "舒适温度最适合叠穿，衬衫+针织马甲、T恤+牛仔外套都是经典组合。",
    },
    {
        "id": "temp_cool",
        "category": "温度穿搭",
        "condition": "10°C <= 温度 < 18°C",
        "temperature_range": [10, 18],
        "title": "凉爽天气穿搭指南",
        "advice": "需要外套了，推荐针织衫、夹克、薄款大衣。内搭可选择长袖T恤、衬衫加薄毛衣。下装选长裤、牛仔裤。注意早晚温差，可随身携带围巾。",
        "items": ["针织衫", "夹克", "薄大衣", "长袖T恤", "牛仔裤", "围巾", "短靴"],
        "style_tips": "凉爽天气穿搭注重层次感，内搭+中间层+外套的三层穿法既保暖又时尚。",
    },
    {
        "id": "temp_cold",
        "category": "温度穿搭",
        "condition": "0°C <= 温度 < 10°C",
        "temperature_range": [0, 10],
        "title": "寒冷天气穿搭指南",
        "advice": "需要厚外套，如羽绒服、呢大衣、棉服。内搭穿保暖内衣+毛衣。注意保暖重点部位：脖子（围巾）、手（手套）、脚（厚袜+保暖鞋）。颜色可选暖色系增加视觉温暖感。",
        "items": ["羽绒服", "呢大衣", "毛衣", "保暖内衣", "围巾", "手套", "雪地靴"],
        "style_tips": "寒冷天气穿搭要注重保暖与时尚的平衡，选择有设计感的外套是关键。腰带可以勾勒腰线避免臃肿。",
    },
    {
        "id": "temp_freezing",
        "category": "温度穿搭",
        "condition": "温度 < 0°C",
        "temperature_range": [-50, 0],
        "title": "极寒天气穿搭指南",
        "advice": "必须全副武装！长款羽绒服、加厚保暖内衣、毛线帽、围巾、手套缺一不可。选择防风面料，注意四肢末端保暖。叠穿是关键：保暖层+隔热层+防风层。",
        "items": ["长款羽绒服", "加厚保暖内衣", "毛线帽", "厚围巾", "皮手套", "加绒靴"],
        "style_tips": "极寒天气安全第一，选择功能性强的保暖单品，再考虑搭配。",
    },
    {
        "id": "rain_rainy",
        "category": "雨天穿搭",
        "condition": "下雨",
        "title": "雨天穿搭指南",
        "advice": "选择防水面料或深色衣物（不易显水渍）。穿雨衣或带防水涂层的夹克。鞋子选防水靴或雨鞋，避免穿布鞋和浅色鞋。裤子选九分裤或卷起裤脚，避免裤腿沾湿。带一把结实的伞。",
        "items": ["防水夹克", "雨衣", "防水靴", "九分裤", "结实的伞", "防水包"],
        "style_tips": "雨天也可以很时尚，选择透明雨伞+亮色雨衣可以拍出很美的照片。",
    },
    {
        "id": "rain_snowy",
        "category": "雪天穿搭",
        "condition": "下雪",
        "title": "雪天穿搭指南",
        "advice": "保暖+防滑是关键。穿厚羽绒服、防水雪地靴、毛线帽、手套。裤子选加绒款或穿保暖内衣裤。注意路面湿滑，选防滑底的鞋子。深色衣物在雪景中更出片。",
        "items": ["厚羽绒服", "雪地靴", "毛线帽", "皮手套", "加绒裤", "围巾"],
        "style_tips": "雪天穿搭红色单品特别出片，红色围巾或红色大衣在白雪中非常亮眼。",
    },
    {
        "id": "occasion_work",
        "category": "场合穿搭",
        "condition": "上班/商务场合",
        "title": "商务通勤穿搭指南",
        "advice": "商务场合注重专业感。男士：西装/衬衫+西裤+皮鞋；女士：西装外套+衬衫+半裙/西裤+中跟鞋。颜色以黑、灰、藏青、米色为主。避免过于花哨的图案和鲜艳颜色。",
        "items": ["西装", "衬衫", "西裤", "皮鞋/中跟鞋", "公文包", "手表"],
        "style_tips": "商务穿搭讲究合身度，衣服的版型比品牌更重要。一条好皮带能提升整体质感。",
    },
    {
        "id": "occasion_date",
        "category": "场合穿搭",
        "condition": "约会/社交场合",
        "title": "约会社交穿搭指南",
        "advice": "约会穿搭要展现个人魅力又不过于刻意。男士：干净整洁的衬衫/针织衫+休闲裤+干净鞋子；女士：连衣裙/半裙+精致上衣+小高跟。适当使用香水，注意细节（指甲、发型）。",
        "items": ["精致衬衫", "连衣裙", "小高跟鞋", "精致配饰", "香水", "小包"],
        "style_tips": "约会穿搭的关键是'精心但不像精心'，一件亮点单品+基础款组合最有效。",
    },
    {
        "id": "occasion_casual",
        "category": "场合穿搭",
        "condition": "休闲/日常场合",
        "title": "休闲日常穿搭指南",
        "advice": "休闲场合以舒适为主。T恤+牛仔裤+运动鞋是最经典的组合。可以加入棒球帽、帆布包等休闲配饰。颜色搭配可以大胆一些，尝试撞色或同色系搭配。",
        "items": ["T恤", "牛仔裤", "运动鞋", "棒球帽", "帆布包", "卫衣"],
        "style_tips": "休闲穿搭最容易出彩的方式是：全身基础款+一件设计感单品。",
    },
    {
        "id": "occasion_sport",
        "category": "场合穿搭",
        "condition": "运动/户外场合",
        "title": "运动户外穿搭指南",
        "advice": "运动穿搭注重功能性。选择速干面料、弹性好的运动服。跑步：速干T恤+运动短裤/紧身裤+跑鞋；健身：运动背心/速干衣+运动裤+训练鞋；户外：冲锋衣+抓绒内搭+登山鞋。",
        "items": ["速干T恤", "运动裤", "跑鞋/训练鞋", "运动袜", "运动内衣", "水壶"],
        "style_tips": "运动穿搭也可以很时尚，选择有设计感的运动品牌，颜色搭配协调即可。",
    },
    {
        "id": "occasion_formal",
        "category": "场合穿搭",
        "condition": "正式/晚宴场合",
        "title": "正式晚宴穿搭指南",
        "advice": "正式场合需要正装出席。男士：深色西装+领带+皮鞋；女士：晚礼服/小黑裙+高跟鞋+精致首饰。注意着装礼仪，避免过于暴露或休闲。",
        "items": ["晚礼服/西装", "高跟鞋/皮鞋", "精致首饰", "手拿包", "领带/丝巾"],
        "style_tips": "正式场合穿搭讲究质感，选择面料好的单品，细节决定品味。",
    },
    {
        "id": "color_matching",
        "category": "色彩搭配",
        "condition": "通用",
        "title": "色彩搭配基础原则",
        "advice": "1.全身颜色不超过3种主色；2.同色系搭配高级感强；3.黑白灰是万能基础色；4.暖肤色适合暖色调（橘、驼、棕）；5.冷肤色适合冷色调（蓝、紫、灰）；6.撞色搭配要控制面积比例（7:2:1）。",
        "items": [],
        "style_tips": "不确定颜色搭配时，同色系不同深浅是最安全的选择。",
    },
    {
        "id": "body_type",
        "category": "体型穿搭",
        "condition": "通用",
        "title": "不同体型穿搭建议",
        "advice": "梨形身材：上身浅色/亮色+下身深色/A字裙；苹果形身材：V领/开衫+高腰下装；矩形身材：腰带/层次穿搭创造曲线；倒三角身材：上身简约+下身有设计感；沙漏形身材：突出腰线，选择收腰款式。",
        "items": [],
        "style_tips": "了解自己的体型是穿搭的第一步，扬长避短比盲目追潮流更重要。",
    },
]


def _simple_tokenize(text: str) -> List[str]:
    result = []
    word = ""
    for ch in text.lower():
        if "\u4e00" <= ch <= "\u9fff":
            if word:
                result.append(word)
                word = ""
            result.append(ch)
        elif ch.isalnum():
            word += ch
        else:
            if word:
                result.append(word)
                word = ""
    if word:
        result.append(word)
    return result


def _compute_tf(tokens: List[str]) -> Dict[str, float]:
    tf = {}
    for t in tokens:
        tf[t] = tf.get(t, 0) + 1
    total = len(tokens)
    if total > 0:
        for k in tf:
            tf[k] /= total
    return tf


def _cosine_similarity(v1: Dict[str, float], v2: Dict[str, float]) -> float:
    all_keys = set(v1.keys()) | set(v2.keys())
    dot = sum(v1.get(k, 0) * v2.get(k, 0) for k in all_keys)
    norm1 = math.sqrt(sum(v ** 2 for v in v1.values()))
    norm2 = math.sqrt(sum(v ** 2 for v in v2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


@register_tool
class KnowledgeBaseTool(BaseTool):
    name = "knowledge_base"
    description = "检索穿搭知识库。根据关键词搜索穿搭建议、搭配技巧、色彩搭配、体型穿搭等知识。支持按温度、场合、风格等条件检索。"
    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "搜索关键词，如'高温穿搭'、'商务场合'、'色彩搭配'、'雨天'",
            },
            "temperature": {
                "type": "number",
                "description": "当前温度（摄氏度），用于匹配温度相关的穿搭建议",
            },
            "top_k": {
                "type": "integer",
                "description": "返回最相关的K条结果，默认3",
                "default": 3,
            },
        },
        "required": ["query"],
    }

    def _search(self, query: str, temperature: float = None, top_k: int = 3) -> List[Dict[str, Any]]:
        query_tokens = _simple_tokenize(query)
        query_tf = _compute_tf(query_tokens)

        scored = []
        for entry in OUTFIT_KNOWLEDGE:
            score = 0.0

            searchable_text = f"{entry['category']} {entry['condition']} {entry['title']} {entry['advice']} {' '.join(entry.get('items', []))} {entry.get('style_tips', '')}"
            entry_tokens = _simple_tokenize(searchable_text)
            entry_tf = _compute_tf(entry_tokens)

            score = _cosine_similarity(query_tf, entry_tf)

            if temperature is not None:
                temp_range = entry.get("temperature_range")
                if temp_range and temp_range[0] <= temperature <= temp_range[1]:
                    score += 0.5

            keyword_match = 0
            query_lower = query.lower()
            for field in ["category", "condition", "title"]:
                if any(kw in entry.get(field, "").lower() for kw in query_lower.split()):
                    keyword_match += 1
            score += keyword_match * 0.3

            scored.append((score, entry))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [entry for score, entry in scored[:top_k] if score > 0]

    async def execute(self, query: str = "", temperature: float = None, top_k: int = 3, **kwargs) -> str:
        results = self._search(query, temperature, top_k)

        if not results:
            return f"未找到与 '{query}' 相关的穿搭知识。试试搜索：温度穿搭、商务场合、雨天穿搭、色彩搭配等。"

        output_parts = []
        for i, entry in enumerate(results, 1):
            parts = [
                f"【{i}】{entry['title']}",
                f"适用条件: {entry['condition']}",
                f"建议: {entry['advice']}",
            ]
            if entry.get("items"):
                parts.append(f"推荐单品: {', '.join(entry['items'])}")
            if entry.get("style_tips"):
                parts.append(f"搭配技巧: {entry['style_tips']}")
            output_parts.append("\n".join(parts))

        return "\n\n---\n\n".join(output_parts)
