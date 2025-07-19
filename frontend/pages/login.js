import { useState } from 'react'
import { useRouter } from 'next/router'
import { apiClient } from '../lib/api'
import toast from 'react-hot-toast'
import { useAuth } from '../contexts/AuthContext'
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

  const demoUsers = [
    {
      email: 'demo@contentcreator.com',
      password: 'demo123',
      name: 'Demo User',
      description: 'Regular user account'
    },
    {
      email: 'admin@contentcreator.com',
      password: 'admin123', 
      name: 'Admin User',
      description: 'Administrator account'
    }
  ]

  const fillDemoCredentials = (demoUser) => {
    setEmail(demoUser.email)
    setPassword(demoUser.password)
    toast.success(`Filled ${demoUser.name} credentials`)
  }

  const handleLogin = async (e) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      const response = await apiClient.login({ email, password })
      
      if (response.success) {
        toast.success('Login successful!')
        // The backend returns user directly, not in data.user
        login(response.user, null) // No token in current implementation
        router.push('/dashboard')
      } else {
        toast.error(response.error || 'Login failed')
      }
    } catch (error) {
      toast.error('Login failed: ' + error.message)
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
        toast.success('Registration successful! Please login.')
        setPassword('')
        setIsRegistering(false)
      } else {
        toast.error(response.error || 'Registration failed')
        setIsRegistering(false)
      }
    } catch (error) {
      toast.error('Registration failed: ' + error.message)
      setIsRegistering(false)
    }
  }

  return (
    <>
      <Head>
        <title>Login - Content Creator Pro</title>
        <meta name="description" content="Sign in to Content Creator Pro" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <div className="text-center">
            <div className="flex justify-center mb-4">
              <Sparkles className="w-12 h-12 text-blue-600" />
            </div>
            <h2 className="text-3xl font-extrabold text-gray-900 mb-2">
              Content Creator Pro
            </h2>
            <p className="text-lg text-gray-600">
              Sign in to your account
            </p>
          </div>
        </div>

        <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow-xl rounded-xl sm:px-10 border border-gray-100">
            <form className="space-y-6" onSubmit={handleLogin}>
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  Email address
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
                    placeholder="Enter your email"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                  Password
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
                    placeholder="Enter your password"
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
                      Signing in...
                    </>
                  ) : (
                    <>
                      <User className="w-4 h-4 mr-2" />
                      Sign in
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
                      Creating...
                    </>
                  ) : (
                    <>
                      <ArrowRight className="w-4 h-4 mr-2" />
                      Register
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
                  <span className="px-4 bg-white text-gray-500 font-medium">Demo Accounts</span>
                </div>
              </div>

              <div className="mt-6 space-y-3">
                <p className="text-sm text-gray-600 text-center mb-4">
                  Use these demo accounts to test the platform:
                </p>
                
                {demoUsers.map((user, index) => (
                  <div key={index} className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <h3 className="text-sm font-medium text-gray-900">{user.name}</h3>
                        <p className="text-xs text-gray-500">{user.description}</p>
                        <div className="mt-2 text-xs text-gray-600">
                          <span className="font-medium">Email:</span> {user.email}<br/>
                          <span className="font-medium">Password:</span> {user.password}
                        </div>
                      </div>
                      <button
                        onClick={() => fillDemoCredentials(user)}
                        className="ml-4 px-3 py-2 bg-blue-100 text-blue-700 rounded-md text-sm font-medium hover:bg-blue-200 transition-colors duration-200 flex items-center"
                      >
                        <CheckCircle className="w-4 h-4 mr-1" />
                        Use
                      </button>
                    </div>
                  </div>
                ))}
              </div>

                             <div className="mt-6 bg-blue-50 p-4 rounded-lg border border-blue-200">
                 <h3 className="text-sm font-medium text-blue-900 mb-2">Getting Started</h3>
                 <ol className="text-xs text-blue-800 space-y-1">
                   <li>1. Click "Use" on any demo account above</li>
                   <li>2. Click "Sign in" to login</li>
                   <li>3. Explore the platform features</li>
                   <li>4. Try generating content in the Generator</li>
                 </ol>
               </div>

               <div className="mt-4 text-center">
                 <p className="text-sm text-gray-600">
                   Don't have an account?{' '}
                   <Link href="/register" className="font-medium text-blue-600 hover:text-blue-500">
                     Register here
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