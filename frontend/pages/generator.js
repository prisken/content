import { useState } from 'react'
import Head from 'next/head'
import toast from 'react-hot-toast'
import { ChevronRight, Sparkles, Copy, Download, RefreshCw } from 'lucide-react'
import { apiClient, contentDirections, platforms } from '../lib/api'
import { useAuth } from '../contexts/AuthContext'
import { useLanguage } from '../contexts/LanguageContext'
import { useRouter } from 'next/router'

export default function Generator() {
  const [currentStep, setCurrentStep] = useState(1)
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedContent, setGeneratedContent] = useState(null)
  const { isAuthenticated } = useAuth()
  const { t } = useLanguage()
  const router = useRouter()
  
  const [formData, setFormData] = useState({
    direction: '',
    platform: '',
    source: '',
    topic: '',
    tone: '',
    language: 'en'
  })

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const nextStep = () => {
    if (currentStep < 5) {
      setCurrentStep(currentStep + 1)
    }
  }

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const generateContent = async () => {
    // Check if user is authenticated before generating content
    if (!isAuthenticated()) {
      toast.error(t('login_required'))
      router.push('/login')
      return
    }

    if (!formData.direction || !formData.platform || !formData.source || !formData.topic || !formData.tone) {
      toast.error(t('fill_all_fields'))
      return
    }

    setIsGenerating(true)
    try {
      const response = await apiClient.generateContent(formData)
      setGeneratedContent(response)
      toast.success(t('content_generated'))
    } catch (error) {
      toast.error(error.message || t('generation_failed'))
      console.error('Generation error:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text)
      toast.success(t('copied_to_clipboard'))
    } catch (error) {
      toast.error(t('copy_failed'))
    }
  }

  const downloadContent = () => {
    if (!generatedContent) return
    
    const content = `${t('content_creator_pro')} - ${t('generated_content')}

${t('direction')}: ${formData.direction}
${t('platform')}: ${formData.platform}
${t('topic')}: ${formData.topic}
${t('tone')}: ${formData.tone}

${t('content')}:
${generatedContent.content}

${t('hashtags')}:
${generatedContent.hashtags?.join(', ') || 'N/A'}

${t('generated_on')}: ${new Date().toLocaleString()}
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
    toast.success(t('content_downloaded'))
  }

  const regenerateContent = () => {
    setGeneratedContent(null)
    generateContent()
  }

  return (
    <>
      <Head>
        <title>{t('content_generator')} - Content Creator Pro</title>
        <meta name="description" content={t('generator_description')} />
      </Head>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              {t('content_generator')}
            </h1>
            <p className="text-xl text-gray-600">
              {t('generator_subtitle')}
            </p>
          </div>

          {/* Progress Steps */}
          <div className="flex justify-center mb-8">
            <div className="flex items-center space-x-4">
              {[1, 2, 3, 4, 5].map((step) => (
                <div key={step} className="flex items-center">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold ${
                    step <= currentStep 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-200 text-gray-600'
                  }`}>
                    {step}
                  </div>
                  {step < 5 && (
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
                <h2 className="text-2xl font-bold mb-6">{t('choose_direction')}</h2>
                <p className="text-gray-600 mb-6">{t('direction_description')}</p>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {contentDirections.map((direction) => (
                    <button
                      key={direction.key}
                      onClick={() => handleInputChange('direction', direction.key)}
                      className={`p-4 border-2 rounded-lg text-left transition-all duration-200 ${
                        formData.direction === direction.key
                          ? 'border-blue-600 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div className="text-2xl mb-2">{direction.icon}</div>
                      <div className="font-medium">{direction.name}</div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {currentStep === 2 && (
              <div>
                <h2 className="text-2xl font-bold mb-6">{t('choose_platform')}</h2>
                <p className="text-gray-600 mb-6">{t('platform_description')}</p>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {platforms.map((platform) => (
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
              </div>
            )}

            {currentStep === 3 && (
              <div>
                <h2 className="text-2xl font-bold mb-6">What Inspires You?</h2>
                <p className="text-gray-600 mb-6">Tell us what's driving your content creation</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {sources.map((source) => (
                    <button
                      key={source.key}
                      onClick={() => handleInputChange('source', source.key)}
                      className={`p-4 border-2 rounded-lg text-left transition-all duration-200 ${
                        formData.source === source.key
                          ? 'border-blue-600 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div className="font-medium">{source.name}</div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {currentStep === 4 && (
              <div>
                <h2 className="text-2xl font-bold mb-6">Select Topics & Tone</h2>
                <p className="text-gray-600 mb-6">Choose specific topics and tone for your content</p>
                
                <div className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Topic *
                    </label>
                    <input
                      type="text"
                      value={formData.topic}
                      onChange={(e) => handleInputChange('topic', e.target.value)}
                      placeholder="e.g., AI in Business, Digital Marketing Trends..."
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Tone *
                    </label>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                      {tones.map((tone) => (
                        <button
                          key={tone.key}
                          onClick={() => handleInputChange('tone', tone.key)}
                          className={`p-3 border-2 rounded-lg transition-all duration-200 ${
                            formData.tone === tone.key
                              ? 'border-blue-600 bg-blue-50'
                              : 'border-gray-200 hover:border-gray-300'
                          }`}
                        >
                          {tone.name}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Language
                    </label>
                    <select
                      value={formData.language}
                      onChange={(e) => handleInputChange('language', e.target.value)}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="en">English</option>
                      <option value="zh">中文 (Chinese)</option>
                    </select>
                  </div>
                </div>
              </div>
            )}

            {currentStep === 5 && (
              <div>
                <h2 className="text-2xl font-bold mb-6">Generate Content</h2>
                <p className="text-gray-600 mb-6">Review your settings and generate your content</p>
                
                <div className="bg-gray-50 p-6 rounded-lg mb-6">
                  <h3 className="font-semibold mb-4">Your Settings:</h3>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div><strong>Direction:</strong> {contentDirections.find(d => d.key === formData.direction)?.name}</div>
                    <div><strong>Platform:</strong> {platforms.find(p => p.key === formData.platform)?.name}</div>
                    <div><strong>Source:</strong> {sources.find(s => s.key === formData.source)?.name}</div>
                    <div><strong>Tone:</strong> {tones.find(t => t.key === formData.tone)?.name}</div>
                    <div><strong>Topic:</strong> {formData.topic}</div>
                    <div><strong>Language:</strong> {formData.language === 'en' ? 'English' : '中文'}</div>
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
                      Generating...
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
              
              {currentStep < 5 && (
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
                    onClick={() => copyToClipboard(generatedContent.content)}
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
                <h3 className="font-semibold mb-4">Content:</h3>
                <p className="text-gray-800 whitespace-pre-wrap">{generatedContent.content}</p>
              </div>

              {generatedContent.hashtags && generatedContent.hashtags.length > 0 && (
                <div>
                  <h3 className="font-semibold mb-4">Hashtags:</h3>
                  <div className="flex flex-wrap gap-2">
                    {generatedContent.hashtags.map((hashtag, index) => (
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
            </div>
          )}
        </div>
      </div>
    </>
  )
} 