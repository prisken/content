import { useState, useEffect } from 'react'
import Head from 'next/head'
import toast from 'react-hot-toast'
import { Settings as SettingsIcon, User, Globe, Bell, Shield, Palette, Save, RefreshCw } from 'lucide-react'
import { apiClient } from '../lib/api'
import ProtectedRoute from '../components/ProtectedRoute'

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
      toast.success('Settings saved successfully!')
    } catch (error) {
      toast.error('Failed to save settings')
    } finally {
      setIsLoading(false)
    }
  }

  const resetSettings = () => {
    if (confirm('Are you sure you want to reset all settings to default?')) {
      loadSettings()
      toast.success('Settings reset to default')
    }
  }

  return (
    <ProtectedRoute>
      <>
        <Head>
          <title>Settings - Content Creator Pro</title>
          <meta name="description" content="Configure your Content Creator Pro settings" />
        </Head>

        <div className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto">
            {/* Header */}
            <div className="flex items-center justify-between mb-8">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">Settings</h1>
                <p className="text-gray-600">Configure your account and preferences</p>
              </div>
              <div className="flex space-x-3">
                <button
                  onClick={resetSettings}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 flex items-center gap-2"
                >
                  <RefreshCw className="w-4 h-4" />
                  Reset
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
                  {isLoading ? 'Saving...' : 'Save Settings'}
                </button>
              </div>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {/* Navigation */}
              <div className="md:col-span-1">
                <nav className="space-y-2">
                  <a href="#profile" className="flex items-center space-x-3 p-3 rounded-lg bg-blue-50 text-blue-700">
                    <User className="w-5 h-5" />
                    <span>Profile</span>
                  </a>
                  <a href="#preferences" className="flex items-center space-x-3 p-3 rounded-lg text-gray-700 hover:bg-gray-50">
                    <SettingsIcon className="w-5 h-5" />
                    <span>Preferences</span>
                  </a>
                  <a href="#social-media" className="flex items-center space-x-3 p-3 rounded-lg text-gray-700 hover:bg-gray-50">
                    <Globe className="w-5 h-5" />
                    <span>Social Media</span>
                  </a>
                  <a href="#appearance" className="flex items-center space-x-3 p-3 rounded-lg text-gray-700 hover:bg-gray-50">
                    <Palette className="w-5 h-5" />
                    <span>Appearance</span>
                  </a>
                  <a href="#notifications" className="flex items-center space-x-3 p-3 rounded-lg text-gray-700 hover:bg-gray-50">
                    <Bell className="w-5 h-5" />
                    <span>Notifications</span>
                  </a>
                  <a href="#security" className="flex items-center space-x-3 p-3 rounded-lg text-gray-700 hover:bg-gray-50">
                    <Shield className="w-5 h-5" />
                    <span>Security</span>
                  </a>
                </nav>
              </div>

              {/* Settings Content */}
              <div className="md:col-span-2 space-y-8">
                {/* Profile Settings */}
                <section id="profile" className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                    <User className="w-5 h-5" />
                    Profile Settings
                  </h2>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Name</label>
                      <input
                        type="text"
                        value={settings.profile.name}
                        onChange={(e) => handleSettingChange('profile', 'name', e.target.value)}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                      <input
                        type="email"
                        value={settings.profile.email}
                        onChange={(e) => handleSettingChange('profile', 'email', e.target.value)}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Region</label>
                        <select
                          value={settings.profile.region}
                          onChange={(e) => handleSettingChange('profile', 'region', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="global">Global</option>
                          <option value="us">United States</option>
                          <option value="eu">Europe</option>
                          <option value="asia">Asia</option>
                          <option value="au">Australia</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Language</label>
                        <select
                          value={settings.profile.language}
                          onChange={(e) => handleSettingChange('profile', 'language', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="en">English</option>
                          <option value="zh">中文 (Chinese)</option>
                          <option value="es">Español (Spanish)</option>
                          <option value="fr">Français (French)</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </section>

                {/* Content Preferences */}
                <section id="preferences" className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                    <SettingsIcon className="w-5 h-5" />
                    Content Preferences
                  </h2>
                  <div className="space-y-4">
                    <div className="grid grid-cols-3 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Default Direction</label>
                        <select
                          value={settings.preferences.defaultDirection}
                          onChange={(e) => handleSettingChange('preferences', 'defaultDirection', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="business_finance">Business & Finance</option>
                          <option value="technology">Technology</option>
                          <option value="health_wellness">Health & Wellness</option>
                          <option value="education">Education</option>
                          <option value="entertainment">Entertainment</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Default Platform</label>
                        <select
                          value={settings.preferences.defaultPlatform}
                          onChange={(e) => handleSettingChange('preferences', 'defaultPlatform', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="linkedin">LinkedIn</option>
                          <option value="facebook">Facebook</option>
                          <option value="instagram">Instagram</option>
                          <option value="twitter">Twitter</option>
                          <option value="youtube_shorts">YouTube Shorts</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Default Tone</label>
                        <select
                          value={settings.preferences.defaultTone}
                          onChange={(e) => handleSettingChange('preferences', 'defaultTone', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="professional">Professional</option>
                          <option value="casual">Casual</option>
                          <option value="inspirational">Inspirational</option>
                          <option value="educational">Educational</option>
                          <option value="entertaining">Entertaining</option>
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
                        <span className="ml-2 text-sm text-gray-700">Auto-save drafts</span>
                      </label>
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={settings.preferences.notifications}
                          onChange={(e) => handleSettingChange('preferences', 'notifications', e.target.checked)}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">Email notifications</span>
                      </label>
                    </div>
                  </div>
                </section>

                {/* Social Media Connections */}
                <section id="social-media" className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                    <Globe className="w-5 h-5" />
                    Social Media Connections
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
                              {config.connected ? 'Connected' : 'Not connected'}
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
                          {config.connected ? 'Disconnect' : 'Connect'}
                        </button>
                      </div>
                    ))}
                  </div>
                </section>

                {/* Appearance Settings */}
                <section id="appearance" className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                    <Palette className="w-5 h-5" />
                    Appearance
                  </h2>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Theme</label>
                      <select
                        value={settings.appearance.theme}
                        onChange={(e) => handleSettingChange('appearance', 'theme', e.target.value)}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="light">Light</option>
                        <option value="dark">Dark</option>
                        <option value="auto">Auto (System)</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Font Size</label>
                      <select
                        value={settings.appearance.fontSize}
                        onChange={(e) => handleSettingChange('appearance', 'fontSize', e.target.value)}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="small">Small</option>
                        <option value="medium">Medium</option>
                        <option value="large">Large</option>
                      </select>
                    </div>
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={settings.appearance.compactMode}
                        onChange={(e) => handleSettingChange('appearance', 'compactMode', e.target.checked)}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="ml-2 text-sm text-gray-700">Compact mode</span>
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