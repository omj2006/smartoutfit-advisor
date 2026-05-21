
#!/usr/bin/env python3
"""
测试SmartOutfitAdvisor模块导入
"""
import sys
import os

print("=" * 60)
print("SmartOutfitAdvisor - 模块导入测试")
print("=" * 60)

# 测试1: 基础模块
print("\n[1/7] 测试基础模块导入...")
try:
    import config
    print("  ✓ config.py 导入成功")
except Exception as e:
    print(f"  ✗ config.py 导入失败: {e}")

# 测试2: 智能体模块
print("\n[2/7] 测试智能体模块导入...")
try:
    from agents.weather_agent import WeatherAgent
    print("  ✓ WeatherAgent 导入成功")
except Exception as e:
    print(f"  ✗ WeatherAgent 导入失败: {e}")

try:
    from agents.knowledge_agent import KnowledgeAgent
    print("  ✓ KnowledgeAgent 导入成功")
except Exception as e:
    print(f"  ✗ KnowledgeAgent 导入失败: {e}")

try:
    from agents.retrieval_agent import RetrievalAgent
    print("  ✓ RetrievalAgent 导入成功")
except Exception as e:
    print(f"  ✗ RetrievalAgent 导入失败: {e}")

try:
    from agents.image_agent import ImageAgent
    print("  ✓ ImageAgent 导入成功")
except Exception as e:
    print(f"  ✗ ImageAgent 导入失败: {e}")

try:
    from agents.trend_agent import TrendAgent
    print("  ✓ TrendAgent 导入成功")
except Exception as e:
    print(f"  ✗ TrendAgent 导入失败: {e}")

# 测试3: 工作流
print("\n[3/7] 测试工作流模块导入...")
try:
    from agents.outfit_workflow import get_outfit_workflow
    print("  ✓ OutfitWorkflow 导入成功")
except Exception as e:
    print(f"  ✗ OutfitWorkflow 导入失败: {e}")

# 测试4: 工具模块
print("\n[4/7] 测试工具模块导入...")
try:
    from utils.auth import get_auth
    print("  ✓ auth.py 导入成功")
except Exception as e:
    print(f"  ✗ auth.py 导入失败: {e}")

try:
    from utils.database import get_db
    print("  ✓ database.py 导入成功")
except Exception as e:
    print(f"  ✗ database.py 导入失败: {e}")

try:
    from utils.memory_store import get_user_memory
    print("  ✓ memory_store.py 导入成功")
except Exception as e:
    print(f"  ✗ memory_store.py 导入失败: {e}")

# 测试5: 其他模块
print("\n[5/7] 测试其他模块导入...")
try:
    import product_database
    print("  ✓ product_database.py 导入成功")
except Exception as e:
    print(f"  ✗ product_database.py 导入失败: {e}")

try:
    import image_generator
    print("  ✓ image_generator.py 导入成功")
except Exception as e:
    print(f"  ✗ image_generator.py 导入失败: {e}")

# 测试6: 数据库路径
print("\n[6/7] 测试数据库路径...")
try:
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "smartoutfit.db")
    if os.path.exists(db_path):
        print(f"  ✓ 数据库文件存在: {db_path}")
    else:
        print(f"  ⚠ 数据库文件不存在（首次运行会自动创建）: {db_path}")
except Exception as e:
    print(f"  ✗ 数据库路径测试失败: {e}")

# 测试7: 环境变量
print("\n[7/7] 测试环境变量...")
try:
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        print(f"  ✓ .env文件存在: {env_path}")
    else:
        print(f"  ⚠ .env文件不存在，请复制.env.example并配置API密钥")
except Exception as e:
    print(f"  ✗ 环境变量测试失败: {e}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
print("\n下一步:")
print("  1. 配置 .env 文件中的API密钥")
print("  2. 运行 `streamlit run app.py` 启动Web界面")
print("  3. 或运行 `python main.py` 启动控制台模式")

