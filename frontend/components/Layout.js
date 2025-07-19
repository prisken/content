import { useState } from 'react'
import Link from 'next/link'
import { Menu, X, Sparkles, LogOut, User, Shield } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { useLanguage } from '../contexts/LanguageContext'
import LanguageSelector from './LanguageSelector'

export default function Layout({ children }) {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const { user, isAuthenticated, logout } = useAuth()
  const { t } = useLanguage()

  // Navigation items based on authentication status and user role
  const getNavigation = () => {
    const baseNav = [
      { name: t('home'), href: '/' },
      { name: t('generator'), href: '/generator' },
    ]

    if (isAuthenticated()) {
      const userNav = [
        ...baseNav,
        { name: t('dashboard'), href: '/dashboard' },
        { name: t('library'), href: '/library' },
        { name: t('post_management'), href: '/post-management' },
        { name: t('settings'), href: '/settings' },
        { name: t('setup'), href: '/setup' },
      ]

      // Add admin menu for admin users
      if (user?.email === 'admin@contentcreator.com') {
        userNav.push({ name: t('user_management'), href: '/admin/users', icon: Shield })
      }

      return userNav
    } else {
      return [
        ...baseNav,
        { name: t('login'), href: '/login' },
        { name: t('register'), href: '/register' },
      ]
    }
  }

  const navigation = getNavigation()

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link href="/" className="flex items-center space-x-2">
              <Sparkles className="w-8 h-8 text-blue-600" />
              <span className="text-xl font-bold text-gray-900">{t('welcome')}</span>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center space-x-8">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className="text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 flex items-center space-x-1"
                >
                  {item.icon && <item.icon className="w-4 h-4" />}
                  <span>{item.name}</span>
                </Link>
              ))}
              
              {/* Language Selector */}
              <LanguageSelector />
              
              {/* User Menu */}
              {isAuthenticated() && (
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2 text-sm text-gray-600">
                    <User className="w-4 h-4" />
                    <span>{user?.name || user?.email}</span>
                    {user?.email === 'admin@contentcreator.com' && (
                      <Shield className="w-4 h-4 text-red-500" title="Admin" />
                    )}
                  </div>
                  <button
                    onClick={logout}
                    className="flex items-center space-x-1 text-gray-600 hover:text-red-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
                  >
                    <LogOut className="w-4 h-4" />
                    <span>{t('logout')}</span>
                  </button>
                </div>
              )}
            </nav>

            {/* Mobile menu button */}
            <div className="md:hidden">
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="text-gray-600 hover:text-gray-900 focus:outline-none focus:text-gray-900"
              >
                {isMenuOpen ? (
                  <X className="w-6 h-6" />
                ) : (
                  <Menu className="w-6 h-6" />
                )}
              </button>
            </div>
          </div>

          {/* Mobile Navigation */}
          {isMenuOpen && (
            <div className="md:hidden">
              <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t border-gray-200">
                {navigation.map((item) => (
                  <Link
                    key={item.name}
                    href={item.href}
                    className="text-gray-600 hover:text-blue-600 block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200 flex items-center space-x-2"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    {item.icon && <item.icon className="w-4 h-4" />}
                    <span>{item.name}</span>
                  </Link>
                ))}
                
                {/* Mobile Language Selector */}
                <div className="px-3 py-2">
                  <LanguageSelector />
                </div>
                
                {/* Mobile User Menu */}
                {isAuthenticated() && (
                  <div className="border-t border-gray-200 pt-3 mt-3">
                    <div className="flex items-center space-x-2 px-3 py-2 text-sm text-gray-600">
                      <User className="w-4 h-4" />
                      <span>{user?.name || user?.email}</span>
                      {user?.email === 'admin@contentcreator.com' && (
                        <Shield className="w-4 h-4 text-red-500" title="Admin" />
                      )}
                    </div>
                    <button
                      onClick={() => {
                        logout()
                        setIsMenuOpen(false)
                      }}
                      className="w-full text-left flex items-center space-x-2 text-gray-600 hover:text-red-600 px-3 py-2 rounded-md text-base font-medium transition-colors duration-200"
                    >
                      <LogOut className="w-4 h-4" />
                      <span>{t('logout')}</span>
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main>{children}</main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="col-span-2">
              <div className="flex items-center space-x-2 mb-4">
                <Sparkles className="w-8 h-8 text-blue-400" />
                <span className="text-xl font-bold">Content Creator Pro</span>
              </div>
              <p className="text-gray-300 mb-4 max-w-md">
                {t('footer_description')}
              </p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">{t('features')}</h3>
              <ul className="space-y-2 text-gray-300">
                <li>{t('ai_content_generation')}</li>
                <li>{t('multi_platform_support')}</li>
                <li>{t('regional_adaptation')}</li>
                <li>{t('content_library')}</li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">{t('platforms')}</h3>
              <ul className="space-y-2 text-gray-300">
                <li>LinkedIn</li>
                <li>Facebook</li>
                <li>Instagram</li>
                <li>Twitter</li>
                <li>YouTube</li>
                <li>Blog</li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Content Creator Pro. {t('all_rights_reserved')}.</p>
          </div>
        </div>
      </footer>
    </div>
  )
} 