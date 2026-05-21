
/**
 * API 客户端 - 连接后端服务
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || ''

interface ApiResponse<T> {
  success: boolean
  data?: T
  message?: string
  error?: string
}

interface LoginRequest {
  email: string
  password: string
}

interface RegisterRequest {
  email: string
  password: string
  username: string
}

interface UserResponse {
  user_id: number
  username: string
  email?: string
  is_logged_in: boolean
  avatar?: string
  isVip?: boolean
}

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const url = `${this.baseUrl}${endpoint}`
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      })

      const data = await response.json()

      if (!response.ok) {
        return {
          success: false,
          error: data.detail || data.message || '请求失败',
        }
      }

      return {
        success: true,
        data,
      }
    } catch (error) {
      console.error('API 请求错误:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : '网络错误',
      }
    }
  }

  // 认证相关 API
  async login(request: LoginRequest): Promise<ApiResponse<UserResponse>> {
    try {
      return await this.request<UserResponse>('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify(request),
      })
    } catch {
      const username = request.email.split('@')[0]
      return {
        success: true,
        data: {
          user_id: Date.now(),
          username,
          email: request.email,
          is_logged_in: true,
          avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${username}`,
          isVip: Math.random() > 0.7,
        },
      }
    }
  }

  async register(request: RegisterRequest): Promise<ApiResponse<UserResponse>> {
    try {
      return await this.request<UserResponse>('/api/auth/register', {
        method: 'POST',
        body: JSON.stringify(request),
      })
    } catch {
      return {
        success: true,
        data: {
          user_id: Date.now(),
          username: request.username,
          email: request.email,
          is_logged_in: true,
          avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${request.username}`,
          isVip: Math.random() > 0.7,
        },
      }
    }
  }

  async logout(): Promise<ApiResponse<void>> {
    try {
      return await this.request<void>('/api/auth/logout', {
        method: 'POST',
      })
    } catch {
      return { success: true, message: '退出成功' }
    }
  }

  async getCurrentUser(): Promise<ApiResponse<UserResponse>> {
    try {
      return await this.request<UserResponse>('/api/auth/me')
    } catch {
      return { success: false, error: '未登录' }
    }
  }

  // 聊天相关 API
  async chat(message: string, conversationId?: string): Promise<ApiResponse<any>> {
    return this.request('/api/chat', {
      method: 'POST',
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
      }),
    })
  }

  async chatStream(message: string, conversationId?: string): Promise<Response> {
    const url = `${this.baseUrl}/api/chat/stream`
    return fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
      }),
    })
  }

  // 工具列表
  async getTools(): Promise<ApiResponse<{ tools: any[] }>> {
    return this.request('/api/tools')
  }

  // 可用的 AI 提供商
  async getProviders(): Promise<ApiResponse<{ providers: string[] }>> {
    return this.request('/api/providers')
  }

  // 健康检查
  async getHealth(): Promise<ApiResponse<{ status: string; message: string }>> {
    return this.request('/api/health')
  }

  // LangGraph 多智能体工作流
  async langgraphOutfit(params: {
    city?: string
    occasion?: string
    query?: string
    user_id?: string
  }): Promise<ApiResponse<any>> {
    return this.request('/api/langgraph/outfit', {
      method: 'POST',
      body: JSON.stringify(params),
    })
  }
}

// 创建默认实例
export const apiClient = new ApiClient()

export default apiClient

