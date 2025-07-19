import { useState } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'
import toast from 'react-hot-toast'
import { CheckCircle, ArrowRight, User, Globe, Target, Bell } from 'lucide-react'
import ProtectedRoute from '../components/ProtectedRoute'
import { useLanguage } from '../contexts/LanguageContext'

export default function Setup() {
  const router = useRouter()
  const [currentStep, setCurrentStep] = useState(1)
  const { t } = useLanguage()
  const [setupData, setSetupData] = useState({
    profile: {
      name: '',
      company: '',
      industry: '',
      role: ''
    },
    preferences: {
      primaryPlatform: '',
      contentFrequency: '',
      targetAudience: '',
      goals: []
    },
    socialMedia: {
      platforms: []
    },
    notifications: {
      email: true,
      push: true,
      weeklyReport: true
    }
  })

  const steps = [
    { id: 1, title: t('profile_setup'), icon: User },
    { id: 2, title: t('content_preferences'), icon: Target },
    { id: 3, title: t('social_media'), icon: Globe },
    { id: 4, title: t('notifications'), icon: Bell }
  ]

  const industries = [
    t('technology'), t('healthcare'), t('finance'), t('education'), t('marketing'),
    t('real_estate'), t('ecommerce'), t('consulting'), t('manufacturing'), t('other')
  ]

  const platforms = [
    { key: 'linkedin', name: t('linkedin'), icon: '💼' },
    { key: 'facebook', name: t('facebook'), icon: '📘' },
    { key: 'instagram', name: t('instagram'), icon: '📷' },
    { key: 'twitter', name: t('twitter'), icon: '🐦' },
    { key: 'youtube', name: t('youtube'), icon: '📺' }
  ]

  const goals = [
    t('increase_brand_awareness'),
    t('generate_leads'),
    t('drive_website_traffic'),
    t('build_community'),
    t('share_thought_leadership'),
    t('promote_products_services')
  ]

  const handleInputChange = (section, field, value) => {
    setSetupData(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }))
  }

  const handleGoalToggle = (goal) => {
    const currentGoals = setupData.preferences.goals
    const updatedGoals = currentGoals.includes(goal)
      ? currentGoals.filter(g => g !== goal)
      : [...currentGoals, goal]
    
    handleInputChange('preferences', 'goals', updatedGoals)
  }

  const handlePlatformToggle = (platform) => {
    const currentPlatforms = setupData.socialMedia.platforms
    const updatedPlatforms = currentPlatforms.includes(platform)
      ? currentPlatforms.filter(p => p !== platform)
      : [...currentPlatforms, platform]
    
    handleInputChange('socialMedia', 'platforms', updatedPlatforms)
  }

  const nextStep = () => {
    if (currentStep < steps.length) {
      setCurrentStep(currentStep + 1)
    }
  }

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const completeSetup = async () => {
    try {
      // In a real app, this would save to backend
      await new Promise(resolve => setTimeout(resolve, 1000))
      toast.success(t('setup_completed'))
      router.push('/dashboard')
    } catch (error) {
      toast.error(t('setup_failed'))
    }
  }

  const isStepValid = () => {
    switch (currentStep) {
      case 1:
        return setupData.profile.name && setupData.profile.industry
      case 2:
        return setupData.preferences.primaryPlatform && setupData.preferences.goals.length > 0
      case 3:
        return setupData.socialMedia.platforms.length > 0
      case 4:
        return true
      default:
        return false
    }
  }

  return (
    <ProtectedRoute>
      <>
        <Head>
          <title>{t('setup')} - Content Creator Pro</title>
          <meta name="description" content={t('setup_description')} />
        </Head>

        <div className="min-h-screen bg-gray-50">
          <div className="container mx-auto px-4 py-8">
            <div className="max-w-4xl mx-auto">
              {/* Header */}
              <div className="text-center mb-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">{t('welcome_to_content_creator_pro')}</h1>
                <p className="text-gray-600">{t('setup_subtitle')}</p>
              </div>

              {/* Progress Steps */}
              <div className="flex justify-center mb-8">
                <div className="flex items-center space-x-4">
                  {steps.map((step, index) => (
                    <div key={step.id} className="flex items-center">
                      <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                        step.id <= currentStep 
                          ? 'bg-blue-600 text-white' 
                          : 'bg-gray-200 text-gray-600'
                      }`}>
                        {step.id < currentStep ? (
                          <CheckCircle className="w-6 h-6" />
                        ) : (
                          <step.icon className="w-6 h-6" />
                        )}
                      </div>
                      {index < steps.length - 1 && (
                        <div className={`w-16 h-1 mx-2 ${
                          step.id < currentStep ? 'bg-blue-600' : 'bg-gray-200'
                        }`} />
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Step Content */}
              <div className="bg-white rounded-lg shadow-lg p-8">
                {currentStep === 1 && (
                  <div>
                    <h2 className="text-2xl font-bold mb-6">{t('tell_us_about_yourself')}</h2>
                    <div className="space-y-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">{t('full_name')} *</label>
                        <input
                          type="text"
                          value={setupData.profile.name}
                          onChange={(e) => handleInputChange('profile', 'name', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder={t('enter_full_name')}
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">{t('company_organization')}</label>
                        <input
                          type="text"
                          value={setupData.profile.company}
                          onChange={(e) => handleInputChange('profile', 'company', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder={t('enter_company_name')}
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">{t('industry')} *</label>
                        <select
                          value={setupData.profile.industry}
                          onChange={(e) => handleInputChange('profile', 'industry', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="">{t('select_your_industry')}</option>
                          {industries.map(industry => (
                            <option key={industry} value={industry}>{industry}</option>
                          ))}
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">{t('your_role')}</label>
                        <input
                          type="text"
                          value={setupData.profile.role}
                          onChange={(e) => handleInputChange('profile', 'role', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder={t('e_g_marketing_manager_ceo_content_creator')}
                        />
                      </div>
                    </div>
                  </div>
                )}

                {currentStep === 2 && (
                  <div>
                    <h2 className="text-2xl font-bold mb-6">{t('content_preferences')}</h2>
                    <div className="space-y-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">{t('primary_platform')} *</label>
                        <select
                          value={setupData.preferences.primaryPlatform}
                          onChange={(e) => handleInputChange('preferences', 'primaryPlatform', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="">{t('select_your_primary_platform')}</option>
                          {platforms.map(platform => (
                            <option key={platform.key} value={platform.key}>
                              {platform.icon} {platform.name}
                            </option>
                          ))}
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">{t('content_frequency')}</label>
                        <select
                          value={setupData.preferences.contentFrequency}
                          onChange={(e) => handleInputChange('preferences', 'contentFrequency', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="">{t('select_frequency')}</option>
                          <option value="daily">{t('daily')}</option>
                          <option value="weekly">{t('weekly')}</option>
                          <option value="biweekly">{t('biweekly')}</option>
                          <option value="monthly">{t('monthly')}</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">{t('your_goals')} *</label>
                        <p className="text-sm text-gray-500 mb-3">{t('select_all_that_apply')}</p>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          {goals.map(goal => (
                            <label key={goal} className="flex items-center">
                              <input
                                type="checkbox"
                                checked={setupData.preferences.goals.includes(goal)}
                                onChange={() => handleGoalToggle(goal)}
                                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                              />
                              <span className="ml-2 text-sm text-gray-700">{goal}</span>
                            </label>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {currentStep === 3 && (
                  <div>
                    <h2 className="text-2xl font-bold mb-6">{t('connect_your_social_media')}</h2>
                    <p className="text-gray-600 mb-6">{t('select_the_platforms_you_want_to_create_content_for')}</p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {platforms.map(platform => (
                        <button
                          key={platform.key}
                          onClick={() => handlePlatformToggle(platform.key)}
                          className={`p-4 border-2 rounded-lg text-left transition-all duration-200 ${
                            setupData.socialMedia.platforms.includes(platform.key)
                              ? 'border-blue-600 bg-blue-50'
                              : 'border-gray-200 hover:border-gray-300'
                          }`}
                        >
                          <div className="text-2xl mb-2">{platform.icon}</div>
                          <div className="font-medium">{platform.name}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {currentStep === 4 && (
                  <div>
                    <h2 className="text-2xl font-bold mb-6">{t('notification_preferences')}</h2>
                    <p className="text-gray-600 mb-6">{t('choose_how_you_d_like_to_stay_updated')}</p>
                    <div className="space-y-4">
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={setupData.notifications.email}
                          onChange={(e) => handleInputChange('notifications', 'email', e.target.checked)}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">{t('email_notifications')}</span>
                      </label>
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={setupData.notifications.push}
                          onChange={(e) => handleInputChange('notifications', 'push', e.target.checked)}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">{t('push_notifications')}</span>
                      </label>
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={setupData.notifications.weeklyReport}
                          onChange={(e) => handleInputChange('notifications', 'weeklyReport', e.target.checked)}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">{t('weekly_performance_reports')}</span>
                      </label>
                    </div>
                  </div>
                )}

                {/* Navigation */}
                <div className="flex justify-between mt-8">
                  <button
                    onClick={prevStep}
                    disabled={currentStep === 1}
                    className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {t('previous')}
                  </button>
                  
                  {currentStep < steps.length ? (
                    <button
                      onClick={nextStep}
                      disabled={!isStepValid()}
                      className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                    >
                      {t('next')}
                      <ArrowRight className="w-4 h-4" />
                    </button>
                  ) : (
                    <button
                      onClick={completeSetup}
                      className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center gap-2"
                    >
                      {t('complete_setup')}
                      <CheckCircle className="w-4 h-4" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </>
    </ProtectedRoute>
  )
} 