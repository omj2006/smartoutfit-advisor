import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Wand2, Download, Share2, RefreshCw, Sparkles, Check, Loader2 } from 'lucide-react'

const styleOptions = [
  { key: 'casual', label: '休闲' },
  { key: 'formal', label: '正式' },
  { key: 'street', label: '街头' },
  { key: 'elegant', label: '优雅' },
  { key: 'vintage', label: '复古' },
  { key: 'sporty', label: '运动' },
]

const effectImages: Record<string, string> = {
  casual: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=casual%20outfit%20full%20body%20fashion%20photography%20studio%20lighting%20neutral%20background&image_size=portrait_4_3',
  formal: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=formal%20business%20suit%20full%20body%20fashion%20photography%20elegant%20studio&image_size=portrait_4_3',
  street: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=street%20style%20urban%20outfit%20full%20body%20fashion%20photography%20edgy&image_size=portrait_4_3',
  elegant: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=elegant%20evening%20dress%20full%20body%20fashion%20photography%20glamour%20studio&image_size=portrait_4_3',
  vintage: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=vintage%20retro%20outfit%20full%20body%20fashion%20photography%20classic%20style&image_size=portrait_4_3',
  sporty: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=sporty%20athleisure%20outfit%20full%20body%20fashion%20photography%20active%20wear&image_size=portrait_4_3',
}

export default function AiEffect() {
  const [selectedStyle, setSelectedStyle] = useState('casual')
  const [isGenerating, setIsGenerating] = useState(false)
  const [isSaved, setIsSaved] = useState(false)
  const [imageLoaded, setImageLoaded] = useState(false)

  const handleGenerate = () => {
    setIsGenerating(true)
    setImageLoaded(false)
    setIsSaved(false)
    setTimeout(() => {
      setIsGenerating(false)
    }, 2000)
  }

  const handleSave = () => {
    setIsSaved(true)
    setTimeout(() => setIsSaved(false), 2000)
  }

  return (
    <div className="min-h-screen p-4 md:p-6 lg:p-8">
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-6"
      >
        <h2 className="text-2xl font-display font-bold">AI穿搭效果图</h2>
        <p className="text-sm text-muted-foreground mt-0.5">AI为你生成专属穿搭效果图</p>
      </motion.div>

      <div className="max-w-4xl mx-auto space-y-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="relative overflow-hidden rounded-3xl gradient-border"
        >
          <div className="relative glass-card rounded-3xl overflow-hidden">
            <AnimatePresence mode="wait">
              {isGenerating ? (
                <motion.div
                  key="generating"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="aspect-[3/4] md:aspect-[4/3] flex flex-col items-center justify-center gap-4"
                >
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                  >
                    <Loader2 className="w-12 h-12 text-primary" />
                  </motion.div>
                  <div className="text-center">
                    <p className="font-medium">AI正在生成穿搭效果图</p>
                    <p className="text-sm text-muted-foreground mt-1">请稍候...</p>
                  </div>
                  <div className="w-48 h-1.5 rounded-full bg-muted overflow-hidden">
                    <motion.div
                      initial={{ width: '0%' }}
                      animate={{ width: '100%' }}
                      transition={{ duration: 2, ease: 'easeInOut' }}
                      className="h-full rounded-full bg-gradient-rose"
                    />
                  </div>
                </motion.div>
              ) : (
                <motion.div
                  key={selectedStyle}
                  initial={{ opacity: 0, scale: 0.98 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.98 }}
                  transition={{ duration: 0.5 }}
                  className="relative"
                >
                  <img
                    src={effectImages[selectedStyle]}
                    alt={`${selectedStyle} style outfit`}
                    className="w-full aspect-[3/4] md:aspect-[4/3] object-cover"
                    onLoad={() => setImageLoaded(true)}
                  />
                  {!imageLoaded && (
                    <div className="absolute inset-0 bg-muted animate-pulse rounded-3xl" />
                  )}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent" />

                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="absolute bottom-4 left-4 right-4"
                  >
                    <div className="glass rounded-2xl p-3 flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-primary flex-shrink-0" />
                      <p className="text-xs">
                        AI基于你的风格偏好与今日天气生成的
                        <span className="font-medium text-primary">
                          {styleOptions.find((s) => s.key === selectedStyle)?.label}风
                        </span>
                        穿搭效果图
                      </p>
                    </div>
                  </motion.div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <p className="text-xs text-muted-foreground mb-2">选择风格</p>
          <div className="flex gap-2 overflow-x-auto scrollbar-hide pb-1">
            {styleOptions.map((style) => (
              <motion.button
                key={style.key}
                whileTap={{ scale: 0.95 }}
                onClick={() => {
                  setSelectedStyle(style.key)
                  setImageLoaded(false)
                }}
                className={`relative flex-shrink-0 px-5 py-2.5 rounded-full text-xs font-medium transition-all duration-300 ${
                  selectedStyle === style.key
                    ? 'text-white'
                    : 'glass-card text-muted-foreground hover:text-foreground'
                }`}
              >
                {selectedStyle === style.key && (
                  <motion.div
                    layoutId="style-indicator"
                    className="absolute inset-0 bg-gradient-rose rounded-full"
                    transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                  />
                )}
                <span className="relative z-10">{style.label}</span>
              </motion.button>
            ))}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="flex gap-3"
        >
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleGenerate}
            className="flex-1 py-3.5 rounded-2xl bg-gradient-rose text-white font-medium text-sm shadow-glow-rose hover:shadow-lg transition-shadow duration-300 flex items-center justify-center gap-2"
          >
            <Wand2 className="w-4 h-4" />
            重新生成
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleSave}
            className="w-12 h-12 rounded-2xl glass-card flex items-center justify-center hover:shadow-glass transition-shadow duration-300"
          >
            {isSaved ? (
              <Check className="w-5 h-5 text-green-500" />
            ) : (
              <Download className="w-5 h-5" />
            )}
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="w-12 h-12 rounded-2xl glass-card flex items-center justify-center hover:shadow-glass transition-shadow duration-300"
          >
            <Share2 className="w-5 h-5" />
          </motion.button>
        </motion.div>
      </div>
    </div>
  )
}
