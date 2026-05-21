
# ========================================
# SmartOutfitAdvisor - Render.com 部署指南
# ========================================

## 🚀 项目已就绪，可直接部署到 Render！

---

## 📋 前置准备

### 1. 上传到 GitHub
首先将项目上传到 GitHub 仓库：
```bash
cd /Users/ouminjun/Desktop/文1/前端ui
git init
git add .
git commit -m "Initial commit: SmartOutfitAdvisor"
git branch -M main
git remote add origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
```

### 2. Render 账户
确保你有 Render.com 账户（https://render.com/）

---

## 🎯 Render 部署配置

### 第一步：创建新 Web Service
1. 登录 Render 控制台
2. 点击 **New +** → **Web Service**
3. 选择你刚才上传的 GitHub 仓库

### 第二步：填写部署参数（非常重要）

#### 基础信息
- **Name**: `smartoutfit-advisor`（或你喜欢的名字）
- **Region**: 选择离你最近的区域（建议 `Singapore` 或 `Oregon`）

#### 构建和部署设置（⚠️ 必须严格按此填写）
| 配置项 | 值 |
|--------|-----|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless true` |

#### 实例类型
- **Instance Type**: 选择 **Starter**（免费额度足够）
  - 如果有较多用户，可升级到 **Pro**

### 第三步：配置环境变量（Environment Variables）

点击 **Add Environment Variable**，添加以下变量：

| Key | Value | Required? |
|-----|-------|-----------|
| `TONGYI_API_KEY` | 你的通义万相API密钥 | ✅ 推荐 |
| `DEEPSEEK_API_KEY` | 你的DeepSeek API密钥 | ⚪ 可选 |
| `DEBUG_MODE` | `false` | ✅ 必须 |
| `API_TIMEOUT` | `30` | ✅ 必须 |
| `MAX_RETRIES` | `3` | ✅ 必须 |

**复制粘贴你的 API 密钥：**
- 通义万相: `你的通义万相API密钥`
- DeepSeek: `你的DeepSeek API密钥`

### 第四步：高级设置（可选）

#### 自动部署
- **Auto-Deploy**: `Yes`（每次 push 代码自动部署）

#### 磁盘
- **Disk Size**: 保持默认即可

---

## 🔍 项目文件说明

### 必须的部署文件（已创建 ✅）

| 文件名 | 作用 |
|--------|------|
| `Procfile` | Render 启动配置 |
| `requirements.txt` | Python 依赖（稳定版本） |
| `runtime.txt` | Python 版本指定 |
| `.gitignore` | Git 忽略文件 |

### Procfile 内容
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless true
```

### requirements.txt 特点
- ✅ 所有依赖使用固定版本号
- ✅ Streamlit 1.29.0（稳定版）
- ✅ FAISS、LangChain 等核心库已兼容

---

## 📊 部署检查清单

部署前确认：

- [x] 项目已上传 GitHub
- [x] `Procfile` 存在
- [x] `requirements.txt` 存在
- [x] `runtime.txt` 存在
- [x] `.gitignore` 已配置
- [x] 准备好 API 密钥（可选但推荐）

---

## ⚙️ Render 具体填写步骤（一步一图式）

### 详细步骤 1-10

#### 1. 进入 Render 控制台
访问 https://dashboard.render.com/

#### 2. 创建新 Web Service
点击 **New +** 按钮 → 选择 **Web Service**

#### 3. 连接 GitHub 仓库
- 如果是第一次，需要授权 Render 访问你的 GitHub
- 选择刚才上传的仓库

#### 4. 配置 Name 和 Region
- **Name**: `smartoutfit-advisor`（必须是唯一的）
- **Region**: 选择 `Singapore`（对国内访问较快）

#### 5. 配置 Build Command
在 **Build Command** 输入框填入：
```
pip install -r requirements.txt
```

#### 6. 配置 Start Command
在 **Start Command** 输入框填入：
```
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless true
```

#### 7. 配置环境变量
- 滚动到 **Environment** 部分
- 点击 **Add Environment Variable**
- 添加以下变量：
  - Key: `TONGYI_API_KEY`, Value: `你的通义万相API密钥`
  - Key: `DEEPSEEK_API_KEY`, Value: `你的DeepSeek API密钥`
  - Key: `DEBUG_MODE`, Value: `false`
  - Key: `API_TIMEOUT`, Value: `30`
  - Key: `MAX_RETRIES`, Value: `3`

#### 8. 选择实例类型
在 **Instance Type** 选择：
- 免费方案：选择 **Starter**（包含 750 小时/月）
- 付费方案：选择 **Pro**（更好的性能）

#### 9. 创建并部署
点击蓝色的 **Create Web Service** 按钮

#### 10. 等待部署完成
- 查看部署日志，等待状态变为 **Live**
- 这个过程需要 5-10 分钟（首次构建较慢）

---

## ✅ 部署成功后

### 访问地址
部署成功后，Render 会分配一个地址，类似：
```
https://smartoutfit-advisor.onrender.com
```

### 测试功能
1. 打开分配的网址
2. 注册一个测试账号
3. 测试穿搭推荐功能
4. 测试图像生成（如已配置 API）

---

## 🎛️ 本地测试部署版本

部署前，可以在本地测试 Render 版本：

```bash
cd /Users/ouminjun/Desktop/文1/前端ui

# 使用指定 Python 版本
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# 或
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 模拟 Render 环境测试
PORT=8501 streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

访问 http://localhost:8501 测试。

---

## 🔧 常见问题排查

### 问题 1: 构建失败，依赖安装错误
**原因**: requirements.txt 版本问题
**解决**: 检查是否使用了固定版本号（我们已配置 ✅）

### 问题 2: 部署成功但无法访问
**原因**: 端口配置错误
**解决**: 确认 Start Command 包含 `--server.port=$PORT --server.address=0.0.0.0`

### 问题 3: 图像生成失败
**原因**: 未配置 API Key 或配额用完
**解决**: 在 Render 环境变量中正确配置 `TONGYI_API_KEY`

### 问题 4: 数据库错误
**原因**: 文件系统权限问题
**解决**: 确保 data/ 目录有写权限（Render 临时磁盘可写）

---

## 📈 性能优化建议

### 免费额度限制
- 免费实例 15 分钟无活动会自动休眠
- 访问时会有冷启动延迟（几秒到几十秒）

### 升级方案
- 升级到 **Pro** 实例可避免休眠
- 获得更好的 CPU 和内存性能

---

## 📞 技术支持

部署中遇到问题：
1. 查看 Render **Logs** 标签页获取错误信息
2. 检查环境变量是否正确配置
3. 确认 Procfile 和 requirements.txt 位置正确

---

## 🎉 部署参数速查表

### Render Web Service 配置（复制粘贴即可）

```
项目名称: smartoutfit-advisor
运行环境: Python 3
构建命令: pip install -r requirements.txt
启动命令: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless true
环境变量:
  TONGYI_API_KEY: 你的通义万相API密钥
  DEEPSEEK_API_KEY: 你的DeepSeek API密钥
  DEBUG_MODE: false
  API_TIMEOUT: 30
  MAX_RETRIES: 3
```

---

## ✨ 总结

**项目已完全配置好 Render 部署，只需：**
1. 上传到 GitHub
2. 在 Render 按上述配置创建 Web Service
3. 等待部署完成，访问外网地址！

---

**祝你部署顺利！🚀**

