import { useState, useEffect } from 'react'
import Head from 'next/head'
import { BarChart3, FileText, TrendingUp, Users, Calendar, Target } from 'lucide-react'
import { apiClient } from '../lib/api'

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalContent: 0,
    thisMonth: 0,
    engagementRate: 0,
    topPlatform: 'LinkedIn'
  })

  const [recentContent, setRecentContent] = useState([])
  const [isLoading, setIsLoading] = useState(true)

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
            title: 'AI in Business: The Future is Now',
            platform: 'LinkedIn',
            direction: 'Business & Finance',
            created: '2024-12-19',
            engagement: 156
          },
          {
            id: 2,
            title: 'Digital Marketing Trends 2024',
            platform: 'Twitter',
            direction: 'Technology',
            created: '2024-12-18',
            engagement: 89
          },
          {
            id: 3,
            title: 'Healthy Work-Life Balance Tips',
            platform: 'Instagram',
            direction: 'Health & Wellness',
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
  }, [])

  const platformPerformance = [
    { platform: 'LinkedIn', posts: 12, engagement: 156 },
    { platform: 'Twitter', posts: 8, engagement: 89 },
    { platform: 'Instagram', posts: 4, engagement: 234 },
    { platform: 'Facebook', posts: 6, engagement: 67 },
  ]

  return (
    <>
      <Head>
        <title>Dashboard - Content Creator Pro</title>
        <meta name="description" content="Your content creation dashboard and analytics" />
      </Head>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
            <p className="text-gray-600">Welcome back! Here's an overview of your content performance.</p>
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
                      <p className="text-sm font-medium text-gray-600">Total Content</p>
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
                      <p className="text-sm font-medium text-gray-600">This Month</p>
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
                      <p className="text-sm font-medium text-gray-600">Engagement Rate</p>
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
                      <p className="text-sm font-medium text-gray-600">Top Platform</p>
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
                      <h2 className="text-xl font-bold text-gray-900">Recent Content</h2>
                      <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                        View All
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
                              <p className="text-sm text-gray-600">Engagement</p>
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
                    <h2 className="text-xl font-bold text-gray-900 mb-6">Platform Performance</h2>
                    
                    <div className="space-y-4">
                      {platformPerformance.map((platform) => (
                        <div key={platform.platform} className="flex items-center justify-between">
                          <div className="flex items-center">
                            <div className="w-3 h-3 bg-blue-500 rounded-full mr-3"></div>
                            <span className="font-medium text-gray-900">{platform.platform}</span>
                          </div>
                          <div className="text-right">
                            <p className="text-sm text-gray-600">{platform.posts} posts</p>
                            <p className="font-semibold text-gray-900">{platform.engagement} engagement</p>
                          </div>
                        </div>
                      ))}
                    </div>

                    <div className="mt-6 pt-6 border-t border-gray-200">
                      <h3 className="font-semibold text-gray-900 mb-4">Quick Actions</h3>
                      <div className="space-y-2">
                        <button className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors duration-200 text-sm">
                          Create New Content
                        </button>
                        <button className="w-full bg-gray-100 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-200 transition-colors duration-200 text-sm">
                          View Analytics
                        </button>
                        <button className="w-full bg-gray-100 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-200 transition-colors duration-200 text-sm">
                          Export Report
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Content Directions Performance */}
              <div className="mt-8">
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-6">Content Directions Performance</h2>
                  
                  <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                    {[
                      { name: 'Business & Finance', posts: 8, engagement: 234 },
                      { name: 'Technology', posts: 6, engagement: 189 },
                      { name: 'Health & Wellness', posts: 4, engagement: 156 },
                      { name: 'Education', posts: 3, engagement: 98 },
                      { name: 'Entertainment', posts: 2, engagement: 145 },
                      { name: 'Travel & Tourism', posts: 1, engagement: 67 },
                    ].map((direction) => (
                      <div key={direction.name} className="text-center p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow duration-200">
                        <h3 className="font-semibold text-gray-900 text-sm mb-2">{direction.name}</h3>
                        <p className="text-2xl font-bold text-blue-600">{direction.posts}</p>
                        <p className="text-xs text-gray-600">{direction.engagement} engagement</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </>
  )
} 