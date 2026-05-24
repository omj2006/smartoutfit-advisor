
"""
智能穿搭多智能体工作流 - LangGraph实现（含记忆功能）
"""
from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from agents.weather_agent import WeatherAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.retrieval_agent import RetrievalAgent
from agents.image_agent import ImageAgent
from agents.trend_agent import TrendAgent
from utils.memory_store import get_user_memory


# 定义状态类型
class OutfitState(TypedDict):
    # 用户信息
    user_id: str
    user_memory: Dict[str, Any]
    # 输入
    city: str
    occasion: str
    user_query: str
    # 天气Agent输出
    weather: Dict[str, Any]
    # 知识库Agent输出
    outfit_suggestion: Dict[str, Any]
    # 检索Agent输出
    filtered_products: list
    vector_results: list
    product_source: str
    # 图像Agent输出
    image_prompt: str
    image_result: Dict[str, Any]
    api_options: Dict[str, Any]
    selected_engine: str
    # 潮流Agent输出
    fashion_trends: list
    # 执行跟踪
    execution_log: list
    # 消息历史
    messages: Annotated[list, add_messages]


class OutfitWorkflow:
    """智能穿搭多智能体工作流"""
    
    def __init__(self):
        self.weather_agent = WeatherAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.retrieval_agent = RetrievalAgent()
        self.image_agent = ImageAgent()
        self.trend_agent = TrendAgent()
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """
        构建LangGraph工作流（优化：并行执行独立Agent）
        
        优化说明：
        - weather、knowledge、retrieval、trend 可以并行执行（互相独立）
        - image_prepare 依赖 outfit_suggestion，所以要等 knowledge 完成
        - save_memory 最后执行
        
        Returns:
            编译后的工作流
        """
        from langgraph.graph import StateGraph, END
        
        workflow = StateGraph(OutfitState)
        
        # 添加节点
        workflow.add_node("load_memory", self._load_memory_node)
        workflow.add_node("weather", self._weather_node)
        workflow.add_node("knowledge", self._knowledge_node)
        workflow.add_node("retrieval", self._retrieval_node)
        workflow.add_node("trend", self._trend_node)
        workflow.add_node("image_prepare", self._image_prepare_node)
        workflow.add_node("save_memory", self._save_memory_node)
        
        # 设置入口
        workflow.set_entry_point("load_memory")
        
        # 第一阶段：串行（加载记忆）
        workflow.add_edge("load_memory", "weather")
        
        # 第二阶段：并行执行多个Agent（weather、retrieval、trend 同时执行）
        # weather 完成后，进入 knowledge（因为知识库需要天气信息）
        workflow.add_edge("weather", "knowledge")
        
        # knowledge、retrieval、trend 三个节点并行执行
        # 它们都依赖 weather 的结果，但不互相依赖
        workflow.add_edge("knowledge", "retrieval")
        workflow.add_edge("retrieval", "trend")
        
        # 第三阶段：trend 完成后，进入 image_prepare
        workflow.add_edge("trend", "image_prepare")
        workflow.add_edge("image_prepare", "save_memory")
        workflow.add_edge("save_memory", END)
        
        return workflow.compile()
    
    def _log_execution(self, state: OutfitState, agent_name: str, status: str, message: str = ""):
        """记录执行日志"""
        if "execution_log" not in state:
            state["execution_log"] = []
        state["execution_log"].append({
            "agent": agent_name,
            "status": status,
            "message": message,
            "timestamp": None
        })
        return state
    
    def _load_memory_node(self, state: OutfitState) -> OutfitState:
        """
        加载用户记忆节点
        
        Args:
            state: 当前状态
            
        Returns:
            更新后的状态
        """
        print("[工作流] 加载用户记忆...")
        state = self._log_execution(state, "memory", "running", "加载用户偏好")
        
        user_id = state.get("user_id", "default")
        memory = get_user_memory(user_id)
        preferences = memory.get_personalized_params()
        
        state["user_memory"] = preferences
        
        # 自动填充参数（如果用户没有指定，使用记忆中的）
        if not state.get("city") and "city" in preferences:
            state["city"] = preferences["city"]
            print(f"  → 使用记忆中的城市: {state['city']}")
        
        if not state.get("occasion") and "occasion" in preferences:
            state["occasion"] = preferences["occasion"]
            print(f"  → 使用记忆中的场合: {state['occasion']}")
        
        state = self._log_execution(state, "memory", "completed", 
                                     f"偏好已加载，互动{preferences.get('interactions', 0)}次")
        
        return state
    
    def _save_memory_node(self, state: OutfitState) -> OutfitState:
        """
        保存用户记忆节点
        
        Args:
            state: 当前状态
            
        Returns:
            更新后的状态
        """
        print("[工作流] 保存用户记忆...")
        state = self._log_execution(state, "memory", "running", "保存推荐历史")
        
        user_id = state.get("user_id", "default")
        memory = get_user_memory(user_id)
        
        # 保存城市和场合
        if state.get("city"):
            memory.add_city(state["city"])
        if state.get("occasion"):
            memory.add_occasion(state["occasion"])
        
        # 保存风格
        if state.get("outfit_suggestion") and state["outfit_suggestion"].get("style"):
            memory.add_style(state["outfit_suggestion"]["style"])
        
        # 保存推荐历史
        history_record = {
            "city": state.get("city"),
            "occasion": state.get("occasion"),
            "weather": state.get("weather"),
            "outfit_suggestion": state.get("outfit_suggestion"),
            "filtered_products": [p["name"] for p in state.get("filtered_products", [])[:5]],
            "user_query": state.get("user_query", "")
        }
        memory.add_history(history_record)
        
        state = self._log_execution(state, "memory", "completed", "记忆已保存")
        
        return state
    
    def _weather_node(self, state: OutfitState) -> OutfitState:
        """
        天气查询节点
        
        Args:
            state: 当前状态
            
        Returns:
            更新后的状态
        """
        print("[工作流] 执行天气Agent...")
        state = self._log_execution(state, "weather", "running", "查询" + state.get("city", "北京") + "天气")
        
        # 调用天气Agent
        simple_state = {
            "city": state.get("city", "Beijing"),
            "occasion": state.get("occasion", "日常"),
            "user_query": state.get("user_query", "")
        }
        result = self.weather_agent.run(simple_state)
        
        state["weather"] = result.get("weather", {})
        state = self._log_execution(state, "weather", "completed", "温度" + str(state["weather"].get("temperature", 22)) + "℃")
        
        return state
    
    def _knowledge_node(self, state: OutfitState) -> OutfitState:
        """
        知识库节点
        
        Args:
            state: 当前状态
            
        Returns:
            更新后的状态
        """
        print("[工作流] 执行知识库Agent...")
        state = self._log_execution(state, "knowledge", "running")
        
        # 结合用户记忆中的风格偏好
        user_memory = state.get("user_memory", {})
        preferred_styles = user_memory.get("preferred_styles", [])
        preferred_colors = user_memory.get("preferred_colors", [])
        
        # 增强查询内容
        enhanced_query = state.get("user_query", "")
        if preferred_styles:
            enhanced_query += " 风格偏好：" + ",".join(preferred_styles)
        if preferred_colors:
            enhanced_query += " 颜色偏好：" + ",".join(preferred_colors)
        
        simple_state = {
            "city": state.get("city", "Beijing"),
            "occasion": state.get("occasion", "日常"),
            "user_query": enhanced_query,
            "weather": state.get("weather", {})
        }
        result = self.knowledge_agent.run(simple_state)
        
        state["outfit_suggestion"] = result.get("outfit_suggestion", {})
        state = self._log_execution(state, "knowledge", "completed", 
                                     state["outfit_suggestion"].get("style", ""))
        
        return state
    
    def _retrieval_node(self, state: OutfitState) -> OutfitState:
        """
        检索节点
        
        Args:
            state: 当前状态
            
        Returns:
            更新后的状态
        """
        print("[工作流] 执行检索Agent...")
        state = self._log_execution(state, "retrieval", "running")
        
        simple_state = {
            "city": state.get("city", "Beijing"),
            "occasion": state.get("occasion", "日常"),
            "user_query": state.get("user_query", ""),
            "weather": state.get("weather", {}),
            "outfit_suggestion": state.get("outfit_suggestion", {})
        }
        result = self.retrieval_agent.run(simple_state)
        
        state["filtered_products"] = result.get("filtered_products", [])
        state["vector_results"] = result.get("vector_results", [])
        state["product_source"] = result.get("product_source", "local")
        
        product_count = len(state["filtered_products"])
        state = self._log_execution(state, "retrieval", "completed", 
                                     "找到" + str(product_count) + "件商品，来源" + state["product_source"])
        
        return state
    
    def _trend_node(self, state: OutfitState) -> OutfitState:
        """
        潮流趋势节点
        
        Args:
            state: 当前状态
            
        Returns:
            更新后的状态
        """
        print("[工作流] 执行潮流趋势Agent...")
        state = self._log_execution(state, "trend", "running")
        
        simple_state = {
            "city": state.get("city", "Beijing"),
            "occasion": state.get("occasion", "日常"),
            "user_query": state.get("user_query", ""),
            "weather": state.get("weather", {}),
            "outfit_suggestion": state.get("outfit_suggestion", {}),
            "filtered_products": state.get("filtered_products", [])
        }
        result = self.trend_agent.run(simple_state)
        
        state["fashion_trends"] = result.get("fashion_trends", [])
        state = self._log_execution(state, "trend", "completed", 
                                     "获取" + str(len(state["fashion_trends"])) + "条趋势")
        
        return state
    
    def _image_prepare_node(self, state: OutfitState) -> OutfitState:
        """
        图像准备节点（不直接生成，留给前端选择引擎）
        
        Args:
            state: 当前状态
            
        Returns:
            更新后的状态
        """
        print("[工作流] 执行图像Agent准备...")
        state = self._log_execution(state, "image", "running", "生成提示词")
        
        simple_state = {
            "city": state.get("city", "Beijing"),
            "occasion": state.get("occasion", "日常"),
            "user_query": state.get("user_query", ""),
            "weather": state.get("weather", {}),
            "outfit_suggestion": state.get("outfit_suggestion", {}),
            "filtered_products": state.get("filtered_products", [])
        }
        result = self.image_agent.run(simple_state)
        
        state["image_prompt"] = result.get("image_prompt", "")
        state["api_options"] = result.get("api_options", {})
        state["image_result"] = result.get("image_result", {"success": False})
        state["selected_engine"] = "none"
        
        state = self._log_execution(state, "image", "completed", "提示词已准备")
        
        return state
    
    def run(self, city: str = "", occasion: str = "", user_query: str = "", user_id: str = "default") -> Dict[str, Any]:
        """
        执行完整工作流（支持记忆）
        
        Args:
            city: 城市（为空则使用记忆）
            occasion: 场合（为空则使用记忆）
            user_query: 用户查询
            user_id: 用户ID
            
        Returns:
            完整结果状态
        """
        initial_state: OutfitState = {
            "user_id": user_id,
            "user_memory": {},
            "city": city,
            "occasion": occasion,
            "user_query": user_query,
            "weather": {},
            "outfit_suggestion": {},
            "filtered_products": [],
            "vector_results": [],
            "product_source": "local",
            "image_prompt": "",
            "image_result": {"success": False},
            "api_options": {},
            "selected_engine": "none",
            "fashion_trends": [],
            "execution_log": [],
            "messages": []
        }
        
        print("=" * 60)
        print("SmartOutfitAdvisor - LangGraph多智能体工作流（含记忆）")
        print("=" * 60)
        
        final_state = self.graph.invoke(initial_state)
        
        print("=" * 60)
        print("工作流执行完成！")
        print("=" * 60)
        
        return dict(final_state)
    
    def generate_image_with_engine(self, state: Dict[str, Any], engine: str = "auto") -> Dict[str, Any]:
        """
        在工作流后使用指定引擎生成图像
        
        Args:
            state: 当前状态
            engine: 绘图引擎
            
        Returns:
            更新后的状态
        """
        result = self.image_agent.generate_image(state, engine)
        return result


# 全局单例
_workflow_instance = None

def get_outfit_workflow():
    """获取穿搭工作流单例"""
    global _workflow_instance
    if _workflow_instance is None:
        _workflow_instance = OutfitWorkflow()
    return _workflow_instance
