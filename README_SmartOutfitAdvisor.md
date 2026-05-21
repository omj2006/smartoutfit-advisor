
# SmartOutfitAdvisor - 智能穿搭推荐系统

## 项目简介

SmartOutfitAdvisor是一个基于AI的智能穿搭推荐系统，整合了以下功能：
- 多智能体工作流（使用LangGraph）
- Streamlit Web界面
- 用户账号和记忆管理系统
- 天气查询和穿搭推荐
- 商品检索和向量搜索
- 图像生成（支持多种AI绘图引擎）
- 潮流趋势分析

## 项目结构

```
SmartOutfitAdvisor/
├── agents/                      # AI智能体模块
│   ├── weather_agent.py        # 天气查询Agent
│   ├── knowledge_agent.py      # 穿搭知识库Agent
│   ├── retrieval_agent.py      # 商品检索Agent
│   ├── image_agent.py          # 图像生成Agent
│   ├── trend_agent.py          # 潮流趋势Agent
│   └── outfit_workflow.py      # LangGraph工作流编排
├── utils/                       # 工具模块
│   ├── auth.py                 # 用户认证
│   ├── database.py             # 数据库管理
│   ├── memory_store.py         # 用户记忆存储
│   ├── vector_search.py        # 向量搜索
│   └── weather_api.py          # 天气API
├── data/                        # 数据目录
│   └── smartoutfit.db          # SQLite数据库
├── config.py                    # 配置文件
├── product_database.py          # 商品数据库
├── image_generator.py          # 图像生成器
├── knowledge_base.py          # 知识库
├── vector_search.py           # 向量搜索
├── requirements.txt           # Python依赖
├── .env                       # 环境变量（API密钥）
├── main.py                    # 控制台入口
└── app.py                     # Streamlit Web界面入口
```

## 安装说明

### 1. 安装Python依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

编辑 `.env` 文件，填入你的API密钥：

```env
# 通义万相API（阿里云图像生成）
TONGYI_API_KEY=your_tongyi_api_key_here
TONGYI_API_URL=https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis
TONGYI_MODEL=wanx-v1

# 字节豆包生图API
DOUBAO_API_KEY=your_doubao_api_key_here
DOUBAO_API_URL=https://ark.cn-beijing.volces.com/api/v3/images/generations
DOUBAO_MODEL=doubao-v2

# Stable Diffusion WebUI API
SD_API_KEY=your_sd_api_key_here
SD_ENDPOINT=http://127.0.0.1:7860/sdapi/v1/txt2img
SD_MODEL=v1-5-pruned-emaonly
```

## 快速开始

### 方式1：Streamlit Web界面（推荐）

```bash
streamlit run app.py
```

然后在浏览器中打开显示的地址（通常是 http://localhost:8501）

### 方式2：控制台模式

```bash
python main.py
```

按照提示输入城市、选择场合即可。

## 功能特性

### 1. 用户系统
- 注册/登录
- 个人资料管理
- 用户偏好记忆

### 2. 多智能体工作流
- **天气Agent**: 查询实时天气
- **知识库Agent**: 提供穿搭建议
- **检索Agent**: 搜索匹配商品
- **图像Agent**: 生成穿搭效果图
- **趋势Agent**: 分析时尚潮流

### 3. 图像生成
支持多种AI绘图引擎：
- 通义万相
- 豆包生图
- Stable Diffusion

### 4. 数据持久化
- SQLite本地数据库
- 用户历史记录
- 收藏功能

## 技术栈

- **AI框架**: LangGraph, LangChain
- **Web框架**: Streamlit, FastAPI
- **数据库**: SQLite
- **向量搜索**: FAISS
- **机器学习**: sentence-transformers
- **图像生成**: 通义万相、豆包、Stable Diffusion

## 注意事项

1. 首次运行会自动创建数据库文件
2. 图像生成功能需要配置相应的API密钥
3. 系统会自动学习和记忆用户的穿搭偏好
4. 数据存储在本地 `data/` 目录下

## 开发说明

如需添加新功能或修改代码，请参考：
- `agents/` 目录下的各智能体实现
- `app.py` 为Streamlit前端主文件
- `main.py` 为控制台主入口

## 许可证

MIT License

