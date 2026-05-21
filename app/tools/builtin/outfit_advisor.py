from __future__ import annotations

from typing import Optional

from app.tools.base import BaseTool, register_tool
from app.tools.builtin.image_generator import ImageGeneratorTool
from app.tools.builtin.knowledge_base import KnowledgeBaseTool
from app.tools.builtin.product_search import ProductSearchTool, get_search_engine
from app.tools.builtin.trend_analyzer import TrendAnalyzerTool
from app.tools.builtin.weather_query import WeatherQueryTool


@register_tool
class OutfitAdvisorTool(BaseTool):
    name = "outfit_advisor"
    description = "根据城市天气和场合智能推荐穿搭方案，从商品库中搜索匹配单品，并生成穿搭效果图。会自动查询天气、检索穿搭知识库、搜索推荐商品、生成效果图，给出完整的穿搭方案。"
    parameters = {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "所在城市，如'北京'、'上海'",
            },
            "occasion": {
                "type": "string",
                "description": "场合类型，如'上班'、'约会'、'休闲'、'运动'、'正式晚宴'",
                "default": "休闲",
            },
            "gender": {
                "type": "string",
                "description": "性别偏好，'男'或'女'，可选",
            },
            "style_preference": {
                "type": "string",
                "description": "风格偏好，如'简约'、'文艺'、'街头'、'优雅'，可选",
            },
            "budget": {
                "type": "number",
                "description": "预算上限（元），可选",
            },
        },
        "required": ["city"],
    }

    WEATHER_KEYWORDS = {
        "晴朗": "晴天",
        "大部晴朗": "晴天",
        "多云": "多云",
        "阴天": "阴天",
        "雾": "雾天",
        "小雨": "雨天",
        "中雨": "雨天",
        "大雨": "雨天",
        "阵雨": "雨天",
        "毛毛雨": "雨天",
        "小雪": "雪天",
        "中雪": "雪天",
        "大雪": "雪天",
        "阵雪": "雪天",
        "雷暴": "雨天",
        "冻雨": "雨天",
    }

    OCCASION_MAP = {
        "上班": "商务",
        "工作": "商务",
        "商务": "商务",
        "通勤": "商务",
        "约会": "约会",
        "社交": "约会",
        "休闲": "休闲",
        "日常": "休闲",
        "运动": "运动",
        "户外": "户外",
        "健身": "运动",
        "正式": "正式",
        "晚宴": "正式",
        "宴会": "正式",
    }

    SEASON_MAP = {
        range(3, 6): "春",
        range(6, 9): "夏",
        range(9, 12): "秋",
        range(12, 3): "冬",
    }

    async def execute(
        self,
        city: str = "",
        occasion: str = "休闲",
        gender: str = "",
        style_preference: str = "",
        budget: Optional[float] = None,
        **kwargs,
    ) -> str:
        weather_tool = WeatherQueryTool()
        kb_tool = KnowledgeBaseTool()
        product_tool = ProductSearchTool()

        weather_info = await weather_tool.execute(city=city)

        if "未找到城市" in weather_info or "查询失败" in weather_info or "查询出错" in weather_info:
            return f"无法获取天气信息，请检查城市名称。\n{weather_info}"

        temp = self._extract_temperature(weather_info)
        weather_type = self._extract_weather_type(weather_info)
        season = self._get_season(temp)

        occasion_key = self.OCCASION_MAP.get(occasion, occasion)

        temp_query = "温度穿搭"
        weather_query = self.WEATHER_KEYWORDS.get(weather_type, "")

        queries = [temp_query]
        if weather_query:
            queries.append(f"{weather_query}穿搭")
        if occasion_key:
            queries.append(f"{occasion_key}穿搭")

        all_results = []
        for q in queries:
            result = await kb_tool.execute(query=q, temperature=temp, top_k=2)
            if "未找到" not in result:
                all_results.append(result)

        color_result = await kb_tool.execute(query="色彩搭配", top_k=1)

        trend_tool = TrendAnalyzerTool()
        trend_query = f"{season}季{occasion}穿搭趋势" if season and occasion else f"穿搭趋势 {season or ''} {occasion or ''}"
        trend_result = await trend_tool.execute(
            query=trend_query,
            season=season,
            occasion=occasion_key if occasion_key else occasion,
            style=style_preference,
            depth="quick",
        )

        search_occasion = occasion_key if occasion_key else occasion
        product_results = await self._search_recommended_products(
            product_tool=product_tool,
            temp=temp,
            weather_type=weather_type,
            season=season,
            occasion=search_occasion,
            gender=gender,
            style=style_preference,
            budget=budget,
        )

        outfit_plan = self._generate_outfit_plan(
            city=city,
            weather_info=weather_info,
            temp=temp,
            weather_type=weather_type,
            season=season,
            occasion=occasion,
            gender=gender,
            style_preference=style_preference,
            budget=budget,
            knowledge_results=all_results,
            color_tips=color_result if "未找到" not in color_result else "",
            product_results=product_results,
            trend_result=trend_result,
        )

        image_result = await self._generate_outfit_image(
            product_results=product_results,
            season=season,
            occasion=occasion,
            gender=gender,
            style=style_preference,
            weather=weather_type,
        )

        if image_result:
            outfit_plan += f"\n\n🖼️ 穿搭效果图\n{image_result}"

        return outfit_plan

    async def _search_recommended_products(
        self,
        product_tool: ProductSearchTool,
        temp: float,
        weather_type: str,
        season: str,
        occasion: str,
        gender: str,
        style: str,
        budget: Optional[float],
    ) -> dict:
        results = {}

        categories_to_search = [
            ("上装", f"适合{season}{occasion}的上装"),
            ("下装", f"适合{season}{occasion}的下装"),
            ("鞋履", f"适合{season}{occasion}的鞋子"),
        ]

        if "雨" in weather_type:
            categories_to_search.append(("配饰", "雨天防水配饰雨伞"))
        elif "雪" in weather_type:
            categories_to_search.append(("配饰", "冬季保暖配饰围巾手套帽子"))

        if occasion in ("约会", "正式"):
            categories_to_search.append(("连衣裙", f"适合{occasion}的连衣裙"))

        for category, query in categories_to_search:
            search_result = await product_tool.execute(
                query=query,
                category=category,
                season=season,
                occasion=occasion,
                style=style if style else None,
                gender=gender if gender else None,
                max_price=budget,
                top_k=3,
            )
            if "未找到" not in search_result:
                results[category] = search_result

        return results

    async def _generate_outfit_image(
        self,
        product_results: dict,
        season: str,
        occasion: str,
        gender: str,
        style: str,
        weather: str,
    ) -> Optional[str]:
        try:
            img_tool = ImageGeneratorTool()

            top = ""
            bottom = ""
            dress = ""
            shoes = ""
            accessory = ""

            for category, products_text in product_results.items():
                lines = products_text.split("\n")
                first_item = ""
                for line in lines:
                    line = line.strip()
                    if line and line[0].isdigit() and "." in line[:4]:
                        parts = line.split(".", 1)
                        if len(parts) > 1:
                            name_part = parts[1].strip()
                            paren_idx = name_part.find("(")
                            if paren_idx > 0:
                                first_item = name_part[:paren_idx].strip()
                            else:
                                first_item = name_part.strip()
                            break

                if category == "上装":
                    top = first_item
                elif category == "下装":
                    bottom = first_item
                elif category == "连衣裙":
                    dress = first_item
                elif category == "鞋履":
                    shoes = first_item
                elif category == "配饰":
                    accessory = first_item

            if not top and not dress:
                return None

            result = await img_tool.execute(
                top=top,
                bottom=bottom,
                dress=dress,
                shoes=shoes,
                accessory=accessory,
                style=style if style else None,
                season=season,
                occasion=occasion,
                gender=gender if gender else "女",
                weather=weather,
            )

            if "[IMAGE_URL]" in result:
                return result
            return None
        except Exception as e:
            return None

    def _get_season(self, temp: float) -> str:
        if temp >= 28:
            return "夏"
        elif temp >= 18:
            return "春"
        elif temp >= 5:
            return "秋"
        else:
            return "冬"

    def _extract_temperature(self, weather_info: str) -> float:
        for line in weather_info.split("\n"):
            if "温度:" in line and "体感" not in line:
                try:
                    temp_str = line.split(":")[1].strip().replace("°C", "")
                    return float(temp_str)
                except (ValueError, IndexError):
                    pass
        return 20.0

    def _extract_weather_type(self, weather_info: str) -> str:
        for line in weather_info.split("\n"):
            if "天气:" in line:
                return line.split(":")[1].strip()
        return "晴朗"

    def _generate_outfit_plan(
        self,
        city: str,
        weather_info: str,
        temp: float,
        weather_type: str,
        season: str,
        occasion: str,
        gender: str,
        style_preference: str,
        budget: Optional[float],
        knowledge_results: list,
        color_tips: str,
        product_results: dict,
        trend_result: str = "",
    ) -> str:
        sections = []

        sections.append(f"📍 {city} 当前天气")
        sections.append(weather_info)
        sections.append("")

        sections.append("👗 穿搭推荐方案")
        sections.append(f"场合: {occasion} | 温度: {temp}°C | 天气: {weather_type} | 季节: {season}")
        if gender:
            sections.append(f"性别偏好: {gender}")
        if style_preference:
            sections.append(f"风格偏好: {style_preference}")
        if budget:
            sections.append(f"预算: ¥{budget}")
        sections.append("")

        if temp >= 30:
            sections.append("🔥 高温提醒：选择轻薄透气面料，浅色系为主")
        elif temp >= 25:
            sections.append("☀️ 温暖天气：短袖+薄外套，方便调节")
        elif temp >= 18:
            sections.append("🌤️ 舒适温度：适合各种风格，层次穿搭最佳")
        elif temp >= 10:
            sections.append("🍂 凉爽天气：需要外套，注意早晚温差")
        elif temp >= 0:
            sections.append("❄️ 寒冷天气：厚外套必备，注意保暖")
        else:
            sections.append("🥶 极寒天气：全副武装，保暖第一")

        if "雨" in weather_type or "阵雨" in weather_type:
            sections.append("🌧️ 雨天提醒：选防水面料，避免布鞋和浅色鞋")
        elif "雪" in weather_type:
            sections.append("🌨️ 雪天提醒：防滑鞋+保暖装备，深色衣物更出片")

        sections.append("")

        if product_results:
            sections.append("🛍️ 推荐单品")
            for category, products in product_results.items():
                sections.append(f"\n--- {category} ---\n{products}")

        if trend_result:
            sections.append(f"\n📊 潮流趋势\n{trend_result}")

        if knowledge_results:
            sections.append("\n📚 穿搭知识参考")
            for i, result in enumerate(knowledge_results, 1):
                sections.append(f"\n--- 参考 {i} ---\n{result}")

        if color_tips:
            sections.append(f"\n🎨 色彩搭配提示\n{color_tips}")

        return "\n".join(sections)
