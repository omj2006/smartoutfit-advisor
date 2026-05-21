import { create } from 'zustand'
import { apiClient } from '@/api/client'

// 个人信息接口
interface PersonalInfo {
  height: number | null
  weight: number | null
  gender: string
  age: number | null
  stylePreferences: string[]
  colorPreferences: string[]
}

// 记忆系统
interface UserMemory {
  favoriteCities: string[]
  favoriteOccasions: string[]
  favoriteStyles: string[]
  temperaturePreference: 'warm' | 'cool' | 'neutral'
}

// 收藏的穿搭
interface SavedOutfit {
  id: string
  image: string
  title: string
  description: string
  occasion: string
  style: string
  temperature: string
  savedAt: string
}

// 历史记录
interface HistoryRecord {
  id: string
  query: string
  outfit: {
    title: string
    image: string
  }
  weather: {
    city: string
    temp: number
    condition: string
  }
  createdAt: string
}

interface UserState {
  isLoggedIn: boolean
  username: string
  avatar: string
  isVip: boolean
  isLoading: boolean
  error: string | null
  
  // 个人信息
  personalInfo: PersonalInfo
  
  // 记忆系统
  memory: UserMemory
  
  // 收藏和历史
  savedOutfits: SavedOutfit[]
  historyRecords: HistoryRecord[]
  
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, username: string) => Promise<void>
  logout: () => Promise<void>
  checkAuth: () => Promise<void>
  clearError: () => void
  
  // 个人信息管理
  updatePersonalInfo: (info: Partial<PersonalInfo>) => void
  
  // 记忆系统
  addFavoriteCity: (city: string) => void
  addFavoriteOccasion: (occasion: string) => void
  addFavoriteStyle: (style: string) => void
  setTemperaturePreference: (pref: 'warm' | 'cool' | 'neutral') => void
  
  // 收藏功能
  saveOutfit: (outfit: Omit<SavedOutfit, 'savedAt'>) => void
  removeSavedOutfit: (id: string) => void
  isOutfitSaved: (id: string) => boolean
  
  // 历史记录
  addHistoryRecord: (record: Omit<HistoryRecord, 'createdAt'>) => void
  clearHistory: () => void
}

// 默认值
const defaultPersonalInfo: PersonalInfo = {
  height: null,
  weight: null,
  gender: '',
  age: null,
  stylePreferences: [],
  colorPreferences: []
}

const defaultMemory: UserMemory = {
  favoriteCities: [],
  favoriteOccasions: [],
  favoriteStyles: [],
  temperaturePreference: 'neutral'
}

export const useUserStore = create<UserState>((set, get) => ({
  isLoggedIn: false,
  username: '',
  avatar: '',
  isVip: false,
  isLoading: false,
  error: null,
  
  personalInfo: defaultPersonalInfo,
  memory: defaultMemory,
  savedOutfits: [],
  historyRecords: [],

  login: async (email: string, password: string) => {
    set({ isLoading: true, error: null })
    try {
      const response = await apiClient.login({ email, password })
      if (response.success && response.data) {
        set({
          isLoggedIn: true,
          username: response.data.username,
          avatar: response.data.avatar || `https://api.dicebear.com/7.x/avataaars/svg?seed=${response.data.username}`,
          isVip: response.data.isVip || false,
          isLoading: false,
        })
      } else {
        set({ error: response.message || '登录失败', isLoading: false })
      }
    } catch (error) {
      set({ error: '登录失败，请稍后重试', isLoading: false })
    }
  },

  register: async (email: string, password: string, username: string) => {
    set({ isLoading: true, error: null })
    try {
      const response = await apiClient.register({ email, password, username })
      if (response.success && response.data) {
        set({
          isLoggedIn: true,
          username: response.data.username,
          avatar: response.data.avatar || `https://api.dicebear.com/7.x/avataaars/svg?seed=${response.data.username}`,
          isVip: response.data.isVip || false,
          isLoading: false,
        })
      } else {
        set({ error: response.message || '注册失败', isLoading: false })
      }
    } catch (error) {
      set({ error: '注册失败，请稍后重试', isLoading: false })
    }
  },

  logout: async () => {
    set({ isLoading: true })
    try {
      await apiClient.logout()
    } finally {
      set({
        isLoggedIn: false,
        username: '',
        avatar: '',
        isVip: false,
        isLoading: false,
        error: null,
        personalInfo: defaultPersonalInfo,
        memory: defaultMemory,
        savedOutfits: [],
        historyRecords: [],
      })
    }
  },

  checkAuth: async () => {
    try {
      const response = await apiClient.getCurrentUser()
      if (response.success && response.data) {
        set({
          isLoggedIn: true,
          username: response.data.username,
          avatar: response.data.avatar || `https://api.dicebear.com/7.x/avataaars/svg?seed=${response.data.username}`,
          isVip: response.data.isVip || false,
        })
      }
    } catch (error) {
      set({ isLoggedIn: false })
    }
  },

  clearError: () => set({ error: null }),
  
  // 个人信息管理
  updatePersonalInfo: (info) => set((state) => ({
    personalInfo: { ...state.personalInfo, ...info }
  })),
  
  // 记忆系统
  addFavoriteCity: (city) => set((state) => ({
    memory: {
      ...state.memory,
      favoriteCities: state.memory.favoriteCities.includes(city) 
        ? state.memory.favoriteCities 
        : [...state.memory.favoriteCities, city]
    }
  })),
  
  addFavoriteOccasion: (occasion) => set((state) => ({
    memory: {
      ...state.memory,
      favoriteOccasions: state.memory.favoriteOccasions.includes(occasion)
        ? state.memory.favoriteOccasions
        : [...state.memory.favoriteOccasions, occasion]
    }
  })),
  
  addFavoriteStyle: (style) => set((state) => ({
    memory: {
      ...state.memory,
      favoriteStyles: state.memory.favoriteStyles.includes(style)
        ? state.memory.favoriteStyles
        : [...state.memory.favoriteStyles, style]
    }
  })),
  
  setTemperaturePreference: (pref) => set((state) => ({
    memory: { ...state.memory, temperaturePreference: pref }
  })),
  
  // 收藏功能
  saveOutfit: (outfit) => set((state) => ({
    savedOutfits: [
      ...state.savedOutfits,
      { ...outfit, savedAt: new Date().toISOString() }
    ]
  })),
  
  removeSavedOutfit: (id) => set((state) => ({
    savedOutfits: state.savedOutfits.filter(o => o.id !== id)
  })),
  
  isOutfitSaved: (id) => get().savedOutfits.some(o => o.id === id),
  
  // 历史记录
  addHistoryRecord: (record) => set((state) => ({
    historyRecords: [
      { ...record, createdAt: new Date().toISOString() },
      ...state.historyRecords.slice(0, 99) // 保留最近100条
    ]
  })),
  
  clearHistory: () => set({ historyRecords: [] }),
}))
