import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import {
  User,
  Shirt,
  Heart,
  Settings,
  ChevronRight,
  Crown,
  Palette,
  Bell,
  Shield,
  HelpCircle,
  LogOut,
  Sparkles,
  Edit2,
  Save,
  Trash2,
  Calendar,
  Thermometer,
  MapPin,
  UserPlus,
  Hash,
  History,
  Star,
  Plus,
  X,
  Check,
} from 'lucide-react'
import { useUserStore } from '@/store/useUserStore'
import { useThemeStore } from '@/store/useThemeStore'
import { Loading } from '@/components/Loading'
import { ErrorDisplay, EmptyState } from '@/components/ErrorBoundary'
import { ProfileSkeleton } from '@/components/Skeleton'

// 标签页类型
type TabType = 'profile' | 'collections' | 'history' | 'settings'

const styleOptions = ['简约', '优雅', '知性', '街头', '甜美', '休闲', '商务', '复古']
const colorOptions = ['蓝色系', '粉色系', '灰色系', '黑色系', '米色系', '绿色系', '红色系']
const occasionOptions = ['通勤', '约会', '休闲', '运动', '派对', '旅行']

const container = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.05 } },
}

const item = {
  hidden: { opacity: 0, x: -10 },
  show: { opacity: 1, x: 0 },
}

export default function Profile() {
  const {
    username,
    avatar,
    isVip,
    isLoggedIn,
    logout,
    personalInfo,
    memory,
    savedOutfits,
    historyRecords,
    updatePersonalInfo,
    addFavoriteCity,
    addFavoriteOccasion,
    addFavoriteStyle,
    setTemperaturePreference,
    saveOutfit,
    removeSavedOutfit,
    clearHistory,
  } = useUserStore()
  const { isDark, toggle } = useThemeStore()
  const navigate = useNavigate()

  // 当前标签页
  const [activeTab, setActiveTab] = useState<TabType>('profile')
  // 编辑模式
  const [isEditing, setIsEditing] = useState(false)
  // 加载状态
  const [isLoading, setIsLoading] = useState(false)
  // 错误状态
  const [error, setError] = useState<string | null>(null)
  // 编辑表单
  const [editForm, setEditForm] = useState({
    height: '',
    weight: '',
    gender: '',
    age: '',
  })

  // 模拟加载效果
  useEffect(() => {
    setIsLoading(true)
    const timer = setTimeout(() => {
      setIsLoading(false)
    }, 500)
    return () => clearTimeout(timer)
  }, [activeTab])

  // 加载个人信息到编辑表单
  useEffect(() => {
    setEditForm({
      height: personalInfo.height?.toString() || '',
      weight: personalInfo.weight?.toString() || '',
      gender: personalInfo.gender || '',
      age: personalInfo.age?.toString() || '',
    })
  }, [])

  const handleLogout = () => {
    setIsLoading(true)
    try {
      logout()
      navigate('/login')
    } catch (err) {
      setError('退出登录失败')
      setIsLoading(false)
    }
  }

  const handleSaveProfile = () => {
    updatePersonalInfo({
      height: editForm.height ? parseInt(editForm.height) : null,
      weight: editForm.weight ? parseInt(editForm.weight) : null,
      gender: editForm.gender,
      age: editForm.age ? parseInt(editForm.age) : null,
    })
    setIsEditing(false)
  }

  const handleToggleStyle = (style: string) => {
    const current = personalInfo.stylePreferences
    if (current.includes(style)) {
      updatePersonalInfo({
        stylePreferences: current.filter(s => s !== style)
      })
    } else {
      updatePersonalInfo({
        stylePreferences: [...current, style]
      })
    }
  }

  const handleToggleColor = (color: string) => {
    const current = personalInfo.colorPreferences
    if (current.includes(color)) {
      updatePersonalInfo({
        colorPreferences: current.filter(c => c !== color)
      })
    } else {
      updatePersonalInfo({
        colorPreferences: [...current, color]
      })
    }
  }

  const tabs = [
    { id: 'profile', label: '个人信息', icon: User },
    { id: 'collections', label: '收藏', icon: Heart, badge: savedOutfits.length },
    { id: 'history', label: '历史', icon: History, badge: historyRecords.length },
    { id: 'settings', label: '设置', icon: Settings },
  ]

  // 显示加载状态
  if (isLoading) {
    return (
      <div className="min-h-screen p-4 md:p-6 lg:p-8">
        <ProfileSkeleton />
      </div>
    )
  }

  // 显示错误状态
  if (error) {
    return (
      <div className="min-h-screen p-4 md:p-6 lg:p-8">
        <ErrorDisplay 
          error={error} 
          onRetry={() => setError(null)} 
          showHome={false}
        />
      </div>
    )
  }

  return (
    <div className="min-h-screen p-4 md:p-6 lg:p-8 space-y-6">
      {/* 头部卡片 */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative overflow-hidden rounded-3xl glass-card p-6"
      >
        <div className="absolute top-0 right-0 w-40 h-40 rounded-full bg-rose-soft/10 dark:bg-rose-soft/5 blur-3xl" />
        <div className="absolute bottom-0 left-0 w-32 h-32 rounded-full bg-lavender-soft/10 dark:bg-lavender-soft/5 blur-3xl" />

        <div className="relative z-10 flex items-center gap-4">
          <div className="relative">
            <div className="w-20 h-20 rounded-full bg-gradient-rose p-0.5">
              <div className="w-full h-full rounded-full bg-background flex items-center justify-center overflow-hidden">
                {isLoggedIn ? (
                  <img src={avatar} alt={username} className="w-full h-full object-cover" />
                ) : (
                  <User className="w-8 h-8 text-muted-foreground" />
                )}
              </div>
            </div>
            {isVip && (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className="absolute -bottom-1 -right-1 w-7 h-7 rounded-full bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center shadow-lg"
              >
                <Crown className="w-3.5 h-3.5 text-white" />
              </motion.div>
            )}
          </div>

          <div className="flex-1">
            <h3 className="text-lg font-semibold">
              {isLoggedIn ? username : '未登录'}
            </h3>
            <p className="text-sm text-muted-foreground mt-0.5">
              {isVip ? 'VIP会员 · 专属风格分析' : '普通用户 · 升级VIP解锁更多'}
            </p>
            <div className="flex gap-2 mt-2 flex-wrap">
              {personalInfo.stylePreferences.slice(0, 3).map((tag) => (
                <span
                  key={tag}
                  className="px-2 py-0.5 rounded-full bg-primary/10 text-primary text-[10px] font-medium"
                >
                  {tag}
                </span>
              ))}
              {personalInfo.stylePreferences.length > 3 && (
                <span className="px-2 py-0.5 rounded-full bg-muted text-muted-foreground text-[10px]">
                  +{personalInfo.stylePreferences.length - 3}
                </span>
              )}
            </div>
          </div>

          {!isVip && (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="hidden md:flex items-center gap-1.5 px-4 py-2 rounded-full bg-gradient-to-r from-amber-400 to-amber-600 text-white text-xs font-medium shadow-lg"
            >
              <Crown className="w-3.5 h-3.5" />
              开通VIP
            </motion.button>
          )}
        </div>

        {/* 记忆系统展示 */}
        {(memory.favoriteCities.length > 0 || memory.favoriteOccasions.length > 0) && (
          <div className="relative z-10 mt-6 pt-4 border-t border-[var(--border-color)]">
            <p className="text-xs text-muted-foreground mb-2">🧠 你的偏好记忆</p>
            <div className="flex flex-wrap gap-2">
              {memory.favoriteCities.map(city => (
                <span key={city} className="px-2 py-1 rounded-lg bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs">
                  <MapPin className="w-3 h-3 inline mr-1" />
                  {city}
                </span>
              ))}
              {memory.favoriteOccasions.map(occasion => (
                <span key={occasion} className="px-2 py-1 rounded-lg bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 text-xs">
                  {occasion}
                </span>
              ))}
              {memory.temperaturePreference !== 'neutral' && (
                <span className="px-2 py-1 rounded-lg bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300 text-xs">
                  <Thermometer className="w-3 h-3 inline mr-1" />
                  {memory.temperaturePreference === 'warm' ? '喜欢偏暖' : '喜欢偏凉'}
                </span>
              )}
            </div>
          </div>
        )}

        <div className="relative z-10 grid grid-cols-3 gap-4 mt-6 pt-4 border-t border-[var(--border-color)]">
          {[
            { label: '穿搭方案', value: savedOutfits.length.toString() },
            { label: '历史记录', value: historyRecords.length.toString() },
            { label: '风格评分', value: '92' },
          ].map((stat) => (
            <div key={stat.label} className="text-center">
              <p className="text-xl font-bold gradient-text">{stat.value}</p>
              <p className="text-[10px] text-muted-foreground mt-0.5">{stat.label}</p>
            </div>
          ))}
        </div>
      </motion.div>

      {/* 标签页导航 */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as TabType)}
            className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all ${
              activeTab === tab.id
                ? 'bg-primary text-white shadow-lg'
                : 'glass-card hover:shadow-glass dark:hover:shadow-glass-dark'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
            {tab.badge > 0 && (
              <span className="ml-1 px-1.5 py-0.5 rounded-full bg-white/20 text-[10px]">
                {tab.badge}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* 个人信息标签页 */}
      {activeTab === 'profile' && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4"
        >
          {/* 基本信息编辑 */}
          <div className="glass-card rounded-2xl p-6">
            <div className="flex items-center justify-between mb-4">
              <h4 className="font-semibold flex items-center gap-2">
                <UserPlus className="w-5 h-5" />
                基本信息
              </h4>
              <button
                onClick={() => isEditing ? handleSaveProfile() : setIsEditing(true)}
                className="flex items-center gap-1 text-sm text-primary hover:text-primary/80"
              >
                {isEditing ? (
                  <>
                    <Save className="w-4 h-4" />
                    保存
                  </>
                ) : (
                  <>
                    <Edit2 className="w-4 h-4" />
                    编辑
                  </>
                )}
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">身高 (cm)</label>
                {isEditing ? (
                  <input
                    type="number"
                    value={editForm.height}
                    onChange={(e) => setEditForm({ ...editForm, height: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-background border border-[var(--border-color)] focus:border-primary focus:outline-none"
                    placeholder="165"
                  />
                ) : (
                  <div className="px-3 py-2 rounded-xl bg-muted">
                    {personalInfo.height ? `${personalInfo.height} cm` : '未设置'}
                  </div>
                )}
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">体重 (kg)</label>
                {isEditing ? (
                  <input
                    type="number"
                    value={editForm.weight}
                    onChange={(e) => setEditForm({ ...editForm, weight: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-background border border-[var(--border-color)] focus:border-primary focus:outline-none"
                    placeholder="55"
                  />
                ) : (
                  <div className="px-3 py-2 rounded-xl bg-muted">
                    {personalInfo.weight ? `${personalInfo.weight} kg` : '未设置'}
                  </div>
                )}
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">性别</label>
                {isEditing ? (
                  <select
                    value={editForm.gender}
                    onChange={(e) => setEditForm({ ...editForm, gender: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-background border border-[var(--border-color)] focus:border-primary focus:outline-none"
                  >
                    <option value="">请选择</option>
                    <option value="female">女</option>
                    <option value="male">男</option>
                  </select>
                ) : (
                  <div className="px-3 py-2 rounded-xl bg-muted">
                    {personalInfo.gender === 'female' ? '女' : personalInfo.gender === 'male' ? '男' : '未设置'}
                  </div>
                )}
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">年龄</label>
                {isEditing ? (
                  <input
                    type="number"
                    value={editForm.age}
                    onChange={(e) => setEditForm({ ...editForm, age: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-background border border-[var(--border-color)] focus:border-primary focus:outline-none"
                    placeholder="25"
                  />
                ) : (
                  <div className="px-3 py-2 rounded-xl bg-muted">
                    {personalInfo.age ? `${personalInfo.age} 岁` : '未设置'}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* 风格偏好 */}
          <div className="glass-card rounded-2xl p-6">
            <h4 className="font-semibold flex items-center gap-2 mb-4">
              <Sparkles className="w-5 h-5" />
              风格偏好
            </h4>
            <div className="flex flex-wrap gap-2">
              {styleOptions.map((style) => (
                <button
                  key={style}
                  onClick={() => handleToggleStyle(style)}
                  className={`px-3 py-1.5 rounded-full text-sm transition-all ${
                    personalInfo.stylePreferences.includes(style)
                      ? 'bg-primary text-white'
                      : 'bg-muted hover:bg-muted/80'
                  }`}
                >
                  {personalInfo.stylePreferences.includes(style) && (
                    <Check className="w-3 h-3 inline mr-1" />
                  )}
                  {style}
                </button>
              ))}
            </div>
          </div>

          {/* 颜色偏好 */}
          <div className="glass-card rounded-2xl p-6">
            <h4 className="font-semibold flex items-center gap-2 mb-4">
              <Palette className="w-5 h-5" />
              颜色偏好
            </h4>
            <div className="flex flex-wrap gap-2">
              {colorOptions.map((color) => (
                <button
                  key={color}
                  onClick={() => handleToggleColor(color)}
                  className={`px-3 py-1.5 rounded-full text-sm transition-all ${
                    personalInfo.colorPreferences.includes(color)
                      ? 'bg-primary text-white'
                      : 'bg-muted hover:bg-muted/80'
                  }`}
                >
                  {personalInfo.colorPreferences.includes(color) && (
                    <Check className="w-3 h-3 inline mr-1" />
                  )}
                  {color}
                </button>
              ))}
            </div>
          </div>

          {/* 记忆系统设置 */}
          <div className="glass-card rounded-2xl p-6">
            <h4 className="font-semibold flex items-center gap-2 mb-4">
              <Hash className="w-5 h-5" />
              快捷偏好
            </h4>
            <div className="space-y-4">
              <div>
                <label className="text-xs text-muted-foreground mb-2 block">常用城市</label>
                <div className="flex flex-wrap gap-2">
                  {['北京', '上海', '广州', '深圳', '成都'].map((city) => (
                    <button
                      key={city}
                      onClick={() => addFavoriteCity(city)}
                      className={`px-3 py-1.5 rounded-full text-sm transition-all ${
                        memory.favoriteCities.includes(city)
                          ? 'bg-blue-500 text-white'
                          : 'bg-muted hover:bg-muted/80'
                      }`}
                    >
                      {city}
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-2 block">常用场合</label>
                <div className="flex flex-wrap gap-2">
                  {occasionOptions.map((occasion) => (
                    <button
                      key={occasion}
                      onClick={() => addFavoriteOccasion(occasion)}
                      className={`px-3 py-1.5 rounded-full text-sm transition-all ${
                        memory.favoriteOccasions.includes(occasion)
                          ? 'bg-green-500 text-white'
                          : 'bg-muted hover:bg-muted/80'
                      }`}
                    >
                      {occasion}
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-2 block">冷暖偏好</label>
                <div className="flex gap-2">
                  {[
                    { value: 'cool', label: '偏凉', icon: '❄️' },
                    { value: 'neutral', label: '中性', icon: '🍃' },
                    { value: 'warm', label: '偏暖', icon: '☀️' },
                  ].map((pref) => (
                    <button
                      key={pref.value}
                      onClick={() => setTemperaturePreference(pref.value as any)}
                      className={`px-4 py-2 rounded-full text-sm transition-all ${
                        memory.temperaturePreference === pref.value
                          ? 'bg-orange-500 text-white'
                          : 'bg-muted hover:bg-muted/80'
                      }`}
                    >
                      {pref.icon} {pref.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {/* 收藏标签页 */}
      {activeTab === 'collections' && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4"
        >
          {savedOutfits.length === 0 ? (
            <EmptyState 
              icon={<Heart className="w-8 h-8 text-pink-500" />}
              title="暂无收藏"
              description="快去收藏喜欢的穿搭方案吧"
            />
          ) : (
            <div className="grid gap-4 md:grid-cols-2">
              {savedOutfits.map((outfit) => (
                <div key={outfit.id} className="glass-card rounded-2xl overflow-hidden">
                  <div className="relative">
                    <img src={outfit.image} alt={outfit.title} className="w-full h-48 object-cover" />
                    <button
                      onClick={() => removeSavedOutfit(outfit.id)}
                      className="absolute top-2 right-2 p-2 rounded-full bg-white/80 hover:bg-white text-red-500"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                  <div className="p-4">
                    <h5 className="font-semibold">{outfit.title}</h5>
                    <p className="text-sm text-muted-foreground mt-1">{outfit.description}</p>
                    <div className="flex gap-2 mt-3 flex-wrap">
                      <span className="px-2 py-1 rounded-full bg-primary/10 text-primary text-xs">
                        {outfit.occasion}
                      </span>
                      <span className="px-2 py-1 rounded-full bg-green-100 text-green-700 text-xs">
                        {outfit.style}
                      </span>
                      <span className="px-2 py-1 rounded-full bg-blue-100 text-blue-700 text-xs">
                        {outfit.temperature}
                      </span>
                    </div>
                    <p className="text-xs text-muted-foreground mt-3">
                      <Calendar className="w-3 h-3 inline mr-1" />
                      {new Date(outfit.savedAt).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </motion.div>
      )}

      {/* 历史记录标签页 */}
      {activeTab === 'history' && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4"
        >
          {historyRecords.length === 0 ? (
            <EmptyState 
              icon={<History className="w-8 h-8 text-blue-500" />}
              title="暂无历史记录"
              description="开始探索穿搭推荐吧"
            />
          ) : (
            <>
              <div className="flex justify-end">
                <button
                  onClick={clearHistory}
                  className="flex items-center gap-1 text-sm text-red-500 hover:text-red-600"
                >
                  <Trash2 className="w-4 h-4" />
                  清空历史
                </button>
              </div>
              <div className="space-y-3">
                {historyRecords.map((record) => (
                  <div key={record.id} className="glass-card rounded-2xl p-4 flex gap-4">
                    <img src={record.outfit.image} alt={record.outfit.title} className="w-20 h-20 rounded-xl object-cover" />
                    <div className="flex-1">
                      <h5 className="font-semibold">{record.outfit.title}</h5>
                      <p className="text-sm text-muted-foreground mt-1">{record.query}</p>
                      <div className="flex items-center gap-3 mt-2 text-xs text-muted-foreground">
                        <span><MapPin className="w-3 h-3 inline mr-1" />{record.weather.city}</span>
                        <span>{record.weather.temp}°C</span>
                        <span>{record.weather.condition}</span>
                      </div>
                      <p className="text-xs text-muted-foreground mt-1">
                        <Calendar className="w-3 h-3 inline mr-1" />
                        {new Date(record.createdAt).toLocaleString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </motion.div>
      )}

      {/* 设置标签页 */}
      {activeTab === 'settings' && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          variants={container}
          className="space-y-2"
        >
          {[
            { icon: Palette, label: '主题设置', desc: '切换浅色/深色主题', action: toggle, extra: isDark ? '深色' : '浅色' },
            { icon: Bell, label: '消息通知', desc: '推送与提醒设置' },
            { icon: Shield, label: '隐私安全', desc: '账号与隐私设置' },
            { icon: HelpCircle, label: '帮助中心', desc: '常见问题与反馈' },
          ].map((menuItem) => (
            <motion.button
              key={menuItem.label}
              variants={item}
              whileHover={{ x: 4 }}
              onClick={() => menuItem.action?.()}
              className="w-full flex items-center gap-4 p-4 rounded-2xl glass-card hover:shadow-glass dark:hover:shadow-glass-dark transition-all duration-300 group"
            >
              <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center group-hover:bg-primary/20 transition-colors">
                <menuItem.icon className="w-5 h-5 text-primary" />
              </div>
              <div className="flex-1 text-left">
                <p className="text-sm font-medium">{menuItem.label}</p>
                <p className="text-xs text-muted-foreground">{menuItem.desc}</p>
              </div>
              <div className="flex items-center gap-2">
                {menuItem.extra && (
                  <span className="text-xs text-muted-foreground">{menuItem.extra}</span>
                )}
                <ChevronRight className="w-4 h-4 text-muted-foreground group-hover:text-foreground transition-colors" />
              </div>
            </motion.button>
          ))}
        </motion.div>
      )}

      {isLoggedIn && (
        <motion.button
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleLogout}
          className="w-full flex items-center justify-center gap-2 p-4 rounded-2xl glass-card text-red-400 hover:bg-red-50 dark:hover:bg-red-950/20 transition-colors duration-300"
        >
          <LogOut className="w-4 h-4" />
          <span className="text-sm font-medium">退出登录</span>
        </motion.button>
      )}

      <p className="text-center text-[10px] text-muted-foreground pb-4">StyleAI v1.0.0 · Made with ❤️</p>
    </div>
  )
}
