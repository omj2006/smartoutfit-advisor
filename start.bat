
@echo off
REM ========================================
REM SmartOutfitAdvisor - 一键启动脚本 (Windows)
REM ========================================

cd /d "%~dp0"

echo ========================================
echo   SmartOutfitAdvisor - 智能穿搭推荐系统
echo ========================================
echo.

REM 检查Python
python --version &gt;nul 2&gt;&amp;1
if %errorlevel% neq 0 (
    echo ❌ Python未找到，请先安装Python
    pause
    exit /b 1
)

REM 检查依赖
echo 📦 检查/安装依赖...
pip install -r requirements.txt -q
echo ✅ 依赖检查完成
echo.

REM 检查.env文件
if not exist ".env" (
    echo ⚠️ .env文件不存在，将使用默认配置
) else (
    echo ✅ .env配置文件已加载
)
echo.

echo 请选择启动模式:
echo 1. Streamlit网页模式
echo 2. 控制台交互模式
echo 3. 退出
echo.
set /p choice=请输入选项 (1-3):

if "%choice%"=="1" (
    echo.
    echo 🚀 启动Streamlit网页模式...
    echo 🌐 访问地址: http://localhost:8502
    echo.
    python -m streamlit run app.py
) else if "%choice%"=="2" (
    echo.
    echo 🚀 启动控制台交互模式...
    echo.
    python main.py
) else if "%choice%"=="3" (
    echo 👋 再见！
) else (
    echo ❌ 无效选项
)

pause

