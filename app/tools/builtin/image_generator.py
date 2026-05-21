from __future__ import annotations

import base64
import logging
import os
import urllib.parse
import uuid
from typing import Optional

import httpx

from app.config import settings
from app.tools.base import BaseTool, register_tool

logger = logging.getLogger(__name__)

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "generated_images")
IMAGES_DIR = os.path.abspath(IMAGES_DIR)

os.makedirs(IMAGES_DIR, exist_ok=True)


def _build_outfit_prompt(
    top: str = "",
    bottom: str = "",
    dress: str = "",
    shoes: str = "",
    accessory: str = "",
    style: str = "",
    season: str = "",
    occasion: str = "",
    gender: str = "female",
    weather: str = "",
) -> str:
    parts = []

    if dress:
        parts.append(f"wearing {dress}")
    else:
        clothing_parts = []
        if top:
            clothing_parts.append(top)
        if bottom:
            clothing_parts.append(bottom)
        if clothing_parts:
            parts.append(f"wearing {' and '.join(clothing_parts)}")

    if shoes:
        parts.append(f"with {shoes}")
    if accessory:
        parts.append(f"accessorized with {accessory}")

    outfit_desc = ", ".join(parts) if parts else "stylish modern outfit"

    scene_parts = []
    if occasion == "约会":
        scene_parts.append("romantic cafe setting")
    elif occasion in ("商务", "上班", "通勤"):
        scene_parts.append("modern office setting")
    elif occasion in ("休闲", "日常"):
        scene_parts.append("casual street setting")
    elif occasion == "运动":
        scene_parts.append("outdoor park setting")
    elif occasion in ("正式", "晚宴"):
        scene_parts.append("elegant evening setting")
    elif occasion == "户外":
        scene_parts.append("outdoor nature setting")

    if weather and "雨" in weather:
        scene_parts.append("rainy day atmosphere")
    elif weather and "雪" in weather:
        scene_parts.append("snowy winter scene")

    if season == "夏":
        scene_parts.append("bright summer lighting")
    elif season == "冬":
        scene_parts.append("warm winter lighting")

    scene = ", ".join(scene_parts) if scene_parts else "clean studio background"

    gender_str = "woman" if gender == "女" else "man"

    style_str = ""
    if style:
        style_map = {
            "简约": "minimalist",
            "休闲": "casual",
            "优雅": "elegant",
            "通勤": "business casual",
            "街头": "streetwear",
            "运动": "athleisure",
            "文艺": "artsy",
            "经典": "classic",
            "浪漫": "romantic",
            "性感": "sensual",
        }
        style_str = f", {style_map.get(style, style)} style"

    prompt = (
        f"Full body fashion photo of a stylish {gender_str} {outfit_desc}{style_str}, "
        f"standing pose, {scene}, "
        f"professional fashion photography, high quality, detailed, "
        f"realistic, editorial style, 8k"
    )

    return prompt


async def _generate_with_wanx(prompt: str) -> Optional[str]:
    api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    if not api_key:
        return None
    try:
        import dashscope
        from dashscope import ImageSynthesis

        dashscope.api_key = api_key
        response = ImageSynthesis.call(
            model="wanx-v1",
            prompt=prompt,
            n=1,
            size="512*768",
        )
        if response.status_code == 200 and response.output and response.output.results:
            url = response.output.results[0].url
            async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
                img_resp = await client.get(url, timeout=30.0)
                if img_resp.status_code == 200:
                    filename = f"{uuid.uuid4().hex}.png"
                    filepath = os.path.join(IMAGES_DIR, filename)
                    with open(filepath, "wb") as f:
                        f.write(img_resp.content)
                    return f"/images/{filename}"
        logger.error(f"Wanx API error: {response.code} {response.message}")
        return None
    except Exception as e:
        logger.error(f"Wanx generation failed: {e}")
        return None


async def _generate_with_doubao(prompt: str) -> Optional[str]:
    access_key = os.environ.get("VOLC_ACCESSKEY", "")
    secret_key = os.environ.get("VOLC_SECRETKEY", "")
    if not access_key or not secret_key:
        return None
    try:
        from volcengine.visual.VisualService import VisualService

        visual_service = VisualService()
        visual_service.set_ak(access_key)
        visual_service.set_sk(secret_key)

        form = {
            "req_key": "high_aes_general_v21",
            "prompt": prompt,
            "width": 512,
            "height": 768,
            "return_url": True,
        }
        response = visual_service.cv_process2(form)
        data = response.get("data", {})
        image_urls = data.get("image_urls", [])
        if image_urls:
            url = image_urls[0]
            async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
                img_resp = await client.get(url, timeout=30.0)
                if img_resp.status_code == 200:
                    filename = f"{uuid.uuid4().hex}.png"
                    filepath = os.path.join(IMAGES_DIR, filename)
                    with open(filepath, "wb") as f:
                        f.write(img_resp.content)
                    return f"/images/{filename}"
        logger.error(f"Doubao API error: {response}")
        return None
    except Exception as e:
        logger.error(f"Doubao generation failed: {e}")
        return None


async def _generate_with_sd_api(prompt: str, api_url: str = "http://127.0.0.1:7860") -> Optional[str]:
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                f"{api_url}/sdapi/v1/txt2img",
                json={
                    "prompt": prompt,
                    "negative_prompt": "low quality, blurry, deformed, ugly, bad anatomy",
                    "steps": 25,
                    "width": 512,
                    "height": 768,
                    "cfg_scale": 7,
                },
            )

            if resp.status_code != 200:
                logger.error(f"SD API error: {resp.status_code}")
                return None

            data = resp.json()
            if "images" in data and data["images"]:
                img_data = base64.b64decode(data["images"][0])
                filename = f"{uuid.uuid4().hex}.png"
                filepath = os.path.join(IMAGES_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(img_data)
                return f"/images/{filename}"

            return None
    except Exception as e:
        logger.error(f"SD API generation failed: {e}")
        return None


async def _generate_with_pollinations(prompt: str) -> Optional[str]:
    try:
        encoded_prompt = urllib.parse.quote(prompt, safe="")
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=768&nologo=true"
        async with httpx.AsyncClient(timeout=120.0, follow_redirects=True) as client:
            img_resp = await client.get(url, timeout=120.0)
            if img_resp.status_code == 200:
                content_type = img_resp.headers.get("content-type", "")
                if "image" in content_type or len(img_resp.content) > 1024:
                    filename = f"{uuid.uuid4().hex}.png"
                    filepath = os.path.join(IMAGES_DIR, filename)
                    with open(filepath, "wb") as f:
                        f.write(img_resp.content)
                    return f"/images/{filename}"
        logger.error(f"Pollinations API error: {img_resp.status_code}")
        return None
    except Exception as e:
        logger.error(f"Pollinations generation failed: {e}")
        return None


@register_tool
class ImageGeneratorTool(BaseTool):
    name = "image_generator"
    description = "根据穿搭描述生成穿搭效果图。支持通义万相、豆包生图、Stable Diffusion 和 Pollinations 图像生成。输入穿搭单品描述，自动构建 prompt 并生成时尚穿搭效果图。"
    parameters = {
        "type": "object",
        "properties": {
            "top": {
                "type": "string",
                "description": "上装描述，如'白色衬衫'、'灰色卫衣'",
            },
            "bottom": {
                "type": "string",
                "description": "下装描述，如'深蓝色牛仔裤'、'黑色半身裙'",
            },
            "dress": {
                "type": "string",
                "description": "连衣裙描述（如有则替代上装+下装），如'粉色连衣裙'",
            },
            "shoes": {
                "type": "string",
                "description": "鞋子描述，如'白色运动鞋'、'黑色短靴'",
            },
            "accessory": {
                "type": "string",
                "description": "配饰描述，如'遮阳帽和墨镜'、'围巾和手套'",
            },
            "style": {
                "type": "string",
                "description": "风格：简约/休闲/优雅/通勤/街头/运动/文艺/经典/浪漫/性感",
            },
            "season": {
                "type": "string",
                "description": "季节：春/夏/秋/冬",
            },
            "occasion": {
                "type": "string",
                "description": "场合：商务/休闲/约会/运动/正式/户外",
            },
            "gender": {
                "type": "string",
                "description": "性别：男/女，默认女",
                "default": "女",
            },
            "weather": {
                "type": "string",
                "description": "天气描述，如'小雨'、'晴朗'、'大雪'",
            },
            "custom_prompt": {
                "type": "string",
                "description": "自定义图像生成 prompt（高级用法，会覆盖自动构建的 prompt）",
            },
        },
        "required": [],
    }

    async def execute(
        self,
        top: str = "",
        bottom: str = "",
        dress: str = "",
        shoes: str = "",
        accessory: str = "",
        style: str = "",
        season: str = "",
        occasion: str = "",
        gender: str = "女",
        weather: str = "",
        custom_prompt: str = "",
        **kwargs,
    ) -> str:
        if custom_prompt:
            prompt = custom_prompt
        else:
            prompt = _build_outfit_prompt(
                top=top,
                bottom=bottom,
                dress=dress,
                shoes=shoes,
                accessory=accessory,
                style=style,
                season=season,
                occasion=occasion,
                gender=gender,
                weather=weather,
            )

        logger.info(f"Generating outfit image with prompt: {prompt[:100]}...")

        image_url = None
        backend_used = ""

        image_url = await _generate_with_wanx(prompt)
        if image_url:
            backend_used = "通义万相"

        if image_url is None:
            image_url = await _generate_with_doubao(prompt)
            if image_url:
                backend_used = "豆包生图"

        if image_url is None:
            image_url = await _generate_with_sd_api(prompt)
            if image_url:
                backend_used = "Stable Diffusion"

        if image_url is None:
            image_url = await _generate_with_pollinations(prompt)
            if image_url:
                backend_used = "Pollinations.ai"

        if image_url:
            outfit_desc_parts = []
            if dress:
                outfit_desc_parts.append(dress)
            else:
                if top:
                    outfit_desc_parts.append(top)
                if bottom:
                    outfit_desc_parts.append(bottom)
            if shoes:
                outfit_desc_parts.append(shoes)
            if accessory:
                outfit_desc_parts.append(accessory)

            outfit_desc = " + ".join(outfit_desc_parts) if outfit_desc_parts else "穿搭方案"

            return (
                f"✅ 穿搭效果图已生成！\n"
                f"搭配: {outfit_desc}\n"
                f"风格: {style or '自动'} | 场合: {occasion or '通用'} | 季节: {season or '通用'}\n"
                f"生成引擎: {backend_used}\n"
                f"图片链接: {image_url}\n"
                f"[IMAGE_URL]{image_url}[/IMAGE_URL]"
            )
        else:
            return (
                f"⚠️ 图像生成暂时不可用。\n"
                f"生成 Prompt: {prompt}\n"
                f"请确保配置了以下任一图像生成服务：\n"
                f"1. 通义万相（设置 DASHSCOPE_API_KEY 环境变量）\n"
                f"2. 豆包生图（设置 VOLC_ACCESSKEY 和 VOLC_SECRETKEY 环境变量）\n"
                f"3. 本地 Stable Diffusion WebUI（http://127.0.0.1:7860）\n"
                f"4. Pollinations.ai（免费无需 key，请检查网络连接）"
            )
