
# ========================================
# SmartOutfitAdvisor - Render 部署参数
# ========================================
# 直接复制粘贴到 Render 配置中即可

## 🚀 快速部署步骤

### 1. 在 Render 上创建新的 Web Service
- 访问：https://dashboard.render.com/
- 点击 "New" -&gt; "Web Service"
- 连接你的 GitHub 账户
- 选择仓库：omj2006/smartoutfit-advisor

---

### 2. 填写基本配置（复制粘贴）

#### 项目信息
```
Name: smartoutfit-advisor
Region: Singapore（推荐）
Runtime: Python 3
Instance Type: Starter（免费）
```

#### 构建和启动命令（重要！）
```
Build Command: pip install -r requirements.txt
Start Command: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

---

### 3. 添加环境变量（Environment Variables）

点击 "Advanced" -&gt; "Add Environment Variable"，添加以下变量：

| Key | Value |
|-----|-------|
| `TONGYI_API_KEY` | `你的API密钥` |
| `DEEPSEEK_API_KEY` | `你的API密钥` |
| `DEBUG_MODE` | `false` |
| `API_TIMEOUT` | `30` |
| `MAX_RETRIES` | `3` |

---

### 4. 完成部署

- 点击 "Create Web Service"
- 等待 5-15 分钟（首次构建较慢）
- 构建成功后，访问提供的 URL

---

## 📋 完整配置参考

### Render Web Service 完整配置
```yaml
name: smartoutfit-advisor
region: singapore
plan: starter
runtime: python
buildCommand: pip install -r requirements.txt
startCommand: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
envVars:
  - key: TONGYI_API_KEY
    value: 你的API密钥
  - key: DEEPSEEK_API_KEY
    value: 你的API密钥
  - key: DEBUG_MODE
    value: false
  - key: API_TIMEOUT
    value: 30
  - key: MAX_RETRIES
    value: 3
```

---

## 🔧 验证部署

### 构建成功标志
- Render 控制台显示 "Live" 状态
- 无红色错误信息
- 日志显示 "Streamlit server listening on port 10000"

### 访问验证
- 打开 Render 提供的 URL
- 能看到登录/注册页面
- 能正常导航

---

## 📞 常见问题

### Q: 构建失败怎么办？
A: 检查 requirements.txt 第一行是否是 setuptools&gt;=68.0.0

### Q: 启动后 404？
A: 确认 Start Command 中有 --server.address=0.0.0.0

### Q: 构建超时？
A: 升级到 Basic 实例，或精简 dependencies

### Q: API 功能不工作？
A: 检查环境变量是否正确配置

---

## 📚 相关文档

- 部署检查清单：DEPLOYMENT_CHECKLIST.md
- Render 官方文档：https://docs.render.com/
- Streamlit 部署指南：https://docs.streamlit.io/streamlit-community-cloud

