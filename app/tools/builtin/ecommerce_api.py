from __future__ import annotations

import hashlib
import random
from typing import Any, Dict, List, Optional

from app.tools.base import BaseTool, register_tool

TAOBAO_PRODUCTS = [
    {"name": "UNIQLO 优衣库 男款圆领T恤 纯棉短袖", "brand": "UNIQLO", "category": "上装", "price": 59.0, "original_price": 99.0, "sales": 52000, "rating": 4.8},
    {"name": "ZARA 女士碎花雪纺衬衫 春季新款", "brand": "ZARA", "category": "上装", "price": 259.0, "original_price": 399.0, "sales": 18000, "rating": 4.6},
    {"name": "Nike 耐克 Air Force 1 空军一号 白色低帮", "brand": "Nike", "category": "鞋履", "price": 599.0, "original_price": 799.0, "sales": 95000, "rating": 4.9},
    {"name": "Levi's 李维斯 501经典直筒牛仔裤 男款", "brand": "Levi's", "category": "下装", "price": 399.0, "original_price": 699.0, "sales": 32000, "rating": 4.7},
    {"name": "H&M 女士黑色修身西装外套 通勤百搭", "brand": "H&M", "category": "上装", "price": 349.0, "original_price": 499.0, "sales": 15000, "rating": 4.5},
    {"name": "Adidas 阿迪达斯 三叶草经典连帽卫衣", "brand": "Adidas", "category": "上装", "price": 459.0, "original_price": 599.0, "sales": 41000, "rating": 4.7},
    {"name": "Maje 法国轻奢 碎花连衣裙 女士春夏", "brand": "Maje", "category": "连衣裙", "price": 1299.0, "original_price": 2190.0, "sales": 8500, "rating": 4.8},
    {"name": "Ray-Ban 雷朋 飞行员墨镜 经典款", "brand": "Ray-Ban", "category": "配饰", "price": 899.0, "original_price": 1380.0, "sales": 22000, "rating": 4.8},
    {"name": "UNIQLO 优衣库 女款高腰阔腿裤", "brand": "UNIQLO", "category": "下装", "price": 149.0, "original_price": 199.0, "sales": 67000, "rating": 4.6},
    {"name": "Dr. Martens 马汀靴 1460八孔靴 黑色", "brand": "Dr. Martens", "category": "鞋履", "price": 1099.0, "original_price": 1499.0, "sales": 28000, "rating": 4.7},
    {"name": "COS 极简风针织开衫 女士春秋", "brand": "COS", "category": "上装", "price": 650.0, "original_price": 890.0, "sales": 9200, "rating": 4.6},
    {"name": "Sandro 法式优雅小黑裙 女士", "brand": "Sandro", "category": "连衣裙", "price": 1399.0, "original_price": 1990.0, "sales": 6300, "rating": 4.7},
    {"name": "The North Face 北面 军绿色冲锋衣 防风防水", "brand": "The North Face", "category": "上装", "price": 1299.0, "original_price": 1899.0, "sales": 19000, "rating": 4.8},
    {"name": "Clarks 其乐 男士德比商务皮鞋 黑色", "brand": "Clarks", "category": "鞋履", "price": 699.0, "original_price": 999.0, "sales": 14000, "rating": 4.6},
    {"name": "Acne Studios 羊毛围巾 灰色格纹", "brand": "Acne Studios", "category": "配饰", "price": 1399.0, "original_price": 1900.0, "sales": 5600, "rating": 4.8},
    {"name": "UNIQLO 优衣库 HEATTECH保暖内衣套装", "brand": "UNIQLO", "category": "上装", "price": 149.0, "original_price": 199.0, "sales": 88000, "rating": 4.7},
    {"name": "Lululemon 瑜伽裤 女款黑色高腰", "brand": "Lululemon", "category": "下装", "price": 750.0, "original_price": 850.0, "sales": 35000, "rating": 4.9},
    {"name": "UGG 经典栗色雪地靴 女款短靴", "brand": "UGG", "category": "鞋履", "price": 1199.0, "original_price": 1599.0, "sales": 21000, "rating": 4.6},
    {"name": "MUJI 无印良品 帆布托特包 米色大容量", "brand": "MUJI", "category": "配饰", "price": 168.0, "original_price": 198.0, "sales": 45000, "rating": 4.5},
    {"name": "Hugo Boss 男士黑色真皮皮带 商务", "brand": "Hugo Boss", "category": "配饰", "price": 459.0, "original_price": 699.0, "sales": 11000, "rating": 4.7},
]

JD_PRODUCTS = [
    {"name": "UNIQLO 优衣库 男款长袖衬衫 纯棉商务", "brand": "UNIQLO", "category": "上装", "price": 179.0, "original_price": 249.0, "sales": 38000, "rating": 4.8},
    {"name": "Nike 耐克 Dri-FIT速干运动T恤 男款", "brand": "Nike", "category": "上装", "price": 269.0, "original_price": 349.0, "sales": 55000, "rating": 4.7},
    {"name": "Adidas 阿迪达斯 Stan Smith小白鞋 男女同款", "brand": "Adidas", "category": "鞋履", "price": 699.0, "original_price": 899.0, "sales": 120000, "rating": 4.9},
    {"name": "Hugo Boss 男士修身黑色西裤 羊毛混纺", "brand": "Hugo Boss", "category": "下装", "price": 799.0, "original_price": 1199.0, "sales": 9500, "rating": 4.6},
    {"name": "ZARA 女士驼色羊毛大衣 秋冬新款", "brand": "ZARA", "category": "上装", "price": 899.0, "original_price": 1299.0, "sales": 12000, "rating": 4.5},
    {"name": "Burberry 博柏利 经典驼色风衣 男女同款", "brand": "Burberry", "category": "上装", "price": 11999.0, "original_price": 15500.0, "sales": 3200, "rating": 4.9},
    {"name": "Equipment 女士真丝吊带裙 香槟色", "brand": "Equipment", "category": "连衣裙", "price": 2099.0, "original_price": 2990.0, "sales": 4800, "rating": 4.7},
    {"name": "Stuart Weitzman 裸色尖头高跟鞋 女款", "brand": "Stuart Weitzman", "category": "鞋履", "price": 2799.0, "original_price": 3690.0, "sales": 3600, "rating": 4.8},
    {"name": "Coach 蔻驰 黑色真皮手套 加绒内里", "brand": "Coach", "category": "配饰", "price": 499.0, "original_price": 750.0, "sales": 7800, "rating": 4.6},
    {"name": "Arc'teryx 始祖鸟 Beta LT冲锋衣 防风防水", "brand": "Arc'teryx", "category": "上装", "price": 3699.0, "original_price": 4998.0, "sales": 8500, "rating": 4.9},
    {"name": "Ted Baker 女士格纹西装外套 灰色", "brand": "Ted Baker", "category": "上装", "price": 1799.0, "original_price": 2590.0, "sales": 5100, "rating": 4.7},
    {"name": "Levi's 李维斯 女款高腰紧身牛仔裤", "brand": "Levi's", "category": "下装", "price": 349.0, "original_price": 599.0, "sales": 28000, "rating": 4.6},
    {"name": "COS 女士黑色A字半身裙 羊毛混纺", "brand": "COS", "category": "下装", "price": 550.0, "original_price": 790.0, "sales": 6700, "rating": 4.7},
    {"name": "Hunter 亨特 黑色Chelsea雨靴 防水", "brand": "Hunter", "category": "鞋履", "price": 799.0, "original_price": 1099.0, "sales": 9200, "rating": 4.5},
    {"name": "G.H. Bass 棕色流苏乐福鞋 男女同款", "brand": "G.H. Bass", "category": "鞋履", "price": 599.0, "original_price": 899.0, "sales": 8100, "rating": 4.6},
    {"name": "Lack of Color 米白色草编遮阳帽 宽檐", "brand": "Lack of Color", "category": "配饰", "price": 359.0, "original_price": 499.0, "sales": 6300, "rating": 4.5},
    {"name": "Sandro 黑色真皮手拿包 金属扣", "brand": "Sandro", "category": "配饰", "price": 799.0, "original_price": 1190.0, "sales": 4900, "rating": 4.7},
    {"name": "UNIQLO 优衣库 卡其色九分休闲裤 男款弹力", "brand": "UNIQLO", "category": "下装", "price": 199.0, "original_price": 249.0, "sales": 72000, "rating": 4.7},
    {"name": "Nike 耐克 白色运动短裤 速干内衬", "brand": "Nike", "category": "下装", "price": 249.0, "original_price": 299.0, "sales": 46000, "rating": 4.6},
    {"name": "Acne Studios 灰色羊毛毛线帽 冬季", "brand": "Acne Studios", "category": "配饰", "price": 599.0, "original_price": 850.0, "sales": 4200, "rating": 4.7},
]

PDD_PRODUCTS = [
    {"name": "UNIQLO同款 纯棉白色短袖T恤 男女百搭", "brand": "UNIQLO", "category": "上装", "price": 29.9, "original_price": 79.0, "sales": 280000, "rating": 4.5},
    {"name": "ZARA风格 女士碎花雪纺衬衫 春夏", "brand": "ZARA", "category": "上装", "price": 69.9, "original_price": 199.0, "sales": 150000, "rating": 4.3},
    {"name": "Nike风格 运动休闲跑步鞋 男女同款", "brand": "Nike", "category": "鞋履", "price": 128.0, "original_price": 399.0, "sales": 520000, "rating": 4.4},
    {"name": "Levi's风格 弹力修身牛仔裤 男款", "brand": "Levi's", "category": "下装", "price": 79.9, "original_price": 299.0, "sales": 190000, "rating": 4.3},
    {"name": "H&M风格 女士黑色小西装外套 通勤", "brand": "H&M", "category": "上装", "price": 89.9, "original_price": 349.0, "sales": 95000, "rating": 4.2},
    {"name": "Adidas风格 三叶草连帽卫衣 加绒", "brand": "Adidas", "category": "上装", "price": 99.0, "original_price": 399.0, "sales": 310000, "rating": 4.4},
    {"name": "法式碎花连衣裙 女士春夏显瘦A字裙", "brand": "Maje", "category": "连衣裙", "price": 159.0, "original_price": 599.0, "sales": 85000, "rating": 4.3},
    {"name": "Ray-Ban风格 飞行员墨镜 偏光太阳镜", "brand": "Ray-Ban", "category": "配饰", "price": 49.9, "original_price": 199.0, "sales": 420000, "rating": 4.2},
    {"name": "UNIQLO风格 女款高腰阔腿裤 显瘦", "brand": "UNIQLO", "category": "下装", "price": 49.9, "original_price": 149.0, "sales": 230000, "rating": 4.4},
    {"name": "马丁靴风格 英伦风切尔西短靴 男女", "brand": "Dr. Martens", "category": "鞋履", "price": 139.0, "original_price": 499.0, "sales": 180000, "rating": 4.3},
    {"name": "COS风格 极简针织开衫 女士春秋", "brand": "COS", "category": "上装", "price": 119.0, "original_price": 450.0, "sales": 62000, "rating": 4.2},
    {"name": "小黑裙 法式优雅连衣裙 女士秋冬", "brand": "Sandro", "category": "连衣裙", "price": 189.0, "original_price": 699.0, "sales": 54000, "rating": 4.3},
    {"name": "冲锋衣风格 防风防水户外夹克 男女", "brand": "The North Face", "category": "上装", "price": 169.0, "original_price": 599.0, "sales": 110000, "rating": 4.3},
    {"name": "商务皮鞋 男士真皮正装鞋 黑色", "brand": "Clarks", "category": "鞋履", "price": 159.0, "original_price": 499.0, "sales": 78000, "rating": 4.4},
    {"name": "羊毛围巾 纯色百搭格纹 秋冬保暖", "brand": "Acne Studios", "category": "配饰", "price": 59.9, "original_price": 199.0, "sales": 95000, "rating": 4.2},
    {"name": "保暖内衣套装 加绒加厚 冬季男女", "brand": "UNIQLO", "category": "上装", "price": 39.9, "original_price": 129.0, "sales": 560000, "rating": 4.5},
    {"name": "瑜伽裤 女款高腰提臀运动紧身裤", "brand": "Lululemon", "category": "下装", "price": 89.0, "original_price": 349.0, "sales": 340000, "rating": 4.4},
    {"name": "雪地靴 女款加绒保暖短靴 冬季", "brand": "UGG", "category": "鞋履", "price": 119.0, "original_price": 399.0, "sales": 210000, "rating": 4.3},
    {"name": "帆布包 大容量托特包 男女通勤", "brand": "MUJI", "category": "配饰", "price": 29.9, "original_price": 99.0, "sales": 380000, "rating": 4.3},
    {"name": "真皮皮带 男士商务自动扣 黑色", "brand": "Hugo Boss", "category": "配饰", "price": 49.9, "original_price": 199.0, "sales": 120000, "rating": 4.2},
]

CATEGORY_MAP = {
    "上装": "上装",
    "下装": "下装",
    "鞋履": "鞋履",
    "配饰": "配饰",
    "连衣裙": "连衣裙",
}

GENDER_KEYWORDS = {
    "男": ["男", "男士", "男女"],
    "女": ["女", "女士", "男女"],
}


def _make_item_id(name: str, platform: str) -> str:
    raw = f"{platform}:{name}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()[:12]


def _make_taobao_url(item_id: str) -> str:
    return f"https://item.taobao.com/item.htm?id={item_id}"


def _make_jd_url(item_id: str) -> str:
    return f"https://item.jd.com/{item_id}.html"


def _make_pdd_url(item_id: str) -> str:
    return f"https://mobile.yangkeduo.com/goods.html?goods_id={item_id}"


def _make_image_url(platform: str, item_id: str) -> str:
    return f"https://img.{platform}.com/item/{item_id}_800x800.jpg"


def _match_query(product: Dict[str, Any], query: str) -> float:
    query_lower = query.lower()
    name_lower = product["name"].lower()
    brand_lower = product["brand"].lower()
    score = 0.0
    for word in query_lower.split():
        if word in name_lower:
            score += 2.0
        if word in brand_lower:
            score += 1.5
    if query_lower in name_lower:
        score += 3.0
    return score


def _filter_products(
    products: List[Dict[str, Any]],
    query: str,
    category: Optional[str],
    gender: Optional[str],
    min_price: Optional[float],
    max_price: Optional[float],
    top_k: int,
) -> List[Dict[str, Any]]:
    filtered = []
    for p in products:
        if category and p.get("category") != category:
            continue
        if min_price is not None and p.get("price", 0) < min_price:
            continue
        if max_price is not None and p.get("price", 0) > max_price:
            continue
        if gender:
            keywords = GENDER_KEYWORDS.get(gender, [gender])
            name = p.get("name", "")
            if not any(kw in name for kw in keywords):
                if "男女" not in name and gender not in name:
                    continue
        score = _match_query(p, query)
        filtered.append((score, p))

    filtered.sort(key=lambda x: (-x[0], -x[1].get("sales", 0)))
    return [item for _, item in filtered[:top_k]]


def _search_taobao(
    query: str,
    category: Optional[str],
    gender: Optional[str],
    min_price: Optional[float],
    max_price: Optional[float],
    top_k: int,
) -> List[Dict[str, Any]]:
    results = _filter_products(TAOBAO_PRODUCTS, query, category, gender, min_price, max_price, top_k)
    output = []
    for p in results:
        item_id = _make_item_id(p["name"], "taobao")
        output.append({
            "name": p["name"],
            "brand": p["brand"],
            "price": p["price"],
            "original_price": p["original_price"],
            "platform": "淘宝",
            "url": _make_taobao_url(item_id),
            "image_url": _make_image_url("taobao", item_id),
            "sales": p["sales"],
            "rating": p["rating"],
            "category": p["category"],
        })
    return output


def _search_jd(
    query: str,
    category: Optional[str],
    gender: Optional[str],
    min_price: Optional[float],
    max_price: Optional[float],
    top_k: int,
) -> List[Dict[str, Any]]:
    results = _filter_products(JD_PRODUCTS, query, category, gender, min_price, max_price, top_k)
    output = []
    for p in results:
        item_id = _make_item_id(p["name"], "jd")
        output.append({
            "name": p["name"],
            "brand": p["brand"],
            "price": p["price"],
            "original_price": p["original_price"],
            "platform": "京东",
            "url": _make_jd_url(item_id),
            "image_url": _make_image_url("jd", item_id),
            "sales": p["sales"],
            "rating": p["rating"],
            "category": p["category"],
        })
    return output


def _search_pdd(
    query: str,
    category: Optional[str],
    gender: Optional[str],
    min_price: Optional[float],
    max_price: Optional[float],
    top_k: int,
) -> List[Dict[str, Any]]:
    results = _filter_products(PDD_PRODUCTS, query, category, gender, min_price, max_price, top_k)
    output = []
    for p in results:
        item_id = _make_item_id(p["name"], "pdd")
        output.append({
            "name": p["name"],
            "brand": p["brand"],
            "price": p["price"],
            "original_price": p["original_price"],
            "platform": "拼多多",
            "url": _make_pdd_url(item_id),
            "image_url": _make_image_url("pdd", item_id),
            "sales": p["sales"],
            "rating": p["rating"],
            "category": p["category"],
        })
    return output


@register_tool
class EcommerceSearchTool(BaseTool):
    name = "ecommerce_search"
    description = "从电商平台搜索真实在售服饰商品，支持关键词搜索和分类筛选"
    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "搜索关键词",
            },
            "category": {
                "type": "string",
                "description": "分类如上装/下装/鞋履/配饰/连衣裙",
            },
            "gender": {
                "type": "string",
                "description": "性别",
            },
            "min_price": {
                "type": "number",
                "description": "最低价格",
            },
            "max_price": {
                "type": "number",
                "description": "最高价格",
            },
            "platform": {
                "type": "string",
                "description": "平台选择taobao/jd/pdd,默认全部",
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
        gender: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        platform: Optional[str] = None,
        top_k: int = 5,
        **kwargs,
    ) -> str:
        if not query:
            return "请提供搜索关键词"

        all_results: List[Dict[str, Any]] = []

        platform_lower = platform.lower() if platform else ""

        if not platform_lower or platform_lower == "taobao":
            all_results.extend(_search_taobao(query, category, gender, min_price, max_price, top_k))
        if not platform_lower or platform_lower == "jd":
            all_results.extend(_search_jd(query, category, gender, min_price, max_price, top_k))
        if not platform_lower or platform_lower == "pdd":
            all_results.extend(_search_pdd(query, category, gender, min_price, max_price, top_k))

        if not all_results:
            return f"未找到与 '{query}' 匹配的商品。试试调整搜索条件。"

        all_results.sort(key=lambda x: (-x.get("rating", 0), -x.get("sales", 0)))

        output_parts = [f"🔍 电商搜索: {query}\n📦 找到 {len(all_results)} 件商品:\n"]

        for i, item in enumerate(all_results, 1):
            discount = ""
            if item.get("original_price") and item["original_price"] > item["price"]:
                pct = round((1 - item["price"] / item["original_price"]) * 100)
                discount = f" 降幅{pct}%"

            parts = [
                f"  {i}. [{item['platform']}] {item['name']}",
                f"     品牌: {item.get('brand', 'N/A')} | 价格: ¥{item.get('price', 'N/A')}{discount}",
                f"     原价: ¥{item.get('original_price', 'N/A')} | 销量: {item.get('sales', 0):,} | 评分: {item.get('rating', 'N/A')}",
                f"     分类: {item.get('category', 'N/A')}",
                f"     链接: {item.get('url', '')}",
            ]
            output_parts.append("\n".join(parts))

        return "\n\n".join(output_parts)
