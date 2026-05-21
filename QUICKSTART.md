
# SmartOutfitAdvisor 快速启动指南

## 📦 项目合并完成！

您的两个独立项目已成功合并为一个完整的智能穿搭系统：
- ✅ 后端多智能体业务逻辑（agents/）
- ✅ Streamlit前端界面（app.py）
- ✅ 统一配置文件和依赖管理

## 🚀 快速启动

### 方式一：Streamlit Web界面（推荐）
```bash
cd /Users/ouminjun/Desktop/文1/前端ui
streamlit run app.py
```

### 方式二：控制台模式
```bash
cd /Users/ouminjun/Desktop/文1/前端ui
python3 main.py
```

## 📁 项目结构

```
前端ui/
├── agents/                    # AI智能体模块
│   ├── weather_agent.py      # 天气查询Agent
│   ├── knowledge_agent.py    # 穿搭知识库Agent
│   ├── retrieval_agent.py    # 商品检索Agent
│   ├── image_agent.py        # 图像生成Agent
│   ├── trend_agent.py        # 潮流趋势Agent
│   └── outfit_workflow.py    # LangGraph工作流
├── utils/                     # 工具模块
│   ├── auth.py               # 用户认证
│   ├── database.py           # 数据库管理
│   ├── memory_store.py       # 用户记忆
│   └── ...
├── data/                      # 数据目录
│   └── smartoutfit.db        # SQLite数据库
├── config.py                  # 配置文件
├── product_database.py        # 商品库
├── image_generator.py         # 图像生成
├── requirements.txt           # Python依赖
├── .env                       # 环境变量
├── main.py                    # 控制台入口
├── app.py                     # Streamlit入口
└── test_import.py            # 导入测试脚本
```

## ⚙️ 配置API密钥（可选）

编辑 `.env` 文件，填入您的API密钥以使用图像生成功能：

```env
# 通义万相API（阿里云图像生成）
TONGYI_API_KEY=your_tongyi_api_key_here

# 字节豆包生图API
DOUBAO_API_KEY=your_doubao_api_key_here

# Stable Diffusion WebUI API
SD_ENDPOINT=http://127.0.0.1:7860/sdapi/v1/txt2img
```

## ✅ 验证安装

运行导入测试脚本：
```bash
python3 test_import.py
```

所有模块应该显示 "✓ 导入成功"

## 🎯 功能特性

1. **多智能体协作** - 5个AI Agent协同工作
2. **用户系统** - 注册/登录/个人资料
3. **记忆功能** - 记住您的穿搭偏好
4. **商品推荐** - 智能筛选合适单品
5. **图像生成** - AI生成穿搭效果图
6. **潮流分析** - 时尚趋势洞察

## 📞 遇到问题？

1. 确保已安装Python 3.8+
2. 安装依赖：`pip3 install -r requirements.txt`
3. 运行测试：`python3 test_import.py`
4. 检查数据库：`data/smartoutfit.db` 会自动创建

---

🎉 **项目合并成功！** 开始使用您的智能穿搭系统吧！

