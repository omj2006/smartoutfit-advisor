import { Loader2 } from 'lucide-react'
import { motion } from 'framer-motion'

interface LoadingProps {
  text?: string
  size?: 'sm' | 'md' | 'lg'
}

export function Loading({ text = '加载中...', size = 'md' }: LoadingProps) {
  const sizeClasses = {
    sm: 'w-5 h-5',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="flex flex-col items-center justify-center gap-4 py-12"
    >
      <Loader2 className={`${sizeClasses[size]} animate-spin text-purple-600`} />
      <p className="text-gray-500 text-sm">{text}</p>
    </motion.div>
  )
}

export function PageLoading() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <div className="text-center">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
        >
          <Loader2 className="w-16 h-16 text-purple-600 mx-auto" />
        </motion.div>
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mt-4 text-gray-600 dark:text-gray-300"
        >
          加载中...
        </motion.p>
      </div>
    </div>
  )
}

export function ButtonLoading({ children, isLoading }: { children: React.ReactNode, isLoading: boolean }) {
  return (
    <div className="relative">
      {children}
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-inherit rounded-lg">
          <Loader2 className="w-5 h-5 animate-spin" />
        </div>
      )}
    </div>
  )
}
