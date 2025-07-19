import { useState } from 'react'
import { useRouter } from 'next/router'
import { apiClient } from '../lib/api'
import toast from 'react-hot-toast'
import Head from 'next/head'
import { User, Lock, Mail, Eye, EyeOff, Sparkles, ArrowRight, UserPlus, CheckCircle, AlertCircle } from 'lucide-react'
import Link from 'next/link'
import { useLanguage } from '../contexts/LanguageContext'

export default function Register() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    region: 'global',
    language: 'en'
  })
  const [isLoading, setIsLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [errors, setErrors] = useState({})
  const router = useRouter()
  const { t } = useLanguage()

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }))
    }
  }

  const validateForm = () => {
    const newErrors = {}

    // Name validation
    if (!formData.name.trim()) {
      newErrors.name = t('name_required')
    } else if (formData.name.trim().length < 2) {
      newErrors.name = t('name_min_length')
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!formData.email) {
      newErrors.email = t('email_required')
    } else if (!emailRegex.test(formData.email)) {
      newErrors.email = t('email_invalid')
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = t('password_required')
    } else if (formData.password.length < 6) {
      newErrors.password = t('password_min_length')
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(formData.password)) {
      newErrors.password = t('password_complexity')
    }

    // Confirm password validation
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = t('confirm_password_required')
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = t('passwords_not_match')
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) {
      toast.error(t('fix_form_errors'))
      return
    }

    setIsLoading(true)

    try {
      const response = await apiClient.register({
        email: formData.email.trim(),
        name: formData.name.trim(),
        password: formData.password,
        region: formData.region,
        language: formData.language
      })
      
      if (response.success) {
        toast.success(t('registration_successful'))
        router.push('/login')
      } else {
        // Handle specific backend errors
        if (response.error && response.error.includes('already exists')) {
          setErrors({ email: t('email_already_exists') })
          toast.error(t('email_already_exists'))
        } else {
          toast.error(response.error || t('registration_failed'))
        }
      }
    } catch (error) {
      console.error('Registration error:', error)
      
      // Handle network errors
      if (error.message.includes('fetch')) {
        toast.error(t('network_error'))
      } else if (error.message.includes('API Error: 500')) {
        toast.error(t('server_error'))
      } else if (error.message.includes('API Error: 400')) {
        toast.error(t('invalid_data'))
      } else {
        toast.error(t('registration_failed') + ': ' + error.message)
      }
    } finally {
      setIsLoading(false)
    }
  }

  const getPasswordStrength = () => {
    const password = formData.password
    if (!password) return { strength: 0, text: '', color: '' }
    
    let strength = 0
    if (password.length >= 6) strength++
    if (password.length >= 8) strength++
    if (/[a-z]/.test(password)) strength++
    if (/[A-Z]/.test(password)) strength++
    if (/\d/.test(password)) strength++
    if (/[^A-Za-z0-9]/.test(password)) strength++

    if (strength <= 2) return { strength, text: t('password_weak'), color: 'text-red-500' }
    if (strength <= 4) return { strength, text: t('password_fair'), color: 'text-yellow-500' }
    return { strength, text: t('password_strong'), color: 'text-green-500' }
  }

  const passwordStrength = getPasswordStrength()

  return (
    <>
      <Head>
        <title>{t('register')} - Content Creator Pro</title>
        <meta name="description" content={t('register_description')} />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <div className="text-center">
            <div className="flex justify-center mb-4">
              <Sparkles className="w-12 h-12 text-blue-600" />
            </div>
            <h2 className="text-3xl font-extrabold text-gray-900 mb-2">
              {t('create_account')}
            </h2>
            <p className="text-lg text-gray-600">
              {t('join_today')}
            </p>
          </div>
        </div>

        <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow-xl rounded-xl sm:px-10 border border-gray-100">
            <form className="space-y-6" onSubmit={handleSubmit}>
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                  {t('full_name')} *
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <User className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="name"
                    name="name"
                    type="text"
                    autoComplete="name"
                    required
                    value={formData.name}
                    onChange={(e) => handleInputChange('name', e.target.value)}
                    className={`appearance-none block w-full pl-10 pr-3 py-3 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${
                      errors.name ? 'border-red-300' : 'border-gray-300'
                    }`}
                    placeholder={t('enter_full_name')}
                  />
                </div>
                {errors.name && (
                  <p className="mt-1 text-sm text-red-600 flex items-center">
                    <AlertCircle className="w-4 h-4 mr-1" />
                    {errors.name}
                  </p>
                )}
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  {t('email_address')} *
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Mail className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                    value={formData.email}
                    onChange={(e) => handleInputChange('email', e.target.value)}
                    className={`appearance-none block w-full pl-10 pr-3 py-3 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${
                      errors.email ? 'border-red-300' : 'border-gray-300'
                    }`}
                    placeholder={t('enter_email_address')}
                  />
                </div>
                {errors.email && (
                  <p className="mt-1 text-sm text-red-600 flex items-center">
                    <AlertCircle className="w-4 h-4 mr-1" />
                    {errors.email}
                  </p>
                )}
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                  {t('password')} *
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="password"
                    name="password"
                    type={showPassword ? "text" : "password"}
                    autoComplete="new-password"
                    required
                    value={formData.password}
                    onChange={(e) => handleInputChange('password', e.target.value)}
                    className={`appearance-none block w-full pl-10 pr-10 py-3 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${
                      errors.password ? 'border-red-300' : 'border-gray-300'
                    }`}
                    placeholder={t('create_strong_password')}
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5 text-gray-400" />
                    ) : (
                      <Eye className="h-5 w-5 text-gray-400" />
                    )}
                  </button>
                </div>
                {formData.password && (
                  <div className="mt-1">
                    <div className="flex items-center justify-between text-xs">
                      <span className={passwordStrength.color}>{passwordStrength.text}</span>
                      <div className="flex space-x-1">
                        {[1, 2, 3, 4, 5].map((level) => (
                          <div
                            key={level}
                            className={`h-1 w-8 rounded ${
                              level <= passwordStrength.strength
                                ? passwordStrength.strength <= 2
                                  ? 'bg-red-500'
                                  : passwordStrength.strength <= 4
                                  ? 'bg-yellow-500'
                                  : 'bg-green-500'
                                : 'bg-gray-200'
                            }`}
                          />
                        ))}
                      </div>
                    </div>
                  </div>
                )}
                {errors.password && (
                  <p className="mt-1 text-sm text-red-600 flex items-center">
                    <AlertCircle className="w-4 h-4 mr-1" />
                    {errors.password}
                  </p>
                )}
              </div>

              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-2">
                  {t('confirm_password')} *
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="confirmPassword"
                    name="confirmPassword"
                    type={showConfirmPassword ? "text" : "password"}
                    autoComplete="new-password"
                    required
                    value={formData.confirmPassword}
                    onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
                    className={`appearance-none block w-full pl-10 pr-10 py-3 border rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${
                      errors.confirmPassword ? 'border-red-300' : 'border-gray-300'
                    }`}
                    placeholder={t('confirm_password')}
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  >
                    {showConfirmPassword ? (
                      <EyeOff className="h-5 w-5 text-gray-400" />
                    ) : (
                      <Eye className="h-5 w-5 text-gray-400" />
                    )}
                  </button>
                </div>
                {errors.confirmPassword && (
                  <p className="mt-1 text-sm text-red-600 flex items-center">
                    <AlertCircle className="w-4 h-4 mr-1" />
                    {errors.confirmPassword}
                  </p>
                )}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label htmlFor="region" className="block text-sm font-medium text-gray-700 mb-2">
                    {t('region')}
                  </label>
                  <select
                    id="region"
                    name="region"
                    value={formData.region}
                    onChange={(e) => handleInputChange('region', e.target.value)}
                    className="block w-full px-3 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  >
                    <option value="global">{t('global')}</option>
                    <option value="us">{t('united_states')}</option>
                    <option value="eu">{t('europe')}</option>
                    <option value="asia">{t('asia')}</option>
                    <option value="au">{t('australia')}</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="language" className="block text-sm font-medium text-gray-700 mb-2">
                    {t('language')}
                  </label>
                  <select
                    id="language"
                    name="language"
                    value={formData.language}
                    onChange={(e) => handleInputChange('language', e.target.value)}
                    className="block w-full px-3 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  >
                    <option value="en">{t('english')}</option>
                    <option value="zh">{t('chinese')}</option>
                    <option value="es">{t('spanish')}</option>
                    <option value="fr">{t('french')}</option>
                  </select>
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
              >
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    {t('creating_account')}
                  </>
                ) : (
                  <>
                    <UserPlus className="w-4 h-4 mr-2" />
                    {t('create_account')}
                  </>
                )}
              </button>
            </form>

            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600">
                {t('already_have_account')}{' '}
                <Link href="/login" className="font-medium text-blue-600 hover:text-blue-500">
                  {t('sign_in_here')}
                </Link>
              </p>
            </div>

            <div className="mt-6 bg-green-50 p-4 rounded-lg border border-green-200">
              <h3 className="text-sm font-medium text-green-900 mb-2 flex items-center">
                <CheckCircle className="w-4 h-4 mr-2" />
                {t('why_join_content_creator_pro')}
              </h3>
              <ul className="text-xs text-green-800 space-y-1">
                <li>• {t('ai_powered_content_generation')}</li>
                <li>• {t('multi_platform_social_media_support')}</li>
                <li>• {t('regional_content_adaptation')}</li>
                <li>• {t('content_library_and_management')}</li>
                <li>• {t('post_scheduling_and_analytics')}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </>
  )
} 