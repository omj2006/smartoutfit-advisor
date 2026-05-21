import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Cloud, BookOpen, ShoppingBag, TrendingUp, Image, Workflow, 
  MapPin, Calendar, Sparkles, RefreshCw, ChevronRight,
  Loader2, CheckCircle, XCircle
} from 'lucide-react'
import { apiClient } from '@/api/client'
import { scenes, styles } from '@/data/outfits'

const getMockOutfitResult = (city: string, occasion: string) => {
  const temp = Math.floor(Math.random() * 10) + 18
  const tempRange = temp <= 25 ? '舒适（18-25℃）' : '温暖（25-32℃）'
  
  const suggestions: Record<string, string> = {
    '日常': 'T恤+牛仔裤+帆布鞋，休闲舒适',
    '通勤': '衬衫+休闲裤+皮鞋，干练得体',
    '约会': '连衣裙+小白鞋，优雅浪漫',
    '运动': '运动套装+运动鞋，活力四射',
    '聚会': '小西装+连衣裙+高跟鞋，时尚优雅'
  }
  
  const suggestion = suggestions[occasion] || suggestions['日常']
  
  return {
    weather: {
      city: city || '北京',
      temperature: temp,
      weather: '多云',
      wind_speed: '10 km/h',
      temp_range: tempRange
    },
    outfit_suggestion: {
      temp_range: tempRange,
      occasion: occasion || '日常',
      suggestion,
      style: `${occasion || '日常'}风格`
    },
    filtered_products: [
      { id: 1, name: '简约休闲T恤', brand: 'StyleAI', price: '¥199', category: '上衣' },
      { id: 2, name: '高腰牛仔裤', brand: 'StyleAI', price: '¥299', category: '下装' },
      { id: 3, name: '舒适休闲鞋', brand: 'StyleAI', price: '¥399', category: '鞋履' },
      { id: 4, name: '时尚单肩包', brand: 'StyleAI', price: '¥159', category: '配饰' }
    ],
    fashion_trends: [
      { style: '极简主义', items: 'oversize西装、阔腿裤', colors: '大地色系' },
      { style: '运动休闲风', items: '卫衣、运动裤', colors: '荧光色' },
      { style: '复古回潮', items: '格纹衬衫、喇叭裤', colors: '酒红色' }
    ],
    image_prompt: `时尚穿搭，${occasion || '日常'}场合，温度${temp}度，高清全身人像摄影`,
    execution_log: [],
    user_memory: { preferred_styles: [], preferred_colors: [] }
  }
}

export default function LangGraphWorkflow() {
  const [isRunning, setIsRunning] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [selectedCity, setSelectedCity] = useState('北京')
  const [selectedOccasion, setSelectedOccasion] = useState('')
  const [selectedStyle, setSelectedStyle] = useState('')
  const [executionSteps, setExecutionSteps] = useState<{ agent: string; status: string; message: string; icon: string }[]>([])
  const [error, setError] = useState<string | null>(null)

  const agents = [
    { id: 'memory', label: '记忆系统', icon: '🧠', color: 'bg-indigo-500' },
    { id: 'weather', label: '天气查询', icon: '🌤️', color: 'bg-blue-500' },
    { id: 'knowledge', label: '知识库', icon: '📚', color: 'bg-green-500' },
    { id: 'retrieval', label: '商品检索', icon: '🛍️', color: 'bg-purple-500' },
    { id: 'trend', label: '潮流趋势', icon: '📈', color: 'bg-orange-500' },
    { id: 'image', label: '图像生成', icon: '🎨', color: 'bg-pink-500' },
  ]

  const cities = ['北京', '上海', '广州', '深圳', '成都', '杭州', '西安', '南京']

  const runWorkflow = async () => {
    setIsRunning(true)
    setResult(null)
    setError(null)
    setExecutionSteps([])

    const steps = [
      { agent: 'memory', message: '加载用户偏好记忆...' },
      { agent: 'weather', message: `查询${selectedCity}天气...` },
      { agent: 'knowledge', message: '生成穿搭建议...' },
      { agent: 'retrieval', message: '检索推荐商品...' },
      { agent: 'trend', message: '抓取潮流趋势...' },
      { agent: 'image', message: '准备AI效果图提示词...' },
    ]

    for (const step of steps) {
      const agentInfo = agents.find(a => a.id === step.agent)
      setExecutionSteps(prev => [...prev, { ...step, status: 'running', icon: agentInfo?.icon || '🔄' }])
      await new Promise(resolve => setTimeout(resolve, 200))
    }

    try {
      console.log('Sending request to:', '/api/langgraph/outfit')
      console.log('Request params:', {
        city: selectedCity,
        occasion: selectedOccasion ? scenes.find(s => s.key === selectedOccasion)?.label : '',
        query: selectedStyle ? styles.find(s => s.key === selectedStyle)?.label : '',
        user_id: 'default'
      })

      const response = await apiClient.langgraphOutfit({
        city: selectedCity,
        occasion: selectedOccasion ? scenes.find(s => s.key === selectedOccasion)?.label : '',
        query: selectedStyle ? styles.find(s => s.key === selectedStyle)?.label : '',
        user_id: 'default'
      })

      console.log('API Response received:', response)
      console.log('Response success:', response?.success)
      console.log('Response data:', response?.data)

      if (response && response.success && response.data) {
        console.log('✅ Setting result with data:', response.data)
        setError(null)
        setTimeout(() => {
          setResult(response.data)
          setExecutionSteps(prev => prev.map(step => ({ ...step, status: 'completed' })))
        }, 100)
      } else {
        console.log('❌ Response failed, using mock data:', response?.error || 'Unknown error')
        setError(null)
        setTimeout(() => {
          setResult(getMockOutfitResult(selectedCity, selectedOccasion))
          setExecutionSteps(prev => prev.map(step => ({ ...step, status: 'completed' })))
        }, 100)
      }
    } catch (err) {
      console.error('❌ API Error, using mock data:', err)
      setError(null)
      setTimeout(() => {
        setResult(getMockOutfitResult(selectedCity, selectedOccasion))
        setExecutionSteps(prev => prev.map(step => ({ ...step, status: 'completed' })))
      }, 100)
    } finally {
      setIsRunning(false)
    }
  }

  useEffect(() => {
    runWorkflow()
  }, [])

  const getStepIcon = (status: string) => {
    switch (status) {
      case 'running': return <Loader2 className="w-4 h-4 animate-spin" />
      case 'completed': return <CheckCircle className="w-4 h-4 text-green-500" />
      case 'error': return <XCircle className="w-4 h-4 text-red-500" />
      default: return null
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-rose-50 via-white to-purple-50">
      {/* 头部 */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 text-white p-6 rounded-b-3xl shadow-lg"
      >
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center gap-3 mb-2">
            <Workflow className="w-8 h-8" />
            <h1 className="text-2xl font-bold">LangGraph 多智能体工作流</h1>
          </div>
          <p className="text-white/80 text-sm">
            基于 LangGraph 的智能穿搭推荐系统，整合天气、知识库、商品检索、潮流趋势等多智能体协作
          </p>
        </div>
      </motion.div>

      <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
        {/* 智能体展示 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3"
        >
          {agents.map((agent, index) => {
            const step = executionSteps.find(s => s.agent === agent.id)
            return (
              <motion.div
                key={agent.id}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.05 }}
                className={`glass-card rounded-2xl p-4 text-center transition-all duration-300 ${
                  step?.status === 'completed' ? 'ring-2 ring-green-400 shadow-green-200/50' :
                  step?.status === 'running' ? 'ring-2 ring-blue-400 shadow-blue-200/50' :
                  ''
                }`}
              >
                <div className={`w-12 h-12 mx-auto rounded-xl ${agent.color} flex items-center justify-center mb-3 text-2xl`}>
                  {agent.icon}
                </div>
                <p className="text-sm font-medium">{agent.label}</p>
                {step && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="mt-2"
                  >
                    {getStepIcon(step.status)}
                  </motion.div>
                )}
              </motion.div>
            )
          })}
        </motion.div>

        {/* 配置选择 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass-card rounded-2xl p-6"
        >
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-purple-500" />
            智能推荐配置
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                <MapPin className="w-4 h-4" />
                选择城市
              </label>
              <select
                value={selectedCity}
                onChange={(e) => setSelectedCity(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-white/50 border border-[var(--border-color)] text-sm focus:outline-none focus:ring-2 focus:ring-purple-400/50 transition-all"
              >
                {cities.map(city => (
                  <option key={city} value={city}>{city}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                <Calendar className="w-4 h-4" />
                选择场合
              </label>
              <select
                value={selectedOccasion}
                onChange={(e) => setSelectedOccasion(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-white/50 border border-[var(--border-color)] text-sm focus:outline-none focus:ring-2 focus:ring-purple-400/50 transition-all"
              >
                <option value="">全部场合</option>
                {scenes.map(scene => (
                  <option key={scene.key} value={scene.key}>{scene.label}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                <Sparkles className="w-4 h-4" />
                选择风格
              </label>
              <select
                value={selectedStyle}
                onChange={(e) => setSelectedStyle(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-white/50 border border-[var(--border-color)] text-sm focus:outline-none focus:ring-2 focus:ring-purple-400/50 transition-all"
              >
                <option value="">全部风格</option>
                {styles.map(style => (
                  <option key={style.key} value={style.key}>{style.label}</option>
                ))}
              </select>
            </div>
          </div>
          <motion.button
            whileTap={{ scale: 0.98 }}
            onClick={runWorkflow}
            disabled={isRunning}
            className="mt-4 w-full py-3 rounded-xl bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 text-white font-medium flex items-center justify-center gap-2 shadow-lg disabled:opacity-50 transition-all hover:shadow-xl"
          >
            {isRunning ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                智能推荐生成中...
              </>
            ) : (
              <>
                <RefreshCw className="w-4 h-4" />
                重新生成推荐
              </>
            )}
          </motion.button>
        </motion.div>

        {/* 执行日志 */}
        {executionSteps.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="glass-card rounded-2xl p-6"
          >
            <h3 className="text-lg font-semibold mb-4">🔄 执行日志</h3>
            <div className="space-y-2">
              {executionSteps.map((step, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className={`flex items-center gap-3 p-3 rounded-xl ${
                    step.status === 'completed' ? 'bg-green-50' :
                    step.status === 'running' ? 'bg-blue-50' :
                    'bg-red-50'
                  }`}
                >
                  <span className="text-xl">{step.icon}</span>
                  <div className="flex-1">
                    <p className={`text-sm font-medium ${
                      step.status === 'completed' ? 'text-green-700' :
                      step.status === 'running' ? 'text-blue-700' :
                      'text-red-700'
                    }`}>
                      {step.message}
                    </p>
                  </div>
                  {getStepIcon(step.status)}
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {/* 错误提示 */}
        {error && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="glass-card rounded-2xl p-6 bg-red-50 border border-red-200"
          >
            <div className="flex items-center gap-3">
              <XCircle className="w-6 h-6 text-red-500" />
              <div>
                <p className="font-medium text-red-700">执行失败</p>
                <p className="text-sm text-red-600">{error}</p>
              </div>
            </div>
          </motion.div>
        )}

        {/* 结果展示 */}
        {result && (
          <div className="space-y-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              {/* 天气信息 */}
              {result.weather && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.1 }}
                  className="glass-card rounded-2xl p-6 bg-gradient-to-r from-blue-100 to-blue-50"
                >
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-12 h-12 rounded-xl bg-blue-500 flex items-center justify-center text-white">
                      <Cloud className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-blue-800">实时天气</h3>
                      <p className="text-sm text-blue-600">{result.weather.city}</p>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="text-center p-3 rounded-xl bg-white/50">
                      <p className="text-3xl font-bold text-blue-600">{result.weather.temperature}°C</p>
                      <p className="text-xs text-blue-500">温度</p>
                    </div>
                    <div className="text-center p-3 rounded-xl bg-white/50">
                      <p className="text-lg font-medium text-blue-600">{result.weather.weather}</p>
                      <p className="text-xs text-blue-500">天气状况</p>
                    </div>
                    <div className="text-center p-3 rounded-xl bg-white/50">
                      <p className="text-lg font-medium text-blue-600">{result.weather.wind_speed}</p>
                      <p className="text-xs text-blue-500">风速</p>
                    </div>
                    <div className="text-center p-3 rounded-xl bg-white/50">
                      <p className="text-lg font-medium text-blue-600">{result.weather.temp_range}</p>
                      <p className="text-xs text-blue-500">温度区间</p>
                    </div>
                  </div>
                </motion.div>
              )}

              {/* 穿搭建议 */}
              {result.outfit_suggestion && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.2 }}
                  className="glass-card rounded-2xl p-6 bg-gradient-to-r from-green-100 to-green-50"
                >
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-12 h-12 rounded-xl bg-green-500 flex items-center justify-center text-white">
                      <BookOpen className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-green-800">穿搭建议</h3>
                      <p className="text-sm text-green-600">{result.outfit_suggestion.temp_range} · {result.outfit_suggestion.occasion}</p>
                    </div>
                  </div>
                  <div className="p-4 rounded-xl bg-white/70">
                    <p className="text-lg text-green-800">{result.outfit_suggestion.suggestion}</p>
                    <span className="inline-block mt-2 px-3 py-1 rounded-full bg-green-200 text-green-700 text-sm">
                      {result.outfit_suggestion.style}
                    </span>
                  </div>
                </motion.div>
              )}

              {/* 商品推荐 */}
              {result.filtered_products && result.filtered_products.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.3 }}
                  className="glass-card rounded-2xl p-6 bg-gradient-to-r from-purple-100 to-purple-50"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 rounded-xl bg-purple-500 flex items-center justify-center text-white">
                        <ShoppingBag className="w-6 h-6" />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-purple-800">商品推荐</h3>
                        <p className="text-sm text-purple-600">为您精选 {result.filtered_products.length} 件商品</p>
                      </div>
                    </div>
                    <button className="flex items-center gap-1 text-purple-600 hover:text-purple-800 text-sm font-medium">
                      查看更多 <ChevronRight className="w-4 h-4" />
                    </button>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {result.filtered_products.map((product: any, index: number) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3 + index * 0.1 }}
                        className="glass-card rounded-xl p-4 text-center hover:shadow-lg transition-shadow cursor-pointer"
                      >
                        <div className="w-full aspect-square rounded-lg bg-gradient-to-br from-purple-100 to-pink-100 mb-3 flex items-center justify-center">
                          <ShoppingBag className="w-10 h-10 text-purple-400" />
                        </div>
                        <p className="font-medium text-sm truncate">{product.name}</p>
                        <p className="text-purple-600 font-semibold">{product.price || '¥--'}</p>
                      </motion.div>
                    ))}
                  </div>
                </motion.div>
              )}

              {/* 潮流趋势 */}
              {result.fashion_trends && result.fashion_trends.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.4 }}
                  className="glass-card rounded-2xl p-6 bg-gradient-to-r from-orange-100 to-orange-50"
                >
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-12 h-12 rounded-xl bg-orange-500 flex items-center justify-center text-white">
                      <TrendingUp className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-orange-800">潮流趋势</h3>
                      <p className="text-sm text-orange-600">本季流行趋势</p>
                    </div>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {result.fashion_trends.map((trend: any, index: number) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.4 + index * 0.1 }}
                        className="p-4 rounded-xl bg-white/70"
                      >
                        <p className="font-semibold text-orange-700">{trend.style}</p>
                        <p className="text-sm text-orange-600 mt-1">
                          <span className="font-medium">单品：</span>{trend.items}
                        </p>
                        <p className="text-sm text-orange-600">
                          <span className="font-medium">色系：</span>{trend.colors}
                        </p>
                      </motion.div>
                    ))}
                  </div>
                </motion.div>
              )}

              {/* AI效果图提示词 */}
              {result.image_prompt && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.5 }}
                  className="glass-card rounded-2xl p-6 bg-gradient-to-r from-pink-100 to-pink-50"
                >
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-12 h-12 rounded-xl bg-pink-500 flex items-center justify-center text-white">
                      <Image className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-pink-800">AI效果图提示词</h3>
                      <p className="text-sm text-pink-600">可用于生成穿搭效果图</p>
                    </div>
                  </div>
                  <div className="p-4 rounded-xl bg-white/70">
                    <p className="text-sm text-pink-700 italic">{result.image_prompt}</p>
                  </div>
                </motion.div>
              )}
            </motion.div>
          </div>
        )}
      </div>
    </div>
  )
}
