from __future__ import annotations

import json
import os
import sqlite3
from typing import Any, Dict, List, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "products.db")
DB_PATH = os.path.abspath(DB_PATH)

SEED_PRODUCTS = [
    {"id": 1, "name": "经典白色衬衫", "category": "上装", "subcategory": "衬衫", "brand": "UNIQLO", "price": 199.0, "color": "白色", "color_family": "浅色", "season": "春夏秋", "occasion": "商务,休闲,约会", "style": "简约,通勤", "gender": "男女通用", "material": "棉", "description": "经典百搭白色衬衫，优质棉质面料，修身版型，适合商务和日常穿搭", "image_url": ""},
    {"id": 2, "name": "浅蓝色牛仔衬衫", "category": "上装", "subcategory": "衬衫", "brand": "ZARA", "price": 299.0, "color": "浅蓝色", "color_family": "浅色", "season": "春夏秋", "occasion": "休闲,约会", "style": "休闲,街头", "gender": "男", "material": "棉", "description": "经典浅蓝色牛仔衬衫，柔软水洗牛仔面料，休闲百搭", "image_url": ""},
    {"id": 3, "name": "黑色修身西装外套", "category": "上装", "subcategory": "外套", "brand": "H&M", "price": 599.0, "color": "黑色", "color_family": "深色", "season": "春秋", "occasion": "商务,正式", "style": "通勤,优雅", "gender": "男", "material": "聚酯纤维", "description": "黑色修身西装外套，合体剪裁，商务场合必备单品", "image_url": ""},
    {"id": 4, "name": "驼色风衣", "category": "上装", "subcategory": "外套", "brand": "Burberry", "price": 12999.0, "color": "驼色", "color_family": "暖色", "season": "春秋", "occasion": "商务,休闲,约会", "style": "优雅,通勤", "gender": "男女通用", "material": "棉混纺", "description": "经典驼色风衣，双排扣设计，腰带收腰，优雅永不过时", "image_url": ""},
    {"id": 5, "name": "白色短袖T恤", "category": "上装", "subcategory": "T恤", "brand": "UNIQLO", "price": 79.0, "color": "白色", "color_family": "浅色", "season": "夏", "occasion": "休闲,运动", "style": "简约,休闲", "gender": "男女通用", "material": "棉", "description": "基础款白色短袖T恤，纯棉面料，舒适透气，百搭基础款", "image_url": ""},
    {"id": 6, "name": "灰色连帽卫衣", "category": "上装", "subcategory": "卫衣", "brand": "Nike", "price": 499.0, "color": "灰色", "color_family": "中性色", "season": "春秋冬", "occasion": "休闲,运动", "style": "休闲,街头", "gender": "男女通用", "material": "棉混纺", "description": "灰色连帽卫衣，加绒内里，前袋设计，运动休闲两不误", "image_url": ""},
    {"id": 7, "name": "红色针织开衫", "category": "上装", "subcategory": "针织衫", "brand": "COS", "price": 699.0, "color": "红色", "color_family": "暖色", "season": "春秋冬", "occasion": "休闲,约会", "style": "文艺,优雅", "gender": "女", "material": "羊毛混纺", "description": "红色针织开衫，V领设计，温柔优雅，秋冬必备", "image_url": ""},
    {"id": 8, "name": "黑色高领毛衣", "category": "上装", "subcategory": "针织衫", "brand": "Massimo Dutti", "price": 599.0, "color": "黑色", "color_family": "深色", "season": "秋冬", "occasion": "商务,休闲,约会", "style": "优雅,通勤", "gender": "男女通用", "material": "羊毛", "description": "黑色高领毛衣，纯羊毛面料，修身版型，秋冬百搭", "image_url": ""},
    {"id": 9, "name": "白色吊带背心", "category": "上装", "subcategory": "背心", "brand": "ZARA", "price": 99.0, "color": "白色", "color_family": "浅色", "season": "夏", "occasion": "休闲,约会", "style": "简约,性感", "gender": "女", "material": "粘胶纤维", "description": "白色吊带背心，细肩带设计，清凉性感，夏日必备", "image_url": ""},
    {"id": 10, "name": "军绿色夹克", "category": "上装", "subcategory": "外套", "brand": "The North Face", "price": 899.0, "color": "军绿色", "color_family": "中性色", "season": "春秋", "occasion": "休闲,户外", "style": "街头,户外", "gender": "男", "material": "尼龙", "description": "军绿色工装夹克，防风面料，多口袋设计，户外休闲首选", "image_url": ""},
    {"id": 11, "name": "黑色长款羽绒服", "category": "上装", "subcategory": "外套", "brand": "UNIQLO", "price": 999.0, "color": "黑色", "color_family": "深色", "season": "冬", "occasion": "休闲,通勤", "style": "简约,通勤", "gender": "男女通用", "material": "聚酯纤维", "description": "黑色长款羽绒服，90%白鸭绒填充，极寒天气保暖利器", "image_url": ""},
    {"id": 12, "name": "粉色连衣裙", "category": "连衣裙", "subcategory": "连衣裙", "brand": "Maje", "price": 1899.0, "color": "粉色", "color_family": "暖色", "season": "春夏", "occasion": "约会,正式", "style": "优雅,浪漫", "gender": "女", "material": "雪纺", "description": "粉色碎花连衣裙，A字版型，收腰设计，约会首选", "image_url": ""},
    {"id": 13, "name": "小黑裙", "category": "连衣裙", "subcategory": "连衣裙", "brand": "Sandro", "price": 1599.0, "color": "黑色", "color_family": "深色", "season": "四季", "occasion": "约会,正式,商务", "style": "优雅,经典", "gender": "女", "material": "聚酯纤维", "description": "经典小黑裙，修身剪裁，及膝长度，永不过时的优雅", "image_url": ""},
    {"id": 14, "name": "深蓝色直筒牛仔裤", "category": "下装", "subcategory": "牛仔裤", "brand": "Levi's", "price": 599.0, "color": "深蓝色", "color_family": "深色", "season": "四季", "occasion": "休闲,约会,通勤", "style": "休闲,经典", "gender": "男女通用", "material": "棉", "description": "501经典直筒牛仔裤，深蓝色水洗，百搭经典款", "image_url": ""},
    {"id": 15, "name": "黑色西裤", "category": "下装", "subcategory": "西裤", "brand": "Hugo Boss", "price": 899.0, "color": "黑色", "color_family": "深色", "season": "四季", "occasion": "商务,正式", "style": "通勤,优雅", "gender": "男", "material": "羊毛混纺", "description": "黑色修身西裤，弹力面料，商务场合必备", "image_url": ""},
    {"id": 16, "name": "卡其色休闲九分裤", "category": "下装", "subcategory": "休闲裤", "brand": "UNIQLO", "price": 249.0, "color": "卡其色", "color_family": "暖色", "season": "春夏秋", "occasion": "休闲,通勤", "style": "休闲,简约", "gender": "男", "material": "棉", "description": "卡其色九分休闲裤，弹力棉面料，舒适百搭", "image_url": ""},
    {"id": 17, "name": "黑色半身裙", "category": "下装", "subcategory": "半裙", "brand": "COS", "price": 599.0, "color": "黑色", "color_family": "深色", "season": "四季", "occasion": "商务,约会", "style": "优雅,通勤", "gender": "女", "material": "羊毛混纺", "description": "黑色A字半身裙，及膝长度，优雅得体，通勤约会两相宜", "image_url": ""},
    {"id": 18, "name": "白色运动短裤", "category": "下装", "subcategory": "短裤", "brand": "Nike", "price": 299.0, "color": "白色", "color_family": "浅色", "season": "夏", "occasion": "运动,休闲", "style": "运动,休闲", "gender": "男女通用", "material": "聚酯纤维", "description": "白色运动短裤，速干面料，内衬设计，运动必备", "image_url": ""},
    {"id": 19, "name": "黑色皮鞋", "category": "鞋履", "subcategory": "皮鞋", "brand": "Clarks", "price": 899.0, "color": "黑色", "color_family": "深色", "season": "四季", "occasion": "商务,正式", "style": "通勤,经典", "gender": "男", "material": "真皮", "description": "黑色德比皮鞋，真皮材质，商务场合首选", "image_url": ""},
    {"id": 20, "name": "白色运动鞋", "category": "鞋履", "subcategory": "运动鞋", "brand": "Adidas", "price": 799.0, "color": "白色", "color_family": "浅色", "season": "四季", "occasion": "休闲,运动", "style": "休闲,运动", "gender": "男女通用", "material": "合成材料", "description": "Stan Smith经典白鞋，百搭休闲鞋，永不过时", "image_url": ""},
    {"id": 21, "name": "黑色短靴", "category": "鞋履", "subcategory": "靴子", "brand": "Dr. Martens", "price": 1299.0, "color": "黑色", "color_family": "深色", "season": "秋冬", "occasion": "休闲,约会", "style": "街头,酷感", "gender": "男女通用", "material": "真皮", "description": "经典1460八孔马丁靴，黑色真皮，街头酷感十足", "image_url": ""},
    {"id": 22, "name": "裸色高跟鞋", "category": "鞋履", "subcategory": "高跟鞋", "brand": "Stuart Weitzman", "price": 2999.0, "color": "裸色", "color_family": "浅色", "season": "四季", "occasion": "约会,正式,商务", "style": "优雅,性感", "gender": "女", "material": "真皮", "description": "裸色尖头高跟鞋，7cm细跟，拉长腿部线条，优雅百搭", "image_url": ""},
    {"id": 23, "name": "棕色乐福鞋", "category": "鞋履", "subcategory": "乐福鞋", "brand": "G.H. Bass", "price": 699.0, "color": "棕色", "color_family": "暖色", "season": "春秋", "occasion": "休闲,商务", "style": "休闲,通勤", "gender": "男女通用", "material": "真皮", "description": "经典棕色乐福鞋，流苏设计，商务休闲两相宜", "image_url": ""},
    {"id": 24, "name": "防水 Chelsea 雨靴", "category": "鞋履", "subcategory": "雨靴", "brand": "Hunter", "price": 899.0, "color": "黑色", "color_family": "深色", "season": "四季", "occasion": "休闲,户外", "style": "户外,休闲", "gender": "男女通用", "material": "橡胶", "description": "经典Chelsea雨靴，防水橡胶材质，雨天出行必备", "image_url": ""},
    {"id": 25, "name": "丝绒围巾", "category": "配饰", "subcategory": "围巾", "brand": "Acne Studios", "price": 1599.0, "color": "灰色", "color_family": "中性色", "season": "秋冬", "occasion": "休闲,商务,约会", "style": "优雅,文艺", "gender": "男女通用", "material": "羊毛", "description": "灰色羊毛围巾，经典格纹设计，秋冬保暖又时尚", "image_url": ""},
    {"id": 26, "name": "黑色皮带", "category": "配饰", "subcategory": "腰带", "brand": "Hugo Boss", "price": 499.0, "color": "黑色", "color_family": "深色", "season": "四季", "occasion": "商务,休闲", "style": "通勤,经典", "gender": "男", "material": "真皮", "description": "黑色真皮皮带，简约针扣设计，商务休闲必备", "image_url": ""},
    {"id": 27, "name": "墨镜", "category": "配饰", "subcategory": "墨镜", "brand": "Ray-Ban", "price": 1299.0, "color": "黑色", "color_family": "深色", "season": "夏", "occasion": "休闲,户外,约会", "style": "酷感,经典", "gender": "男女通用", "material": "金属+树脂", "description": "Ray-Ban经典飞行员墨镜，夏日防晒又时尚", "image_url": ""},
    {"id": 28, "name": "帆布托特包", "category": "配饰", "subcategory": "包袋", "brand": "MUJI", "price": 199.0, "color": "米色", "color_family": "浅色", "season": "四季", "occasion": "休闲,通勤", "style": "简约,休闲", "gender": "男女通用", "material": "帆布", "description": "米色帆布托特包，大容量设计，日常通勤好帮手", "image_url": ""},
    {"id": 29, "name": "黑色手拿包", "category": "配饰", "subcategory": "包袋", "brand": "Sandro", "price": 899.0, "color": "黑色", "color_family": "深色", "season": "四季", "occasion": "约会,正式", "style": "优雅,经典", "gender": "女", "material": "真皮", "description": "黑色真皮手拿包，金属扣设计，晚宴约会精致之选", "image_url": ""},
    {"id": 30, "name": "遮阳帽", "category": "配饰", "subcategory": "帽子", "brand": "Lack of Color", "price": 399.0, "color": "米白色", "color_family": "浅色", "season": "夏", "occasion": "休闲,户外", "style": "休闲,文艺", "gender": "男女通用", "material": "草编", "description": "米白色草编遮阳帽，宽檐设计，夏日防晒又文艺", "image_url": ""},
    {"id": 31, "name": "速干运动T恤", "category": "上装", "subcategory": "T恤", "brand": "Nike", "price": 299.0, "color": "黑色", "color_family": "深色", "season": "夏", "occasion": "运动,户外", "style": "运动", "gender": "男女通用", "material": "聚酯纤维", "description": "Dri-FIT速干运动T恤，透气排汗，运动健身必备", "image_url": ""},
    {"id": 32, "name": "运动紧身裤", "category": "下装", "subcategory": "运动裤", "brand": "Lululemon", "price": 850.0, "color": "黑色", "color_family": "深色", "season": "四季", "occasion": "运动", "style": "运动", "gender": "女", "material": "尼龙混纺", "description": "黑色高腰运动紧身裤，塑形支撑，瑜伽跑步通用", "image_url": ""},
    {"id": 33, "name": "冲锋衣", "category": "上装", "subcategory": "外套", "brand": "Arc'teryx", "price": 3999.0, "color": "深蓝色", "color_family": "深色", "season": "春秋冬", "occasion": "户外,运动", "style": "户外", "gender": "男女通用", "material": "GORE-TEX", "description": "Beta LT冲锋衣，GORE-TEX面料，防风防水透气，户外专业之选", "image_url": ""},
    {"id": 34, "name": "雪地靴", "category": "鞋履", "subcategory": "靴子", "brand": "UGG", "price": 1399.0, "color": "栗色", "color_family": "暖色", "season": "冬", "occasion": "休闲", "style": "休闲", "gender": "女", "material": "羊皮", "description": "经典栗色雪地靴，羊毛内里，冬季保暖舒适", "image_url": ""},
    {"id": 35, "name": "毛线帽", "category": "配饰", "subcategory": "帽子", "brand": "Acne Studios", "price": 699.0, "color": "灰色", "color_family": "中性色", "season": "冬", "occasion": "休闲,户外", "style": "休闲,街头", "gender": "男女通用", "material": "羊毛", "description": "灰色羊毛毛线帽，简约设计，冬季保暖必备", "image_url": ""},
    {"id": 36, "name": "皮手套", "category": "配饰", "subcategory": "手套", "brand": "Coach", "price": 599.0, "color": "黑色", "color_family": "深色", "season": "秋冬", "occasion": "商务,休闲", "style": "经典,通勤", "gender": "男女通用", "material": "真皮", "description": "黑色真皮手套，内里加绒，保暖又有型", "image_url": ""},
    {"id": 37, "name": "真丝吊带裙", "category": "连衣裙", "subcategory": "连衣裙", "brand": "Equipment", "price": 2299.0, "color": "香槟色", "color_family": "暖色", "season": "夏", "occasion": "约会,正式", "style": "优雅,性感", "gender": "女", "material": "真丝", "description": "香槟色真丝吊带裙，丝滑面料，高级质感，约会晚宴皆宜", "image_url": ""},
    {"id": 38, "name": "格纹西装外套", "category": "上装", "subcategory": "外套", "brand": "Ted Baker", "price": 1999.0, "color": "灰色", "color_family": "中性色", "season": "春秋", "occasion": "商务,约会", "style": "优雅,通勤", "gender": "女", "material": "羊毛混纺", "description": "灰色格纹西装外套，修身版型，英伦优雅", "image_url": ""},
    {"id": 39, "name": "加绒保暖内衣套装", "category": "上装", "subcategory": "内衣", "brand": "UNIQLO", "price": 199.0, "color": "黑色", "color_family": "深色", "season": "冬", "occasion": "休闲,通勤", "style": "简约", "gender": "男女通用", "material": "聚酯纤维", "description": "HEATTECH加绒保暖内衣套装，发热科技，冬季打底必备", "image_url": ""},
    {"id": 40, "name": "防水夹克", "category": "上装", "subcategory": "外套", "brand": "Stüssy", "price": 1299.0, "color": "黑色", "color_family": "深色", "season": "春夏秋", "occasion": "休闲,户外", "style": "街头,户外", "gender": "男女通用", "material": "尼龙", "description": "黑色防水夹克，DWR涂层，雨天也能时尚出街", "image_url": ""},
]


def get_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT,
            brand TEXT,
            price REAL,
            color TEXT,
            color_family TEXT,
            season TEXT,
            occasion TEXT,
            style TEXT,
            gender TEXT,
            material TEXT,
            description TEXT,
            image_url TEXT DEFAULT '',
            search_vector TEXT DEFAULT ''
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

    if count == 0:
        for p in SEED_PRODUCTS:
            search_text = f"{p['name']} {p['category']} {p['subcategory']} {p['brand']} {p['color']} {p['color_family']} {p['season']} {p['occasion']} {p['style']} {p['gender']} {p['material']} {p['description']}"
            cursor.execute(
                """
                INSERT INTO products (id, name, category, subcategory, brand, price, color, color_family,
                    season, occasion, style, gender, material, description, image_url, search_vector)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    p["id"], p["name"], p["category"], p["subcategory"], p["brand"],
                    p["price"], p["color"], p["color_family"], p["season"],
                    p["occasion"], p["style"], p["gender"], p["material"],
                    p["description"], p.get("image_url", ""), search_text,
                ),
            )
        conn.commit()
        print(f"Initialized product database with {len(SEED_PRODUCTS)} items")

    conn.close()


def query_products(
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    color_family: Optional[str] = None,
    season: Optional[str] = None,
    occasion: Optional[str] = None,
    style: Optional[str] = None,
    gender: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()

    conditions = []
    params = []

    if category:
        conditions.append("category = ?")
        params.append(category)
    if subcategory:
        conditions.append("subcategory = ?")
        params.append(subcategory)
    if color_family:
        conditions.append("color_family = ?")
        params.append(color_family)
    if season:
        conditions.append("season LIKE ?")
        params.append(f"%{season}%")
    if occasion:
        conditions.append("occasion LIKE ?")
        params.append(f"%{occasion}%")
    if style:
        conditions.append("style LIKE ?")
        params.append(f"%{style}%")
    if gender:
        conditions.append("(gender = ? OR gender = '男女通用')")
        params.append(gender)
    if min_price is not None:
        conditions.append("price >= ?")
        params.append(min_price)
    if max_price is not None:
        conditions.append("price <= ?")
        params.append(max_price)

    where_clause = " AND ".join(conditions) if conditions else "1=1"
    query = f"SELECT * FROM products WHERE {where_clause} ORDER BY price ASC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_all_products() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products ORDER BY category, price")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_categories() -> List[str]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM products ORDER BY category")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]
