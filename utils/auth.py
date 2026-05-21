
"""
SmartOutfitAdvisor 用户认证管理器
整合了数据库认证和记忆功能
"""
from typing import Dict, Optional, Any, List
from .database import get_db, DatabaseManager
from .memory_store import UserMemory, get_user_memory

class AuthManager:
    """用户认证管理器"""
    
    def __init__(self):
        self.db = get_db()
        self._current_user: Optional[Dict[str, Any]] = None
    
    def register(self, username: str, password: str, email: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        注册新用户
        
        Returns:
            用户信息 或 None
        """
        user_id = self.db.register_user(username, password, email)
        if user_id:
            user_info = self.db.get_user_by_id(user_id)
            # 初始化用户的JSON记忆文件
            UserMemory(str(user_id))
            return user_info
        return None
    
    def login(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        用户登录
        
        Returns:
            用户信息 或 None
        """
        user_info = self.db.login_user(username, password)
        if user_info:
            self._current_user = user_info
            # 自动同步数据库偏好到JSON记忆
            self._sync_db_to_memory(user_info["user_id"])
            return user_info
        return None
    
    def logout(self):
        """用户退出登录"""
        self._current_user = None
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """获取当前登录用户"""
        return self._current_user
    
    def is_logged_in(self) -> bool:
        """检查是否已登录"""
        return self._current_user is not None
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """获取当前用户的完整偏好（数据库优先）"""
        if not self._current_user:
            return {}
        
        user_id = self._current_user["user_id"]
        db_prefs = self.db.get_user_preferences(user_id)
        
        # 获取个人资料
        profile = self.db.get_user_profile(user_id)
        
        # 合并所有偏好
        return {
            "cities": db_prefs.get("cities", []),
            "occasions": db_prefs.get("occasions", []),
            "styles": db_prefs.get("styles", []),
            "colors": db_prefs.get("colors", []),
            "brands": db_prefs.get("brands", []),
            "temp_range_min": db_prefs.get("temp_range_min"),
            "temp_range_max": db_prefs.get("temp_range_max"),
            "profile": profile
        }
    
    def save_user_preferences(self, **kwargs):
        """保存用户偏好（同时保存到数据库和JSON）"""
        if not self._current_user:
            return
        
        user_id = self._current_user["user_id"]
        
        # 更新数据库
        self.db.update_user_preferences(user_id, **kwargs)
        
        # 同步更新JSON记忆
        memory = get_user_memory(str(user_id))
        if "cities" in kwargs:
            for city in kwargs["cities"]:
                memory.add_city(city)
        if "occasions" in kwargs:
            for occ in kwargs["occasions"]:
                memory.add_occasion(occ)
        if "styles" in kwargs:
            for style in kwargs["styles"]:
                memory.add_style(style)
        if "colors" in kwargs:
            for color in kwargs["colors"]:
                memory.add_color(color)
    
    def add_user_history(self, city: str, occasion: str, weather: str,
                       outfit_suggestion: str, products: List[str]):
        """添加用户历史记录（数据库）"""
        if not self._current_user:
            return
        
        user_id = self._current_user["user_id"]
        self.db.add_history_record(user_id, city, occasion, weather,
                                   outfit_suggestion, products)
    
    def add_user_favorite(self, title: str, outfit_suggestion: str,
                        products: List[str], image_url: Optional[str] = None) -> Optional[int]:
        """添加用户收藏（数据库）"""
        if not self._current_user:
            return None
        
        user_id = self._current_user["user_id"]
        return self.db.add_favorite(user_id, title, outfit_suggestion,
                                   products, image_url)
    
    def get_user_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取用户历史记录"""
        if not self._current_user:
            return []
        
        user_id = self._current_user["user_id"]
        return self.db.get_history_records(user_id, limit)
    
    def get_user_favorites(self) -> List[Dict[str, Any]]:
        """获取用户收藏"""
        if not self._current_user:
            return []
        
        user_id = self._current_user["user_id"]
        return self.db.get_favorites(user_id)
    
    def delete_user_favorite(self, favorite_id: int) -> bool:
        """删除用户收藏"""
        if not self._current_user:
            return False
        
        user_id = self._current_user["user_id"]
        return self.db.delete_favorite(user_id, favorite_id)
    
    def get_user_memory(self) -> Optional[UserMemory]:
        """获取用户JSON记忆实例"""
        if not self._current_user:
            return None
        return get_user_memory(str(self._current_user["user_id"]))
    
    def update_user_profile(self, **kwargs):
        """更新用户个人资料"""
        if not self._current_user:
            return
        
        user_id = self._current_user["user_id"]
        self.db.update_user_profile(user_id, **kwargs)
    
    def get_user_profile(self) -> Dict[str, Any]:
        """获取用户个人资料"""
        if not self._current_user:
            return {}
        
        user_id = self._current_user["user_id"]
        return self.db.get_user_profile(user_id)
    
    def _sync_db_to_memory(self, user_id: int):
        """将数据库偏好同步到JSON记忆"""
        db_prefs = self.db.get_user_preferences(user_id)
        memory = get_user_memory(str(user_id))
        
        # 同步城市
        for city in db_prefs.get("cities", []):
            memory.add_city(city)
        
        # 同步场合
        for occ in db_prefs.get("occasions", []):
            memory.add_occasion(occ)
        
        # 同步风格
        for style in db_prefs.get("styles", []):
            memory.add_style(style)
        
        # 同步颜色
        for color in db_prefs.get("colors", []):
            memory.add_color(color)
        
        # 同步温度范围
        if db_prefs.get("temp_range_min") and db_prefs.get("temp_range_max"):
            memory.set_temperature_range(db_prefs["temp_range_min"], db_prefs["temp_range_max"])

# 全局认证管理器实例
_auth_instance = None

def get_auth() -> AuthManager:
    """获取认证管理器单例"""
    global _auth_instance
    if _auth_instance is None:
        _auth_instance = AuthManager()
    return _auth_instance

