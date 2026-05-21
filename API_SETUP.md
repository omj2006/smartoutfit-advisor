
# SmartOutfitAdvisor API 配置指南

## 🎨 1. 通义万相API（图像生成）

### 🔑 获取API密钥
1. 访问阿里云百炼平台：https://bailian.console.aliyun.com/
2. 登录/注册阿里云账号
3. 进入"API-KEY管理" → 创建新的API Key
4. 复制您的API密钥

### ⚙️ 配置步骤
编辑 `.env` 文件：
```env
# 通义万相API
TONGYI_API_KEY=你的API密钥
TONGYI_API_URL=https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis
TONGYI_MODEL=wanx-v1
```

### ✅ 验证配置
在代码中测试：
```python
from image_generator import ImageGenerator
gen = ImageGenerator("tongyi_wanxiang")
# 会提示配置是否正确
```

---

## 🛍️ 2. 淘宝开放API（商品搜索）

### 🔑 获取API密钥
1. 访问淘宝开放平台：https://open.taobao.com/
2. 注册成为开发者
3. 创建应用 → 获取 App Key 和 App Secret
4. 申请"商品搜索"相关API权限

### ⚙️ 配置步骤
编辑 `.env` 文件：
```env
# 淘宝开放API
TAOBAO_APP_KEY=12345678
TAOBAO_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TAOBAO_API_URL=https://eco.taobao.com/router/rest
```

---

## 🛒 3. 京东开放API（商品搜索）

### 🔑 获取API密钥
1. 访问京东开放平台：https://open.jd.com/
2. 注册成为开发者
3. 创建应用 → 获取 App Key 和 App Secret
4. 申请"商品API"相关权限

### ⚙️ 配置步骤
编辑 `.env` 文件：
```env
# 京东开放API
JD_APP_KEY=12345678
JD_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
JD_API_URL=https://api.jd.com/routerjson
```

---

## 📝 快速配置模板

将您的API密钥填入以下模板，然后保存为 `.env`：

```env
# ========================================
# SmartOutfitAdvisor API 配置
# ========================================

# 🎨 通义万相API（必填，用于图像生成）
TONGYI_API_KEY=your_actual_api_key_here
TONGYI_API_URL=https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis
TONGYI_MODEL=wanx-v1

# 🫛 豆包生图API（可选）
DOUBAO_API_KEY=your_doubao_api_key_here
DOUBAO_API_URL=https://ark.cn-beijing.volces.com/api/v3/images/generations
DOUBAO_MODEL=doubao-v2

# 🎨 Stable Diffusion（可选，本地部署）
SD_API_KEY=your_sd_api_key_here
SD_ENDPOINT=http://127.0.0.1:7860/sdapi/v1/txt2img
SD_MODEL=v1-5-pruned-emaonly

# 🛍️ 淘宝API（可选，商品搜索）
TAOBAO_APP_KEY=your_taobao_app_key
TAOBAO_APP_SECRET=your_taobao_app_secret
TAOBAO_API_URL=https://eco.taobao.com/router/rest

# 🛒 京东API（可选，商品搜索）
JD_APP_KEY=your_jd_app_key
JD_APP_SECRET=your_jd_app_secret
JD_API_URL=https://api.jd.com/routerjson

# ⚙️ 应用配置
DEBUG_MODE=false
API_TIMEOUT=30
MAX_RETRIES=3
```

---

## 🧪 测试API配置

运行测试脚本验证配置：
```bash
cd /Users/ouminjun/Desktop/文1/前端ui
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()

print('=== API配置检查 ===')
print(f'通义万相: {\"✅ 已配置\" if os.getenv(\"TONGYI_API_KEY\") != \"your_tongyi_api_key_here\" else \"❌ 未配置\"}')
print(f'淘宝API: {\"✅ 已配置\" if os.getenv(\"TAOBAO_APP_KEY\") != \"your_taobao_app_key_here\" else \"❌ 未配置\"}')
print(f'京东API: {\"✅ 已配置\" if os.getenv(\"JD_APP_KEY\") != \"your_jd_app_key_here\" else \"❌ 未配置\"}')
"
```

---

## 💡 提示

- **通义万相**：新用户通常有免费额度，建议优先配置
- **淘宝/京东API**：审核需要时间，先用本地商品库也可以
- **本地商品库**：即使不配置电商API，系统也有内置的10件商品可以使用

---

## 🆘 需要帮助？

如果配置过程中遇到问题，请告诉我！我会帮您解决。

