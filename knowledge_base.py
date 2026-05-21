
"""
穿搭知识库模块
"""
from typing import Dict, List
from config import OCCASIONS


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


def get_outfit_suggestion(temp_range: str, occasion: str) -&gt; Dict:
    """
    获取穿搭建议
    
    Args:
        temp_range: 温度区间
        occasion: 场合
        
    Returns:
        穿搭建议字典
    """
    if occasion not in OCCASIONS:
        occasion = "日常"
    
    suggestion = OUTFIT_RULES.get(temp_range, OUTFIT_RULES["舒适（18-25℃）"]).get(occasion, OUTFIT_RULES["舒适（18-25℃）"]["日常"])
    
    return {
        "temp_range": temp_range,
        "occasion": occasion,
        "suggestion": suggestion,
        "style": f"{temp_range} + {occasion}风格"
    }


if __name__ == "__main__":
    suggestion = get_outfit_suggestion("舒适（18-25℃）", "约会")
    print(f"温度区间: {suggestion['temp_range']}")
    print(f"场合: {suggestion['occasion']}")
    print(f"穿搭建议: {suggestion['suggestion']}")
    print(f"风格: {suggestion['style']}")
