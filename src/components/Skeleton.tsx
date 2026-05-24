import { motion } from 'framer-motion'

interface SkeletonProps {
  className?: string
}

export function Skeleton({ className = '' }: SkeletonProps) {
  return (
    <motion.div
      animate={{ opacity: [0.4, 0.7, 0.4] }}
      transition={{ duration: 1.5, repeat: Infinity }}
      className={`bg-gray-200 dark:bg-gray-700 rounded ${className}`}
    />
  )
}

export function CardSkeleton() {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl p-4 shadow-sm">
      <Skeleton className="w-full h-48 rounded-xl mb-4" />
      <Skeleton className="w-3/4 h-4 mb-2" />
      <Skeleton className="w-1/2 h-4" />
    </div>
  )
}

export function ProfileSkeleton() {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Skeleton className="w-20 h-20 rounded-full" />
        <div className="flex-1 space-y-2">
          <Skeleton className="w-32 h-5" />
          <Skeleton className="w-48 h-4" />
        </div>
      </div>
      <div className="grid grid-cols-2 gap-4">
        <Skeleton className="w-full h-24 rounded-xl" />
        <Skeleton className="w-full h-24 rounded-xl" />
      </div>
    </div>
  )
}

export function WorkflowSkeleton() {
  return (
    <div className="space-y-6">
      <Skeleton className="w-full h-32 rounded-2xl" />
      <div className="flex gap-3">
        {[1, 2, 3].map((i) => (
          <Skeleton key={i} className="w-24 h-10 rounded-lg" />
        ))}
      </div>
      <div className="space-y-3">
        {[1, 2, 3, 4, 5].map((i) => (
          <div key={i} className="flex items-center gap-3">
            <Skeleton className="w-8 h-8 rounded-full" />
            <Skeleton className="w-32 h-4" />
          </div>
        ))}
      </div>
    </div>
  )
}

export function ProductListSkeleton({ count = 4 }: { count?: number }) {
  return (
    <div className="grid grid-cols-2 gap-4">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="bg-white dark:bg-gray-800 rounded-xl p-3 shadow-sm">
          <Skeleton className="w-full h-32 rounded-lg mb-3" />
          <Skeleton className="w-3/4 h-4 mb-2" />
          <Skeleton className="w-1/2 h-3" />
        </div>
      ))}
    </div>
  )
}

export function WeatherSkeleton() {
  return (
    <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl p-6 text-white">
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <Skeleton className="w-20 h-8 bg-white/20" />
          <Skeleton className="w-32 h-4 bg-white/20" />
        </div>
        <Skeleton className="w-16 h-16 rounded-full bg-white/20" />
      </div>
    </div>
  )
}
