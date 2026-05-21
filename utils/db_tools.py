
"""
商品数据库工具模块
"""

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


OUTFIT_RULES = {
    "极寒（0℃及以下）": {
        "日常": "羽绒服+厚毛衣+保暖裤+雪地靴，注重保暖",
        "通勤": "长款羽绒服+西装内搭+毛呢裤+短靴",
        "约会": "时尚羽绒服+连衣裙+打底裤+长靴",
        "运动": "保暖运动套装+冲锋衣+运动鞋",
        "聚会": "毛呢大衣+礼服裙+保暖裤+高跟鞋"
    },
    "寒冷（0-10℃）": {
        "日常": "棉服+毛衣+牛仔裤+板鞋",
        "通勤": "毛呢大衣+衬衫+西裤+皮鞋",
        "约会": "呢子外套+针织衫+半身裙+短靴",
        "运动": "卫衣+运动裤+运动外套+运动鞋",
        "聚会": "小西装+连衣裙+打底裤+浅口鞋"
    },
    "凉爽（10-18℃）": {
        "日常": "风衣+卫衣+休闲裤+帆布鞋",
        "通勤": "小西装+衬衫+西裤+皮鞋",
        "约会": "针织开衫+连衣裙+单鞋",
        "运动": "运动套装+运动鞋",
        "聚会": "衬衫+针织背心+休闲裤+乐福鞋"
    },
    "舒适（18-25℃）": {
        "日常": "T恤+牛仔裤+帆布鞋",
        "通勤": "衬衫+休闲裤+小皮鞋",
        "约会": "连衣裙+小白鞋",
        "运动": "速干衣+运动裤+运动鞋",
        "聚会": "衬衫+休闲裤+乐福鞋"
    },
    "温暖（25-32℃）": {
        "日常": "短袖T恤+短裤+凉鞋",
        "通勤": "短袖衬衫+休闲裤+皮鞋",
        "约会": "连衣裙+凉鞋",
        "运动": "运动背心+短裤+运动鞋",
        "聚会": "短袖衬衫+休闲裤+板鞋"
    },
    "炎热（32℃以上）": {
        "日常": "无袖T恤+短裤+拖鞋",
        "通勤": "短袖衬衫+轻薄西裤+透气皮鞋",
        "约会": "吊带连衣裙+凉鞋",
        "运动": "速干背心+运动短裤+透气运动鞋",
        "聚会": "轻薄衬衫+休闲短裤+凉鞋"
    }
}


def filter_products(temp, occasion, weather=None):
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


def get_outfit_suggestion(temp_range, occasion):
    """
    获取穿搭建议
    
    Args:
        temp_range: 温度区间
        occasion: 场合
        
    Returns:
        穿搭建议字典
    """
    valid_occasions = ["日常", "通勤", "约会", "运动", "聚会"]
    if occasion not in valid_occasions:
        occasion = "日常"
    
    suggestion = OUTFIT_RULES.get(temp_range, OUTFIT_RULES["舒适（18-25℃）"]).get(occasion, OUTFIT_RULES["舒适（18-25℃）"]["日常"])
    
    return {
        "temp_range": temp_range,
        "occasion": occasion,
        "suggestion": suggestion,
        "style": temp_range + " + " + occasion + "风格"
    }
