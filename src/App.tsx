import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from '@/components/Layout'
import Login from '@/pages/Login'
import Home from '@/pages/Home'
import Recommend from '@/pages/Recommend'
import AiEffect from '@/pages/AiEffect'
import Profile from '@/pages/Profile'
import Trends from '@/pages/Trends'
import LangGraphWorkflow from '@/pages/LangGraphWorkflow'
import ProtectedRoute from '@/components/ProtectedRoute'

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<Layout />}>
          <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />
          <Route path="/recommend" element={<ProtectedRoute><Recommend /></ProtectedRoute>} />
          <Route path="/ai-effect" element={<ProtectedRoute><AiEffect /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
          <Route path="/trends" element={<ProtectedRoute><Trends /></ProtectedRoute>} />
          <Route path="/workflow" element={<ProtectedRoute><LangGraphWorkflow /></ProtectedRoute>} />
        </Route>
      </Routes>
    </Router>
  )
}
