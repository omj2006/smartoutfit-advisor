
"""
结构化商品库模块
"""
from typing import List, Dict


PRODUCTS = [
    {
        "id": 1,
        "name": "经典白T恤",
        "min_temp": 18,
        "max_temp": 35,
        "weather": ["晴", "多云", "阴"],
        "occasions": ["日常", "通勤"],
        "description": "纯棉材质，舒适透气，百搭单品，适合春夏穿着"
    },
    {
        "id": 2,
        "name": "修身牛仔裤",
        "min_temp": 10,
        "max_temp": 30,
        "weather": ["晴", "多云", "阴", "小雨"],
        "occasions": ["日常", "约会", "通勤"],
        "description": "修身版型，弹力面料，舒适百搭，四季皆宜"
    },
    {
        "id": 3,
        "name": "轻薄羽绒服",
        "min_temp": -10,
        "max_temp": 10,
        "weather": ["晴", "多云", "阴", "雪"],
        "occasions": ["日常", "通勤", "约会"],
        "description": "轻便保暖，时尚设计，冬季必备单品"
    },
    {
        "id": 4,
        "name": "针织连衣裙",
        "min_temp": 15,
        "max_temp": 28,
        "weather": ["晴", "多云", "阴"],
        "occasions": ["约会", "聚会", "日常"],
        "description": "优雅设计，舒适面料，展现女性魅力"
    },
    {
        "id": 5,
        "name": "运动套装",
        "min_temp": 10,
        "max_temp": 35,
        "weather": ["晴", "多云", "阴"],
        "occasions": ["运动", "日常"],
        "description": "速干透气，弹力舒适，运动休闲两相宜"
    },
    {
        "id": 6,
        "name": "小西装外套",
        "min_temp": 12,
        "max_temp": 25,
        "weather": ["晴", "多云", "阴"],
        "occasions": ["通勤", "聚会", "约会"],
        "description": "修身版型，精致剪裁，职场时尚必备"
    },
    {
        "id": 7,
        "name": "毛呢大衣",
        "min_temp": -5,
        "max_temp": 15,
        "weather": ["晴", "多云", "阴", "小雨"],
        "occasions": ["日常", "通勤", "聚会"],
        "description": "优质面料，优雅版型，冬季时尚之选"
    },
    {
        "id": 8,
        "name": "休闲短裤",
        "min_temp": 25,
        "max_temp": 40,
        "weather": ["晴", "多云"],
        "occasions": ["日常", "运动"],
        "description": "轻薄透气，舒适自在，夏季必备"
    },
    {
        "id": 9,
        "name": "帆布鞋",
        "min_temp": 10,
        "max_temp": 35,
        "weather": ["晴", "多云"],
        "occasions": ["日常", "约会", "运动"],
        "description": "经典款式，舒适百搭，青春时尚"
    },
    {
        "id": 10,
        "name": "真皮高跟鞋",
        "min_temp": 15,
        "max_temp": 32,
        "weather": ["晴", "多云", "阴"],
        "occasions": ["约会", "聚会", "通勤"],
        "description": "精致设计，优雅气质，提升整体品味"
    }
]


def filter_products(temp: int, occasion: str, weather: str = None) -> List[Dict]:
    """
    按温度、场合筛选商品
    
    Args:
        temp: 温度
        occasion: 场合
        weather: 天气（可选）
        
    Returns:
        筛选后的商品列表
    """
    filtered = []
    for product in PRODUCTS:
        if product["min_temp"] <= temp <= product["max_temp"]:
            if occasion in product["occasions"]:
                if weather is None or weather in product["weather"] or len(product["weather"]) >= 3:
                    filtered.append(product)
    return filtered


def get_product_by_id(product_id: int) -> Dict:
    """
    根据ID获取商品
    
    Args:
        product_id: 商品ID
        
    Returns:
        商品信息
    """
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None


if __name__ == "__main__":
    products = filter_products(22, "约会")
    print(f"找到 {len(products)} 件匹配商品:")
    for p in products:
        print(f"{p['id']}. {p['name']} - {p['description']}")

