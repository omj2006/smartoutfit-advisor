
"""
天气查询Agent
"""
from utils.weather_api import get_weather


class WeatherAgent:
    """天气查询智能体"""
    
    def __init__(self):
        self.name = "天气查询Agent"
    
    def run(self, state):
        """
        执行天气查询
        
        Args:
            state: 状态字典，包含城市信息
            
        Returns:
            更新后的状态
        """
        city = state.get("city", "Beijing")
        print("[" + self.name + "] 正在查询 " + city + " 的天气...")
        
        weather_data = get_weather(city)
        if weather_data:
            state["weather"] = weather_data
            print("[" + self.name + "] 查询成功: " + str(weather_data["temperature"]) + "℃, " + weather_data["weather"])
        else:
            print("[" + self.name + "] 查询失败，使用默认天气数据")
            state["weather"] = {
                "city": city,
                "temperature": 22,
                "weather": "多云",
                "wind_speed": "10 km/h",
                "temp_range": "舒适（18-25℃）"
            }
        
        return state
