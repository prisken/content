import { useState, useEffect } from 'react'
import Head from 'next/head'
import toast from 'react-hot-toast'
import { Calendar, Clock, Edit, Trash2, Share2, Eye, Search, Plus } from 'lucide-react'
import { apiClient } from '../lib/api'
import ProtectedRoute from '../components/ProtectedRoute'
import { useLanguage } from '../contexts/LanguageContext'

export default function PostManagement() {
  const [posts, setPosts] = useState([])
  const [filteredPosts, setFilteredPosts] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterPlatform, setFilterPlatform] = useState('all')
  const [filterStatus, setFilterStatus] = useState('all')
  const [showScheduleModal, setShowScheduleModal] = useState(false)
  const [selectedPost, setSelectedPost] = useState(null)
  const { t } = useLanguage()

  // Mock data for demonstration
  const mockPosts = [
    {
      id: 1,
      title: t('sample_post_1_title'),
      content: t('sample_post_1_content'),
      platform: 'linkedin',
      status: 'scheduled',
      scheduledDate: '2024-01-20T10:00:00Z',
      createdAt: '2024-01-18T14:30:00Z',
      engagement: { likes: 45, comments: 12, shares: 8 }
    },
    {
      id: 2,
      title: t('sample_post_2_title'),
      content: t('sample_post_2_content'),
      platform: 'instagram',
      status: 'published',
      publishedDate: '2024-01-19T15:30:00Z',
      createdAt: '2024-01-17T09:15:00Z',
      engagement: { likes: 128, comments: 23, shares: 15 }
    },
    {
      id: 3,
      title: t('sample_post_3_title'),
      content: t('sample_post_3_content'),
      platform: 'facebook',
      status: 'draft',
      createdAt: '2024-01-20T11:45:00Z',
      engagement: null
    }
  ]

  useEffect(() => {
    setPosts(mockPosts)
    setFilteredPosts(mockPosts)
  }, [t])

  useEffect(() => {
    filterPosts()
  }, [posts, searchTerm, filterPlatform, filterStatus])

  const filterPosts = () => {
    let filtered = posts

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(post =>
        post.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        post.content.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    // Platform filter
    if (filterPlatform !== 'all') {
      filtered = filtered.filter(post => post.platform === filterPlatform)
    }

    // Status filter
    if (filterStatus !== 'all') {
      filtered = filtered.filter(post => post.status === filterStatus)
    }

    setFilteredPosts(filtered)
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'published': return 'bg-green-100 text-green-800'
      case 'scheduled': return 'bg-blue-100 text-blue-800'
      case 'draft': return 'bg-gray-100 text-gray-800'
      case 'failed': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getPlatformIcon = (platform) => {
    switch (platform) {
      case 'linkedin': return '💼'
      case 'facebook': return '📘'
      case 'instagram': return '📷'
      case 'twitter': return '🐦'
      case 'youtube': return '📺'
      default: return '📝'
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const handleEditPost = (post) => {
    setSelectedPost(post)
    setShowScheduleModal(true)
  }

  const handleDeletePost = (postId) => {
    if (confirm(t('confirm_delete_post'))) {
      setPosts(posts.filter(post => post.id !== postId))
      toast.success(t('post_deleted'))
    }
  }

  const handleSchedulePost = (postData) => {
    // In a real app, this would save to backend
    const updatedPost = {
      ...selectedPost,
      ...postData,
      status: 'scheduled'
    }
    
    setPosts(posts.map(post => 
      post.id === selectedPost.id ? updatedPost : post
    ))
    
    setShowScheduleModal(false)
    setSelectedPost(null)
    toast.success(t('post_scheduled'))
  }

  const handlePublishNow = (post) => {
    const updatedPost = { ...post, status: 'published', publishedDate: new Date().toISOString() }
    setPosts(posts.map(p => p.id === post.id ? updatedPost : p))
    toast.success(t('post_published'))
  }

  return (
    <ProtectedRoute>
      <>
        <Head>
          <title>{t('post_management')} - Content Creator Pro</title>
          <meta name="description" content={t('post_management_description')} />
        </Head>

        <div className="container mx-auto px-4 py-8">
          <div className="max-w-6xl mx-auto">
            {/* Header */}
            <div className="flex items-center justify-between mb-8">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">{t('post_management')}</h1>
                <p className="text-gray-600">{t('post_management_subtitle')}</p>
              </div>
              <button
                onClick={() => setShowScheduleModal(true)}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
              >
                <Plus className="w-4 h-4" />
                {t('new_post')}
              </button>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">{t('total_posts')}</p>
                    <p className="text-2xl font-bold text-gray-900">{posts.length}</p>
                  </div>
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <Calendar className="w-6 h-6 text-blue-600" />
                  </div>
                </div>
              </div>
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">{t('scheduled')}</p>
                    <p className="text-2xl font-bold text-blue-600">
                      {posts.filter(p => p.status === 'scheduled').length}
                    </p>
                  </div>
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <Clock className="w-6 h-6 text-blue-600" />
                  </div>
                </div>
              </div>
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">{t('published')}</p>
                    <p className="text-2xl font-bold text-green-600">
                      {posts.filter(p => p.status === 'published').length}
                    </p>
                  </div>
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                    <Share2 className="w-6 h-6 text-green-600" />
                  </div>
                </div>
              </div>
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">{t('drafts')}</p>
                    <p className="text-2xl font-bold text-gray-600">
                      {posts.filter(p => p.status === 'draft').length}
                    </p>
                  </div>
                  <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                    <Edit className="w-6 h-6 text-gray-600" />
                  </div>
                </div>
              </div>
            </div>

            {/* Filters */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                    <input
                      type="text"
                      placeholder={t('search_posts')}
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>
                <select
                  value={filterPlatform}
                  onChange={(e) => setFilterPlatform(e.target.value)}
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="all">{t('all_platforms')}</option>
                  <option value="linkedin">{t('linkedin')}</option>
                  <option value="facebook">{t('facebook')}</option>
                  <option value="instagram">{t('instagram')}</option>
                  <option value="twitter">{t('twitter')}</option>
                  <option value="youtube">{t('youtube')}</option>
                </select>
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="all">{t('all_status')}</option>
                  <option value="published">{t('published')}</option>
                  <option value="scheduled">{t('scheduled')}</option>
                  <option value="draft">{t('draft')}</option>
                  <option value="failed">{t('failed')}</option>
                </select>
              </div>
            </div>

            {/* Posts List */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-900">{t('posts')}</h2>
              </div>
              <div className="divide-y divide-gray-200">
                {filteredPosts.map((post) => (
                  <div key={post.id} className="p-6 hover:bg-gray-50 transition-colors duration-200">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <span className="text-2xl">{getPlatformIcon(post.platform)}</span>
                          <h3 className="text-lg font-medium text-gray-900">{post.title}</h3>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(post.status)}`}>
                            {post.status}
                          </span>
                        </div>
                        <p className="text-gray-600 mb-3 line-clamp-2">{post.content}</p>
                        <div className="flex items-center space-x-6 text-sm text-gray-500">
                          <span>{t('created_at')}: {formatDate(post.createdAt)}</span>
                          {post.scheduledDate && (
                            <span>{t('scheduled_at')}: {formatDate(post.scheduledDate)}</span>
                          )}
                          {post.publishedDate && (
                            <span>{t('published_at')}: {formatDate(post.publishedDate)}</span>
                          )}
                          {post.engagement && (
                            <span className="flex items-center space-x-1">
                              <Eye className="w-4 h-4" />
                              <span>{t('likes')}: {post.engagement.likes}</span>
                            </span>
                          )}
                        </div>
                      </div>
                      <div className="flex items-center space-x-2 ml-4">
                        {post.status === 'draft' && (
                          <button
                            onClick={() => handlePublishNow(post)}
                            className="p-2 text-green-600 hover:bg-green-50 rounded-lg"
                            title={t('publish_now')}
                          >
                            <Share2 className="w-4 h-4" />
                          </button>
                        )}
                        <button
                          onClick={() => handleEditPost(post)}
                          className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg"
                          title={t('edit_post')}
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDeletePost(post.id)}
                          className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                          title={t('delete_post')}
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
                {filteredPosts.length === 0 && (
                  <div className="p-12 text-center">
                    <Calendar className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">{t('no_posts_found')}</h3>
                    <p className="text-gray-500">{t('create_first_post')}</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Schedule Modal */}
        {showScheduleModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
              <h3 className="text-lg font-semibold mb-4">
                {selectedPost ? t('edit_post') : t('schedule_new_post')}
              </h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">{t('title')}</label>
                  <input
                    type="text"
                    defaultValue={selectedPost?.title || ''}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">{t('platform')}</label>
                  <select className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <option value="linkedin">{t('linkedin')}</option>
                    <option value="facebook">{t('facebook')}</option>
                    <option value="instagram">{t('instagram')}</option>
                    <option value="twitter">{t('twitter')}</option>
                    <option value="youtube">{t('youtube')}</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">{t('schedule_date')}</label>
                  <input
                    type="datetime-local"
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
              <div className="flex justify-end space-x-3 mt-6">
                <button
                  onClick={() => setShowScheduleModal(false)}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
                >
                  {t('cancel')}
                </button>
                <button
                  onClick={() => handleSchedulePost({})}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {t('schedule')}
                </button>
              </div>
            </div>
          </div>
        )}
      </>
    </ProtectedRoute>
  )
} 