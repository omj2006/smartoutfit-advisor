from __future__ import annotations

import httpx

from app.tools.base import BaseTool, register_tool


@register_tool
class WeatherQueryTool(BaseTool):
    name = "weather_query"
    description = "查询指定城市的当前天气信息，包括温度、湿度、风速、天气状况等。用于根据天气推荐穿搭。"
    parameters = {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "城市名称（中文或英文），如'北京'、'上海'、'Tokyo'",
            },
        },
        "required": ["city"],
    }

    CITY_COORDS = {
        "北京": (39.9042, 116.4074),
        "上海": (31.2304, 121.4737),
        "广州": (23.1291, 113.2644),
        "深圳": (22.5431, 114.0579),
        "成都": (30.5728, 104.0668),
        "杭州": (30.2741, 120.1551),
        "武汉": (30.5928, 114.3055),
        "南京": (32.0603, 118.7969),
        "重庆": (29.4316, 106.9123),
        "西安": (34.3416, 108.9398),
        "长沙": (28.2282, 112.9388),
        "苏州": (31.2990, 120.5853),
        "天津": (39.0842, 117.2010),
        "青岛": (36.0671, 120.3826),
        "大连": (38.9140, 121.6147),
        "厦门": (24.4798, 118.0894),
        "昆明": (25.0389, 102.7183),
        "哈尔滨": (45.8038, 126.5350),
        "沈阳": (41.8057, 123.4315),
        "济南": (36.6512, 117.1201),
        "tokyo": (35.6762, 139.6503),
        "new york": (40.7128, -74.0060),
        "london": (51.5074, -0.1278),
        "paris": (48.8566, 2.3522),
        "seoul": (37.5665, 126.9780),
        "singapore": (1.3521, 103.8198),
        "bangkok": (13.7563, 100.5018),
        "sydney": (-33.8688, 151.2093),
    }

    WEATHER_CODES = {
        0: "晴朗", 1: "大部晴朗", 2: "多云", 3: "阴天",
        45: "雾", 48: "雾凇",
        51: "小毛毛雨", 53: "中毛毛雨", 55: "大毛毛雨",
        61: "小雨", 63: "中雨", 65: "大雨",
        66: "冻雨(小)", 67: "冻雨(大)",
        71: "小雪", 73: "中雪", 75: "大雪",
        77: "雪粒", 80: "阵雨(小)", 81: "阵雨(中)", 82: "阵雨(大)",
        85: "阵雪(小)", 86: "阵雪(大)",
        95: "雷暴", 96: "雷暴+冰雹(小)", 99: "雷暴+冰雹(大)",
    }

    async def execute(self, city: str = "", **kwargs) -> str:
        coords = self._get_coords(city)
        if not coords:
            return f"未找到城市 '{city}' 的坐标。支持的城市: {', '.join(list(self.CITY_COORDS.keys())[:20])}等。"

        lat, lon = coords
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": lat,
                        "longitude": lon,
                        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m",
                        "timezone": "auto",
                    },
                )
                if resp.status_code != 200:
                    return f"天气查询失败: HTTP {resp.status_code}"

                data = resp.json()
                current = data.get("current", {})

                temp = current.get("temperature_2m", "N/A")
                feels_like = current.get("apparent_temperature", "N/A")
                humidity = current.get("relative_humidity_2m", "N/A")
                wind_speed = current.get("wind_speed_10m", "N/A")
                weather_code = current.get("weather_code", 0)
                weather_desc = self.WEATHER_CODES.get(weather_code, "未知")

                return (
                    f"城市: {city}\n"
                    f"天气: {weather_desc}\n"
                    f"温度: {temp}°C\n"
                    f"体感温度: {feels_like}°C\n"
                    f"湿度: {humidity}%\n"
                    f"风速: {wind_speed} km/h"
                )
        except Exception as e:
            return f"天气查询出错: {str(e)}"

    def _get_coords(self, city: str):
        city_lower = city.strip().lower()
        if city in self.CITY_COORDS:
            return self.CITY_COORDS[city]
        if city_lower in self.CITY_COORDS:
            return self.CITY_COORDS[city_lower]
        for name, coords in self.CITY_COORDS.items():
            if city_lower in name.lower() or name.lower() in city_lower:
                return coords
        return None
