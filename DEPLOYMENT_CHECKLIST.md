
# ========================================
# SmartOutfitAdvisor - Render 部署检查清单
# ========================================
# 确保推送到 GitHub 前所有项目都已检查

## ✅ 第一部分：部署文件检查

### 1.1 必需文件检查
- [x] requirements.txt - 已配置构建工具和稳定版本依赖
- [x] Procfile - 已配置标准启动命令
- [x] runtime.txt - 已指定 Python 3.11.7
- [x] .gitignore - 已排除 .env 和敏感文件
- [x] app.py - 已禁用自动安装依赖
- [x] README.md - 项目文档已更新

### 1.2 requirements.txt 内容验证
- [x] 构建工具在最前面：setuptools&gt;=68.0.0, pip&gt;=23.2.1, wheel&gt;=0.41.2
- [x] 核心依赖有固定版本号
- [x] faiss-cpu==1.7.4 - 稳定版本
- [x] sentence-transformers==2.2.2 - 稳定版本
- [x] streamlit==1.29.0 - 稳定版本
- [x] 所有依赖版本兼容

### 1.3 Procfile 内容验证
- [x] 内容：web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
- [x] 使用 $PORT 环境变量
- [x] 监听 0.0.0.0
- [x] 无 --server.headless（可选）

## ✅ 第二部分：代码适配检查

### 2.1 环境变量使用
- [x] config.py 使用 os.getenv() 读取 API 密钥
- [x] API 密钥有默认值（不影响部署）
- [x] 无硬编码路径

### 2.2 路径兼容性
- [x] 数据库路径使用 os.path.join()
- [x] data/ 目录会自动创建
- [x] 无绝对路径依赖

### 2.3 异常处理
- [x] 导入时禁用了自动安装依赖（已注释）
- [x] 代码有基础错误处理

## ✅ 第三部分：Git 仓库准备

### 3.1 已提交的文件
- [x] 所有核心代码文件（agents/, utils/, app.py, config.py 等）
- [x] requirements.txt（最新版本）
- [x] Procfile（最新版本）
- [x] runtime.txt
- [x] .gitignore
- [x] README.md 和部署文档

### 3.2 已排除的文件
- [x] .env - 已在 .gitignore 中
- [x] __pycache__/ - 已在 .gitignore 中
- [x] venv/ - 已在 .gitignore 中
- [x] data/*.db - 已在 .gitignore 中
- [x] .DS_Store - 已在 .gitignore 中

## ✅ 第四部分：Render 配置参数

### 4.1 Web Service 基本配置
```
项目名称：smartoutfit-advisor
运行环境：Python 3
区域：Singapore（推荐）
实例类型：Starter（免费）
```

### 4.2 构建和启动命令
```
Build Command: pip install -r requirements.txt
Start Command: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### 4.3 环境变量（Environment Variables）
```
TONGYI_API_KEY=你的API密钥
DEEPSEEK_API_KEY=你的API密钥
DEBUG_MODE=false
API_TIMEOUT=30
MAX_RETRIES=3
```

## ✅ 第五部分：部署前最后检查

### 5.1 本地测试（可选）
- [ ] 本地运行：streamlit run app.py 能正常启动
- [ ] 所有页面能正常访问
- [ ] 基本功能测试通过

### 5.2 Git 状态检查
- [ ] git status - 工作区干净
- [ ] git log - 最新提交已包含所有更改
- [ ] git remote -v - 远程仓库配置正确

### 5.3 推送确认
- [ ] git push - 成功推送到 GitHub
- [ ] GitHub 仓库已更新

## 📋 部署完成验证

部署成功后，检查以下内容：
- [ ] 访问 Render 提供的 URL，页面正常显示
- [ ] 能打开登录/注册页面
- [ ] 无控制台报错
- [ ] 基础功能可用

## 🛠️ 常见问题

### 问题1：构建失败，setuptools 错误
解决：requirements.txt 第一行必须是 setuptools&gt;=68.0.0

### 问题2：构建超时
解决：升级 Render 实例类型，或精简依赖

### 问题3：启动后访问 404
解决：确认 Procfile 中的 --server.address=0.0.0.0

### 问题4：API 调用失败
解决：检查 Render 环境变量是否正确配置

