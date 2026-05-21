import { NavLink } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Home, Sparkles, Wand2, User, Newspaper, LogOut, Crown } from 'lucide-react'
import ThemeToggle from './ThemeToggle'
import { useUserStore } from '@/store/useUserStore'

const navItems = [
  { to: '/', icon: Home, label: '首页' },
  { to: '/recommend', icon: Sparkles, label: '穿搭推荐' },
  { to: '/ai-effect', icon: Wand2, label: 'AI效果图' },
  { to: '/trends', icon: Newspaper, label: '潮流资讯' },
  { to: '/profile', icon: User, label: '个人中心' },
]

export default function Sidebar() {
  const { username, avatar, isVip, logout, isLoading } = useUserStore()

  return (
    <aside className="hidden lg:flex flex-col w-64 h-screen fixed left-0 top-0 glass border-r border-[var(--border-color)] z-50">
      <div className="p-6 flex items-center gap-3">
        <div className="w-10 h-10 rounded-2xl bg-gradient-rose flex items-center justify-center">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="font-display text-xl font-semibold gradient-text">StyleAI</h1>
          <p className="text-xs text-muted-foreground">AI穿搭助手</p>
        </div>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-medium transition-all duration-300 group ${
                isActive
                  ? 'bg-gradient-rose text-white shadow-glow-rose'
                  : 'text-muted-foreground hover:text-foreground hover:bg-muted/50'
              }`
            }
          >
            {({ isActive }) => (
              <>
                <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.95 }}>
                  <item.icon className="w-5 h-5" />
                </motion.div>
                <span>{item.label}</span>
                {isActive && (
                  <motion.div
                    layoutId="sidebar-active"
                    className="ml-auto w-1.5 h-1.5 rounded-full bg-white"
                  />
                )}
              </>
            )}
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-[var(--border-color)] space-y-4">
        <div className="flex items-center gap-3 px-2">
          <img
            src={avatar}
            alt={username}
            className="w-10 h-10 rounded-full object-cover"
          />
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-1">
              <p className="text-sm font-medium truncate">{username || '用户'}</p>
              {isVip && <Crown className="w-3.5 h-3.5 text-amber-400" />}
            </div>
            <p className="text-xs text-muted-foreground">{isVip ? 'VIP会员' : '普通用户'}</p>
          </div>
        </div>
        
        <div className="flex items-center justify-between px-2">
          <span className="text-xs text-muted-foreground">主题切换</span>
          <ThemeToggle />
        </div>
        
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={logout}
          disabled={isLoading}
          className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-muted/50 text-muted-foreground hover:bg-muted hover:text-foreground text-sm transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <LogOut className="w-4 h-4" />
          <span>退出登录</span>
        </motion.button>
      </div>
    </aside>
  )
}
