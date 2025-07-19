import { useState, useEffect } from 'react'
import Head from 'next/head'
import { BarChart3, FileText, TrendingUp, Users, Calendar, Target } from 'lucide-react'
import { apiClient } from '../lib/api'
import ProtectedRoute from '../components/ProtectedRoute'
import { useLanguage } from '../contexts/LanguageContext'

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalContent: 0,
    thisMonth: 0,
    engagementRate: 0,
    topPlatform: 'LinkedIn'
  })

  const [recentContent, setRecentContent] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const { t } = useLanguage()

  useEffect(() => {
    // Simulate loading dashboard data
    const loadDashboardData = async () => {
      try {
        // In a real app, you'd fetch this from your API
        // For now, we'll use mock data
        setStats({
          totalContent: 24,
          thisMonth: 8,
          engagementRate: 12.5,
          topPlatform: 'LinkedIn'
        })

        setRecentContent([
          {
            id: 1,
            title: t('sample_content_1'),
            platform: 'LinkedIn',
            direction: t('business_finance'),
            created: '2024-12-19',
            engagement: 156
          },
          {
            id: 2,
            title: t('sample_content_2'),
            platform: 'Twitter',
            direction: t('technology'),
            created: '2024-12-18',
            engagement: 89
          },
          {
            id: 3,
            title: t('sample_content_3'),
            platform: 'Instagram',
            direction: t('health_wellness'),
            created: '2024-12-17',
            engagement: 234
          }
        ])
      } catch (error) {
        console.error('Error loading dashboard data:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadDashboardData()
  }, [t])

  const platformPerformance = [
    { platform: 'LinkedIn', posts: 12, engagement: 156 },
    { platform: 'Twitter', posts: 8, engagement: 89 },
    { platform: 'Instagram', posts: 4, engagement: 234 },
    { platform: 'Facebook', posts: 6, engagement: 67 },
  ]

  return (
    <ProtectedRoute>
      <>
        <Head>
          <title>{t('dashboard')} - Content Creator Pro</title>
          <meta name="description" content={t('dashboard_description')} />
        </Head>

        <div className="container mx-auto px-4 py-8">
          <div className="max-w-7xl mx-auto">
            {/* Header */}
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{t('dashboard')}</h1>
              <p className="text-gray-600">{t('dashboard_welcome')}</p>
            </div>

            {isLoading ? (
              <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              </div>
            ) : (
              <>
                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                  <div className="bg-white p-6 rounded-lg shadow-lg">
                    <div className="flex items-center">
                      <div className="p-2 bg-blue-100 rounded-lg">
                        <FileText className="w-6 h-6 text-blue-600" />
                      </div>
                      <div className="ml-4">
                        <p className="text-sm font-medium text-gray-600">{t('total_content')}</p>
                        <p className="text-2xl font-bold text-gray-900">{stats.totalContent}</p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white p-6 rounded-lg shadow-lg">
                    <div className="flex items-center">
                      <div className="p-2 bg-green-100 rounded-lg">
                        <Calendar className="w-6 h-6 text-green-600" />
                      </div>
                      <div className="ml-4">
                        <p className="text-sm font-medium text-gray-600">{t('this_month')}</p>
                        <p className="text-2xl font-bold text-gray-900">{stats.thisMonth}</p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white p-6 rounded-lg shadow-lg">
                    <div className="flex items-center">
                      <div className="p-2 bg-purple-100 rounded-lg">
                        <TrendingUp className="w-6 h-6 text-purple-600" />
                      </div>
                      <div className="ml-4">
                        <p className="text-sm font-medium text-gray-600">{t('engagement_rate')}</p>
                        <p className="text-2xl font-bold text-gray-900">{stats.engagementRate}%</p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white p-6 rounded-lg shadow-lg">
                    <div className="flex items-center">
                      <div className="p-2 bg-orange-100 rounded-lg">
                        <Target className="w-6 h-6 text-orange-600" />
                      </div>
                      <div className="ml-4">
                        <p className="text-sm font-medium text-gray-600">{t('top_platform')}</p>
                        <p className="text-2xl font-bold text-gray-900">{stats.topPlatform}</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Main Content Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  {/* Recent Content */}
                  <div className="lg:col-span-2">
                    <div className="bg-white rounded-lg shadow-lg p-6">
                      <div className="flex justify-between items-center mb-6">
                        <h2 className="text-xl font-bold text-gray-900">{t('recent_content')}</h2>
                        <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                          {t('view_all')}
                        </button>
                      </div>

                      <div className="space-y-4">
                        {recentContent.map((content) => (
                          <div key={content.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200">
                            <div className="flex justify-between items-start">
                              <div className="flex-1">
                                <h3 className="font-semibold text-gray-900 mb-1">{content.title}</h3>
                                <div className="flex items-center space-x-4 text-sm text-gray-600">
                                  <span className="flex items-center">
                                    <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                                    {content.platform}
                                  </span>
                                  <span>{content.direction}</span>
                                  <span>{content.created}</span>
                                </div>
                              </div>
                              <div className="text-right">
                                <p className="text-sm text-gray-600">{t('engagement')}</p>
                                <p className="font-semibold text-gray-900">{content.engagement}</p>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Platform Performance */}
                  <div className="lg:col-span-1">
                    <div className="bg-white rounded-lg shadow-lg p-6">
                      <h2 className="text-xl font-bold text-gray-900 mb-6">{t('platform_performance')}</h2>
                      
                      <div className="space-y-4">
                        {platformPerformance.map((platform) => (
                          <div key={platform.platform} className="flex items-center justify-between">
                            <div className="flex items-center">
                              <div className="w-3 h-3 bg-blue-500 rounded-full mr-3"></div>
                              <span className="font-medium text-gray-900">{platform.platform}</span>
                            </div>
                            <div className="text-right">
                              <p className="text-sm text-gray-600">{platform.posts} {t('posts')}</p>
                              <p className="font-semibold text-gray-900">{platform.engagement} {t('engagement')}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </>
    </ProtectedRoute>
  )
} 