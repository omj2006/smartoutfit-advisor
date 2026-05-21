
"""
天气查询工具模块
"""
import requests


TEMPERATURE_RANGES = [
    {"max": 0, "label": "极寒（0℃及以下）"},
    {"min": 0, "max": 10, "label": "寒冷（0-10℃）"},
    {"min": 10, "max": 18, "label": "凉爽（10-18℃）"},
    {"min": 18, "max": 25, "label": "舒适（18-25℃）"},
    {"min": 25, "max": 32, "label": "温暖（25-32℃）"},
    {"min": 32, "label": "炎热（32℃以上）"}
]


def get_weather(city):
    """
    获取城市天气信息
    
    Args:
        city: 城市名称
        
    Returns:
        包含温度、天气状况、风力的字典
    """
    try:
        url = "https://wttr.in/" + city + "?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current = data["current_condition"][0]
        temp_c = int(current["temp_C"])
        weather_desc = current["weatherDesc"][0]["value"]
        wind_speed = current["windspeedKmph"]
        
        return {
            "city": city,
            "temperature": temp_c,
            "weather": weather_desc,
            "wind_speed": wind_speed + " km/h",
            "temp_range": get_temperature_range(temp_c)
        }
    except Exception as e:
        print("天气查询失败:", e)
        return None


def get_temperature_range(temp):
    """
    获取温度区间标签
    
    Args:
        temp: 温度值
        
    Returns:
        温度区间标签
    """
    for range_info in TEMPERATURE_RANGES:
        if "min" in range_info and "max" in range_info:
            if range_info["min"] <= temp < range_info["max"]:
                return range_info["label"]
        elif "max" in range_info and temp <= range_info["max"]:
            return range_info["label"]
        elif "min" in range_info and temp >= range_info["min"]:
            return range_info["label"]
    return TEMPERATURE_RANGES[-1]["label"]
