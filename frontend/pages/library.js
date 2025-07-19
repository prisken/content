import { useState, useEffect } from 'react'
import Head from 'next/head'
import { Search, Download, Copy, Edit, Trash2 } from 'lucide-react'
import { apiClient } from '../lib/api'
import ProtectedRoute from '../components/ProtectedRoute'
import { useLanguage } from '../contexts/LanguageContext'
import toast from 'react-hot-toast'

export default function Library() {
  const [content, setContent] = useState([])
  const [filteredContent, setFilteredContent] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedPlatform, setSelectedPlatform] = useState('all')
  const [selectedDirection, setSelectedDirection] = useState('all')
  const [sortBy, setSortBy] = useState('newest')
  const [isLoading, setIsLoading] = useState(true)
  const { t } = useLanguage()

  useEffect(() => {
    // Simulate loading content data
    const loadContent = async () => {
      try {
        // Mock data - in real app, fetch from API
        const mockContent = [
          {
            id: 1,
            title: t('sample_content_1'),
            content: t('sample_content_1_text'),
            platform: 'LinkedIn',
            direction: t('business_finance'),
            created: '2024-12-19',
            engagement: 156,
            hashtags: ['AI', 'Business', 'Innovation', 'Technology']
          },
          {
            id: 2,
            title: t('sample_content_2'),
            content: t('sample_content_2_text'),
            platform: 'Twitter',
            direction: t('technology'),
            created: '2024-12-18',
            engagement: 89,
            hashtags: ['Marketing', 'Digital', 'Trends', '2024']
          },
          {
            id: 3,
            title: t('sample_content_3'),
            content: t('sample_content_3_text'),
            platform: 'Instagram',
            direction: t('health_wellness'),
            created: '2024-12-17',
            engagement: 234,
            hashtags: ['Wellness', 'Balance', 'Health', 'Lifestyle']
          },
          {
            id: 4,
            title: t('sample_content_4'),
            content: t('sample_content_4_text'),
            platform: 'LinkedIn',
            direction: t('business_finance'),
            created: '2024-12-16',
            engagement: 198,
            hashtags: ['RemoteWork', 'FutureOfWork', 'Business']
          },
          {
            id: 5,
            title: t('sample_content_5'),
            content: t('sample_content_5_text'),
            platform: 'Facebook',
            direction: t('environment'),
            created: '2024-12-15',
            engagement: 145,
            hashtags: ['Sustainability', 'EcoFriendly', 'GreenLiving']
          }
        ]

        setContent(mockContent)
        setFilteredContent(mockContent)
      } catch (error) {
        console.error('Error loading content:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadContent()
  }, [t])

  useEffect(() => {
    // Filter and sort content
    let filtered = content.filter(item => {
      const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           item.content.toLowerCase().includes(searchTerm.toLowerCase())
      const matchesPlatform = selectedPlatform === 'all' || item.platform === selectedPlatform
      const matchesDirection = selectedDirection === 'all' || item.direction === selectedDirection

      return matchesSearch && matchesPlatform && matchesDirection
    })

    // Sort content
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'newest':
          return new Date(b.created) - new Date(a.created)
        case 'oldest':
          return new Date(a.created) - new Date(b.created)
        case 'most_engaged':
          return b.engagement - a.engagement
        case 'least_engaged':
          return a.engagement - b.engagement
        default:
          return 0
      }
    })

    setFilteredContent(filtered)
  }, [content, searchTerm, selectedPlatform, selectedDirection, sortBy])

  const platforms = ['all', 'LinkedIn', 'Twitter', 'Instagram', 'Facebook', 'YouTube', 'Blog']
  const directions = ['all', t('business_finance'), t('technology'), t('health_wellness'), t('education'), t('entertainment'), t('travel_tourism')]

  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text)
      toast.success(t('copied_to_clipboard'))
    } catch (error) {
      toast.error(t('copy_failed'))
    }
  }

  const downloadContent = (item) => {
    const content = `${t('content_creator_pro')} - ${item.title}

${t('platform')}: ${item.platform}
${t('direction')}: ${item.direction}
${t('created')}: ${item.created}
${t('engagement')}: ${item.engagement}

${t('content')}:
${item.content}

${t('hashtags')}:
${item.hashtags.join(', ')}

${t('generated_on')}: ${new Date().toLocaleString()}
`

    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${item.title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}-${Date.now()}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <ProtectedRoute>
      <>
        <Head>
          <title>{t('content_library')} - Content Creator Pro</title>
          <meta name="description" content={t('library_description')} />
        </Head>

        <div className="container mx-auto px-4 py-8">
          <div className="max-w-7xl mx-auto">
            {/* Header */}
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{t('content_library')}</h1>
              <p className="text-gray-600">{t('library_subtitle')}</p>
            </div>

            {/* Filters and Search */}
            <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {/* Search */}
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                  <input
                    type="text"
                    placeholder={t('search_content')}
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                {/* Platform Filter */}
                <select
                  value={selectedPlatform}
                  onChange={(e) => setSelectedPlatform(e.target.value)}
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  {platforms.map(platform => (
                    <option key={platform} value={platform}>
                      {platform === 'all' ? t('all_platforms') : platform}
                    </option>
                  ))}
                </select>

                {/* Direction Filter */}
                <select
                  value={selectedDirection}
                  onChange={(e) => setSelectedDirection(e.target.value)}
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  {directions.map(direction => (
                    <option key={direction} value={direction}>
                      {direction === 'all' ? t('all_directions') : direction}
                    </option>
                  ))}
                </select>

                {/* Sort */}
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="newest">{t('newest_first')}</option>
                  <option value="oldest">{t('oldest_first')}</option>
                  <option value="most_engaged">{t('most_engaged')}</option>
                  <option value="least_engaged">{t('least_engaged')}</option>
                </select>
              </div>
            </div>

            {isLoading ? (
              <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              </div>
            ) : filteredContent.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-gray-400 mb-4">
                  <Search className="w-16 h-16 mx-auto" />
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">{t('no_content_found')}</h3>
                <p className="text-gray-600">{t('try_adjusting_filters')}</p>
              </div>
            ) : (
              <div className="space-y-6">
                {filteredContent.map((item) => (
                  <div key={item.id} className="bg-white rounded-lg shadow-lg p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex-1">
                        <h3 className="text-xl font-bold text-gray-900 mb-2">{item.title}</h3>
                        <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
                          <span className="flex items-center">
                            <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                            {item.platform}
                          </span>
                          <span>{item.direction}</span>
                          <span>{item.created}</span>
                          <span className="font-medium text-green-600">{item.engagement} {t('engagement')}</span>
                        </div>
                      </div>
                      <div className="flex space-x-2">
                        <button
                          onClick={() => copyToClipboard(item.content)}
                          className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors duration-200"
                          title={t('copy_content')}
                        >
                          <Copy className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => downloadContent(item)}
                          className="p-2 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors duration-200"
                          title={t('download_content')}
                        >
                          <Download className="w-4 h-4" />
                        </button>
                        <button
                          className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors duration-200"
                          title={t('edit_content')}
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors duration-200"
                          title={t('delete_content')}
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>

                    <div className="bg-gray-50 p-4 rounded-lg mb-4">
                      <p className="text-gray-800 whitespace-pre-wrap">{item.content}</p>
                    </div>

                    {item.hashtags && item.hashtags.length > 0 && (
                      <div className="flex flex-wrap gap-2">
                        {item.hashtags.map((hashtag, index) => (
                          <span
                            key={index}
                            className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                          >
                            #{hashtag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Results Summary */}
            {filteredContent.length > 0 && (
              <div className="mt-8 text-center text-gray-600">
                {t('showing_results_summary', { count: filteredContent.length, total: content.length })}
              </div>
            )}
          </div>
        </div>
      </>
    </ProtectedRoute>
  )
} 