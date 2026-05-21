
"""
电商对接工具模块
支持淘宝、京东开放API，本地静态数据库作为备用
"""
import os
import requests
import hashlib
import time
from dotenv import load_dotenv

# 容错导入 tenacity
tenacity_available = False
try:
    from tenacity import retry, stop_after_attempt, wait_exponential
    tenacity_available = True
except ImportError:
    # 创建兼容的装饰器
    def retry(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    stop_after_attempt = lambda x: None
    wait_exponential = lambda **kwargs: None
    print("⚠️  tenacity 模块不可用，重试功能将被禁用")

from utils.db_tools import PRODUCTS, filter_products

load_dotenv()


class EcommerceAPI:
    """电商API统一接口"""
    
    def __init__(self):
        # 淘宝配置
        self.taobao_app_key = os.getenv("TAOBAO_APP_KEY", "")
        self.taobao_app_secret = os.getenv("TAOBAO_APP_SECRET", "")
        self.taobao_api_url = os.getenv("TAOBAO_API_URL", "https://eco.taobao.com/router/rest")
        # 京东配置
        self.jd_app_key = os.getenv("JD_APP_KEY", "")
        self.jd_app_secret = os.getenv("JD_APP_SECRET", "")
        self.jd_api_url = os.getenv("JD_API_URL", "https://api.jd.com/routerjson")
        # 配置
        self.timeout = int(os.getenv("API_TIMEOUT", "30"))
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))
        self.debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
    
    def _taobao_sign(self, params):
        """
        生成淘宝API签名
        
        Args:
            params: 请求参数字典
            
        Returns:
            签名值
        """
        sorted_params = sorted(params.items())
        sign_str = self.taobao_app_secret + "".join([k + str(v) for k, v in sorted_params]) + self.taobao_app_secret
        sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()
        return sign
    
    def _call_taobao_api(self, method, params):
        """
        调用淘宝开放API
        
        Args:
            method: API方法名
            params: 请求参数
            
        Returns:
            API响应结果
        """
        if not self.taobao_app_key or self.taobao_app_key == "your_taobao_app_key_here":
            raise Exception("淘宝API密钥未配置")
        
        common_params = {
            "method": method,
            "app_key": self.taobao_app_key,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "format": "json",
            "v": "2.0",
            "sign_method": "md5"
        }
        all_params = {**common_params, **params}
        all_params["sign"] = self._taobao_sign(all_params)
        
        response = requests.get(self.taobao_api_url, params=all_params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def search_taobao_products(self, keyword, min_temp=None, max_temp=None, occasion=None, limit=10):
        """
        搜索淘宝商品（预留实现）
        
        Args:
            keyword: 搜索关键词
            min_temp: 最低温度
            max_temp: 最高温度
            occasion: 场合
            limit: 返回数量
            
        Returns:
            商品列表
        """
        try:
            # 实际API调用示例（保留结构）
            """
            params = {
                "q": keyword,
                "page_size": limit,
                "page_no": 1
            }
            result = self._call_taobao_api("taobao.tbk.item.get", params)
            if result.get("tbk_item_get_response"):
                items = result["tbk_item_get_response"].get("results", {}).get("n_tbk_item", [])
                return self._convert_taobao_items(items)
            """
            raise Exception("淘宝API功能预留")
        except Exception as e:
            print("[电商API] 淘宝搜索失败: " + str(e))
            return None
    
    def _convert_taobao_items(self, items):
        """
        转换淘宝商品格式为系统统一格式
        
        Args:
            items: 淘宝原始商品列表
            
        Returns:
            转换后的商品列表
        """
        converted = []
        for item in items:
            converted.append({
                "id": item.get("num_iid", 0),
                "source": "taobao",
                "name": item.get("title", ""),
                "description": item.get("nick", ""),
                "price": item.get("price", 0),
                "image_url": item.get("pict_url", ""),
                "item_url": item.get("click_url", ""),
                "min_temp": 10,
                "max_temp": 30,
                "weather": ["晴", "多云", "阴"],
                "occasions": ["日常", "通勤"],
                "sales": item.get("volume", 0)
            })
        return converted
    
    def _call_jd_api(self, method, params):
        """
        调用京东开放API
        
        Args:
            method: API方法名
            params: 请求参数
            
        Returns:
            API响应结果
        """
        if not self.jd_app_key or self.jd_app_key == "your_jd_app_key_here":
            raise Exception("京东API密钥未配置")
        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        sign_str = self.jd_app_secret + method + timestamp + str(sorted(params.items())) + self.jd_app_secret
        sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()
        
        all_params = {
            "method": method,
            "app_key": self.jd_app_key,
            "timestamp": timestamp,
            "sign": sign,
            "format": "json",
            "v": "2.0"
        }
        all_params.update(params)
        
        response = requests.get(self.jd_api_url, params=all_params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def search_jd_products(self, keyword, min_temp=None, max_temp=None, occasion=None, limit=10):
        """
        搜索京东商品（预留实现）
        
        Args:
            keyword: 搜索关键词
            min_temp: 最低温度
            max_temp: 最高温度
            occasion: 场合
            limit: 返回数量
            
        Returns:
            商品列表
        """
        try:
            # 实际API调用示例（保留结构）
            """
            params = {
                "keyword": keyword,
                "pageIndex": 1,
                "pageSize": limit
            }
            result = self._call_jd_api("jd.union.open.goods.query", params)
            return self._convert_jd_items(result)
            """
            raise Exception("京东API功能预留")
        except Exception as e:
            print("[电商API] 京东搜索失败: " + str(e))
            return None
    
    def _convert_jd_items(self, items):
        """
        转换京东商品格式为系统统一格式
        
        Args:
            items: 京东原始商品列表
            
        Returns:
            转换后的商品列表
        """
        converted = []
        # 结构保留
        return converted
    
    def search_products(self, keyword, min_temp=None, max_temp=None, occasion=None, weather=None, limit=10, prefer_platform=None):
        """
        统一商品搜索接口（优先使用电商API，失败后回退本地库）
        
        Args:
            keyword: 搜索关键词
            min_temp: 最低温度
            max_temp: 最高温度
            occasion: 场合
            weather: 天气
            limit: 返回数量
            prefer_platform: 优先平台 "taobao", "jd", "local"
            
        Returns:
            商品列表
        """
        # 温度处理
        if min_temp is None:
            min_temp = 10
        if max_temp is None:
            max_temp = 30
        
        platforms = []
        if prefer_platform == "taobao":
            platforms = ["taobao", "jd", "local"]
        elif prefer_platform == "jd":
            platforms = ["jd", "taobao", "local"]
        else:
            platforms = ["taobao", "jd", "local"]
        
        for platform in platforms:
            try:
                if platform == "taobao":
                    result = self.search_taobao_products(keyword, min_temp, max_temp, occasion, limit)
                    if result is not None:
                        print("[电商API] 使用淘宝商品数据")
                        return result, "taobao"
                elif platform == "jd":
                    result = self.search_jd_products(keyword, min_temp, max_temp, occasion, limit)
                    if result is not None:
                        print("[电商API] 使用京东商品数据")
                        return result, "jd"
                elif platform == "local":
                    print("[电商API] 使用本地商品数据库")
                    return self._get_local_products(min_temp, max_temp, occasion, weather, limit), "local"
            except Exception as e:
                print("[电商API] " + platform + " 搜索异常: " + str(e))
                continue
        
        # 兜底
        return self._get_local_products(min_temp, max_temp, occasion, weather, limit), "local"
    
    def _get_local_products(self, min_temp, max_temp, occasion, weather, limit):
        """
        从本地数据库获取商品
        
        Args:
            min_temp: 最低温度
            max_temp: 最高温度
            occasion: 场合
            weather: 天气
            limit: 返回数量
            
        Returns:
            本地商品列表
        """
        temp = (min_temp + max_temp) / 2
        filtered = filter_products(temp, occasion, weather)
        return filtered[:limit]


# 全局实例
_ecommerce_api = None

def get_ecommerce_api():
    """获取电商API单例"""
    global _ecommerce_api
    if _ecommerce_api is None:
        _ecommerce_api = EcommerceAPI()
    return _ecommerce_api
