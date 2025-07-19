import { createContext, useContext, useState, useEffect } from 'react'
import { apiClient } from '../lib/api'

const LanguageContext = createContext()

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState('en')
  const [translations, setTranslations] = useState({})
  const [loading, setLoading] = useState(true)

  // Load language from localStorage on mount
  useEffect(() => {
    const savedLanguage = localStorage.getItem('language')
    if (savedLanguage) {
      setLanguage(savedLanguage)
    }
    loadTranslations(savedLanguage || 'en')
  }, [])

  const loadTranslations = async (lang) => {
    try {
      setLoading(true)
      const response = await apiClient.request(`/api/translations?language=${lang}`)
      if (response.success) {
        setTranslations(response.translations)
      }
    } catch (error) {
      console.error('Error loading translations:', error)
      // Fallback to English
      setTranslations({})
    } finally {
      setLoading(false)
    }
  }

  const changeLanguage = async (newLanguage) => {
    setLanguage(newLanguage)
    localStorage.setItem('language', newLanguage)
    await loadTranslations(newLanguage)
  }

  const t = (key) => {
    return translations[key] || key
  }

  const value = {
    language,
    translations,
    loading,
    changeLanguage,
    t
  }

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  const context = useContext(LanguageContext)
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider')
  }
  return context
} 