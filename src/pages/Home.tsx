import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import {
  Cloud,
  CloudRain,
  Sun,
  CloudSun,
  Briefcase,
  Heart,
  Coffee,
  Dumbbell,
  PartyPopper,
  Plane,
  ChevronRight,
  Sparkles,
  Thermometer,
  Droplets,
  Wind,
} from 'lucide-react'
import { weatherData } from '@/data/weather'
import { outfitsData, scenes } from '@/data/outfits'
import ThemeToggle from '@/components/ThemeToggle'

const iconMap: Record<string, React.ElementType> = {
  cloud: Cloud,
  'cloud-rain': CloudRain,
  sun: Sun,
  'cloud-sun': CloudSun,
  Briefcase,
  Heart,
  Coffee,
  Dumbbell,
  PartyPopper,
  Plane,
}

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.08 },
  },
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
}

export default function Home() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen p-4 md:p-6 lg:p-8 space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h2 className="text-2xl font-display font-bold">早上好 ☀️</h2>
          <p className="text-sm text-muted-foreground mt-0.5">今天想穿什么？</p>
        </div>
        <ThemeToggle />
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="relative overflow-hidden rounded-3xl bg-gradient-rose p-6 text-white shadow-glow-rose"
      >
        <div className="absolute top-0 right-0 w-32 h-32 rounded-full bg-white/10 blur-2xl -translate-y-8 translate-x-8" />
        <div className="absolute bottom-0 left-0 w-24 h-24 rounded-full bg-white/10 blur-2xl translate-y-6 -translate-x-6" />

        <div className="relative z-10">
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-white/80 text-sm">{weatherData.city}</p>
              <div className="flex items-baseline gap-2 mt-1">
                <span className="text-5xl font-display font-bold">{weatherData.temperature}°</span>
                <span className="text-white/80 text-sm">{weatherData.weather}</span>
              </div>
            </div>
            <motion.div
              animate={{ y: [0, -5, 0] }}
              transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
            >
              {(() => {
                const Icon = iconMap[weatherData.icon] || Cloud
                return <Icon className="w-12 h-12 text-white/90" />
              })()}
            </motion.div>
          </div>

          <div className="flex gap-4 mb-4 text-sm text-white/80">
            <div className="flex items-center gap-1">
              <Thermometer className="w-3.5 h-3.5" />
              <span>体感 {weatherData.temperature - 2}°</span>
            </div>
            <div className="flex items-center gap-1">
              <Droplets className="w-3.5 h-3.5" />
              <span>湿度 {weatherData.humidity}%</span>
            </div>
            <div className="flex items-center gap-1">
              <Wind className="w-3.5 h-3.5" />
              <span>微风</span>
            </div>
          </div>

          <div className="bg-white/15 rounded-2xl p-3 backdrop-blur-sm">
            <p className="text-sm font-medium">💡 {weatherData.suggestion}</p>
          </div>

          <div className="flex gap-3 mt-4 overflow-x-auto scrollbar-hide">
            {weatherData.forecast.map((day, i) => {
              const Icon = iconMap[day.icon] || Cloud
              return (
                <div key={i} className="flex-shrink-0 text-center bg-white/10 rounded-xl px-3 py-2 backdrop-blur-sm min-w-[60px]">
                  <p className="text-[10px] text-white/70">{day.day}</p>
                  <Icon className="w-4 h-4 mx-auto my-1 text-white/90" />
                  <p className="text-xs font-medium">{day.temp}°</p>
                </div>
              )
            })}
          </div>
        </div>
      </motion.div>

      <div>
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-semibold">场景穿搭</h3>
          <button
            onClick={() => navigate('/recommend')}
            className="text-xs text-primary flex items-center gap-1 hover:gap-2 transition-all"
          >
            查看全部 <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>
        <motion.div
          variants={container}
          initial="hidden"
          animate="show"
          className="grid grid-cols-3 md:grid-cols-6 gap-3"
        >
          {scenes.map((scene) => {
            const Icon = iconMap[scene.icon] || Sparkles
            return (
              <motion.button
                key={scene.key}
                variants={item}
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/recommend')}
                className="flex flex-col items-center gap-2 p-4 rounded-2xl glass-card hover:shadow-glass dark:hover:shadow-glass-dark transition-shadow duration-300"
              >
                <div className="w-10 h-10 rounded-xl bg-gradient-rose flex items-center justify-center">
                  <Icon className="w-5 h-5 text-white" />
                </div>
                <span className="text-xs font-medium">{scene.label}</span>
              </motion.button>
            )
          })}
        </motion.div>
      </div>

      <div>
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-semibold">今日推荐</h3>
          <button
            onClick={() => navigate('/recommend')}
            className="text-xs text-primary flex items-center gap-1 hover:gap-2 transition-all"
          >
            更多 <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>
        <div className="flex gap-4 overflow-x-auto scrollbar-hide pb-2 -mx-4 px-4 md:mx-0 md:px-0">
          {outfitsData.slice(0, 4).map((outfit, i) => (
            <motion.div
              key={outfit.id}
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 * i }}
              whileHover={{ y: -8, shadow: '0 20px 60px rgba(0,0,0,0.15)' }}
              onClick={() => navigate('/recommend')}
              className="flex-shrink-0 w-56 cursor-pointer group"
            >
              <div className="relative overflow-hidden rounded-2xl mb-3">
                <img
                  src={outfit.image}
                  alt={outfit.title}
                  className="w-full h-72 object-cover group-hover:scale-105 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent" />
                <div className="absolute bottom-3 left-3 right-3">
                  <div className="flex gap-1.5">
                    {outfit.tags.map((tag) => (
                      <span
                        key={tag}
                        className="px-2 py-0.5 rounded-full bg-white/20 backdrop-blur-sm text-[10px] text-white font-medium"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
              <h4 className="text-sm font-semibold line-clamp-1">{outfit.title}</h4>
              <p className="text-xs text-muted-foreground line-clamp-1 mt-0.5">{outfit.description}</p>
            </motion.div>
          ))}
        </div>
      </div>

      <div>
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-semibold">潮流速递</h3>
          <button
            onClick={() => navigate('/trends')}
            className="text-xs text-primary flex items-center gap-1 hover:gap-2 transition-all"
          >
            更多 <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>
        <div className="flex gap-3 overflow-x-auto scrollbar-hide pb-2 -mx-4 px-4 md:mx-0 md:px-0">
          {[1, 2, 3].map((i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.15 * i }}
              whileHover={{ y: -4 }}
              onClick={() => navigate('/trends')}
              className="flex-shrink-0 w-40 cursor-pointer group"
            >
              <div className="relative overflow-hidden rounded-2xl mb-2">
                <img
                  src={`https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=fashion%20trend%20news%20${i}%20editorial%20style&image_size=square`}
                  alt="trend"
                  className="w-full h-40 object-cover group-hover:scale-105 transition-transform duration-500"
                />
              </div>
              <h4 className="text-xs font-medium line-clamp-2">
                {['春夏色彩趋势', '复古风回潮', '极简穿搭术'][i - 1]}
              </h4>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  )
}
