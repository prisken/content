import { useState, useEffect } from 'react'
import Head from 'next/head'
import toast from 'react-hot-toast'
import { ChevronRight, Sparkles, Copy, Download, RefreshCw, Search, Globe, TrendingUp, BookOpen, Youtube, Mic, Bot } from 'lucide-react'
import { apiClient, contentDirections, platforms, tones } from '../lib/api'
import { useAuth } from '../contexts/AuthContext'
import { useLanguage } from '../contexts/LanguageContext'
import { useRouter } from 'next/router'

export default function Generator() {
  const [currentStep, setCurrentStep] = useState(1)
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedContent, setGeneratedContent] = useState(null)
  const [selectedTopics, setSelectedTopics] = useState([])
  const [isLoadingTopics, setIsLoadingTopics] = useState(false)
  const [googleSearchQuery, setGoogleSearchQuery] = useState('')
  const [selectedCountry, setSelectedCountry] = useState('US')
  const { isAuthenticated } = useAuth()
  const { t } = useLanguage()
  const router = useRouter()
  
  const [formData, setFormData] = useState({
    direction: '',
    platform: '',
    postType: '',
    source: '',
    sourceDetails: {},
    selectedTopic: '',
    tone: '',
    language: 'en',
    imageStyle: 'professional'
  })

  // Enhanced platforms with post types - Updated to match design document exactly
  const enhancedPlatforms = [
    {
      key: 'linkedin',
      name: 'LinkedIn Posts',
      icon: '💼',
      postTypes: [
        { key: 'posts', name: 'Posts' },
        { key: 'articles', name: 'Articles' },
        { key: 'newsletters', name: 'Newsletters' }
      ]
    },
    {
      key: 'facebook',
      name: 'Facebook Posts',
      icon: '📘',
      postTypes: [
        { key: 'posts', name: 'Posts' },
        { key: 'stories', name: 'Stories' },
        { key: 'reels', name: 'Reels (Coming Soon)', disabled: true }
      ]
    },
    {
      key: 'instagram',
      name: 'Instagram Posts',
      icon: '📷',
      postTypes: [
        { key: 'posts', name: 'Posts' },
        { key: 'stories', name: 'Stories' },
        { key: 'reels', name: 'Reels (Coming Soon)', disabled: true },
        { key: 'igtv', name: 'IGTV (Coming Soon)', disabled: true }
      ]
    },
    {
      key: 'twitter',
      name: 'Twitter Posts',
      icon: '🐦',
      postTypes: [
        { key: 'tweets', name: 'Tweets' },
        { key: 'threads', name: 'Threads' },
        { key: 'spaces', name: 'Spaces (Coming Soon)', disabled: true }
      ]
    },
    {
      key: 'youtube',
      name: 'YouTube Shorts',
      icon: '📺',
      postTypes: [
        { key: 'shorts', name: 'Shorts (Coming Soon)', disabled: true },
        { key: 'videos', name: 'Videos (Coming Soon)', disabled: true },
        { key: 'scripts', name: 'Scripts' }
      ]
    },
    {
      key: 'blog',
      name: 'Blog Articles',
      icon: '📝',
      postTypes: [
        { key: 'articles', name: 'Articles' },
        { key: 'newsletters', name: 'Newsletters' },
        { key: 'guides', name: 'Guides' }
      ]
    }
  ]

  // Enhanced sources with Google integration - Updated to match design document exactly (8 sources)
  const enhancedSources = [
    {
      key: 'news',
      name: 'News',
      icon: <Globe className="w-6 h-6" />,
      description: 'Financial, tech, business, industry news (localised by region)',
      hasSearch: true
    },
    {
      key: 'books',
      name: 'Books',
      icon: <BookOpen className="w-6 h-6" />,
      description: 'Business, self-help, industry, fiction',
      hasSearch: true
    },
    {
      key: 'popular_threads',
      name: 'Popular Threads',
      icon: <TrendingUp className="w-6 h-6" />,
      description: 'Reddit, Twitter, LinkedIn viral content',
      hasSearch: true
    },
    {
      key: 'podcasts',
      name: 'Podcasts',
      icon: <Mic className="w-6 h-6" />,
      description: 'Business and tech podcasts',
      hasSearch: true
    },
    {
      key: 'youtube',
      name: 'YouTube Videos',
      icon: <Youtube className="w-6 h-6" />,
      description: 'Educational content, TED Talks',
      hasSearch: true
    },
    {
      key: 'research_papers',
      name: 'Research Papers',
      icon: <Search className="w-6 h-6" />,
      description: 'Academic insights',
      hasSearch: true
    },
    {
      key: 'case_studies',
      name: 'Case Studies',
      icon: <BookOpen className="w-6 h-6" />,
      description: 'Business success stories',
      hasSearch: true
    },
    {
      key: 'trending_topics',
      name: 'Trending Topics',
      icon: <TrendingUp className="w-6 h-6" />,
      description: 'Current events and viral content (localised)',
      hasSearch: true
    }
  ]

  // Image style options
  const imageStyles = [
    {
      key: 'professional',
      name: 'Professional',
      description: 'Clean, corporate, business-focused',
      icon: '💼'
    },
    {
      key: 'creative',
      name: 'Creative',
      description: 'Artistic, innovative, imaginative',
      icon: '🎨'
    },
    {
      key: 'minimalist',
      name: 'Minimalist',
      description: 'Simple, clean, elegant',
      icon: '⚪'
    },
    {
      key: 'vibrant',
      name: 'Vibrant',
      description: 'Colorful, energetic, eye-catching',
      icon: '🌈'
    },
    {
      key: 'modern',
      name: 'Modern',
      description: 'Contemporary, sleek, trendy',
      icon: '🚀'
    },
    {
      key: 'natural',
      name: 'Natural',
      description: 'Organic, earthy, authentic',
      icon: '🌿'
    }
  ]

  // Countries for Google search
  const countries = [
    { code: 'US', name: 'United States' },
    { code: 'CA', name: 'Canada' },
    { code: 'GB', name: 'United Kingdom' },
    { code: 'AU', name: 'Australia' },
    { code: 'DE', name: 'Germany' },
    { code: 'FR', name: 'France' },
    { code: 'JP', name: 'Japan' },
    { code: 'IN', name: 'India' },
    { code: 'BR', name: 'Brazil' },
    { code: 'MX', name: 'Mexico' }
  ]

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    
    // Reset dependent fields
    if (field === 'platform') {
      setFormData(prev => ({ ...prev, postType: '' }))
    }
    if (field === 'source') {
      setFormData(prev => ({ ...prev, sourceDetails: {}, selectedTopic: '' }))
      setSelectedTopics([])
    }
  }

  const nextStep = () => {
    if (currentStep < 6) {
      setCurrentStep(currentStep + 1)
    }
  }

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const generateTopics = async () => {
    if (!formData.direction || !formData.source) {
      toast.error('Please select direction and source first')
      return
    }

    setIsLoadingTopics(true)
    try {
      const response = await apiClient.generateTopics({
        direction: formData.direction,
        source: formData.source,
        sourceDetails: {
          country: selectedCountry,
          query: googleSearchQuery
        }
      })
      
      setSelectedTopics(response.topics || [])
      toast.success('Topics generated successfully!')
    } catch (error) {
      toast.error('Failed to generate topics')
      console.error('Topic generation error:', error)
    } finally {
      setIsLoadingTopics(false)
    }
  }

  const generateContent = async () => {
    if (!isAuthenticated()) {
      toast.error(t('login_required'))
      router.push('/login')
      return
    }

    if (!formData.direction || !formData.platform || !formData.postType || !formData.source || !formData.selectedTopic || !formData.tone) {
      toast.error('Please fill in all required fields')
      return
    }

    setIsGenerating(true)
    try {
      const response = await apiClient.generateContent({
        ...formData,
        generate_images: true
      })
      setGeneratedContent(response.data)
      toast.success('Content generated successfully!')
    } catch (error) {
      toast.error(error.message || 'Generation failed')
      console.error('Generation error:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text)
      toast.success('Copied to clipboard!')
    } catch (error) {
      toast.error('Failed to copy')
    }
  }

  const downloadContent = () => {
    if (!generatedContent) return
    
    const content = `Content Creator Pro - Generated Content

Direction: ${contentDirections.find(d => d.key === formData.direction)?.name}
Platform: ${enhancedPlatforms.find(p => p.key === formData.platform)?.name}
Post Type: ${enhancedPlatforms.find(p => p.key === formData.platform)?.postTypes.find(pt => pt.key === formData.postType)?.name}
Topic: ${formData.selectedTopic}
Tone: ${tones.find(t => t.key === formData.tone)?.name}
Image Style: ${imageStyles.find(s => s.key === formData.imageStyle)?.name}

Content:
${generatedContent.content?.text || generatedContent.content}

Hashtags:
${generatedContent.content?.hashtags?.join(', ') || 'N/A'}

Generated on: ${new Date().toLocaleString()}
`

    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `content-${Date.now()}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    toast.success('Content downloaded!')
  }

  const regenerateContent = () => {
    setGeneratedContent(null)
    generateContent()
  }

  return (
    <>
      <Head>
        <title>AI Content Generator - Content Creator Pro</title>
        <meta name="description" content="Generate high-quality content with AI using DeepSeek and Stable Diffusion" />
      </Head>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              AI Content Generator
            </h1>
            <p className="text-xl text-gray-600">
              Create engaging content with DeepSeek AI and Stable Diffusion
            </p>
          </div>

          {/* Progress Steps */}
          <div className="flex justify-center mb-8">
            <div className="flex items-center space-x-4">
              {[1, 2, 3, 4].map((step) => (
                <div key={step} className="flex items-center">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold ${
                    step <= currentStep 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-200 text-gray-600'
                  }`}>
                    {step}
                  </div>
                  {step < 4 && (
                    <ChevronRight className={`w-6 h-6 mx-2 ${
                      step < currentStep ? 'text-blue-600' : 'text-gray-300'
                    }`} />
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Form Steps */}
          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            {currentStep === 1 && (
              <div>
                <h2 className="text-2xl font-bold mb-6">Choose Your Focus</h2>
                <p className="text-gray-600 mb-6">What niche, industry, or lifestyle interests you?</p>
                
                <div className="max-w-2xl">
                  <div className="mb-6">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Content Direction
                    </label>
                    <select
                      value={formData.direction}
                      onChange={(e) => handleInputChange('direction', e.target.value)}
                      className="w-full p-4 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-lg"
                    >
                      <option value="">Select your niche, industry, or lifestyle...</option>
                      {contentDirections.map((direction) => (
                        <option key={direction.key} value={direction.key}>
                          {direction.icon} {direction.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  {formData.direction && (
                    <div className="bg-gray-50 p-6 rounded-lg">
                      <h3 className="text-lg font-semibold mb-4">Categories:</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
                        <div>
                          <h4 className="font-medium mb-2">Interest-based:</h4>
                          <p>Gaming, Photography, Music, Art, Cooking...</p>
                        </div>
                        <div>
                          <h4 className="font-medium mb-2">Industry:</h4>
                          <p>Technology, Healthcare, Finance, Education, Marketing...</p>
                        </div>
                        <div>
                          <h4 className="font-medium mb-2">Lifestyle:</h4>
                          <p>Fitness, Travel, Parenting, Minimalism, Sustainability...</p>
                        </div>
                        <div>
                          <h4 className="font-medium mb-2">Professional:</h4>
                          <p>Entrepreneurship, Career Development, Leadership...</p>
                        </div>
                        <div>
                          <h4 className="font-medium mb-2">Creative:</h4>
                          <p>Design, Writing, Film, Fashion, Architecture...</p>
                        </div>
                        <div>
                          <h4 className="font-medium mb-2">Academic:</h4>
                          <p>Science, Research, Philosophy, History, Literature...</p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {currentStep === 2 && (
              <div>
                <h2 className="text-2xl font-bold mb-6">What Type of Content?</h2>
                <p className="text-gray-600 mb-6">Where will you share this content?</p>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
                  {enhancedPlatforms.map((platform) => (
                    <button
                      key={platform.key}
                      onClick={() => handleInputChange('platform', platform.key)}
                      className={`p-4 border-2 rounded-lg text-left transition-all duration-200 ${
                        formData.platform === platform.key
                          ? 'border-blue-600 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div className="text-2xl mb-2">{platform.icon}</div>
                      <div className="font-medium">{platform.name}</div>
                    </button>
                  ))}
                </div>

                {formData.platform && (
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Select Post Type</h3>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                      {enhancedPlatforms.find(p => p.key === formData.platform)?.postTypes.map((postType) => (
                        <button
                          key={postType.key}
                          onClick={() => handleInputChange('postType', postType.key)}
                          disabled={postType.disabled}
                          className={`p-3 border-2 rounded-lg transition-all duration-200 ${
                            formData.postType === postType.key
                              ? 'border-blue-600 bg-blue-50'
                              : 'border-gray-200 hover:border-gray-300'
                          } ${postType.disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
                        >
                          <div className="font-medium">{postType.name}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {currentStep === 3 && (
              <div>
                <h2 className="text-2xl font-bold mb-6">What Inspires You?</h2>
                <p className="text-gray-600 mb-6">Choose your content source (AI + Google will search based on your direction)</p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                  {enhancedSources.map((source) => (
                    <div
                      key={source.key}
                      className={`p-6 border-2 rounded-lg cursor-pointer transition-all duration-200 ${
                        formData.source === source.key
                          ? 'border-blue-600 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                      onClick={() => handleInputChange('source', source.key)}
                    >
                      <div className="flex items-center mb-3">
                        <div className="text-2xl mr-3">{source.icon}</div>
                        <div className="font-medium text-lg">{source.name}</div>
                      </div>
                      <p className="text-gray-600 text-sm">{source.description}</p>
                    </div>
                  ))}
                </div>

                {formData.source && (
                  <div className="bg-gray-50 p-6 rounded-lg">
                    <h3 className="text-lg font-semibold mb-4">Search Configuration</h3>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Search Query
                        </label>
                        <input
                          type="text"
                          value={googleSearchQuery}
                          onChange={(e) => setGoogleSearchQuery(e.target.value)}
                          placeholder="Enter your search query..."
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Country
                        </label>
                        <select
                          value={selectedCountry}
                          onChange={(e) => setSelectedCountry(e.target.value)}
                          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          {countries.map(country => (
                            <option key={country.code} value={country.code}>
                              {country.name}
                            </option>
                          ))}
                        </select>
                      </div>
                    </div>

                    <button
                      onClick={generateTopics}
                      disabled={isLoadingTopics}
                      className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-3 px-6 rounded-lg flex items-center justify-center gap-2 transition-all duration-200"
                    >
                      {isLoadingTopics ? (
                        <>
                          <RefreshCw className="w-5 h-5 animate-spin" />
                          Generating Topics...
                        </>
                      ) : (
                        <>
                          <Sparkles className="w-5 h-5" />
                          Generate Topics
                        </>
                      )}
                    </button>
                  </div>
                )}

                {selectedTopics.length > 0 && (
                  <div className="mt-6">
                    <h3 className="text-lg font-semibold mb-4">Generated Topics</h3>
                    <div className="grid grid-cols-1 gap-3">
                      {selectedTopics.map((topic, index) => (
                        <button
                          key={index}
                          onClick={() => handleInputChange('selectedTopic', topic.title)}
                          className={`p-4 border-2 rounded-lg text-left transition-all duration-200 ${
                            formData.selectedTopic === topic.title
                              ? 'border-blue-600 bg-blue-50'
                              : 'border-gray-200 hover:border-gray-300'
                          }`}
                        >
                          <div className="font-medium mb-1">{topic.title}</div>
                          <div className="text-sm text-gray-600">{topic.description}</div>
                          {topic.trending_score && (
                            <div className="text-xs text-blue-600 mt-2">
                              Trending Score: {topic.trending_score}
                            </div>
                          )}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {currentStep === 4 && (
              <div>
                <h2 className="text-2xl font-bold mb-6">How Should It Sound?</h2>
                <p className="text-gray-600 mb-6">Review your settings and generate your content</p>
                
                <div className="bg-gray-50 p-6 rounded-lg mb-6">
                  <h3 className="font-semibold mb-4">Your Settings</h3>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div><strong>Direction:</strong> {contentDirections.find(d => d.key === formData.direction)?.name}</div>
                    <div><strong>Platform:</strong> {enhancedPlatforms.find(p => p.key === formData.platform)?.name}</div>
                    <div><strong>Post Type:</strong> {enhancedPlatforms.find(p => p.key === formData.platform)?.postTypes.find(pt => pt.key === formData.postType)?.name}</div>
                    <div><strong>Source:</strong> {enhancedSources.find(s => s.key === formData.source)?.name}</div>
                    <div><strong>Selected Topic:</strong> {formData.selectedTopic}</div>
                    <div><strong>Language:</strong> {formData.language === 'en' ? 'English' : 'Chinese'}</div>
                  </div>
                </div>

                <div className="mb-6">
                  <h3 className="text-lg font-semibold mb-4">Select Tone</h3>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {tones.map((tone) => (
                      <button
                        key={tone.key}
                        onClick={() => handleInputChange('tone', tone.key)}
                        className={`p-4 border-2 rounded-lg transition-all duration-200 ${
                          formData.tone === tone.key
                            ? 'border-blue-600 bg-blue-50'
                            : 'border-gray-200 hover:border-gray-300'
                        }`}
                      >
                        <div className="font-medium mb-1">{tone.name}</div>
                      </button>
                    ))}
                  </div>
                </div>

                <button
                  onClick={generateContent}
                  disabled={isGenerating}
                  className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-4 px-8 rounded-lg flex items-center justify-center gap-2 transition-all duration-200"
                >
                  {isGenerating ? (
                    <>
                      <RefreshCw className="w-5 h-5 animate-spin" />
                      Generating Content...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-5 h-5" />
                      Generate Content
                    </>
                  )}
                </button>
              </div>
            )}

            {/* Navigation Buttons */}
            <div className="flex justify-between mt-8">
              <button
                onClick={prevStep}
                disabled={currentStep === 1}
                className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
              >
                Previous
              </button>
              
              {currentStep < 4 && (
                <button
                  onClick={nextStep}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all duration-200"
                >
                  Next
                </button>
              )}
            </div>
          </div>

          {/* Generated Content */}
          {generatedContent && (
            <div className="bg-white rounded-lg shadow-lg p-8">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold">Generated Content</h2>
                <div className="flex gap-2">
                  <button
                    onClick={() => copyToClipboard(generatedContent.content?.text || generatedContent.content)}
                    className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 flex items-center gap-2 transition-all duration-200"
                  >
                    <Copy className="w-4 h-4" />
                    Copy
                  </button>
                  <button
                    onClick={downloadContent}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center gap-2 transition-all duration-200"
                  >
                    <Download className="w-4 h-4" />
                    Download
                  </button>
                  <button
                    onClick={regenerateContent}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2 transition-all duration-200"
                  >
                    <RefreshCw className="w-4 h-4" />
                    Regenerate
                  </button>
                </div>
              </div>

              <div className="bg-gray-50 p-6 rounded-lg mb-6">
                <h3 className="font-semibold mb-4">Content</h3>
                <p className="text-gray-800 whitespace-pre-wrap">{generatedContent.content?.text || generatedContent.content}</p>
              </div>

              {generatedContent.content?.hashtags && generatedContent.content.hashtags.length > 0 && (
                <div className="mb-6">
                  <h3 className="font-semibold mb-4">Hashtags</h3>
                  <div className="flex flex-wrap gap-2">
                    {generatedContent.content.hashtags.map((hashtag, index) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                      >
                        #{hashtag}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {generatedContent.images && (
                <div className="mb-6">
                  <h3 className="font-semibold mb-4">Generated Images</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {generatedContent.images.primary && (
                      <div className="border rounded-lg p-4">
                        <h4 className="font-medium mb-2">Primary Image</h4>
                        <img 
                          src={`data:image/jpeg;base64,${generatedContent.images.primary}`} 
                          alt="Primary generated image"
                          className="w-full h-48 object-cover rounded-lg"
                        />
                      </div>
                    )}
                    {generatedContent.images.variations && generatedContent.images.variations.map((image, index) => (
                      <div key={index} className="border rounded-lg p-4">
                        <h4 className="font-medium mb-2">Variation {index + 1}</h4>
                        <img 
                          src={`data:image/jpeg;base64,${image}`} 
                          alt={`Generated image variation ${index + 1}`}
                          className="w-full h-48 object-cover rounded-lg"
                        />
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {generatedContent.analytics && (
                <div className="bg-blue-50 p-6 rounded-lg">
                  <h3 className="font-semibold mb-4">Analytics & Insights</h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <div className="font-medium">Engagement Score</div>
                      <div className="text-2xl font-bold text-blue-600">{generatedContent.analytics.engagement_score}%</div>
                    </div>
                    <div>
                      <div className="font-medium">Reach Potential</div>
                      <div className="text-lg font-semibold text-green-600">{generatedContent.analytics.reach_potential}</div>
                    </div>
                    <div>
                      <div className="font-medium">Best Time</div>
                      <div className="text-lg font-semibold text-purple-600">{generatedContent.analytics.optimal_posting_time}</div>
                    </div>
                    <div>
                      <div className="font-medium">Best Days</div>
                      <div className="text-lg font-semibold text-orange-600">{generatedContent.analytics.best_posting_days?.join(', ')}</div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </>
  )
} 