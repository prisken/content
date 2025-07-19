import { useState } from 'react'
import { useRouter } from 'next/router'
import { apiClient } from '../lib/api'
import toast from 'react-hot-toast'
import { useAuth } from '../contexts/AuthContext'
import { useLanguage } from '../contexts/LanguageContext'
import Head from 'next/head'
import Link from 'next/link'
import { User, Lock, Mail, Eye, EyeOff, Sparkles, ArrowRight, CheckCircle } from 'lucide-react'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [isRegistering, setIsRegistering] = useState(false)
  const router = useRouter()
  const { login } = useAuth()
  const { t } = useLanguage()

  const demoUsers = [
    {
      email: 'demo@contentcreator.com',
      password: 'demo123',
      name: t('demo_user'),
      description: t('demo_user_description')
    },
    {
      email: 'admin@contentcreator.com',
      password: 'admin123', 
      name: t('admin_user'),
      description: t('admin_user_description')
    }
  ]

  const fillDemoCredentials = (demoUser) => {
    setEmail(demoUser.email)
    setPassword(demoUser.password)
    toast.success(t('filled_credentials', { name: demoUser.name }))
  }

  const handleLogin = async (e) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      const response = await apiClient.login({ email, password })
      
      if (response.success) {
        toast.success(t('login_successful'))
        // The backend returns user directly, not in data.user
        login(response.user, null) // No token in current implementation
        router.push('/dashboard')
      } else {
        toast.error(response.error || t('login_failed'))
      }
    } catch (error) {
      toast.error(t('login_failed') + ': ' + error.message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleRegister = async () => {
    setIsRegistering(true)

    try {
      const response = await apiClient.register({ 
        email, 
        name: email.split('@')[0], // Use email prefix as name
        password,
        region: 'global',
        language: 'en'
      })
      
      if (response.success) {
        toast.success(t('registration_successful'))
        setPassword('')
        setIsRegistering(false)
      } else {
        toast.error(response.error || t('registration_failed'))
        setIsRegistering(false)
      }
    } catch (error) {
      toast.error(t('registration_failed') + ': ' + error.message)
      setIsRegistering(false)
    }
  }

  return (
    <>
      <Head>
        <title>{t('login')} - Content Creator Pro</title>
        <meta name="description" content={t('sign_in_description')} />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <div className="text-center">
            <div className="flex justify-center mb-4">
              <Sparkles className="w-12 h-12 text-blue-600" />
            </div>
            <h2 className="text-3xl font-extrabold text-gray-900 mb-2">
              {t('welcome')}
            </h2>
            <p className="text-lg text-gray-600">
              {t('sign_in_to_account')}
            </p>
          </div>
        </div>

        <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow-xl rounded-xl sm:px-10 border border-gray-100">
            <form className="space-y-6" onSubmit={handleLogin}>
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  {t('email')}
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
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="appearance-none block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    placeholder={t('enter_email')}
                  />
                </div>
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                  {t('password')}
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="password"
                    name="password"
                    type={showPassword ? "text" : "password"}
                    autoComplete="current-password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="appearance-none block w-full pl-10 pr-10 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    placeholder={t('enter_password')}
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
              </div>

              <div className="flex space-x-3">
                <button
                  type="submit"
                  disabled={isLoading}
                  className="flex-1 w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                >
                  {isLoading ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      {t('signing_in')}
                    </>
                  ) : (
                    <>
                      <User className="w-4 h-4 mr-2" />
                      {t('sign_in')}
                    </>
                  )}
                </button>
                
                <button
                  type="button"
                  onClick={handleRegister}
                  disabled={isRegistering}
                  className="flex-1 w-full flex justify-center items-center py-3 px-4 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                >
                  {isRegistering ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                      {t('creating')}
                    </>
                  ) : (
                    <>
                      <ArrowRight className="w-4 h-4 mr-2" />
                      {t('register')}
                    </>
                  )}
                </button>
              </div>
            </form>

            {/* Demo Users Section */}
            <div className="mt-8">
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300" />
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-4 bg-white text-gray-500 font-medium">{t('demo_accounts')}</span>
                </div>
              </div>

              <div className="mt-6 space-y-3">
                <p className="text-sm text-gray-600 text-center mb-4">
                  {t('demo_accounts_description')}
                </p>
                
                {demoUsers.map((user, index) => (
                  <div key={index} className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <h3 className="text-sm font-medium text-gray-900">{user.name}</h3>
                        <p className="text-xs text-gray-500">{user.description}</p>
                        <div className="mt-2 text-xs text-gray-600">
                          <span className="font-medium">{t('email')}:</span> {user.email}<br/>
                          <span className="font-medium">{t('password')}:</span> {user.password}
                        </div>
                      </div>
                      <button
                        onClick={() => fillDemoCredentials(user)}
                        className="ml-4 px-3 py-2 bg-blue-100 text-blue-700 rounded-md text-sm font-medium hover:bg-blue-200 transition-colors duration-200 flex items-center"
                      >
                        <CheckCircle className="w-4 h-4 mr-1" />
                        {t('use')}
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-6 bg-blue-50 p-4 rounded-lg border border-blue-200">
                <h3 className="text-sm font-medium text-blue-900 mb-2">{t('getting_started')}</h3>
                <ol className="text-xs text-blue-800 space-y-1">
                  <li>1. {t('getting_started_step1')}</li>
                  <li>2. {t('getting_started_step2')}</li>
                  <li>3. {t('getting_started_step3')}</li>
                  <li>4. {t('getting_started_step4')}</li>
                </ol>
              </div>

              <div className="mt-4 text-center">
                <p className="text-sm text-gray-600">
                  {t('dont_have_account')}{' '}
                  <Link href="/register" className="font-medium text-blue-600 hover:text-blue-500">
                    {t('register_here')}
                  </Link>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
} 