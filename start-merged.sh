#!/bin/bash
# 启动合并后的项目

echo "🚀 启动智能穿搭推荐系统..."
echo ""

# 检查是否需要安装 Python 依赖
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖（如果需要）
echo "📦 检查 Python 依赖..."
pip install -q -r requirements-merged.txt

# 启动后端服务器
echo ""
echo "🔧 启动 FastAPI 后端服务器..."
echo "📱 前端地址: http://localhost:8000"
echo "📚 API 文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

python3 merged_main.py
