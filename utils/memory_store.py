
"""
SmartOutfitAdvisor 用户记忆管理模块
使用本地JSON持久化存储用户偏好和历史推荐
"""
import os
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional

# 记忆数据目录
MEMORY_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(MEMORY_DIR, exist_ok=True)


class UserMemory:
    """用户记忆类"""
    
    def __init__(self, user_id: str = "default"):
        """
        初始化用户记忆
        
        Args:
            user_id: 用户唯一标识符
        """
        self.user_id = user_id
        self.memory_file = os.path.join(MEMORY_DIR, f"user_{self._sanitize_filename(user_id)}.json")
        self.memory = self._load_memory()
    
    def _sanitize_filename(self, filename: str) -> str:
        """清理文件名，防止安全问题"""
        return hashlib.md5(filename.encode()).hexdigest()
    
    def _load_memory(self) -> Dict[str, Any]:
        """加载记忆数据"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        # 默认空记忆结构
        return {
            "user_id": self.user_id,
            "created_at": datetime.now().isoformat(),
            "preferences": {
                "cities": [],
                "occasions": [],
                "styles": [],
                "temperature_range": None,
                "colors": [],
                "preferred_brands": []
            },
            "history": [],
            "interactions": 0
        }
    
    def _save_memory(self) -> None:
        """保存记忆数据到本地"""
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)
    
    # ==================== 偏好管理 ====================
    
    def get_preferences(self) -> Dict[str, Any]:
        """获取用户偏好"""
        return self.memory.get("preferences", {})
    
    def update_preferences(self, preferences: Dict[str, Any]) -> None:
        """
        更新用户偏好
        
        Args:
            preferences: 包含要更新的偏好字典
        """
        self.memory["preferences"].update(preferences)
        self._save_memory()
    
    def add_city(self, city: str) -> None:
        """添加常用城市"""
        if city not in self.memory["preferences"]["cities"]:
            self.memory["preferences"]["cities"].append(city)
            self._save_memory()
    
    def add_occasion(self, occasion: str) -> None:
        """添加常用场合"""
        if occasion not in self.memory["preferences"]["occasions"]:
            self.memory["preferences"]["occasions"].append(occasion)
            self._save_memory()
    
    def add_style(self, style: str) -> None:
        """添加风格偏好"""
        if style not in self.memory["preferences"]["styles"]:
            self.memory["preferences"]["styles"].append(style)
            self._save_memory()
    
    def add_color(self, color: str) -> None:
        """添加颜色偏好"""
        if color not in self.memory["preferences"]["colors"]:
            self.memory["preferences"]["colors"].append(color)
            self._save_memory()
    
    def add_brand(self, brand: str) -> None:
        """添加品牌偏好"""
        if brand not in self.memory["preferences"]["preferred_brands"]:
            self.memory["preferences"]["preferred_brands"].append(brand)
            self._save_memory()
    
    def set_temperature_range(self, min_temp: int, max_temp: int) -> None:
        """设置温度偏好范围"""
        self.memory["preferences"]["temperature_range"] = {
            "min": min_temp,
            "max": max_temp
        }
        self._save_memory()
    
    # ==================== 历史记录管理 ====================
    
    def add_history(self, recommendation: Dict[str, Any]) -> None:
        """
        添加推荐历史记录
        
        Args:
            recommendation: 推荐记录字典，包含天气、穿搭建议、商品等
        """
        history_item = {
            "id": len(self.memory["history"]) + 1,
            "timestamp": datetime.now().isoformat(),
            **recommendation
        }
        self.memory["history"].insert(0, history_item)
        self.memory["interactions"] += 1
        # 只保留最近50条记录
        if len(self.memory["history"]) > 50:
            self.memory["history"] = self.memory["history"][:50]
        self._save_memory()
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取历史推荐记录
        
        Args:
            limit: 返回记录数量
            
        Returns:
            历史记录列表
        """
        return self.memory["history"][:limit]
    
    def get_recent_cities(self) -> List[str]:
        """获取最近使用的城市"""
        cities = self.memory["preferences"]["cities"][:3]
        # 从历史记录补充
        for record in self.memory["history"]:
            if "city" in record and record["city"] not in cities:
                cities.append(record["city"])
                if len(cities) >= 3:
                    break
        return cities
    
    def get_recent_occasions(self) -> List[str]:
        """获取最近使用的场合"""
        occasions = self.memory["preferences"]["occasions"][:3]
        # 从历史记录补充
        for record in self.memory["history"]:
            if "occasion" in record and record["occasion"] not in occasions:
                occasions.append(record["occasion"])
                if len(occasions) >= 3:
                    break
        return occasions
    
    def get_popular_styles(self) -> List[str]:
        """获取最常用的风格"""
        style_count = {}
        for record in self.memory["history"]:
            if "outfit_suggestion" in record:
                style = record["outfit_suggestion"].get("style")
                if style:
                    style_count[style] = style_count.get(style, 0) + 1
        sorted_styles = sorted(style_count.items(), key=lambda x: x[1], reverse=True)
        return [s[0] for s in sorted_styles[:3]]
    
    # ==================== 智能推荐辅助 ====================
    
    def get_personalized_params(self) -> Dict[str, Any]:
        """
        获取个性化推荐参数
        
        Returns:
            包含城市、场合、风格等参数的字典
        """
        params = {}
        
        # 常用城市（取第一个或默认北京）
        recent_cities = self.get_recent_cities()
        if recent_cities:
            params["city"] = recent_cities[0]
        
        # 常用场合（取第一个或默认日常）
        recent_occasions = self.get_recent_occasions()
        if recent_occasions:
            params["occasion"] = recent_occasions[0]
        
        # 风格偏好
        params["preferred_styles"] = self.memory["preferences"]["styles"]
        
        # 颜色偏好
        params["preferred_colors"] = self.memory["preferences"]["colors"]
        
        # 温度范围
        temp_range = self.memory["preferences"]["temperature_range"]
        if temp_range:
            params["temperature_range"] = temp_range
        
        # 互动次数（用于调整推荐策略）
        params["interactions"] = self.memory["interactions"]
        
        return params
    
    def clear_memory(self) -> None:
        """清空所有记忆"""
        if os.path.exists(self.memory_file):
            os.remove(self.memory_file)
        self.memory = {
            "user_id": self.user_id,
            "created_at": datetime.now().isoformat(),
            "preferences": {
                "cities": [],
                "occasions": [],
                "styles": [],
                "temperature_range": None,
                "colors": [],
                "preferred_brands": []
            },
            "history": [],
            "interactions": 0
        }


# ==================== 全局实例管理 ====================

_memory_instances: Dict[str, UserMemory] = {}

def get_user_memory(user_id: str = "default") -> UserMemory:
    """
    获取用户记忆实例
    
    Args:
        user_id: 用户ID
        
    Returns:
        UserMemory实例
    """
    if user_id not in _memory_instances:
        _memory_instances[user_id] = UserMemory(user_id)
    return _memory_instances[user_id]

def list_all_users() -> List[str]:
    """列出所有有记忆数据的用户"""
    users = []
    for filename in os.listdir(MEMORY_DIR):
        if filename.startswith("user_") and filename.endswith(".json"):
            user_id = filename[5:-5]
            users.append(user_id)
    return users
