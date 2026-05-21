
"""
AI穿搭效果图生成模块
"""
import requests
import base64
from typing import Dict, Optional
from config import API_CONFIG
from PIL import Image
import io


def generate_prompt(outfit_suggestion: Dict, style: str = "真人实拍") -> str:
    """
    生成文生图提示词
    
    Args:
        outfit_suggestion: 穿搭建议字典
        style: 风格
        
    Returns:
        完整提示词
    """
    prompt_parts = [
        style,
        "全身穿搭",
        "高清照片",
        "自然光影",
        "场景化",
        f"场景：{outfit_suggestion.get('occasion', '日常')}",
        f"穿搭：{outfit_suggestion.get('suggestion', '')}",
        "专业时尚摄影",
        "8k分辨率",
        "细节丰富"
    ]
    
    return ", ".join(prompt_parts)


class ImageGenerator:
    def __init__(self, platform: str = "tongyi_wanxiang"):
        self.platform = platform
        self.config = API_CONFIG.get(platform, {})
        
    def generate(self, prompt: str) -> Optional[bytes]:
        """
        生成图像
        
        Args:
            prompt: 提示词
            
        Returns:
            图像字节数据
        """
        try:
            if self.platform == "tongyi_wanxiang":
                return self._generate_tongyi(prompt)
            elif self.platform == "doubao":
                return self._generate_doubao(prompt)
            elif self.platform == "stable_diffusion":
                return self._generate_sd(prompt)
            else:
                print(f"不支持的平台: {self.platform}")
                return None
        except Exception as e:
            print(f"图像生成失败: {e}")
            return None
            
    def _generate_tongyi(self, prompt: str) -> Optional[bytes]:
        """通义万相API"""
        if self.config.get("api_key") == "your_tongyi_api_key_here":
            print("请配置通义万相API密钥")
            return None
            
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "wanx-v1",
            "input": {
                "prompt": prompt
            },
            "parameters": {
                "size": "1024*1024",
                "n": 1
            }
        }
        
        response = requests.post(self.config["endpoint"], headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        if "output" in result and "results" in result["output"]:
            img_url = result["output"]["results"][0]["url"]
            img_response = requests.get(img_url)
            return img_response.content
        return None
        
    def _generate_doubao(self, prompt: str) -> Optional[bytes]:
        """豆包生图API"""
        if self.config.get("api_key") == "your_doubao_api_key_here":
            print("请配置豆包API密钥")
            return None
            
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "ep-20241212123456-abcde",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024"
        }
        
        response = requests.post(self.config["endpoint"], headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        if "data" in result and len(result["data"]) > 0:
            img_url = result["data"][0]["url"]
            img_response = requests.get(img_url)
            return img_response.content
        return None
        
    def _generate_sd(self, prompt: str) -> Optional[bytes]:
        """Stable Diffusion API"""
        if self.config.get("api_key") == "your_sd_api_key_here":
            print("请配置Stable Diffusion API密钥")
            return None
            
        data = {
            "prompt": prompt,
            "negative_prompt": "bad quality, blurry, distorted",
            "steps": 20,
            "width": 512,
            "height": 512
        }
        
        response = requests.post(self.config["endpoint"], json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        if "images" in result and len(result["images"]) > 0:
            img_data = base64.b64decode(result["images"][0])
            return img_data
        return None


def create_demo_prompt():
    """创建演示用提示词"""
    return "真人实拍,全身穿搭,高清照片,自然光影,场景化,场景：日常,穿搭：白色T恤+蓝色牛仔裤+帆布鞋,专业时尚摄影,8k分辨率,细节丰富"


if __name__ == "__main__":
    prompt = create_demo_prompt()
    print(f"生成提示词:\n{prompt}\n")
    print("注意：需要配置API密钥才能生成实际图像")

