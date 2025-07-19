import { useState, useEffect } from 'react'
import Head from 'next/head'
import toast from 'react-hot-toast'
import { Settings as SettingsIcon, User, Globe, Bell, Shield, Palette, Save, RefreshCw } from 'lucide-react'
import { apiClient } from '../lib/api'
import ProtectedRoute from '../components/ProtectedRoute'
import { useLanguage } from '../contexts/LanguageContext'

export default function Settings() {
  const [isLoading, setIsLoading] = useState(false)
  const [settings, setSettings] = useState({
    profile: {
      name: '',
      email: '',
      region: 'global',
      language: 'en',
      timezone: 'UTC'
    },
    preferences: {
      defaultDirection: 'business_finance',
      defaultPlatform: 'linkedin',
      defaultTone: 'professional',
      autoSave: true,
      notifications: true
    },
    socialMedia: {
      linkedin: { connected: false, username: '' },
      facebook: { connected: false, username: '' },
      instagram: { connected: false, username: '' },
      twitter: { connected: false, username: '' },
      youtube: { connected: false, channel: '' }
    },
    appearance: {
      theme: 'light',
      fontSize: 'medium',
      compactMode: false
    }
  })
  const { t } = useLanguage()

  useEffect(() => {
    loadSettings()
  }, [])

  const loadSettings = async () => {
    try {
      // In a real app, this would fetch from backend
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      setSettings(prev => ({
        ...prev,
        profile: {
          ...prev.profile,
          name: user.name || '',
          email: user.email || ''
        }
      }))
    } catch (error) {
      console.error('Error loading settings:', error)
    }
  }

  const handleSettingChange = (section, key, value) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [key]: value
      }
    }))
  }

  const handleSocialMediaToggle = (platform) => {
    setSettings(prev => ({
      ...prev,
      socialMedia: {
        ...prev.socialMedia,
        [platform]: {
          ...prev.socialMedia[platform],
          connected: !prev.socialMedia[platform].connected
        }
      }
    }))
  }

  const saveSettings = async () => {
    setIsLoading(true)
    try {
      // In a real app, this would save to backend
      await new Promise(resolve => setTimeout(resolve, 1000))
      toast.success(t('settings_saved'))
    } catch (error) {
      toast.error(t('settings_save_failed'))
    } finally {
      setIsLoading(false)
    }
  }

  const resetSettings = () => {
    if (confirm(t('confirm_reset_settings'))) {
      loadSettings()
      toast.success(t('settings_reset'))
    }
  }

  return (
    <ProtectedRoute>
      <>
        <Head>
          <title>{t('settings')} - Content Creator Pro</title>
          <meta name="description" content={t('settings_description')} />
        </Head>

        <div className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto">
            {/* Header */}
            <div className="flex items-center justify-between mb-8">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">{t('settings')}</h1>
                <p className="text-gray-600">{t('settings_subtitle')}</p>
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={resetSettings}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 flex items-center gap-2"
                >
                  <RefreshCw className="w-4 h-4" />
                  {t('reset')}
                </button>
                <button
                  onClick={saveSettings}
                  disabled={isLoading}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
                >
                  {isLoading ? (
                    <RefreshCw className="w-4 h-4 animate-spin" />
                  ) : (
                    <Save className="w-4 h-4" />
                  )}
                  {isLoading ? t('saving') : t('save_settings')}
                </button>
              </div>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {/* Navigation */}
              <div className="md:col-span-1">
                <nav className="space-y-2">
                  <a href="#profile" className="flex items-center space-x-3 p-3 rounded-lg bg-blue-50 text-blue-700">
                    <User className="w-5 h-5" />
                    <span>{t('profile')}</span>
                  </a>
                  <a href="#preferences" className="flex items-center space-x-3 p-3 rounded-lg text-gray-700 hover:bg-gray-50">
                    <SettingsIcon className="w-5 h-5" />
                    <span>{t('preferences')}</span>
                  </a>
                  <a href="#social-media" className="flex items-center space-x-3 p-3 rounded-lg text-gray-700 hover:bg-gray-50">
                    <Globe className="w-5 h-5" />
                    <span>{t('social_media')}</span>
                  </a>
                  <a href="#appearance" className="flex items-center space-x-3 p-3 rounded-lg text-gray-700 hover:bg-gray-50">
                    <Palette className="w-5 h-5" />
                    <span>{t('appearance')}</span>
                  </a>
                  <a href="#notifications" className="flex items-center space-x-3 p-3 rounded-lg text-gray-700 hover:bg-gray-50">
                    <Bell className="w-5 h-5" />
                    <span>{t('notifications')}</span>
                  </a>
                  <a href="#security" className="flex items-center space-x-3 p-3 rounded-lg text-gray-700 hover:bg-gray-50">
                    <Shield className="w-5 h-5" />
                    <span>{t('security')}</span>
                  </a>
                </nav>
              </div>

              {/* Settings Content */}
              <div className="md:col-span-2 space-y-8">
                {/* Profile Settings */}
                <section id="profile" className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                    <User className="w-5 h-5" />
                    {t('profile_settings')}
                  </h2>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">{t('name')}</label>
                      <input
                        type="text"
                        value={settings.profile.name}
                        onChange={(e) => handleSettingChange('profile', 'name', e.target.value)}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">{t('email')}</label>
                      <input
                        type="email"
                        value={settings.profile.email}
                        onChange={(e) => handleSettingChange('profile', 'email', e.target.value)}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">{t('region')}</label>
                        <select
                          value={settings.profile.region}
                          onChange={(e) => handleSettingChange('profile', 'region', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="global">{t('global')}</option>
                          <option value="us">{t('united_states')}</option>
                          <option value="eu">{t('europe')}</option>
                          <option value="asia">{t('asia')}</option>
                          <option value="au">{t('australia')}</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">{t('language')}</label>
                        <select
                          value={settings.profile.language}
                          onChange={(e) => handleSettingChange('profile', 'language', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="en">{t('english')}</option>
                          <option value="zh">{t('chinese')}</option>
                          <option value="es">{t('spanish')}</option>
                          <option value="fr">{t('french')}</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </section>

                {/* Content Preferences */}
                <section id="preferences" className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                    <SettingsIcon className="w-5 h-5" />
                    {t('content_preferences')}
                  </h2>
                  <div className="space-y-4">
                    <div className="grid grid-cols-3 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">{t('default_direction')}</label>
                        <select
                          value={settings.preferences.defaultDirection}
                          onChange={(e) => handleSettingChange('preferences', 'defaultDirection', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="business_finance">{t('business_finance')}</option>
                          <option value="technology">{t('technology')}</option>
                          <option value="health_wellness">{t('health_wellness')}</option>
                          <option value="education">{t('education')}</option>
                          <option value="entertainment">{t('entertainment')}</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">{t('default_platform')}</label>
                        <select
                          value={settings.preferences.defaultPlatform}
                          onChange={(e) => handleSettingChange('preferences', 'defaultPlatform', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="linkedin">{t('linkedin')}</option>
                          <option value="facebook">{t('facebook')}</option>
                          <option value="instagram">{t('instagram')}</option>
                          <option value="twitter">{t('twitter')}</option>
                          <option value="youtube_shorts">{t('youtube_shorts')}</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">{t('default_tone')}</label>
                        <select
                          value={settings.preferences.defaultTone}
                          onChange={(e) => handleSettingChange('preferences', 'defaultTone', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="professional">{t('professional')}</option>
                          <option value="casual">{t('casual')}</option>
                          <option value="inspirational">{t('inspirational')}</option>
                          <option value="educational">{t('educational')}</option>
                          <option value="entertaining">{t('entertaining')}</option>
                        </select>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={settings.preferences.autoSave}
                          onChange={(e) => handleSettingChange('preferences', 'autoSave', e.target.checked)}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">{t('auto_save_drafts')}</span>
                      </label>
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={settings.preferences.notifications}
                          onChange={(e) => handleSettingChange('preferences', 'notifications', e.target.checked)}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">{t('email_notifications')}</span>
                      </label>
                    </div>
                  </div>
                </section>

                {/* Social Media Connections */}
                <section id="social-media" className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                    <Globe className="w-5 h-5" />
                    {t('social_media_connections')}
                  </h2>
                  <div className="space-y-4">
                    {Object.entries(settings.socialMedia).map(([platform, config]) => (
                      <div key={platform} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                            config.connected ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-400'
                          }`}>
                            {platform === 'linkedin' && '💼'}
                            {platform === 'facebook' && '📘'}
                            {platform === 'instagram' && '📷'}
                            {platform === 'twitter' && '🐦'}
                            {platform === 'youtube' && '📺'}
                          </div>
                          <div>
                            <h3 className="font-medium capitalize">{platform}</h3>
                            <p className="text-sm text-gray-500">
                              {config.connected ? t('connected') : t('not_connected')}
                            </p>
                          </div>
                        </div>
                        <button
                          onClick={() => handleSocialMediaToggle(platform)}
                          className={`px-4 py-2 rounded-lg text-sm font-medium ${
                            config.connected
                              ? 'bg-red-100 text-red-700 hover:bg-red-200'
                              : 'bg-blue-100 text-blue-700 hover:bg-blue-200'
                          }`}
                        >
                          {config.connected ? t('disconnect') : t('connect')}
                        </button>
                      </div>
                    ))}
                  </div>
                </section>

                {/* Appearance Settings */}
                <section id="appearance" className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                    <Palette className="w-5 h-5" />
                    {t('appearance')}
                  </h2>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">{t('theme')}</label>
                      <select
                        value={settings.appearance.theme}
                        onChange={(e) => handleSettingChange('appearance', 'theme', e.target.value)}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="light">{t('light')}</option>
                        <option value="dark">{t('dark')}</option>
                        <option value="auto">{t('auto_system')}</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">{t('font_size')}</label>
                      <select
                        value={settings.appearance.fontSize}
                        onChange={(e) => handleSettingChange('appearance', 'fontSize', e.target.value)}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="small">{t('small')}</option>
                        <option value="medium">{t('medium')}</option>
                        <option value="large">{t('large')}</option>
                      </select>
                    </div>
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={settings.appearance.compactMode}
                        onChange={(e) => handleSettingChange('appearance', 'compactMode', e.target.checked)}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="ml-2 text-sm text-gray-700">{t('compact_mode')}</span>
                    </label>
                  </div>
                </section>
              </div>
            </div>
          </div>
        </div>
      </>
    </ProtectedRoute>
  )
} 