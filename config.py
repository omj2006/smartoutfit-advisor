
"""
配置文件 - 智能穿搭推荐系统
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

API_CONFIG = {
    "tongyi_wanxiang": {
        "api_key": os.getenv("TONGYI_API_KEY", "your_tongyi_api_key_here"),
        "endpoint": os.getenv("TONGYI_API_URL", "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis")
    },
    "doubao": {
        "api_key": os.getenv("DOUBAO_API_KEY", "your_doubao_api_key_here"),
        "endpoint": os.getenv("DOUBAO_API_URL", "https://ark.cn-beijing.volces.com/api/v3/images/generations")
    },
    "stable_diffusion": {
        "api_key": os.getenv("SD_API_KEY", "your_sd_api_key_here"),
        "endpoint": os.getenv("SD_ENDPOINT", "http://127.0.0.1:7860/sdapi/v1/txt2img")
    }
}

ECOMMERCE_API_CONFIG = {
    "taobao": {
        "app_key": os.getenv("TAOBAO_APP_KEY", "your_taobao_app_key"),
        "app_secret": os.getenv("TAOBAO_APP_SECRET", "your_taobao_app_secret"),
        "endpoint": os.getenv("TAOBAO_API_URL", "https://eco.taobao.com/router/rest")
    },
    "jd": {
        "app_key": os.getenv("JD_APP_KEY", "your_jd_app_key"),
        "app_secret": os.getenv("JD_APP_SECRET", "your_jd_app_secret"),
        "endpoint": os.getenv("JD_API_URL", "https://api.jd.com/routerjson")
    }
}

VECTOR_MODEL = "all-MiniLM-L6-v2"

TEMPERATURE_RANGES = [
    {"max": 0, "label": "极寒（0℃及以下）"},
    {"min": 0, "max": 10, "label": "寒冷（0-10℃）"},
    {"min": 10, "max": 18, "label": "凉爽（10-18℃）"},
    {"min": 18, "max": 25, "label": "舒适（18-25℃）"},
    {"min": 25, "max": 32, "label": "温暖（25-32℃）"},
    {"min": 32, "label": "炎热（32℃以上）"}
]

OCCASIONS = ["日常", "通勤", "约会", "运动", "聚会"]

FASHION_WEBSITES = [
    "https://www.vogue.com",
    "https://www.harpersbazaar.com",
    "https://www.elle.com"
]
