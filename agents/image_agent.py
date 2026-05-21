
"""
图像生成Agent - 完整实现三大绘图API
"""
import os
import requests
import json
import base64
from dotenv import load_dotenv

# 容错导入 tenacity
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
    tenacity_available = False
    print("⚠️  tenacity 模块不可用，重试功能将被禁用")

load_dotenv()


class ImageAgent:
    """图像生成智能体 - 支持通义万相、豆包生图、Stable Diffusion"""
    
    def __init__(self):
        self.name = "图像Agent"
        # 通义万相API
        self.tongyi_api_key = os.getenv("TONGYI_API_KEY", "")
        self.tongyi_api_url = os.getenv("TONGYI_API_URL", "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis")
        self.tongyi_model = os.getenv("TONGYI_MODEL", "wanx-v1")
        # 豆包生图API
        self.doubao_api_key = os.getenv("DOUBAO_API_KEY", "")
        self.doubao_api_url = os.getenv("DOUBAO_API_URL", "https://ark.cn-beijing.volces.com/api/v3/images/generations")
        self.doubao_model = os.getenv("DOUBAO_MODEL", "doubao-v2")
        # Stable Diffusion API
        self.sd_api_key = os.getenv("SD_API_KEY", "")
        self.sd_endpoint = os.getenv("SD_ENDPOINT", "http://127.0.0.1:7860/sdapi/v1/txt2img")
        self.sd_model = os.getenv("SD_MODEL", "v1-5-pruned-emaonly")
        # 配置
        self.timeout = int(os.getenv("API_TIMEOUT", "30"))
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))
    
    def generate_prompt(self, state):
        """
        生成穿搭效果图提示词
        
        Args:
            state: 状态字典
            
        Returns:
            提示词字符串
        """
        suggestion = state.get("outfit_suggestion", {})
        products = state.get("filtered_products", [])
        
        product_names = ""
        if products:
            product_names = ", ".join([p["name"] for p in products[:3]])
        
        prompt = (
            "真人实拍, 全身穿搭, 高清, 自然光影, 场景化, "
            + suggestion.get("suggestion", "时尚穿搭") + ", "
            + product_names + ", "
            + "专业摄影, 8K画质, 真实感强"
        )
        
        return prompt
    
    def _call_tongyi_wanxiang(self, prompt):
        """
        调用通义万相API生成图像
        
        Args:
            prompt: 提示词
            
        Returns:
            图像URL字典 {"url": "...", "success": True/False, "error": "..."}
        """
        if not self.tongyi_api_key or self.tongyi_api_key == "your_tongyi_api_key_here":
            return {"success": False, "error": "通义万相API密钥未配置"}
        
        try:
            headers = {
                "Authorization": "Bearer " + self.tongyi_api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.tongyi_model,
                "input": {
                    "prompt": prompt
                },
                "parameters": {
                    "size": "1024*1024",
                    "n": 1
                }
            }
            
            response = requests.post(
                self.tongyi_api_url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == "Success" and result.get("output", {}).get("results"):
                image_url = result["output"]["results"][0]["url"]
                return {"success": True, "url": image_url, "engine": "tongyi_wanxiang"}
            else:
                error_msg = result.get("message", "通义万相API调用失败")
                return {"success": False, "error": error_msg}
                
        except Exception as e:
            return {"success": False, "error": "通义万相API异常: " + str(e)}
    
    def _call_doubao(self, prompt):
        """
        调用豆包生图API生成图像
        
        Args:
            prompt: 提示词
            
        Returns:
            图像URL字典
        """
        if not self.doubao_api_key or self.doubao_api_key == "your_doubao_api_key_here":
            return {"success": False, "error": "豆包生图API密钥未配置"}
        
        try:
            headers = {
                "Authorization": "Bearer " + self.doubao_api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.doubao_model,
                "prompt": prompt,
                "n": 1,
                "size": "1024x1024"
            }
            
            response = requests.post(
                self.doubao_api_url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("data") and len(result["data"]) > 0:
                image_url = result["data"][0].get("url")
                return {"success": True, "url": image_url, "engine": "doubao"}
            else:
                error_msg = result.get("error", {}).get("message", "豆包生图API调用失败")
                return {"success": False, "error": error_msg}
                
        except Exception as e:
            return {"success": False, "error": "豆包生图API异常: " + str(e)}
    
    def _call_stable_diffusion(self, prompt):
        """
        调用Stable Diffusion WebUI API生成图像
        
        Args:
            prompt: 提示词
            
        Returns:
            图像URL字典（返回base64模拟URL）
        """
        try:
            headers = {"Content-Type": "application/json"}
            payload = {
                "prompt": prompt,
                "negative_prompt": "blurry, low quality, distorted, ugly",
                "steps": 30,
                "cfg_scale": 7,
                "width": 1024,
                "height": 1024,
                "sampler_name": "Euler a",
                "n_iter": 1,
                "batch_size": 1
            }
            
            if self.sd_api_key and self.sd_api_key != "your_sd_api_key_here":
                headers["Authorization"] = "Bearer " + self.sd_api_key
            
            response = requests.post(
                self.sd_endpoint,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("images") and len(result["images"]) > 0:
                # 直接返回base64编码
                base64_image = result["images"][0]
                image_url = "data:image/png;base64," + base64_image
                return {"success": True, "url": image_url, "engine": "stable_diffusion"}
            else:
                return {"success": False, "error": "Stable Diffusion未返回图像"}
                
        except Exception as e:
            return {"success": False, "error": "Stable Diffusion API异常: " + str(e)}
    
    def generate_image(self, state, engine="auto"):
        """
        统一接口生成图像
        
        Args:
            state: 状态字典
            engine: 绘图引擎选择 "tongyi_wanxiang", "doubao", "stable_diffusion", "auto"
            
        Returns:
            更新后的状态
        """
        prompt = self.generate_prompt(state)
        state["image_prompt"] = prompt
        
        result = {"success": False, "error": "", "url": "", "engine": "none"}
        
        # 确定可用引擎优先级
        available_engines = []
        if self.tongyi_api_key and self.tongyi_api_key != "your_tongyi_api_key_here":
            available_engines.append("tongyi_wanxiang")
        if self.doubao_api_key and self.doubao_api_key != "your_doubao_api_key_here":
            available_engines.append("doubao")
        available_engines.append("stable_diffusion")  # SD总是尝试作为备选
        
        # 选择引擎
        selected_engine = engine
        if engine == "auto":
            if available_engines:
                selected_engine = available_engines[0]
            else:
                selected_engine = "none"
        elif engine not in available_engines and engine != "none":
            selected_engine = available_engines[0] if available_engines else "none"
        
        state["selected_engine"] = selected_engine
        
        if selected_engine == "none":
            result["error"] = "无可用绘图引擎，请配置API密钥"
        elif selected_engine == "tongyi_wanxiang":
            print("[" + self.name + "] 使用通义万相生成图像...")
            result = self._call_tongyi_wanxiang(prompt)
        elif selected_engine == "doubao":
            print("[" + self.name + "] 使用豆包生图生成图像...")
            result = self._call_doubao(prompt)
        elif selected_engine == "stable_diffusion":
            print("[" + self.name + "] 使用Stable Diffusion生成图像...")
            result = self._call_stable_diffusion(prompt)
        
        state["image_result"] = result
        
        if result.get("success"):
            print("[" + self.name + "] 图像生成成功: " + result.get("url", "")[:100] + "...")
        else:
            print("[" + self.name + "] 图像生成失败: " + result.get("error", "未知错误"))
        
        return state
    
    def run(self, state):
        """
        执行图像生成（兼容原有接口）
        
        Args:
            state: 状态字典
            
        Returns:
            更新后的状态
        """
        print("[" + self.name + "] 正在生成穿搭效果图提示词...")
        
        prompt = self.generate_prompt(state)
        state["image_prompt"] = prompt
        
        print("[" + self.name + "] 提示词生成完成")
        print("[" + self.name + "] 提示词: " + prompt)
        
        # 检查各API可用性
        state["api_options"] = {
            "tongyi_wanxiang": {
                "available": bool(self.tongyi_api_key and self.tongyi_api_key != "your_tongyi_api_key_here"),
                "api_key": self.tongyi_api_key
            },
            "doubao": {
                "available": bool(self.doubao_api_key and self.doubao_api_key != "your_doubao_api_key_here"),
                "api_key": self.doubao_api_key
            },
            "stable_diffusion": {
                "available": True,  # SD支持本地无密钥模式
                "endpoint": self.sd_endpoint
            }
        }
        
        # 兼容模式：不直接生成图像，留给前端手动触发
        state["image_result"] = {"success": False, "error": "请在前端选择引擎生成图像", "url": "", "engine": "none"}
        
        return state
