import { NavLink } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Home, Sparkles, Wand2, User, Newspaper, Workflow } from 'lucide-react'

const navItems = [
  { to: '/', icon: Home, label: '首页' },
  { to: '/recommend', icon: Sparkles, label: '推荐' },
  { to: '/workflow', icon: Workflow, label: '智能', isSpecial: true },
  { to: '/ai-effect', icon: Wand2, label: 'AI' },
  { to: '/profile', icon: User, label: '我的' },
]

export default function BottomNav() {
  return (
    <nav className="lg:hidden fixed bottom-0 left-0 right-0 glass border-t border-[var(--border-color)] z-50 safe-area-bottom">
      <div className="flex items-center justify-around h-16 px-2">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) => {
              if (item.isSpecial) {
                return 'flex flex-col items-center justify-center w-14 h-14'
              }
              return `flex flex-col items-center gap-1 px-3 py-1 rounded-xl transition-colors duration-300 ${
                isActive ? 'text-primary' : 'text-muted-foreground'
              }`
            }}
          >
            {({ isActive }) => (
              <>
                {item.isSpecial ? (
                  <motion.div
                    whileTap={{ scale: 0.9 }}
                    className={`w-12 h-12 rounded-2xl flex items-center justify-center shadow-lg transition-all duration-300 ${
                      isActive 
                        ? 'bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 shadow-blue-200/50 shadow-purple-200/50' 
                        : 'bg-gradient-to-r from-blue-500 to-purple-500'
                    }`}
                  >
                    <motion.div
                      animate={{ 
                        scale: isActive ? [1, 1.1, 1] : 1,
                        rotate: isActive ? [0, 5, -5, 0] : 0 
                      }}
                      transition={{ duration: 1.5, repeat: isActive ? Infinity : 0 }}
                    >
                      <Workflow className="w-6 h-6 text-white" />
                    </motion.div>
                  </motion.div>
                ) : (
                  <div className="relative">
                    <motion.div whileTap={{ scale: 0.85 }}>
                      <item.icon className="w-5 h-5" />
                    </motion.div>
                    {isActive && (
                      <motion.div
                        layoutId="bottomnav-dot"
                        className="absolute -bottom-1 left-1/2 -translate-x-1/2 w-1 h-1 rounded-full bg-primary"
                        transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                      />
                    )}
                  </div>
                )}
                {!item.isSpecial && (
                  <span className="text-[10px] font-medium">{item.label}</span>
                )}
                {item.isSpecial && (
                  <motion.span 
                    className="text-[10px] font-bold text-purple-600"
                    animate={{ opacity: isActive ? [1, 0.5, 1] : 1 }}
                    transition={{ duration: 1.5, repeat: isActive ? Infinity : 0 }}
                  >
                    智能
                  </motion.span>
                )}
              </>
            )}
          </NavLink>
        ))}
      </div>
    </nav>
  )
}
