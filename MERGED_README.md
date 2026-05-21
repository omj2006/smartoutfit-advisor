# 👗 智能穿搭推荐系统 - 合并版

## 📋 项目概述

这是一个完整的智能穿搭推荐系统，已经将多个项目合并为一个统一的项目：

- ✅ **React 前端** - 现代化的用户界面
- ✅ **FastAPI 后端** - 强大的 AI 驱动 API
- ✅ **Streamlit 功能** - 所有 AI 能力已整合
- ✅ **穿搭推荐引擎** - 基于天气、场合的智能推荐

## 🚀 快速开始

### 方式一：完整启动（推荐）

```bash
# 在前端ui目录下
./start-merged.sh
```

### 方式二：分别启动

**开发模式（前端热重载）：**
```bash
# 终端 1 - 启动后端
cd ..
python -m app.main

# 终端 2 - 启动前端
cd 前端ui
npm run dev
```

**生产模式：**
```bash
cd 前端ui
npm run build
python merged_main.py
```

## 📁 项目结构

```
文1/
├── 前端ui/                    # 主要工作目录
│   ├── src/                   # React 前端源码
│   │   ├── components/        # 组件
│   │   ├── pages/            # 页面
│   │   ├── data/             # 数据
│   │   └── App.tsx           # 主应用
│   ├── dist/                 # 构建后的前端
│   ├── agents/               # Streamlit AI 智能体
│   ├── utils/                # 工具函数
│   ├── merged_main.py        # 合并后的后端入口
│   ├── requirements-merged.txt # 合并后的依赖
│   └── start-merged.sh       # 一键启动脚本
├── app/                      # FastAPI 后端
│   ├── api/                  # API 路由
│   ├── core/                 # 核心逻辑
│   ├── tools/                # AI 工具
│   └── main.py               # 原始后端入口
└── data/                     # 数据目录
```

## 🎯 功能特性

### 前端功能
- 📱 响应式设计，支持移动端
- 🌙 深色/浅色主题切换
- 🌤️ 实时天气信息展示
- 👗 场景化穿搭推荐
- 🛒 商品搜索与展示
- 🎨 AI 效果图生成
- 📈 潮流趋势分析

### 后端 API
- 💬 智能对话聊天
- 🌤️ 天气查询接口
- 👔 穿搭推荐接口
- 🖼️ 图像生成接口
- 🛍️ 商品搜索接口
- 📊 潮流分析接口

## 🔧 配置说明

### 环境变量

复制 `.env.example` 为 `.env` 并配置：

```env
# OpenAI 或其他 LLM 配置
OPENAI_API_KEY=your-key-here

# 图像生成 API（可选）
TONGYI_API_KEY=your-key-here
DEEPSEEK_API_KEY=your-key-here

# 其他配置
DEBUG_MODE=false
```

### API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/chat` | POST | 智能对话 |
| `/api/chat/stream` | POST | 流式对话 |
| `/api/products` | GET | 商品列表 |
| `/api/products/search` | GET | 商品搜索 |
| `/api/generate-outfit-image` | POST | 生成穿搭图 |
| `/docs` | GET | API 文档 |

## 🛠️ 开发指南

### 添加新页面
1. 在 `src/pages/` 创建新页面
2. 在 `src/App.tsx` 中添加路由
3. 运行 `npm run dev` 预览

### 添加新 API
1. 在 `app/tools/builtin/` 添加工具
2. 在 `app/api/routes.py` 添加路由
3. 重启后端服务

### 整合 Streamlit 功能
所有 Streamlit 的 AI 功能都已经可以通过 FastAPI 调用：
- ✅ 穿搭推荐引擎
- ✅ 图像生成
- ✅ 商品搜索
- ✅ 天气查询

## 📦 依赖管理

### 前端依赖
```bash
npm install          # 安装依赖
npm run dev         # 开发模式
npm run build       # 生产构建
npm run lint        # 代码检查
```

### 后端依赖
```bash
pip install -r requirements-merged.txt
```

## 🚀 部署

### Docker 部署（示例）
```dockerfile
FROM node:18-alpine AS frontend
WORKDIR /app
COPY 前端ui/package*.json ./
RUN npm install
COPY 前端ui/ ./
RUN npm run build

FROM python:3.11-slim
WORKDIR /app
COPY --from=frontend /app/dist ./dist
COPY app/ ./app
COPY requirements-merged.txt ./
RUN pip install -r requirements-merged.txt
COPY 前端ui/merged_main.py ./
CMD ["uvicorn", "merged_main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📞 常见问题

### Q: 前端无法连接后端？
A: 确保后端正在运行在 8000 端口，检查 CORS 配置。

### Q: 图像生成不工作？
A: 检查 API 密钥配置，确保网络连接正常。

### Q: 如何添加新的穿搭场景？
A: 编辑 `src/data/outfits.ts` 添加新场景数据。

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**🎉 祝您穿搭愉快！**
