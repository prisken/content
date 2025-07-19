import { useState } from 'react'
import { useRouter } from 'next/router'
import Head from 'next/head'
import toast from 'react-hot-toast'
import { CheckCircle, ArrowRight, User, Globe, Target, Bell } from 'lucide-react'
import ProtectedRoute from '../components/ProtectedRoute'

export default function Setup() {
  const router = useRouter()
  const [currentStep, setCurrentStep] = useState(1)
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
    { id: 1, title: 'Profile Setup', icon: User },
    { id: 2, title: 'Content Preferences', icon: Target },
    { id: 3, title: 'Social Media', icon: Globe },
    { id: 4, title: 'Notifications', icon: Bell }
  ]

  const industries = [
    'Technology', 'Healthcare', 'Finance', 'Education', 'Marketing',
    'Real Estate', 'E-commerce', 'Consulting', 'Manufacturing', 'Other'
  ]

  const platforms = [
    { key: 'linkedin', name: 'LinkedIn', icon: '💼' },
    { key: 'facebook', name: 'Facebook', icon: '📘' },
    { key: 'instagram', name: 'Instagram', icon: '📷' },
    { key: 'twitter', name: 'Twitter', icon: '🐦' },
    { key: 'youtube', name: 'YouTube', icon: '📺' }
  ]

  const goals = [
    'Increase brand awareness',
    'Generate leads',
    'Drive website traffic',
    'Build community',
    'Share thought leadership',
    'Promote products/services'
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
      toast.success('Setup completed successfully!')
      router.push('/dashboard')
    } catch (error) {
      toast.error('Failed to complete setup')
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
          <title>Setup - Content Creator Pro</title>
          <meta name="description" content="Complete your account setup" />
        </Head>

        <div className="min-h-screen bg-gray-50">
          <div className="container mx-auto px-4 py-8">
            <div className="max-w-4xl mx-auto">
              {/* Header */}
              <div className="text-center mb-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome to Content Creator Pro</h1>
                <p className="text-gray-600">Let's set up your account for the best experience</p>
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
                    <h2 className="text-2xl font-bold mb-6">Tell us about yourself</h2>
                    <div className="space-y-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Full Name *</label>
                        <input
                          type="text"
                          value={setupData.profile.name}
                          onChange={(e) => handleInputChange('profile', 'name', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="Enter your full name"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Company/Organization</label>
                        <input
                          type="text"
                          value={setupData.profile.company}
                          onChange={(e) => handleInputChange('profile', 'company', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="Enter your company name"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Industry *</label>
                        <select
                          value={setupData.profile.industry}
                          onChange={(e) => handleInputChange('profile', 'industry', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="">Select your industry</option>
                          {industries.map(industry => (
                            <option key={industry} value={industry}>{industry}</option>
                          ))}
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Your Role</label>
                        <input
                          type="text"
                          value={setupData.profile.role}
                          onChange={(e) => handleInputChange('profile', 'role', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="e.g., Marketing Manager, CEO, Content Creator"
                        />
                      </div>
                    </div>
                  </div>
                )}

                {currentStep === 2 && (
                  <div>
                    <h2 className="text-2xl font-bold mb-6">Content Preferences</h2>
                    <div className="space-y-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Primary Platform *</label>
                        <select
                          value={setupData.preferences.primaryPlatform}
                          onChange={(e) => handleInputChange('preferences', 'primaryPlatform', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="">Select your primary platform</option>
                          {platforms.map(platform => (
                            <option key={platform.key} value={platform.key}>
                              {platform.icon} {platform.name}
                            </option>
                          ))}
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Content Frequency</label>
                        <select
                          value={setupData.preferences.contentFrequency}
                          onChange={(e) => handleInputChange('preferences', 'contentFrequency', e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="">Select frequency</option>
                          <option value="daily">Daily</option>
                          <option value="weekly">Weekly</option>
                          <option value="biweekly">Bi-weekly</option>
                          <option value="monthly">Monthly</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Your Goals *</label>
                        <p className="text-sm text-gray-500 mb-3">Select all that apply</p>
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
                    <h2 className="text-2xl font-bold mb-6">Connect Your Social Media</h2>
                    <p className="text-gray-600 mb-6">Select the platforms you want to create content for</p>
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
                    <h2 className="text-2xl font-bold mb-6">Notification Preferences</h2>
                    <p className="text-gray-600 mb-6">Choose how you'd like to stay updated</p>
                    <div className="space-y-4">
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={setupData.notifications.email}
                          onChange={(e) => handleInputChange('notifications', 'email', e.target.checked)}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">Email notifications</span>
                      </label>
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={setupData.notifications.push}
                          onChange={(e) => handleInputChange('notifications', 'push', e.target.checked)}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">Push notifications</span>
                      </label>
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={setupData.notifications.weeklyReport}
                          onChange={(e) => handleInputChange('notifications', 'weeklyReport', e.target.checked)}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">Weekly performance reports</span>
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
                    Previous
                  </button>
                  
                  {currentStep < steps.length ? (
                    <button
                      onClick={nextStep}
                      disabled={!isStepValid()}
                      className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                    >
                      Next
                      <ArrowRight className="w-4 h-4" />
                    </button>
                  ) : (
                    <button
                      onClick={completeSetup}
                      className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center gap-2"
                    >
                      Complete Setup
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