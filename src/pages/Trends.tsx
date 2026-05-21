import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, Heart, Bookmark, TrendingUp, Clock } from 'lucide-react'
import { trendsData, categories, hotTopics } from '@/data/trends'
import type { Trend } from '@/data/trends'

const container = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.06 } },
}

const cardVariant = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
}

export default function Trends() {
  const [activeCategory, setActiveCategory] = useState('全部')
  const [searchQuery, setSearchQuery] = useState('')
  const [likes, setLikes] = useState<Record<number, number>>({})

  const filtered = trendsData.filter((t) => {
    if (activeCategory !== '全部' && t.category !== activeCategory) return false
    if (searchQuery && !t.title.includes(searchQuery) && !t.summary.includes(searchQuery)) return false
    return true
  })

  const toggleLike = (id: number) => {
    setLikes((prev) => ({
      ...prev,
      [id]: (prev[id] || 0) === 1 ? 0 : 1,
    }))
  }

  return (
    <div className="min-h-screen p-4 md:p-6 lg:p-8 space-y-5">
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h2 className="text-2xl font-display font-bold">潮流资讯</h2>
        <p className="text-sm text-muted-foreground mt-0.5">发现最新时尚趋势与穿搭灵感</p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="relative"
      >
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
        <input
          type="text"
          placeholder="搜索资讯..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full pl-11 pr-4 py-3 rounded-2xl glass-card text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all duration-300 placeholder:text-muted-foreground/60"
        />
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.15 }}
        className="flex gap-2 overflow-x-auto scrollbar-hide pb-1"
      >
        {categories.map((cat) => (
          <motion.button
            key={cat}
            whileTap={{ scale: 0.95 }}
            onClick={() => setActiveCategory(cat)}
            className={`flex-shrink-0 px-4 py-2 rounded-full text-xs font-medium transition-all duration-300 ${
              activeCategory === cat
                ? 'bg-gradient-rose text-white shadow-glow-rose'
                : 'glass-card text-muted-foreground hover:text-foreground'
            }`}
          >
            {cat}
          </motion.button>
        ))}
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="glass-card rounded-2xl p-4"
      >
        <div className="flex items-center gap-2 mb-3">
          <TrendingUp className="w-4 h-4 text-primary" />
          <span className="text-sm font-medium">热门话题</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {hotTopics.map((topic) => (
            <motion.button
              key={topic}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-3 py-1.5 rounded-full bg-primary/10 text-primary text-xs font-medium hover:bg-primary/20 transition-colors"
            >
              {topic}
            </motion.button>
          ))}
        </div>
      </motion.div>

      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        key={activeCategory}
        className="columns-1 md:columns-2 xl:columns-3 gap-4 space-y-4"
      >
        <AnimatePresence mode="popLayout">
          {filtered.map((trend) => (
            <TrendCard
              key={trend.id}
              trend={trend}
              isLiked={(likes[trend.id] || 0) === 1}
              likeCount={trend.likes + (likes[trend.id] || 0)}
              onLike={() => toggleLike(trend.id)}
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
          <p className="text-muted-foreground">暂无匹配的资讯</p>
        </motion.div>
      )}
    </div>
  )
}

function TrendCard({
  trend,
  isLiked,
  likeCount,
  onLike,
}: {
  trend: Trend
  isLiked: boolean
  likeCount: number
  onLike: () => void
}) {
  return (
    <motion.div
      variants={cardVariant}
      layout
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      whileHover={{ y: -4 }}
      className="break-inside-avoid glass-card rounded-2xl overflow-hidden group cursor-pointer hover:shadow-card-hover dark:hover:shadow-glass-dark transition-shadow duration-500"
    >
      <div className="relative overflow-hidden">
        <img
          src={trend.image}
          alt={trend.title}
          className="w-full object-cover group-hover:scale-105 transition-transform duration-700"
          style={{ height: trend.height }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent" />
        <div className="absolute top-3 left-3">
          <span className="px-2.5 py-1 rounded-full bg-white/20 backdrop-blur-sm text-[10px] text-white font-medium">
            {trend.category}
          </span>
        </div>
      </div>

      <div className="p-4">
        <h3 className="text-sm font-semibold line-clamp-2 mb-1">{trend.title}</h3>
        <p className="text-xs text-muted-foreground line-clamp-2">{trend.summary}</p>

        <div className="flex items-center justify-between mt-3 pt-3 border-t border-[var(--border-color)]">
          <div className="flex items-center gap-2 text-[10px] text-muted-foreground">
            <div className="flex items-center gap-1">
              <Clock className="w-3 h-3" />
              <span>{trend.date}</span>
            </div>
            <span>·</span>
            <span>{trend.author}</span>
          </div>
          <div className="flex items-center gap-2">
            <motion.button
              whileTap={{ scale: 0.8 }}
              onClick={(e) => {
                e.stopPropagation()
                onLike()
              }}
              className="flex items-center gap-1"
            >
              <Heart
                className={`w-3.5 h-3.5 transition-colors ${
                  isLiked ? 'fill-red-400 text-red-400' : 'text-muted-foreground'
                }`}
              />
              <span className="text-[10px] text-muted-foreground">{likeCount}</span>
            </motion.button>
            <motion.button whileTap={{ scale: 0.8 }} onClick={(e) => e.stopPropagation()}>
              <Bookmark className="w-3.5 h-3.5 text-muted-foreground hover:text-primary transition-colors" />
            </motion.button>
          </div>
        </div>
      </div>
    </motion.div>
  )
}
