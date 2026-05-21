
#!/bin/bash
# ========================================
# SmartOutfitAdvisor - 一键启动脚本
# ========================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &amp;&amp; pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "  SmartOutfitAdvisor - 智能穿搭推荐系统"
echo "========================================"
echo ""

# 检查Python
if ! command -v python3 &amp;&gt; /dev/null; then
    echo "❌ Python3未找到，请先安装Python3"
    exit 1
fi

# 检查依赖
echo "📦 检查/安装依赖..."
pip3 install -r requirements.txt -q
echo "✅ 依赖检查完成"
echo ""

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "⚠️ .env文件不存在，将使用默认配置"
else
    echo "✅ .env配置文件已加载"
fi
echo ""

PS3="请选择启动模式: "
select mode in "Streamlit网页模式" "控制台交互模式" "退出"; do
    case $mode in
        "Streamlit网页模式")
            echo ""
            echo "🚀 启动Streamlit网页模式..."
            echo "🌐 访问地址: http://localhost:8502"
            echo ""
            python3 -m streamlit run app.py
            break
            ;;
        "控制台交互模式")
            echo ""
            echo "🚀 启动控制台交互模式..."
            echo ""
            python3 main.py
            break
            ;;
        "退出")
            echo "👋 再见！"
            exit 0
            ;;
        *)
            echo "❌ 无效选项，请重试"
            ;;
    esac
done

