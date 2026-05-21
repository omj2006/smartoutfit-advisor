## 1. 架构设计

```mermaid
flowchart TB
    "前端应用 React 18" --> "路由层 React Router v6"
    "路由层 React Router v6" --> "页面层 Pages"
    "页面层 Pages" --> "组件层 Components"
    "组件层 Components" --> "状态管理 Zustand"
    "状态管理 Zustand" --> "主题系统 ThemeProvider"
    "组件层 Components" --> "动画层 Framer Motion"
    "组件层 Components" --> "UI库 Shadcn/ui + TailwindCSS"
    "前端应用 React 18" --> "Mock数据层"
end
```

## 2. 技术说明

- **前端框架**：React 18 + TypeScript
- **构建工具**：Vite
- **样式方案**：TailwindCSS 3 + CSS Variables（主题切换）
- **UI组件库**：Shadcn/ui（基于Radix UI）
- **动画库**：Framer Motion
- **状态管理**：Zustand
- **路由**：React Router DOM v6
- **图标**：lucide-react
- **后端**：无（纯前端，使用Mock数据）
- **数据**：本地Mock数据模拟API响应

## 3. 路由定义

| 路由 | 用途 |
|------|------|
| /login | 登录/注册页面 |
| / | 首页（天气、穿搭推荐、场景入口） |
| /recommend | 智能穿搭推荐页 |
| /ai-effect | AI穿搭效果图页面 |
| /profile | 个人中心页面 |
| /trends | 潮流资讯页面 |

## 4. 项目结构

```
src/
├── components/          # 通用组件
│   ├── ui/              # Shadcn/ui 组件
│   ├── Layout.tsx       # 全局布局（导航栏+内容区）
│   ├── BottomNav.tsx    # 移动端底部导航
│   ├── Sidebar.tsx      # PC端侧边导航
│   ├── WeatherCard.tsx  # 天气动态卡片
│   ├── OutfitCard.tsx   # 穿搭推荐卡片
│   ├── TrendCard.tsx    # 潮流资讯卡片
│   └── ThemeToggle.tsx  # 主题切换按钮
├── pages/               # 页面组件
│   ├── Login.tsx        # 登录页
│   ├── Home.tsx         # 首页
│   ├── Recommend.tsx    # 智能穿搭推荐页
│   ├── AiEffect.tsx     # AI穿搭效果图页
│   ├── Profile.tsx      # 个人中心页
│   └── Trends.tsx       # 潮流资讯页
├── store/               # Zustand状态管理
│   ├── useThemeStore.ts # 主题状态
│   └── useUserStore.ts  # 用户状态
├── hooks/               # 自定义Hooks
│   └── useMediaQuery.ts # 响应式Hook
├── data/                # Mock数据
│   ├── outfits.ts       # 穿搭数据
│   ├── trends.ts        # 资讯数据
│   └── weather.ts       # 天气数据
├── lib/                 # 工具函数
│   └── utils.ts         # 通用工具
├── App.tsx              # 应用入口+路由配置
├── main.tsx             # 渲染入口
└── index.css            # 全局样式+CSS变量
```

## 5. 主题系统设计

使用CSS变量 + Zustand实现主题切换：

```css
:root {
  --bg-primary: #F7F5F2;
  --bg-card: rgba(255, 255, 255, 0.7);
  --text-primary: #2D2640;
  --text-secondary: #9B8EA8;
  --accent: #E8A0BF;
  --accent-secondary: #C3ACD0;
  --border: rgba(155, 142, 168, 0.2);
}

.dark {
  --bg-primary: #1A1625;
  --bg-card: rgba(40, 35, 55, 0.7);
  --text-primary: #F0EBF5;
  --text-secondary: #8B7FA0;
  --accent: #8B5E83;
  --accent-secondary: #6B5B8A;
  --border: rgba(107, 91, 138, 0.3);
}
```

## 6. 动画规范

| 场景 | 动画类型 | 参数 |
|------|----------|------|
| 页面切换 | 淡入+上移 | duration: 0.4s, y: 20→0 |
| 卡片hover | 上浮+阴影 | y: -8, shadow增强 |
| 列表渲染 | 交错淡入 | staggerChildren: 0.08 |
| 模态框弹出 | 缩放+淡入 | scale: 0.9→1, duration: 0.3s |
| 主题切换 | 颜色过渡 | transition: color 0.3s |
| 天气图标 | 循环动画 | rotate/scale, repeat: Infinity |
