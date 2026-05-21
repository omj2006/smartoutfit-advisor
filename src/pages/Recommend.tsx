import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { SlidersHorizontal, Heart, Star, ChevronDown, X, Sparkles, Send, Loader2, Workflow, Cloud, BookOpen, ShoppingBag, TrendingUp, Image } from 'lucide-react'
import { outfitsData, scenes, styles } from '@/data/outfits'
import type { Outfit } from '@/data/outfits'
import { apiClient } from '@/api/client'

const container = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.06 } },
}

const cardVariant = {
  hidden: { opacity: 0, y: 30 },
  show: { opacity: 1, y: 0 },
}

export default function Recommend() {
  const [selectedScene, setSelectedScene] = useState<string | null>(null)
  const [selectedStyle, setSelectedStyle] = useState<string | null>(null)
  const [expandedId, setExpandedId] = useState<number | null>(null)
  const [favorites, setFavorites] = useState<Set<number>>(new Set())
  const [aiResponse, setAiResponse] = useState<string | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [showAiPanel, setShowAiPanel] = useState(false)
  const [aiMessage, setAiMessage] = useState('')
  // LangGraph 工作流状态
  const [showLangGraphPanel, setShowLangGraphPanel] = useState(false)
  const [langGraphResult, setLangGraphResult] = useState<any>(null)
  const [isLangGraphRunning, setIsLangGraphRunning] = useState(false)
  const [selectedCity, setSelectedCity] = useState('')
  const [executionSteps, setExecutionSteps] = useState<{ agent: string; status: string; message: string }[]>([])
  const navigate = useNavigate()

  const generateAiRecommendation = async () => {
    if (!selectedScene && !selectedStyle) {
      alert('请至少选择一个场景或风格')
      return
    }

    setIsGenerating(true)
    setAiResponse(null)
    
    const prompt = `为我推荐${selectedScene ? `${scenes.find(s => s.key === selectedScene)?.label}场景` : ''}${selectedStyle ? `，${styles.find(s => s.key === selectedStyle)?.label}风格` : ''}的穿搭方案，包括上衣、下装、鞋子和配饰建议。`
    
    try {
      const response = await apiClient.chat(prompt.trim())
      if (response.success && response.data) {
        setAiResponse(response.data.response || JSON.stringify(response.data))
      } else {
        setAiResponse('AI推荐生成失败，请稍后重试')
      }
    } catch (error) {
      setAiResponse(`生成失败: ${error instanceof Error ? error.message : '未知错误'}`)
    } finally {
      setIsGenerating(false)
    }
  }

  const sendAiMessage = async () => {
    if (!aiMessage.trim()) return
    
    setIsGenerating(true)
    setAiResponse(null)
    
    try {
      const response = await apiClient.chat(aiMessage)
      if (response.success && response.data) {
        setAiResponse(response.data.response || JSON.stringify(response.data))
      } else {
        setAiResponse('消息发送失败，请稍后重试')
      }
    } catch (error) {
      setAiResponse(`发送失败: ${error instanceof Error ? error.message : '未知错误'}`)
    } finally {
      setIsGenerating(false)
    }
  }

  // LangGraph 多智能体工作流执行
  const runLangGraphWorkflow = async () => {
    if (!selectedCity) {
      alert('请先选择城市')
      return
    }

    setIsLangGraphRunning(true)
    setLangGraphResult(null)
    setExecutionSteps([])

    const steps = [
      { agent: 'memory', label: '记忆加载', icon: '🧠' },
      { agent: 'weather', label: '天气查询', icon: '🌤️' },
      { agent: 'knowledge', label: '知识库', icon: '📚' },
      { agent: 'retrieval', label: '商品检索', icon: '🛍️' },
      { agent: 'trend', label: '潮流趋势', icon: '📈' },
      { agent: 'image', label: '图像准备', icon: '🎨' },
    ]

    let currentStep = 0
    const updateStep = (agent: string, status: string, message: string) => {
      setExecutionSteps(prev => [...prev, { agent, status, message }])
    }

    try {
      for (const step of steps) {
        updateStep(step.agent, 'running', `${step.icon} ${step.label}...`)
        await new Promise(resolve => setTimeout(resolve, 300))
        currentStep++
      }

      const response = await apiClient.langgraphOutfit({
        city: selectedCity,
        occasion: selectedScene ? scenes.find(s => s.key === selectedScene)?.label : '',
        query: aiMessage || '请给我推荐穿搭方案',
        user_id: 'default'
      })

      if (response.success && response.data) {
        setLangGraphResult(response.data)
        steps.forEach(step => {
          updateStep(step.agent, 'completed', `${step.icon} ${step.label}完成`)
        })
      } else {
        setLangGraphResult({ error: response.error || '工作流执行失败' })
      }
    } catch (error) {
      console.error('LangGraph workflow error:', error)
      setLangGraphResult({ 
        error: error instanceof Error ? error.message : '网络错误，请检查API配置',
        fallback: true 
      })
    } finally {
      setIsLangGraphRunning(false)
    }
  }

  const filtered = outfitsData.filter((o) => {
    if (selectedScene && o.scene !== selectedScene) return false
    if (selectedStyle && o.style !== selectedStyle) return false
    return true
  })

  const toggleFav = (id: number, e: React.MouseEvent) => {
    e.stopPropagation()
    setFavorites((prev) => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  return (
    <div className="min-h-screen p-4 md:p-6 lg:p-8 space-y-5">
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col md:flex-row md:items-center md:justify-between gap-4"
      >
        <div>
          <h2 className="text-2xl font-display font-bold">智能穿搭推荐</h2>
          <p className="text-sm text-muted-foreground mt-0.5">基于天气与偏好的个性化搭配方案</p>
        </div>
        <div className="flex gap-3">
          <motion.button
            whileTap={{ scale: 0.95 }}
            onClick={() => setShowAiPanel(!showAiPanel)}
            className={`flex items-center gap-2 px-4 py-2 rounded-full font-medium text-sm transition-all duration-300 ${
              showAiPanel
                ? 'bg-gradient-rose text-white shadow-glow-rose'
                : 'glass-card text-muted-foreground hover:text-foreground hover:shadow-card'
            }`}
          >
            <Sparkles className="w-4 h-4" />
            AI穿搭顾问
          </motion.button>
          <motion.button
            whileTap={{ scale: 0.95 }}
            onClick={() => setShowLangGraphPanel(!showLangGraphPanel)}
            className={`flex items-center gap-2 px-4 py-2 rounded-full font-medium text-sm transition-all duration-300 ${
              showLangGraphPanel
                ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg'
                : 'glass-card text-muted-foreground hover:text-foreground hover:shadow-card'
            }`}
          >
            <Workflow className="w-4 h-4" />
            多智能体工作流
          </motion.button>
        </div>
      </motion.div>

      <AnimatePresence>
        {showAiPanel && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className="glass-card rounded-3xl p-4 overflow-hidden"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-rose-400" />
                AI穿搭顾问
              </h3>
              <button
                onClick={() => setShowAiPanel(false)}
                className="w-8 h-8 rounded-full hover:bg-white/10 flex items-center justify-center transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="mb-4">
              <p className="text-sm text-muted-foreground mb-3">选择场景和风格后点击生成推荐，或直接向AI咨询穿搭建议</p>
              <motion.button
                whileTap={{ scale: 0.95 }}
                onClick={generateAiRecommendation}
                disabled={isGenerating}
                className="w-full py-3 rounded-xl bg-gradient-rose text-white font-medium flex items-center justify-center gap-2 shadow-glow-rose disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    生成中...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" />
                    生成AI穿搭推荐
                  </>
                )}
              </motion.button>
            </div>

            <div className="border-t border-[var(--border-color)] pt-4">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={aiMessage}
                  onChange={(e) => setAiMessage(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && sendAiMessage()}
                  placeholder="向AI咨询穿搭建议..."
                  className="flex-1 px-4 py-2 rounded-full bg-white/10 border border-[var(--border-color)] text-sm focus:outline-none focus:ring-2 focus:ring-rose-400/50"
                />
                <motion.button
                  whileTap={{ scale: 0.95 }}
                  onClick={sendAiMessage}
                  disabled={isGenerating || !aiMessage.trim()}
                  className="w-10 h-10 rounded-full bg-gradient-rose text-white flex items-center justify-center shadow-glow-rose disabled:opacity-50"
                >
                  {isGenerating ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                </motion.button>
              </div>
            </div>

            {aiResponse && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-4 p-4 rounded-xl bg-white/5 border border-[var(--border-color)]"
              >
                <div className="text-sm whitespace-pre-wrap text-muted-foreground">{aiResponse}</div>
              </motion.div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* LangGraph 多智能体工作流面板 */}
      <AnimatePresence>
        {showLangGraphPanel && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className="glass-card rounded-3xl p-6 overflow-hidden"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold flex items-center gap-2 text-lg">
                <Workflow className="w-5 h-5 text-blue-500" />
                🤖 LangGraph 多智能体工作流
              </h3>
              <button
                onClick={() => setShowLangGraphPanel(false)}
                className="w-8 h-8 rounded-full hover:bg-white/10 flex items-center justify-center transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* 智能体介绍卡片 */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
              {[
                { icon: Cloud, label: '天气查询', desc: '实时天气数据', color: 'bg-blue-500' },
                { icon: BookOpen, label: '知识库', desc: '穿搭建议', color: 'bg-green-500' },
                { icon: ShoppingBag, label: '商品检索', desc: '向量搜索', color: 'bg-purple-500' },
                { icon: TrendingUp, label: '潮流趋势', desc: '时尚抓取', color: 'bg-orange-500' },
                { icon: Image, label: '图像生成', desc: 'AI效果图', color: 'bg-pink-500' },
                { icon: Workflow, label: '记忆系统', desc: '用户偏好', color: 'bg-indigo-500' },
              ].map((agent, index) => (
                <motion.div
                  key={agent.label}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.05 }}
                  className="glass-card rounded-xl p-3 text-center hover:shadow-card transition-shadow"
                >
                  <div className={`w-10 h-10 mx-auto rounded-xl ${agent.color} flex items-center justify-center mb-2`}>
                    <agent.icon className="w-5 h-5 text-white" />
                  </div>
                  <p className="text-xs font-medium">{agent.label}</p>
                  <p className="text-[10px] text-muted-foreground mt-0.5">{agent.desc}</p>
                </motion.div>
              ))}
            </div>

            {/* 执行配置 */}
            <div className="flex flex-col md:flex-row gap-4 mb-4">
              <div className="flex-1">
                <label className="text-xs text-muted-foreground mb-1 block">选择城市</label>
                <select
                  value={selectedCity}
                  onChange={(e) => setSelectedCity(e.target.value)}
                  className="w-full px-4 py-2 rounded-xl bg-white/10 border border-[var(--border-color)] text-sm focus:outline-none focus:ring-2 focus:ring-blue-400/50"
                >
                  <option value="">请选择城市</option>
                  <option value="北京">北京</option>
                  <option value="上海">上海</option>
                  <option value="广州">广州</option>
                  <option value="深圳">深圳</option>
                  <option value="成都">成都</option>
                  <option value="杭州">杭州</option>
                </select>
              </div>
              <div className="flex-1">
                <label className="text-xs text-muted-foreground mb-1 block">选择场合</label>
                <select
                  value={selectedScene || ''}
                  onChange={(e) => setSelectedScene(e.target.value || null)}
                  className="w-full px-4 py-2 rounded-xl bg-white/10 border border-[var(--border-color)] text-sm focus:outline-none focus:ring-2 focus:ring-blue-400/50"
                >
                  <option value="">全部场合</option>
                  {scenes.map((s) => (
                    <option key={s.key} value={s.key}>{s.label}</option>
                  ))}
                </select>
              </div>
              <div className="flex-1">
                <label className="text-xs text-muted-foreground mb-1 block">选择风格</label>
                <select
                  value={selectedStyle || ''}
                  onChange={(e) => setSelectedStyle(e.target.value || null)}
                  className="w-full px-4 py-2 rounded-xl bg-white/10 border border-[var(--border-color)] text-sm focus:outline-none focus:ring-2 focus:ring-blue-400/50"
                >
                  <option value="">全部风格</option>
                  {styles.map((s) => (
                    <option key={s.key} value={s.key}>{s.label}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* 执行按钮 */}
            <motion.button
              whileTap={{ scale: 0.98 }}
              onClick={runLangGraphWorkflow}
              disabled={isLangGraphRunning}
              className="w-full py-3 rounded-xl bg-gradient-to-r from-blue-500 to-purple-500 text-white font-medium flex items-center justify-center gap-2 shadow-lg disabled:opacity-50"
            >
              {isLangGraphRunning ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  多智能体工作流执行中...
                </>
              ) : (
                <>
                  <Workflow className="w-4 h-4" />
                  启动多智能体工作流
                </>
              )}
            </motion.button>

            {/* 执行步骤展示 */}
            {isLangGraphRunning && executionSteps.length > 0 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="mt-4 p-4 rounded-xl bg-white/5 border border-[var(--border-color)]"
              >
                <p className="text-xs text-muted-foreground mb-2">🔄 执行日志</p>
                <div className="space-y-1 max-h-40 overflow-y-auto">
                  {executionSteps.map((step, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      className={`text-xs ${step.status === 'completed' ? 'text-green-500' : step.status === 'running' ? 'text-blue-500' : 'text-muted-foreground'}`}
                    >
                      {step.message}
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            )}

            {/* 结果展示 */}
            {langGraphResult && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-4 space-y-4"
              >
                {langGraphResult.error ? (
                  <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30">
                    <p className="text-sm text-red-400">{langGraphResult.error}</p>
                    {langGraphResult.fallback && (
                      <p className="text-xs text-muted-foreground mt-2">提示：完整功能需要配置 AI API 密钥</p>
                    )}
                  </div>
                ) : (
                  <>
                    {/* 天气信息 */}
                    {langGraphResult.weather && (
                      <div className="glass-card rounded-xl p-4">
                        <h4 className="text-sm font-medium flex items-center gap-2 mb-2">
                          <Cloud className="w-4 h-4 text-blue-400" />
                          天气信息
                        </h4>
                        <div className="text-sm">
                          <p>{langGraphResult.weather.city || selectedCity} {langGraphResult.weather.temperature}°C</p>
                          <p className="text-muted-foreground text-xs">{langGraphResult.weather.condition}</p>
                        </div>
                      </div>
                    )}

                    {/* 穿搭建议 */}
                    {langGraphResult.outfit_suggestion && (
                      <div className="glass-card rounded-xl p-4">
                        <h4 className="text-sm font-medium flex items-center gap-2 mb-2">
                          <BookOpen className="w-4 h-4 text-green-400" />
                          穿搭建议
                        </h4>
                        <p className="text-sm">{langGraphResult.outfit_suggestion.description || '根据您的偏好，为您推荐适合的穿搭方案'}</p>
                        {langGraphResult.outfit_suggestion.style && (
                          <span className="inline-block mt-2 px-2 py-1 rounded-full bg-green-100 text-green-700 text-xs">
                            {langGraphResult.outfit_suggestion.style}风格
                          </span>
                        )}
                      </div>
                    )}

                    {/* 商品推荐 */}
                    {langGraphResult.filtered_products && langGraphResult.filtered_products.length > 0 && (
                      <div className="glass-card rounded-xl p-4">
                        <h4 className="text-sm font-medium flex items-center gap-2 mb-3">
                          <ShoppingBag className="w-4 h-4 text-purple-400" />
                          商品推荐 ({langGraphResult.filtered_products.length})
                        </h4>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                          {langGraphResult.filtered_products.slice(0, 4).map((product, index) => (
                            <div key={index} className="glass rounded-lg p-2 text-center">
                              <p className="text-xs font-medium truncate">{product.name || `商品${index + 1}`}</p>
                              <p className="text-[10px] text-muted-foreground">{product.price || '-'}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* 潮流趋势 */}
                    {langGraphResult.fashion_trends && langGraphResult.fashion_trends.length > 0 && (
                      <div className="glass-card rounded-xl p-4">
                        <h4 className="text-sm font-medium flex items-center gap-2 mb-2">
                          <TrendingUp className="w-4 h-4 text-orange-400" />
                          潮流趋势
                        </h4>
                        <div className="flex flex-wrap gap-2">
                          {langGraphResult.fashion_trends.map((trend, index) => (
                            <span key={index} className="px-2 py-1 rounded-full bg-orange-100 text-orange-700 text-xs">
                              {trend}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* 图像提示词 */}
                    {langGraphResult.image_prompt && (
                      <div className="glass-card rounded-xl p-4">
                        <h4 className="text-sm font-medium flex items-center gap-2 mb-2">
                          <Image className="w-4 h-4 text-pink-400" />
                          AI效果图提示词
                        </h4>
                        <p className="text-xs text-muted-foreground">{langGraphResult.image_prompt}</p>
                      </div>
                    )}
                  </>
                )}
              </motion.div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="space-y-3"
      >
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <SlidersHorizontal className="w-3.5 h-3.5" />
          <span>场景筛选</span>
        </div>
        <div className="flex gap-2 overflow-x-auto scrollbar-hide pb-1">
          <motion.button
            whileTap={{ scale: 0.95 }}
            onClick={() => setSelectedScene(null)}
            className={`flex-shrink-0 px-4 py-2 rounded-full text-xs font-medium transition-all duration-300 ${
              !selectedScene
                ? 'bg-gradient-rose text-white shadow-glow-rose'
                : 'glass-card text-muted-foreground hover:text-foreground'
            }`}
          >
            全部
          </motion.button>
          {scenes.map((s) => (
            <motion.button
              key={s.key}
              whileTap={{ scale: 0.95 }}
              onClick={() => setSelectedScene(s.key === selectedScene ? null : s.key)}
              className={`flex-shrink-0 px-4 py-2 rounded-full text-xs font-medium transition-all duration-300 ${
                selectedScene === s.key
                  ? 'bg-gradient-rose text-white shadow-glow-rose'
                  : 'glass-card text-muted-foreground hover:text-foreground'
              }`}
            >
              {s.label}
            </motion.button>
          ))}
        </div>

        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <SlidersHorizontal className="w-3.5 h-3.5" />
          <span>风格筛选</span>
        </div>
        <div className="flex gap-2 overflow-x-auto scrollbar-hide pb-1">
          <motion.button
            whileTap={{ scale: 0.95 }}
            onClick={() => setSelectedStyle(null)}
            className={`flex-shrink-0 px-4 py-2 rounded-full text-xs font-medium transition-all duration-300 ${
              !selectedStyle
                ? 'bg-gradient-rose text-white shadow-glow-rose'
                : 'glass-card text-muted-foreground hover:text-foreground'
            }`}
          >
            全部
          </motion.button>
          {styles.map((s) => (
            <motion.button
              key={s.key}
              whileTap={{ scale: 0.95 }}
              onClick={() => setSelectedStyle(s.key === selectedStyle ? null : s.key)}
              className={`flex-shrink-0 px-4 py-2 rounded-full text-xs font-medium transition-all duration-300 ${
                selectedStyle === s.key
                  ? 'bg-gradient-rose text-white shadow-glow-rose'
                  : 'glass-card text-muted-foreground hover:text-foreground'
              }`}
            >
              {s.label}
            </motion.button>
          ))}
        </div>
      </motion.div>

      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        key={`${selectedScene}-${selectedStyle}`}
        className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4"
      >
        <AnimatePresence mode="popLayout">
          {filtered.map((outfit) => (
            <OutfitCard
              key={outfit.id}
              outfit={outfit}
              isExpanded={expandedId === outfit.id}
              isFavorite={favorites.has(outfit.id)}
              onToggleExpand={() => setExpandedId(expandedId === outfit.id ? null : outfit.id)}
              onToggleFav={(e) => toggleFav(outfit.id, e)}
              onViewEffect={() => navigate('/ai-effect')}
            />
          ))}
        </AnimatePresence>
      </motion.div>

      {filtered.length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-20"
        >
          <p className="text-muted-foreground">暂无匹配的穿搭方案</p>
          <button
            onClick={() => {
              setSelectedScene(null)
              setSelectedStyle(null)
            }}
            className="mt-2 text-sm text-primary hover:underline"
          >
            清除筛选
          </button>
        </motion.div>
      )}
    </div>
  )
}

function OutfitCard({
  outfit,
  isExpanded,
  isFavorite,
  onToggleExpand,
  onToggleFav,
  onViewEffect,
}: {
  outfit: Outfit
  isExpanded: boolean
  isFavorite: boolean
  onToggleExpand: () => void
  onToggleFav: (e: React.MouseEvent) => void
  onViewEffect: () => void
}) {
  return (
    <motion.div
      variants={cardVariant}
      layout
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      whileHover={{ y: -6 }}
      className="glass-card rounded-3xl overflow-hidden group cursor-pointer hover:shadow-card-hover dark:hover:shadow-glass-dark transition-shadow duration-500"
    >
      <div className="relative overflow-hidden">
        <img
          src={outfit.image}
          alt={outfit.title}
          className="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-700"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent" />

        <motion.button
          whileTap={{ scale: 0.8 }}
          onClick={onToggleFav}
          className="absolute top-3 right-3 w-9 h-9 rounded-full glass flex items-center justify-center"
        >
          <Heart
            className={`w-4 h-4 transition-colors ${
              isFavorite ? 'fill-red-400 text-red-400' : 'text-white'
            }`}
          />
        </motion.button>

        <div className="absolute bottom-3 left-3 flex gap-1.5">
          {outfit.tags.map((tag) => (
            <span
              key={tag}
              className="px-2.5 py-1 rounded-full bg-white/20 backdrop-blur-sm text-[10px] text-white font-medium"
            >
              {tag}
            </span>
          ))}
        </div>
      </div>

      <div className="p-4">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h3 className="font-semibold text-sm">{outfit.title}</h3>
            <p className="text-xs text-muted-foreground mt-1 line-clamp-1">{outfit.description}</p>
          </div>
          <div className="flex items-center gap-1 ml-2 flex-shrink-0">
            <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
            <span className="text-xs font-medium">{outfit.rating}</span>
          </div>
        </div>

        <div className="flex items-center justify-between mt-3">
          <button
            onClick={onToggleExpand}
            className="text-xs text-muted-foreground hover:text-foreground flex items-center gap-1 transition-colors"
          >
            搭配详情
            <motion.div animate={{ rotate: isExpanded ? 180 : 0 }}>
              <ChevronDown className="w-3.5 h-3.5" />
            </motion.div>
          </button>
          <motion.button
            whileTap={{ scale: 0.95 }}
            onClick={onViewEffect}
            className="px-3 py-1.5 rounded-full bg-gradient-rose text-white text-xs font-medium shadow-glow-rose"
          >
            AI效果图
          </motion.button>
        </div>

        <AnimatePresence>
          {isExpanded && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.3 }}
              className="overflow-hidden"
            >
              <div className="mt-3 pt-3 border-t border-[var(--border-color)] space-y-2">
                {outfit.items.map((item, i) => (
                  <div key={i} className="flex items-center justify-between text-xs">
                    <span className="font-medium">{item.name}</span>
                    <div className="flex items-center gap-2 text-muted-foreground">
                      <span>{item.brand}</span>
                      <span className="text-primary font-medium">{item.price}</span>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  )
}
