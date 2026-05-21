
"""
知识库Agent
"""
from utils.db_tools import get_outfit_suggestion


class KnowledgeAgent:
    """知识库智能体"""
    
    def __init__(self):
        self.name = "知识库Agent"
    
    def run(self, state):
        """
        执行穿搭建议查询
        
        Args:
            state: 状态字典
            
        Returns:
            更新后的状态
        """
        temp_range = state.get("weather", {}).get("temp_range", "舒适（18-25℃）")
        occasion = state.get("occasion", "日常")
        
        print("[" + self.name + "] 正在生成 " + temp_range + " + " + occasion + " 的穿搭建议...")
        
        suggestion = get_outfit_suggestion(temp_range, occasion)
        state["outfit_suggestion"] = suggestion
        
        print("[" + self.name + "] 穿搭建议生成完成: " + suggestion["suggestion"])
        return state
