
/**
 * 受保护的路由组件 - 未登录用户重定向到登录页
 */
import { useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useUserStore } from '@/store/useUserStore'

interface ProtectedRouteProps {
  children: React.ReactNode
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const navigate = useNavigate()
  const location = useLocation()
  const isLoggedIn = useUserStore((s) => s.isLoggedIn)

  useEffect(() => {
    if (!isLoggedIn) {
      // 保存用户尝试访问的页面，登录后可以重定向回来
      navigate('/login', {
        replace: true,
        state: { from: location.pathname },
      })
    }
  }, [isLoggedIn, navigate, location.pathname])

  if (!isLoggedIn) {
    // 在检查登录状态时可以显示加载状态
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">正在检查登录状态...</p>
        </div>
      </div>
    )
  }

  return <>{children}</>
}

