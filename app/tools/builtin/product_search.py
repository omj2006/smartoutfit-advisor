from __future__ import annotations

import math
import os
from typing import Any, Dict, List, Optional, Tuple

from app.tools.base import BaseTool, register_tool
from app.tools.builtin.product_db import (
    SEED_PRODUCTS,
    get_all_products,
    get_categories,
    init_db,
    query_products,
)


class VectorSearchEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._index = None
            cls._instance._idf = None
            cls._instance._doc_vectors = None
            cls._instance._docs = None
        return cls._instance

    def _tokenize(self, text: str) -> List[str]:
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

    def _compute_tf(self, tokens: List[str]) -> Dict[str, float]:
        tf = {}
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1
        total = len(tokens)
        if total > 0:
            for k in tf:
                tf[k] /= total
        return tf

    def _cosine_similarity(self, v1: Dict[str, float], v2: Dict[str, float]) -> float:
        all_keys = set(v1.keys()) | set(v2.keys())
        dot = sum(v1.get(k, 0) * v2.get(k, 0) for k in all_keys)
        norm1 = math.sqrt(sum(v ** 2 for v in v1.values()))
        norm2 = math.sqrt(sum(v ** 2 for v in v2.values()))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def build_index(self, docs: List[Dict[str, Any]]):
        self._docs = docs
        doc_freq = {}
        total_docs = len(docs)

        tokenized_docs = []
        for doc in docs:
            search_text = doc.get("search_vector", "")
            if not search_text:
                search_text = f"{doc.get('name', '')} {doc.get('category', '')} {doc.get('subcategory', '')} {doc.get('brand', '')} {doc.get('color', '')} {doc.get('description', '')} {doc.get('season', '')} {doc.get('occasion', '')} {doc.get('style', '')} {doc.get('material', '')}"
            tokens = self._tokenize(search_text)
            tokenized_docs.append(tokens)
            unique_tokens = set(tokens)
            for t in unique_tokens:
                doc_freq[t] = doc_freq.get(t, 0) + 1

        self._idf = {}
        for term, freq in doc_freq.items():
            self._idf[term] = math.log((total_docs + 1) / (freq + 1)) + 1

        self._doc_vectors = []
        for tokens in tokenized_docs:
            tf = self._compute_tf(tokens)
            tfidf = {}
            for term, tf_val in tf.items():
                tfidf[term] = tf_val * self._idf.get(term, 1.0)
            self._doc_vectors.append(tfidf)

    def search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        min_score: float = 0.01,
    ) -> List[Tuple[float, Dict[str, Any]]]:
        if self._docs is None or self._doc_vectors is None:
            return []

        query_tokens = self._tokenize(query)
        query_tf = self._compute_tf(query_tokens)
        query_vector = {}
        for term, tf_val in query_tf.items():
            query_vector[term] = tf_val * self._idf.get(term, 1.0)

        scored = []
        for idx, doc_vector in enumerate(self._doc_vectors):
            if filters and not self._match_filters(self._docs[idx], filters):
                continue
            score = self._cosine_similarity(query_vector, doc_vector)
            if score >= min_score:
                scored.append((score, self._docs[idx]))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:top_k]

    def _match_filters(self, doc: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        for key, value in filters.items():
            if value is None:
                continue
            doc_val = doc.get(key, "")
            if isinstance(doc_val, str):
                if key in ("season", "occasion", "style"):
                    if value.lower() not in doc_val.lower():
                        return False
                elif key == "gender":
                    if doc_val != value and doc_val != "男女通用":
                        return False
                else:
                    if doc_val.lower() != value.lower():
                        return False
        return True


_engine: Optional[VectorSearchEngine] = None


def get_search_engine() -> VectorSearchEngine:
    global _engine
    if _engine is None:
        init_db()
        _engine = VectorSearchEngine()
        products = get_all_products()
        _engine.build_index(products)
    return _engine


@register_tool
class ProductSearchTool(BaseTool):
    name = "product_search"
    description = "从商品库中搜索匹配的穿搭单品。支持语义搜索（用自然语言描述想要的商品）和结构化筛选（按类别、颜色、季节、场合、风格、价格等）。返回匹配商品的名称、品牌、价格、颜色、适用场景等信息。"
    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "搜索描述，如'适合雨天约会的连衣裙'、'冬季保暖外套'、'商务通勤皮鞋'",
            },
            "category": {
                "type": "string",
                "description": "商品类别：上装、下装、连衣裙、鞋履、配饰",
            },
            "color_family": {
                "type": "string",
                "description": "色系：浅色、深色、暖色、中性色",
            },
            "season": {
                "type": "string",
                "description": "季节：春、夏、秋、冬",
            },
            "occasion": {
                "type": "string",
                "description": "场合：商务、休闲、约会、运动、正式、户外",
            },
            "style": {
                "type": "string",
                "description": "风格：简约、休闲、优雅、通勤、街头、运动、户外、文艺、经典、性感、浪漫、酷感",
            },
            "gender": {
                "type": "string",
                "description": "性别：男、女",
            },
            "max_price": {
                "type": "number",
                "description": "最高价格",
            },
            "top_k": {
                "type": "integer",
                "description": "返回结果数量，默认5",
                "default": 5,
            },
        },
        "required": ["query"],
    }

    async def execute(
        self,
        query: str = "",
        category: Optional[str] = None,
        color_family: Optional[str] = None,
        season: Optional[str] = None,
        occasion: Optional[str] = None,
        style: Optional[str] = None,
        gender: Optional[str] = None,
        max_price: Optional[float] = None,
        top_k: int = 5,
        **kwargs,
    ) -> str:
        engine = get_search_engine()

        filters = {}
        if category:
            filters["category"] = category
        if color_family:
            filters["color_family"] = color_family
        if season:
            filters["season"] = season
        if occasion:
            filters["occasion"] = occasion
        if style:
            filters["style"] = style
        if gender:
            filters["gender"] = gender

        vector_results = engine.search(
            query=query,
            top_k=top_k * 2,
            filters=filters if filters else None,
        )

        results = []
        seen_ids = set()
        for score, product in vector_results:
            if max_price and product.get("price", 0) > max_price:
                continue
            if product["id"] not in seen_ids:
                seen_ids.add(product["id"])
                results.append((score, product))

        if len(results) < top_k:
            db_results = query_products(
                category=category,
                color_family=color_family,
                season=season,
                occasion=occasion,
                style=style,
                gender=gender,
                max_price=max_price,
                limit=top_k,
            )
            for product in db_results:
                if product["id"] not in seen_ids:
                    seen_ids.add(product["id"])
                    results.append((0.0, product))

        results = results[:top_k]

        if not results:
            return f"未找到与 '{query}' 匹配的商品。试试调整搜索条件。"

        output_parts = [f"🔍 搜索: {query}\n📦 找到 {len(results)} 件匹配商品:\n"]

        for i, (score, product) in enumerate(results, 1):
            match_indicator = f"(匹配度: {score:.0%})" if score > 0 else ""
            parts = [
                f"  {i}. {product['name']} {match_indicator}",
                f"     品牌: {product.get('brand', 'N/A')} | 价格: ¥{product.get('price', 'N/A')}",
                f"     颜色: {product.get('color', 'N/A')} | 材质: {product.get('material', 'N/A')}",
                f"     季节: {product.get('season', 'N/A')} | 场合: {product.get('occasion', 'N/A')}",
                f"     风格: {product.get('style', 'N/A')}",
                f"     {product.get('description', '')}",
            ]
            output_parts.append("\n".join(parts))

        return "\n\n".join(output_parts)
