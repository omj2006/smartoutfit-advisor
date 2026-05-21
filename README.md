
# 👗 SmartOutfitAdvisor - 智能穿搭推荐系统

基于 AI 多智能体的智能穿搭推荐系统，提供天气感知、商品推荐、潮流分析和 AI 图像生成功能。

---

## ✨ 核心功能

- 🤖 **多智能体协同** - 5个 AI 智能体组成工作流
- 🌤️ **天气感知** - 实时天气查询，智能适配穿搭
- 🛍️ **商品推荐** - 结构化筛选 + 向量语义检索
- 🎨 **AI 绘图** - 通义万相 API 生成穿搭效果图
- 📈 **潮流趋势** - 时尚趋势分析和建议
- 👤 **用户系统** - 注册/登录/个人中心/偏好记忆
- 💾 **记忆系统** - 保存用户历史、偏好和收藏

---

## 🚀 快速开始

### 方式一：Render 云端部署（推荐）

项目已完全配置好可直接部署到 Render.com！

详细步骤请查看：[RENDER_DEPLOY.md](./RENDER_DEPLOY.md)

### 方式二：本地运行

```bash
# 克隆项目
cd /Users/ouminjun/Desktop/文1/前端ui

# 安装依赖
pip install -r requirements.txt

# 启动应用
python3 -m streamlit run app.py
```

访问 http://localhost:8501

---

## 📋 Render 部署参数速查（最新稳定版）

| 配置项 | 值 |
|--------|-----|
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0` |
| **Instance Type** | Starter（免费） |
| **Runtime** | Python 3 |

**环境变量：**
```
TONGYI_API_KEY=你的API密钥
DEEPSEEK_API_KEY=你的API密钥
DEBUG_MODE=false
API_TIMEOUT=30
MAX_RETRIES=3
```

**详细文档：**
- [Render 部署配置](./RENDER_CONFIG.md) - 完整部署参数
- [部署检查清单](./DEPLOYMENT_CHECKLIST.md) - 上线前检查

---

## 📂 项目结构

```
SmartOutfitAdvisor/
├── agents/                      # AI 智能体模块
│   ├── weather_agent.py        # 天气查询 Agent
│   ├── knowledge_agent.py      # 穿搭知识库 Agent
│   ├── retrieval_agent.py      # 商品检索 Agent
│   ├── image_agent.py          # 图像生成 Agent
│   ├── trend_agent.py          # 潮流趋势 Agent
│   └── outfit_workflow.py      # LangGraph 工作流
├── utils/                       # 工具模块
│   ├── auth.py                 # 用户认证
│   ├── database.py             # 数据库管理
│   ├── memory_store.py         # 用户记忆
│   ├── vector_search.py        # 向量检索
│   └── weather_api.py          # 天气 API
├── data/                        # 数据目录
│   └── smartoutfit.db          # SQLite 数据库
├── config.py                    # 配置文件
├── product_database.py          # 商品库
├── image_generator.py           # 图像生成
├── knowledge_base.py            # 知识库
├── main.py                      # 控制台入口
├── app.py                       # Streamlit 入口
├── requirements.txt             # Python 依赖
├── Procfile                     # Render 部署配置
├── runtime.txt                  # Python 版本
├── .gitignore                   # Git 忽略文件
└── RENDER_DEPLOY.md            # Render 部署指南
```

---

## 🛠️ 技术栈

- **后端**: Python + LangGraph + LangChain
- **前端**: Streamlit
- **向量检索**: FAISS + Sentence-Transformers
- **数据库**: SQLite
- **图像生成**: 通义万相 API（阿里云）
- **部署平台**: Render.com

---

## 📚 文档

- [Render 部署指南](./RENDER_DEPLOY.md) - 详细的部署步骤
- [API 配置指南](./API_SETUP.md) - API Key 配置说明
- [快速入门](./QUICKSTART.md) - 本地快速开始
- [部署检查清单](./DEPLOYMENT_CHECKLIST.md) - 项目检查清单

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 💖 致谢

感谢所有贡献者和开源社区！

