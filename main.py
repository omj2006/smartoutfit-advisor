
"""
SmartOutfitAdvisor - 智能穿搭推荐系统
主入口文件（兼容新旧模式）
"""
import sys
import subprocess


def install_dependencies():
    """自动安装依赖"""
    print("正在检查/安装依赖...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("依赖安装完成")
    except Exception as e:
        print("依赖安装失败:", e)


# 导入 - 优先新工作流，回退旧智能体
try:
    from agents.outfit_workflow import get_outfit_workflow
    NEW_MODE = True
    print("✅ 使用LangGraph多智能体工作流模式")
except:
    from agents.weather_agent import WeatherAgent
    from agents.knowledge_agent import KnowledgeAgent
    from agents.retrieval_agent import RetrievalAgent
    from agents.image_agent import ImageAgent
    from agents.trend_agent import TrendAgent
    NEW_MODE = False
    print("⚠️ 使用传统智能体模式")


class SmartOutfitAdvisorLegacy:
    """智能穿搭推荐系统主类（传统模式，保持兼容性）"""
    
    def __init__(self):
        self.weather_agent = WeatherAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.retrieval_agent = RetrievalAgent()
        self.image_agent = ImageAgent()
        self.trend_agent = TrendAgent()
    
    def run(self, city="Beijing", occasion="日常", user_query=""):
        """
        运行完整流程
        
        Args:
            city: 城市
            occasion: 场合
            user_query: 用户额外需求
        """
        print("\n" + "="*60)
        print("           SmartOutfitAdvisor - 智能穿搭推荐系统")
        print("="*60 + "\n")
        
        state = {
            "city": city,
            "occasion": occasion,
            "user_query": user_query
        }
        
        state = self.weather_agent.run(state)
        print("")
        
        state = self.knowledge_agent.run(state)
        print("")
        
        state = self.retrieval_agent.run(state)
        print("")
        
        state = self.image_agent.run(state)
        print("")
        
        state = self.trend_agent.run(state)
        print("")
        
        self._print_results(state)
        
        return state
    
    def _print_results(self, state):
        """打印结果"""
        print("\n" + "-"*60)
        print("【天气信息】")
        weather = state.get("weather", {})
        print("城市:", weather.get("city", "未知"))
        print("温度:", str(weather.get("temperature", "未知")) + "℃")
        print("天气:", weather.get("weather", "未知"))
        print("风力:", weather.get("wind_speed", "未知"))
        print("温度区间:", weather.get("temp_range", "未知"))
        
        print("\n【穿搭建议】")
        suggestion = state.get("outfit_suggestion", {})
        print("温度区间:", suggestion.get("temp_range", "未知"))
        print("场合:", suggestion.get("occasion", "未知"))
        print("穿搭建议:", suggestion.get("suggestion", "未知"))
        print("风格:", suggestion.get("style", "未知"))
        
        print("\n【推荐商品 - 结构化筛选】")
        products = state.get("filtered_products", [])
        for i, p in enumerate(products[:5], 1):
            print(str(i) + ". " + p["name"])
            print("   描述: " + p["description"])
            print("   温度范围: " + str(p["min_temp"]) + "-" + str(p["max_temp"]) + "℃")
            print("   场合: " + ", ".join(p["occasions"]))
        
        print("\n【推荐商品 - 向量检索】")
        vector_products = state.get("vector_results", [])
        if vector_products:
            for i, p in enumerate(vector_products, 1):
                score = p.get("similarity_score", 0)
                print(str(i) + ". " + p["name"] + " (相似度: " + "{:.2f}".format(score) + ")")
                print("   描述: " + p["description"])
        else:
            print("无向量检索结果")
        
        print("\n【穿搭效果图提示词】")
        print(state.get("image_prompt", "无"))
        
        print("\n【潮流趋势】")
        trends = state.get("fashion_trends", [])
        for i, t in enumerate(trends, 1):
            print(str(i) + ". " + t["style"])
            print("   单品: " + t["items"])
            print("   颜色: " + t["colors"])
            print("   描述: " + t["description"])
        
        print("\n" + "-"*60)


def main():
    install_dependencies()
    
    print("\n请输入信息:")
    city = input("城市 (默认Beijing): ").strip() or "Beijing"
    
    print("\n请选择场合:")
    occasions = ["日常", "通勤", "约会", "运动", "聚会"]
    for i, occ in enumerate(occasions, 1):
        print(str(i) + ". " + occ)
    occ_choice = input("请选择 (1-5, 默认1): ").strip()
    occasion = occasions[int(occ_choice)-1] if occ_choice.isdigit() and 1<=int(occ_choice)<=5 else "日常"
    
    user_query = input("\n额外需求 (可选): ").strip()
    
    # 根据可用模式运行
    if NEW_MODE:
        workflow = get_outfit_workflow()
        state = workflow.run(city, occasion, user_query)
        # 打印完整结果（补充打印）
        print("\n" + "-"*60)
        print("【穿搭建议】")
        suggestion = state.get("outfit_suggestion", {})
        print(suggestion.get("suggestion", "无"))
        print("\n【推荐商品】")
        products = state.get("filtered_products", [])
        for i, p in enumerate(products[:5], 1):
            print(str(i) + ". " + p["name"])
        print("\n" + "-"*60)
    else:
        advisor = SmartOutfitAdvisorLegacy()
        advisor.run(city, occasion, user_query)


if __name__ == "__main__":
    main()
