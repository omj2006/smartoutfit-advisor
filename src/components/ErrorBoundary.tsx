import { motion } from 'framer-motion'
import { AlertCircle, RefreshCw, Home } from 'lucide-react'
import { Link } from 'react-router-dom'

interface ErrorBoundaryProps {
  error?: string
  onRetry?: () => void
  showHome?: boolean
}

export function ErrorDisplay({ 
  error = '出错了，请稍后重试', 
  onRetry,
  showHome = true 
}: ErrorBoundaryProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="flex flex-col items-center justify-center py-12 px-4"
    >
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ type: 'spring', delay: 0.1 }}
        className="bg-red-100 dark:bg-red-900/20 p-4 rounded-full mb-4"
      >
        <AlertCircle className="w-8 h-8 text-red-600 dark:text-red-400" />
      </motion.div>
      
      <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-2">
        加载失败
      </h3>
      
      <p className="text-gray-500 dark:text-gray-400 text-center mb-6 max-w-md">
        {error}
      </p>
      
      <div className="flex gap-3">
        {onRetry && (
          <button
            onClick={onRetry}
            className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            重试
          </button>
        )}
        
        {showHome && (
          <Link
            to="/"
            className="flex items-center gap-2 px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            <Home className="w-4 h-4" />
            返回首页
          </Link>
        )}
      </div>
    </motion.div>
  )
}

interface EmptyStateProps {
  icon?: React.ReactNode
  title: string
  description?: string
  action?: {
    label: string
    onClick: () => void
  }
}

export function EmptyState({ 
  icon, 
  title, 
  description, 
  action 
}: EmptyStateProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex flex-col items-center justify-center py-12 px-4"
    >
      {icon && (
        <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-full mb-4">
          {icon}
        </div>
      )}
      
      <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-2">
        {title}
      </h3>
      
      {description && (
        <p className="text-gray-500 dark:text-gray-400 text-center mb-6 max-w-md">
          {description}
        </p>
      )}
      
      {action && (
        <button
          onClick={action.onClick}
          className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
        >
          {action.label}
        </button>
      )}
    </motion.div>
  )
}
