import { Copy, Download, Edit, Trash2, Share2 } from 'lucide-react'
import toast from 'react-hot-toast'

export default function ContentCard({ content, onEdit, onDelete, onShare }) {
  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text)
      toast.success('Copied to clipboard!')
    } catch (error) {
      toast.error('Failed to copy to clipboard')
    }
  }

  const downloadContent = () => {
    const contentText = `Content Creator Pro - Generated Content

Direction: ${content.direction || 'N/A'}
Platform: ${content.platform || 'N/A'}
Topic: ${content.topic || 'N/A'}
Tone: ${content.tone || 'N/A'}

Content:
${content.content}

Generated on: ${new Date().toLocaleString()}
`

    const blob = new Blob([contentText], { type: 'text/plain' })
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

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6 hover:shadow-lg transition-shadow duration-200">
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-1">
            {content.direction || 'Generated Content'}
          </h3>
          <div className="flex items-center space-x-4 text-sm text-gray-500">
            <span className="flex items-center">
              <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
              {content.platform || 'Platform'}
            </span>
            <span>{content.tone || 'Tone'}</span>
            <span>{new Date().toLocaleDateString()}</span>
          </div>
        </div>
        
        {/* Actions */}
        <div className="flex space-x-2">
          <button
            onClick={() => copyToClipboard(content.content)}
            className="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors duration-200"
            title="Copy content"
          >
            <Copy className="w-4 h-4" />
          </button>
          <button
            onClick={downloadContent}
            className="p-2 text-gray-500 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors duration-200"
            title="Download content"
          >
            <Download className="w-4 h-4" />
          </button>
          {onEdit && (
            <button
              onClick={() => onEdit(content)}
              className="p-2 text-gray-500 hover:text-yellow-600 hover:bg-yellow-50 rounded-lg transition-colors duration-200"
              title="Edit content"
            >
              <Edit className="w-4 h-4" />
            </button>
          )}
          {onShare && (
            <button
              onClick={() => onShare(content)}
              className="p-2 text-gray-500 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-colors duration-200"
              title="Share content"
            >
              <Share2 className="w-4 h-4" />
            </button>
          )}
          {onDelete && (
            <button
              onClick={() => onDelete(content.id)}
              className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors duration-200"
              title="Delete content"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="mb-4">
        <p className="text-gray-800 whitespace-pre-wrap leading-relaxed">
          {content.content}
        </p>
      </div>

      {/* Hashtags */}
      {content.hashtags && content.hashtags.length > 0 && (
        <div className="mb-4">
          <div className="flex flex-wrap gap-2">
            {content.hashtags.map((hashtag, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
              >
                #{hashtag}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="flex justify-between items-center pt-4 border-t border-gray-100">
        <div className="text-sm text-gray-500">
          {content.wordCount ? `${content.wordCount} words` : 'Generated content'}
        </div>
        <div className="text-sm text-gray-500">
          {content.language === 'zh' ? '中文' : 'English'}
        </div>
      </div>
    </div>
  )
} 