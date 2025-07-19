import { useState } from 'react'
import Link from 'next/link'
import { Menu, X, Sparkles, LogOut, User, Shield } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

export default function Layout({ children }) {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const { user, isAuthenticated, logout } = useAuth()

  // Navigation items based on authentication status and user role
  const getNavigation = () => {
    const baseNav = [
      { name: 'Home', href: '/' },
      { name: 'Generator', href: '/generator' },
    ]

    if (isAuthenticated()) {
      const userNav = [
        ...baseNav,
        { name: 'Dashboard', href: '/dashboard' },
        { name: 'Library', href: '/library' },
        { name: 'Post Management', href: '/post-management' },
        { name: 'Settings', href: '/settings' },
        { name: 'Setup', href: '/setup' },
      ]

      // Add admin menu for admin users
      if (user?.role === 'admin') {
        userNav.push({ name: 'User Management', href: '/admin/users', icon: Shield })
      }

      return userNav
    } else {
      return [
        ...baseNav,
        { name: 'Login', href: '/login' },
        { name: 'Register', href: '/register' },
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
              <span className="text-xl font-bold text-gray-900">Content Creator Pro</span>
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
              
              {/* User Menu */}
              {isAuthenticated() && (
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2 text-sm text-gray-600">
                    <User className="w-4 h-4" />
                    <span>{user?.name || user?.email}</span>
                    {user?.role === 'admin' && (
                      <Shield className="w-4 h-4 text-red-500" title="Admin" />
                    )}
                  </div>
                  <button
                    onClick={logout}
                    className="flex items-center space-x-1 text-gray-600 hover:text-red-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
                  >
                    <LogOut className="w-4 h-4" />
                    <span>Logout</span>
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
                
                {/* Mobile User Menu */}
                {isAuthenticated() && (
                  <div className="border-t border-gray-200 pt-3 mt-3">
                    <div className="flex items-center space-x-2 px-3 py-2 text-sm text-gray-600">
                      <User className="w-4 h-4" />
                      <span>{user?.name || user?.email}</span>
                      {user?.role === 'admin' && (
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
                      <span>Logout</span>
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
                Generate professional social media posts, blog articles, and more with our AI-powered platform.
              </p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Features</h3>
              <ul className="space-y-2 text-gray-300">
                <li>AI Content Generation</li>
                <li>Multi-Platform Support</li>
                <li>Regional Adaptation</li>
                <li>Content Library</li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Platforms</h3>
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
            <p>&copy; 2024 Content Creator Pro. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
} 