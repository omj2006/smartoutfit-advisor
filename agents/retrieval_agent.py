
"""
检索Agent - 支持电商API
"""
import time
from utils.db_tools import filter_products, PRODUCTS


class RetrievalAgent:
    """检索智能体 - 支持本地商品库检索"""
    
    def __init__(self):
        self.name = "检索Agent"
    
    def run(self, state):
        """
        执行商品检索
        
        Args:
            state: 状态字典
            
        Returns:
            更新后的状态
        """
        temp = state.get("weather", {}).get("temperature", 22)
        occasion = state.get("occasion", "日常")
        weather = state.get("weather", {}).get("weather", "多云")
        
        print("[" + self.name + "] 正在检索商品...")
        
        # 直接使用本地商品库（避免电商API超时问题）
        try:
            filtered_products = filter_products(temp, occasion, weather)
            print("[" + self.name + "] 本地库筛选找到 " + str(len(filtered_products)) + " 件商品")
            state["product_source"] = "local"
            state["filtered_products"] = filtered_products[:10]
        except Exception as e:
            print("[" + self.name + "] 商品检索失败: " + str(e))
            # 使用模拟数据
            state["filtered_products"] = self._get_mock_products(occasion)
            state["product_source"] = "mock"
        
        state["vector_results"] = []
        
        return state
    
    def _get_mock_products(self, occasion):
        """
        获取模拟商品数据
        
        Args:
            occasion: 场合
            
        Returns:
            模拟商品列表
        """
        mock_products = [
            {
                "id": 1,
                "name": "简约休闲T恤",
                "brand": "StyleAI",
                "price": "¥199",
                "category": "上衣",
                "occasion": occasion,
                "image_url": "https://neeko-copilot.bytedance.net/api/text2image?prompt=minimalist%20casual%20t-shirt%20white%20background%20product%20photography&image_size=square"
            },
            {
                "id": 2,
                "name": "高腰牛仔裤",
                "brand": "StyleAI",
                "price": "¥299",
                "category": "下装",
                "occasion": occasion,
                "image_url": "https://neeko-copilot.bytedance.net/api/text2image?prompt=high%20waist%20jeans%20blue%20product%20photography%20white%20background&image_size=square"
            },
            {
                "id": 3,
                "name": "舒适休闲鞋",
                "brand": "StyleAI",
                "price": "¥399",
                "category": "鞋履",
                "occasion": occasion,
                "image_url": "https://neeko-copilot.bytedance.net/api/text2image?prompt=comfortable%20casual%20sneakers%20white%20product%20photography&image_size=square"
            },
            {
                "id": 4,
                "name": "时尚单肩包",
                "brand": "StyleAI",
                "price": "¥159",
                "category": "配饰",
                "occasion": occasion,
                "image_url": "https://neeko-copilot.bytedance.net/api/text2image?prompt=fashion%20shoulder%20bag%20leather%20product%20photography&image_size=square"
            }
        ]
        return mock_products
