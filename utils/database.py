
"""
SmartOutfitAdvisor 数据库管理模块
使用 SQLite 本地存储用户账号和数据
"""
import sqlite3
import hashlib
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "smartoutfit.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_database():
    """初始化数据库，创建所有必要的表"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. 用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        last_login TEXT
    )
    ''')
    
    # 2. 用户个人资料表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_profiles (
        profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        height REAL,
        weight REAL,
        gender TEXT,
        age INTEGER,
        style_preferences TEXT,
        color_preferences TEXT,
        temp_preference TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    # 3. 记忆偏好表（与现有JSON记忆功能整合）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_preferences (
        pref_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        cities TEXT,
        occasions TEXT,
        styles TEXT,
        colors TEXT,
        brands TEXT,
        temp_range_min INTEGER,
        temp_range_max INTEGER,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    # 4. 历史记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS history_records (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        city TEXT,
        occasion TEXT,
        weather TEXT,
        outfit_suggestion TEXT,
        products TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    # 5. 穿搭收藏表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS favorites (
        favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT,
        outfit_suggestion TEXT,
        products TEXT,
        image_url TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    """密码加密（使用SHA256 + 简单salt）"""
    salt = "smartoutfit_2024"
    return hashlib.sha256((password + salt).encode()).hexdigest()

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self):
        init_database()
    
    def _get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(DB_PATH)
    
    # ================ 用户认证 ================
    
    def register_user(self, username: str, password: str, email: Optional[str] = None) -> Optional[int]:
        """
        注册新用户
        
        Returns:
            user_id 或 None（如果注册失败）
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            password_hash = hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            user_id = cursor.lastrowid
            conn.commit()
            
            # 初始化用户资料和偏好
            self._init_user_profile(user_id)
            self._init_user_preferences(user_id)
            
            return user_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def login_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        用户登录
        
        Returns:
            用户信息字典 或 None
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        cursor.execute(
            "SELECT user_id, username, email FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        result = cursor.fetchone()
        
        if result:
            user_id = result[0]
            # 更新最后登录时间
            cursor.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = ?",
                (user_id,)
            )
            conn.commit()
            
            user_info = {
                "user_id": user_id,
                "username": result[1],
                "email": result[2]
            }
            conn.close()
            return user_info
        else:
            conn.close()
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取用户信息"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT user_id, username, email, created_at, last_login FROM users WHERE user_id = ?",
            (user_id,)
        )
        result = cursor.fetchone()
        
        if result:
            user_info = {
                "user_id": result[0],
                "username": result[1],
                "email": result[2],
                "created_at": result[3],
                "last_login": result[4]
            }
            conn.close()
            return user_info
        else:
            conn.close()
            return None
    
    # ================ 用户资料 ================
    
    def _init_user_profile(self, user_id: int):
        """初始化新用户资料"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_profiles (user_id) VALUES (?)",
            (user_id,)
        )
        conn.commit()
        conn.close()
    
    def _init_user_preferences(self, user_id: int):
        """初始化新用户偏好"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_preferences (user_id) VALUES (?)",
            (user_id,)
        )
        conn.commit()
        conn.close()
    
    def get_user_profile(self, user_id: int) -> Dict[str, Any]:
        """获取用户个人资料"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM user_profiles WHERE user_id = ?",
            (user_id,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "profile_id": result[0],
                "user_id": result[1],
                "height": result[2],
                "weight": result[3],
                "gender": result[4],
                "age": result[5],
                "style_preferences": result[6],
                "color_preferences": result[7],
                "temp_preference": result[8]
            }
        return {}
    
    def update_user_profile(self, user_id: int, **kwargs):
        """更新用户个人资料"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        update_fields = []
        update_values = []
        for key, value in kwargs.items():
            if key in ["height", "weight", "gender", "age", "style_preferences", "color_preferences", "temp_preference"]:
                update_fields.append(f"{key} = ?")
                update_values.append(value)
        
        if update_fields:
            update_values.append(user_id)
            cursor.execute(
                f"UPDATE user_profiles SET {', '.join(update_fields)} WHERE user_id = ?",
                update_values
            )
            conn.commit()
        conn.close()
    
    # ================ 用户偏好（与JSON记忆整合） ================
    
    def get_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """获取用户偏好"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM user_preferences WHERE user_id = ?",
            (user_id,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            prefs = {
                "pref_id": result[0],
                "user_id": result[1],
                "cities": self._parse_text_list(result[2]),
                "occasions": self._parse_text_list(result[3]),
                "styles": self._parse_text_list(result[4]),
                "colors": self._parse_text_list(result[5]),
                "brands": self._parse_text_list(result[6]),
                "temp_range_min": result[7],
                "temp_range_max": result[8],
                "updated_at": result[9]
            }
            return prefs
        return {}
    
    def update_user_preferences(self, user_id: int, **kwargs):
        """更新用户偏好"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        update_fields = []
        update_values = []
        for key, value in kwargs.items():
            if key in ["cities", "occasions", "styles", "colors", "brands"]:
                update_fields.append(f"{key} = ?")
                update_values.append(self._join_text_list(value))
            elif key in ["temp_range_min", "temp_range_max"]:
                update_fields.append(f"{key} = ?")
                update_values.append(value)
        
        if update_fields:
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            update_values.append(user_id)
            cursor.execute(
                f"UPDATE user_preferences SET {', '.join(update_fields)} WHERE user_id = ?",
                update_values
            )
            conn.commit()
        conn.close()
    
    def add_city_to_preferences(self, user_id: int, city: str):
        """添加常用城市"""
        prefs = self.get_user_preferences(user_id)
        cities = prefs.get("cities", [])
        if city not in cities:
            cities.append(city)
            self.update_user_preferences(user_id, cities=cities)
    
    def add_occasion_to_preferences(self, user_id: int, occasion: str):
        """添加常用场合"""
        prefs = self.get_user_preferences(user_id)
        occasions = prefs.get("occasions", [])
        if occasion not in occasions:
            occasions.append(occasion)
            self.update_user_preferences(user_id, occasions=occasions)
    
    def add_style_to_preferences(self, user_id: int, style: str):
        """添加风格偏好"""
        prefs = self.get_user_preferences(user_id)
        styles = prefs.get("styles", [])
        if style not in styles:
            styles.append(style)
            self.update_user_preferences(user_id, styles=styles)
    
    def add_color_to_preferences(self, user_id: int, color: str):
        """添加颜色偏好"""
        prefs = self.get_user_preferences(user_id)
        colors = prefs.get("colors", [])
        if color not in colors:
            colors.append(color)
            self.update_user_preferences(user_id, colors=colors)
    
    # ================ 历史记录 ================
    
    def add_history_record(self, user_id: int, city: str, occasion: str, weather: str,
                          outfit_suggestion: str, products: List[str]):
        """添加历史记录"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        products_str = self._join_text_list(products)
        cursor.execute(
            """INSERT INTO history_records (user_id, city, occasion, weather, outfit_suggestion, products)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, city, occasion, weather, outfit_suggestion, products_str)
        )
        conn.commit()
        conn.close()
    
    def get_history_records(self, user_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        """获取用户历史记录"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT record_id, city, occasion, weather, outfit_suggestion, products, created_at
               FROM history_records WHERE user_id = ? ORDER BY created_at DESC LIMIT ?""",
            (user_id, limit)
        )
        results = cursor.fetchall()
        conn.close()
        
        records = []
        for row in results:
            records.append({
                "record_id": row[0],
                "city": row[1],
                "occasion": row[2],
                "weather": row[3],
                "outfit_suggestion": row[4],
                "products": self._parse_text_list(row[5]),
                "created_at": row[6]
            })
        return records
    
    # ================ 收藏管理 ================
    
    def add_favorite(self, user_id: int, title: str, outfit_suggestion: str,
                     products: List[str], image_url: Optional[str] = None):
        """添加收藏"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        products_str = self._join_text_list(products)
        cursor.execute(
            """INSERT INTO favorites (user_id, title, outfit_suggestion, products, image_url)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, title, outfit_suggestion, products_str, image_url)
        )
        favorite_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return favorite_id
    
    def get_favorites(self, user_id: int) -> List[Dict[str, Any]]:
        """获取用户收藏"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT favorite_id, title, outfit_suggestion, products, image_url, created_at
               FROM favorites WHERE user_id = ? ORDER BY created_at DESC""",
            (user_id,)
        )
        results = cursor.fetchall()
        conn.close()
        
        favorites = []
        for row in results:
            favorites.append({
                "favorite_id": row[0],
                "title": row[1],
                "outfit_suggestion": row[2],
                "products": self._parse_text_list(row[3]),
                "image_url": row[4],
                "created_at": row[5]
            })
        return favorites
    
    def delete_favorite(self, user_id: int, favorite_id: int) -> bool:
        """删除收藏"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "DELETE FROM favorites WHERE user_id = ? AND favorite_id = ?",
            (user_id, favorite_id)
        )
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    
    # ================ 辅助方法 ================
    
    def _parse_text_list(self, text: Optional[str]) -> List[str]:
        """解析逗号分隔的字符串为列表"""
        if not text:
            return []
        return [item.strip() for item in text.split(",") if item.strip()]
    
    def _join_text_list(self, items: List[str]) -> str:
        """将列表连接为逗号分隔的字符串"""
        if not items:
            return ""
        return ", ".join(items)

# 全局数据库实例
_db_instance = None

def get_db() -> DatabaseManager:
    """获取数据库管理器单例"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
    return _db_instance

# 初始化数据库
init_database()

