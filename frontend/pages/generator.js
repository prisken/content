import { useState, useEffect } from 'react'
import Head from 'next/head'
import toast from 'react-hot-toast'
import { ChevronRight, Sparkles, Copy, Download, RefreshCw, Search, Globe, TrendingUp, BookOpen, Youtube, Mic, Bot } from 'lucide-react'
import { apiClient, contentDirections, platforms, tones } from '../lib/api'
import { useAuth } from '../contexts/AuthContext'
import { useLanguage } from '../contexts/LanguageContext'
import { useRouter } from 'next/router'

// GeneratedImage component to handle image fetching
function GeneratedImage({ imageHash }) {
  const [imageData, setImageData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    const fetchImage = async () => {
      if (!imageHash || imageHash === 'generated') {
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        setError(false)
        
        // Fetch image data from the backend using the same API configuration
        const backendUrl = process.env.BACKEND_URL || 'https://content-contentmaker.up.railway.app'
        const response = await fetch(`${backendUrl}/api/image/${imageHash}`)
        
        if (!response.ok) {
          throw new Error('Failed to fetch image')
        }
        
        const data = await response.json()
        
        if (data.success && data.data?.image_data) {
          setImageData(data.data.image_data)
        } else {
          throw new Error('No image data received')
        }
      } catch (err) {
        console.error('Error fetching image:', err)
        setError(true)
      } finally {
        setLoading(false)
      }
    }

    fetchImage()
  }, [imageHash])

  if (loading) {
    return (
      <div className="w-full h-48 bg-gray-200 rounded-lg flex items-center justify-center">
        <RefreshCw className="w-6 h-6 animate-spin text-gray-500" />
      </div>
    )
  }

  if (error || !imageData) {
    return (
      <div className="w-full h-48 bg-gray-200 rounded-lg flex items-center justify-center text-gray-500">
        <div className="text-center">
          <div className="text-2xl mb-2">🖼️</div>
          <div className="text-sm">Image not available</div>
        </div>
      </div>
    )
  }

  return (
    <img 
      src={`data:image/jpeg;base64,${imageData}`} 
      alt="Generated image"
      className="w-full h-48 object-cover rounded-lg"
    />
  )
}

export default function Generator() {
  const [currentStep, setCurrentStep] = useState(1)
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedContent, setGeneratedContent] = useState(null)
  const [selectedTopics, setSelectedTopics] = useState([])
  const [isLoadingTopics, setIsLoadingTopics] = useState(false)
  const [googleSearchQuery, setGoogleSearchQuery] = useState('')
  const [selectedCountry, setSelectedCountry] = useState('US')
  const [selectedState, setSelectedState] = useState('')
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

  // Dynamic categories based on content direction
  const getCategoriesForDirection = (direction) => {
    const categories = {
      'business_finance': {
        'Interest-based': ['Entrepreneurship', 'Investment', 'Startups', 'Corporate Strategy', 'Financial Planning'],
        'Industry': ['Technology', 'Healthcare', 'Finance', 'Real Estate', 'Consulting'],
        'Lifestyle': ['Professional Development', 'Career Growth', 'Work-Life Balance', 'Leadership'],
        'Professional': ['Business Strategy', 'Market Analysis', 'Risk Management', 'Innovation']
      },
      'technology': {
        'Interest-based': ['Programming', 'AI/ML', 'Cybersecurity', 'Cloud Computing', 'Mobile Development'],
        'Industry': ['Software', 'Hardware', 'Fintech', 'Healthtech', 'Edtech'],
        'Lifestyle': ['Digital Nomad', 'Tech Culture', 'Remote Work', 'Digital Transformation'],
        'Professional': ['Software Engineering', 'Product Management', 'Data Science', 'DevOps']
      },
      'health_wellness': {
        'Interest-based': ['Fitness', 'Nutrition', 'Mental Health', 'Yoga', 'Meditation'],
        'Industry': ['Healthcare', 'Wellness', 'Fitness', 'Nutrition', 'Mental Health'],
        'Lifestyle': ['Healthy Living', 'Workout Routines', 'Mindfulness', 'Self-Care'],
        'Professional': ['Healthcare Professionals', 'Fitness Trainers', 'Nutritionists', 'Therapists']
      },
      'education': {
        'Interest-based': ['Online Learning', 'Skill Development', 'Academic Success', 'Lifelong Learning'],
        'Industry': ['Edtech', 'Training', 'Academic Institutions', 'Corporate Learning'],
        'Lifestyle': ['Student Life', 'Learning Habits', 'Study Techniques', 'Personal Growth'],
        'Professional': ['Teachers', 'Trainers', 'Educational Consultants', 'Curriculum Developers']
      },
      'entertainment': {
        'Interest-based': ['Movies', 'Music', 'Gaming', 'Streaming', 'Pop Culture'],
        'Industry': ['Film', 'Music', 'Gaming', 'Streaming Services', 'Entertainment'],
        'Lifestyle': ['Entertainment Culture', 'Fan Communities', 'Creative Expression', 'Social Media'],
        'Professional': ['Content Creators', 'Entertainment Professionals', 'Influencers', 'Artists']
      },
      'travel': {
        'Interest-based': ['Adventure Travel', 'Cultural Experiences', 'Budget Travel', 'Luxury Travel'],
        'Industry': ['Tourism', 'Hospitality', 'Travel Tech', 'Airlines', 'Hotels'],
        'Lifestyle': ['Digital Nomad', 'Travel Photography', 'Cultural Exchange', 'Sustainable Travel'],
        'Professional': ['Travel Agents', 'Tour Guides', 'Travel Writers', 'Hospitality Managers']
      },
      'food_cooking': {
        'Interest-based': ['Cooking', 'Baking', 'Food Photography', 'Recipe Development', 'Wine'],
        'Industry': ['Restaurants', 'Food Tech', 'Catering', 'Food Delivery', 'Agriculture'],
        'Lifestyle': ['Home Cooking', 'Food Culture', 'Healthy Eating', 'Culinary Adventures'],
        'Professional': ['Chefs', 'Food Bloggers', 'Restaurant Owners', 'Food Critics']
      },
      'fashion_beauty': {
        'Interest-based': ['Style', 'Makeup', 'Skincare', 'Fashion Trends', 'Sustainable Fashion'],
        'Industry': ['Fashion', 'Beauty', 'Retail', 'E-commerce', 'Luxury'],
        'Lifestyle': ['Personal Style', 'Beauty Routines', 'Fashion Culture', 'Body Positivity'],
        'Professional': ['Fashion Designers', 'Stylists', 'Beauty Influencers', 'Fashion Buyers']
      },
      'sports': {
        'Interest-based': ['Fitness', 'Athletics', 'Team Sports', 'Individual Sports', 'Sports Analysis'],
        'Industry': ['Sports', 'Fitness', 'Athletics', 'Sports Tech', 'Sports Media'],
        'Lifestyle': ['Active Living', 'Sports Culture', 'Fitness Motivation', 'Athletic Performance'],
        'Professional': ['Athletes', 'Coaches', 'Sports Analysts', 'Fitness Trainers']
      },
      'science_research': {
        'Interest-based': ['Scientific Discovery', 'Research', 'Innovation', 'Space', 'Climate'],
        'Industry': ['Research', 'Pharmaceuticals', 'Biotech', 'Aerospace', 'Environmental'],
        'Lifestyle': ['Science Communication', 'Research Culture', 'Innovation Mindset', 'Scientific Literacy'],
        'Professional': ['Researchers', 'Scientists', 'Lab Technicians', 'Science Communicators']
      },
      'politics_society': {
        'Interest-based': ['Current Events', 'Political Analysis', 'Social Issues', 'Policy', 'Activism'],
        'Industry': ['Government', 'Non-profits', 'Media', 'Think Tanks', 'Advocacy'],
        'Lifestyle': ['Civic Engagement', 'Social Awareness', 'Political Participation', 'Community Service'],
        'Professional': ['Politicians', 'Journalists', 'Policy Analysts', 'Activists']
      },
      'environment_sustainability': {
        'Interest-based': ['Climate Action', 'Sustainability', 'Conservation', 'Green Living', 'Renewable Energy'],
        'Industry': ['Environmental', 'Renewable Energy', 'Conservation', 'Green Tech', 'Sustainability'],
        'Lifestyle': ['Eco-friendly Living', 'Sustainable Choices', 'Environmental Awareness', 'Green Communities'],
        'Professional': ['Environmental Scientists', 'Sustainability Consultants', 'Conservationists', 'Green Entrepreneurs']
      },
      'lifestyle': {
        'Interest-based': ['Personal Development', 'Productivity', 'Mindfulness', 'Goal Setting', 'Habits'],
        'Industry': ['Coaching', 'Wellness', 'Personal Development', 'Productivity Tools', 'Lifestyle'],
        'Lifestyle': ['Self-Improvement', 'Work-Life Balance', 'Personal Growth', 'Lifestyle Design'],
        'Professional': ['Life Coaches', 'Productivity Experts', 'Wellness Consultants', 'Personal Development Trainers']
      },
      'parenting': {
        'Interest-based': ['Child Development', 'Parenting Tips', 'Family Activities', 'Education', 'Health'],
        'Industry': ['Education', 'Childcare', 'Family Services', 'Parenting Resources', 'Children\'s Products'],
        'Lifestyle': ['Family Life', 'Parenting Culture', 'Work-Life Balance', 'Family Traditions'],
        'Professional': ['Childcare Providers', 'Educators', 'Parenting Coaches', 'Family Therapists']
      },
      'art_creativity': {
        'Interest-based': ['Art', 'Design', 'Creative Process', 'Digital Art', 'Traditional Art'],
        'Industry': ['Creative Arts', 'Design', 'Advertising', 'Entertainment', 'Fashion'],
        'Lifestyle': ['Creative Expression', 'Artistic Culture', 'Design Thinking', 'Creative Communities'],
        'Professional': ['Artists', 'Designers', 'Creative Directors', 'Art Educators']
      },
      'real_estate': {
        'Interest-based': ['Property Investment', 'Home Buying', 'Real Estate Trends', 'Architecture', 'Interior Design'],
        'Industry': ['Real Estate', 'Construction', 'Property Management', 'Mortgage', 'Architecture'],
        'Lifestyle': ['Home Ownership', 'Property Culture', 'Investment Mindset', 'Home Improvement'],
        'Professional': ['Real Estate Agents', 'Property Developers', 'Architects', 'Mortgage Brokers']
      },
      'automotive': {
        'Interest-based': ['Car Reviews', 'Automotive Technology', 'Electric Vehicles', 'Car Culture', 'Driving'],
        'Industry': ['Automotive', 'Transportation', 'Electric Vehicles', 'Car Tech', 'Auto Services'],
        'Lifestyle': ['Car Enthusiasts', 'Driving Culture', 'Automotive Lifestyle', 'Vehicle Ownership'],
        'Professional': ['Automotive Engineers', 'Car Dealers', 'Mechanics', 'Automotive Journalists']
      },
      'pets_animals': {
        'Interest-based': ['Pet Care', 'Animal Welfare', 'Pet Training', 'Veterinary Care', 'Pet Products'],
        'Industry': ['Pet Care', 'Veterinary', 'Pet Products', 'Animal Welfare', 'Pet Services'],
        'Lifestyle': ['Pet Ownership', 'Animal Companionship', 'Pet Culture', 'Responsible Pet Care'],
        'Professional': ['Veterinarians', 'Pet Trainers', 'Animal Care Workers', 'Pet Product Developers']
      }
    }
    
    return categories[direction] || categories['business_finance']
  }

  // Countries for Google search - Comprehensive list including Hong Kong
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
    { code: 'MX', name: 'Mexico' },
    { code: 'HK', name: 'Hong Kong' },
    { code: 'CN', name: 'China' },
    { code: 'SG', name: 'Singapore' },
    { code: 'KR', name: 'South Korea' },
    { code: 'TW', name: 'Taiwan' },
    { code: 'TH', name: 'Thailand' },
    { code: 'VN', name: 'Vietnam' },
    { code: 'MY', name: 'Malaysia' },
    { code: 'ID', name: 'Indonesia' },
    { code: 'PH', name: 'Philippines' },
    { code: 'IT', name: 'Italy' },
    { code: 'ES', name: 'Spain' },
    { code: 'NL', name: 'Netherlands' },
    { code: 'SE', name: 'Sweden' },
    { code: 'NO', name: 'Norway' },
    { code: 'DK', name: 'Denmark' },
    { code: 'FI', name: 'Finland' },
    { code: 'CH', name: 'Switzerland' },
    { code: 'AT', name: 'Austria' },
    { code: 'BE', name: 'Belgium' },
    { code: 'IE', name: 'Ireland' },
    { code: 'NZ', name: 'New Zealand' },
    { code: 'ZA', name: 'South Africa' },
    { code: 'AR', name: 'Argentina' },
    { code: 'CL', name: 'Chile' },
    { code: 'CO', name: 'Colombia' },
    { code: 'PE', name: 'Peru' },
    { code: 'VE', name: 'Venezuela' },
    { code: 'RU', name: 'Russia' },
    { code: 'PL', name: 'Poland' },
    { code: 'CZ', name: 'Czech Republic' },
    { code: 'HU', name: 'Hungary' },
    { code: 'RO', name: 'Romania' },
    { code: 'BG', name: 'Bulgaria' },
    { code: 'HR', name: 'Croatia' },
    { code: 'SI', name: 'Slovenia' },
    { code: 'SK', name: 'Slovakia' },
    { code: 'LT', name: 'Lithuania' },
    { code: 'LV', name: 'Latvia' },
    { code: 'EE', name: 'Estonia' },
    { code: 'GR', name: 'Greece' },
    { code: 'PT', name: 'Portugal' },
    { code: 'TR', name: 'Turkey' },
    { code: 'IL', name: 'Israel' },
    { code: 'AE', name: 'United Arab Emirates' },
    { code: 'SA', name: 'Saudi Arabia' },
    { code: 'EG', name: 'Egypt' },
    { code: 'MA', name: 'Morocco' },
    { code: 'NG', name: 'Nigeria' },
    { code: 'KE', name: 'Kenya' },
    { code: 'GH', name: 'Ghana' },
    { code: 'UG', name: 'Uganda' },
    { code: 'TZ', name: 'Tanzania' },
    { code: 'ET', name: 'Ethiopia' },
    { code: 'DZ', name: 'Algeria' },
    { code: 'TN', name: 'Tunisia' },
    { code: 'LY', name: 'Libya' },
    { code: 'SD', name: 'Sudan' },
    { code: 'SS', name: 'South Sudan' },
    { code: 'CM', name: 'Cameroon' },
    { code: 'CI', name: 'Ivory Coast' },
    { code: 'SN', name: 'Senegal' },
    { code: 'ML', name: 'Mali' },
    { code: 'BF', name: 'Burkina Faso' },
    { code: 'NE', name: 'Niger' },
    { code: 'TD', name: 'Chad' },
    { code: 'CF', name: 'Central African Republic' },
    { code: 'CG', name: 'Republic of the Congo' },
    { code: 'CD', name: 'Democratic Republic of the Congo' },
    { code: 'AO', name: 'Angola' },
    { code: 'ZM', name: 'Zambia' },
    { code: 'ZW', name: 'Zimbabwe' },
    { code: 'BW', name: 'Botswana' },
    { code: 'NA', name: 'Namibia' },
    { code: 'SZ', name: 'Eswatini' },
    { code: 'LS', name: 'Lesotho' },
    { code: 'MG', name: 'Madagascar' },
    { code: 'MU', name: 'Mauritius' },
    { code: 'SC', name: 'Seychelles' },
    { code: 'KM', name: 'Comoros' },
    { code: 'DJ', name: 'Djibouti' },
    { code: 'SO', name: 'Somalia' },
    { code: 'ER', name: 'Eritrea' },
    { code: 'RW', name: 'Rwanda' },
    { code: 'BI', name: 'Burundi' },
    { code: 'MW', name: 'Malawi' },
    { code: 'MZ', name: 'Mozambique' },
    { code: 'ST', name: 'São Tomé and Príncipe' },
    { code: 'CV', name: 'Cape Verde' },
    { code: 'GW', name: 'Guinea-Bissau' },
    { code: 'GN', name: 'Guinea' },
    { code: 'SL', name: 'Sierra Leone' },
    { code: 'LR', name: 'Liberia' },
    { code: 'TG', name: 'Togo' },
    { code: 'BJ', name: 'Benin' },
    { code: 'GA', name: 'Gabon' },
    { code: 'GQ', name: 'Equatorial Guinea' },
    { code: 'GM', name: 'Gambia' },
    { code: 'MR', name: 'Mauritania' },
    { code: 'EH', name: 'Western Sahara' },
    { code: 'JO', name: 'Jordan' },
    { code: 'LB', name: 'Lebanon' },
    { code: 'SY', name: 'Syria' },
    { code: 'IQ', name: 'Iraq' },
    { code: 'IR', name: 'Iran' },
    { code: 'KW', name: 'Kuwait' },
    { code: 'QA', name: 'Qatar' },
    { code: 'BH', name: 'Bahrain' },
    { code: 'OM', name: 'Oman' },
    { code: 'YE', name: 'Yemen' },
    { code: 'AF', name: 'Afghanistan' },
    { code: 'PK', name: 'Pakistan' },
    { code: 'BD', name: 'Bangladesh' },
    { code: 'LK', name: 'Sri Lanka' },
    { code: 'NP', name: 'Nepal' },
    { code: 'BT', name: 'Bhutan' },
    { code: 'MV', name: 'Maldives' },
    { code: 'MM', name: 'Myanmar' },
    { code: 'LA', name: 'Laos' },
    { code: 'KH', name: 'Cambodia' },
    { code: 'MN', name: 'Mongolia' },
    { code: 'KZ', name: 'Kazakhstan' },
    { code: 'UZ', name: 'Uzbekistan' },
    { code: 'KG', name: 'Kyrgyzstan' },
    { code: 'TJ', name: 'Tajikistan' },
    { code: 'TM', name: 'Turkmenistan' },
    { code: 'AZ', name: 'Azerbaijan' },
    { code: 'GE', name: 'Georgia' },
    { code: 'AM', name: 'Armenia' },
    { code: 'BY', name: 'Belarus' },
    { code: 'MD', name: 'Moldova' },
    { code: 'UA', name: 'Ukraine' },
    { code: 'MK', name: 'North Macedonia' },
    { code: 'RS', name: 'Serbia' },
    { code: 'ME', name: 'Montenegro' },
    { code: 'BA', name: 'Bosnia and Herzegovina' },
    { code: 'AL', name: 'Albania' },
    { code: 'XK', name: 'Kosovo' },
    { code: 'MT', name: 'Malta' },
    { code: 'CY', name: 'Cyprus' },
    { code: 'IS', name: 'Iceland' },
    { code: 'LU', name: 'Luxembourg' },
    { code: 'LI', name: 'Liechtenstein' },
    { code: 'MC', name: 'Monaco' },
    { code: 'SM', name: 'San Marino' },
    { code: 'VA', name: 'Vatican City' },
    { code: 'AD', name: 'Andorra' },
    { code: 'GI', name: 'Gibraltar' },
    { code: 'FO', name: 'Faroe Islands' },
    { code: 'GL', name: 'Greenland' },
    { code: 'AX', name: 'Åland Islands' },
    { code: 'SJ', name: 'Svalbard and Jan Mayen' },
    { code: 'BV', name: 'Bouvet Island' },
    { code: 'TF', name: 'French Southern Territories' },
    { code: 'HM', name: 'Heard Island and McDonald Islands' },
    { code: 'AQ', name: 'Antarctica' },
    { code: 'FK', name: 'Falkland Islands' },
    { code: 'GS', name: 'South Georgia and the South Sandwich Islands' },
    { code: 'IO', name: 'British Indian Ocean Territory' },
    { code: 'PN', name: 'Pitcairn' },
    { code: 'CK', name: 'Cook Islands' },
    { code: 'NU', name: 'Niue' },
    { code: 'TK', name: 'Tokelau' },
    { code: 'WS', name: 'Samoa' },
    { code: 'TO', name: 'Tonga' },
    { code: 'FJ', name: 'Fiji' },
    { code: 'NC', name: 'New Caledonia' },
    { code: 'VU', name: 'Vanuatu' },
    { code: 'SB', name: 'Solomon Islands' },
    { code: 'PG', name: 'Papua New Guinea' },
    { code: 'KI', name: 'Kiribati' },
    { code: 'TV', name: 'Tuvalu' },
    { code: 'NR', name: 'Nauru' },
    { code: 'PW', name: 'Palau' },
    { code: 'MH', name: 'Marshall Islands' },
    { code: 'FM', name: 'Micronesia' },
    { code: 'GU', name: 'Guam' },
    { code: 'MP', name: 'Northern Mariana Islands' },
    { code: 'AS', name: 'American Samoa' },
    { code: 'PF', name: 'French Polynesia' },
    { code: 'WF', name: 'Wallis and Futuna' },
    { code: 'TK', name: 'Tokelau' },
    { code: 'NU', name: 'Niue' },
    { code: 'CK', name: 'Cook Islands' },
    { code: 'PN', name: 'Pitcairn' },
    { code: 'IO', name: 'British Indian Ocean Territory' },
    { code: 'GS', name: 'South Georgia and the South Sandwich Islands' },
    { code: 'FK', name: 'Falkland Islands' },
    { code: 'AQ', name: 'Antarctica' },
    { code: 'HM', name: 'Heard Island and McDonald Islands' },
    { code: 'TF', name: 'French Southern Territories' },
    { code: 'BV', name: 'Bouvet Island' },
    { code: 'SJ', name: 'Svalbard and Jan Mayen' },
    { code: 'AX', name: 'Åland Islands' },
    { code: 'GL', name: 'Greenland' },
    { code: 'FO', name: 'Faroe Islands' },
    { code: 'GI', name: 'Gibraltar' },
    { code: 'AD', name: 'Andorra' },
    { code: 'VA', name: 'Vatican City' },
    { code: 'SM', name: 'San Marino' },
    { code: 'MC', name: 'Monaco' },
    { code: 'LI', name: 'Liechtenstein' },
    { code: 'LU', name: 'Luxembourg' },
    { code: 'IS', name: 'Iceland' },
    { code: 'CY', name: 'Cyprus' },
    { code: 'MT', name: 'Malta' },
    { code: 'XK', name: 'Kosovo' },
    { code: 'AL', name: 'Albania' },
    { code: 'BA', name: 'Bosnia and Herzegovina' },
    { code: 'ME', name: 'Montenegro' },
    { code: 'RS', name: 'Serbia' },
    { code: 'MK', name: 'North Macedonia' },
    { code: 'UA', name: 'Ukraine' },
    { code: 'MD', name: 'Moldova' },
    { code: 'BY', name: 'Belarus' },
    { code: 'AM', name: 'Armenia' },
    { code: 'GE', name: 'Georgia' },
    { code: 'AZ', name: 'Azerbaijan' },
    { code: 'TM', name: 'Turkmenistan' },
    { code: 'TJ', name: 'Tajikistan' },
    { code: 'KG', name: 'Kyrgyzstan' },
    { code: 'UZ', name: 'Uzbekistan' },
    { code: 'KZ', name: 'Kazakhstan' },
    { code: 'MN', name: 'Mongolia' },
    { code: 'KH', name: 'Cambodia' },
    { code: 'LA', name: 'Laos' },
    { code: 'MM', name: 'Myanmar' },
    { code: 'MV', name: 'Maldives' },
    { code: 'BT', name: 'Bhutan' },
    { code: 'NP', name: 'Nepal' },
    { code: 'LK', name: 'Sri Lanka' },
    { code: 'BD', name: 'Bangladesh' },
    { code: 'PK', name: 'Pakistan' },
    { code: 'AF', name: 'Afghanistan' },
    { code: 'YE', name: 'Yemen' },
    { code: 'OM', name: 'Oman' },
    { code: 'BH', name: 'Bahrain' },
    { code: 'QA', name: 'Qatar' },
    { code: 'KW', name: 'Kuwait' },
    { code: 'IR', name: 'Iran' },
    { code: 'IQ', name: 'Iraq' },
    { code: 'SY', name: 'Syria' },
    { code: 'LB', name: 'Lebanon' },
    { code: 'JO', name: 'Jordan' },
    { code: 'EH', name: 'Western Sahara' },
    { code: 'MR', name: 'Mauritania' },
    { code: 'GM', name: 'Gambia' },
    { code: 'GQ', name: 'Equatorial Guinea' },
    { code: 'GA', name: 'Gabon' },
    { code: 'BJ', name: 'Benin' },
    { code: 'TG', name: 'Togo' },
    { code: 'LR', name: 'Liberia' },
    { code: 'SL', name: 'Sierra Leone' },
    { code: 'GN', name: 'Guinea' },
    { code: 'GW', name: 'Guinea-Bissau' },
    { code: 'CV', name: 'Cape Verde' },
    { code: 'ST', name: 'São Tomé and Príncipe' },
    { code: 'MZ', name: 'Mozambique' },
    { code: 'MW', name: 'Malawi' },
    { code: 'BI', name: 'Burundi' },
    { code: 'RW', name: 'Rwanda' },
    { code: 'ER', name: 'Eritrea' },
    { code: 'SO', name: 'Somalia' },
    { code: 'DJ', name: 'Djibouti' },
    { code: 'KM', name: 'Comoros' },
    { code: 'SC', name: 'Seychelles' },
    { code: 'MU', name: 'Mauritius' },
    { code: 'MG', name: 'Madagascar' },
    { code: 'LS', name: 'Lesotho' },
    { code: 'SZ', name: 'Eswatini' },
    { code: 'NA', name: 'Namibia' },
    { code: 'BW', name: 'Botswana' },
    { code: 'ZW', name: 'Zimbabwe' },
    { code: 'ZM', name: 'Zambia' },
    { code: 'AO', name: 'Angola' },
    { code: 'CD', name: 'Democratic Republic of the Congo' },
    { code: 'CG', name: 'Republic of the Congo' },
    { code: 'CF', name: 'Central African Republic' },
    { code: 'TD', name: 'Chad' },
    { code: 'NE', name: 'Niger' },
    { code: 'BF', name: 'Burkina Faso' },
    { code: 'ML', name: 'Mali' },
    { code: 'SN', name: 'Senegal' },
    { code: 'CI', name: 'Ivory Coast' },
    { code: 'CM', name: 'Cameroon' },
    { code: 'SS', name: 'South Sudan' },
    { code: 'SD', name: 'Sudan' },
    { code: 'LY', name: 'Libya' },
    { code: 'TN', name: 'Tunisia' },
    { code: 'DZ', name: 'Algeria' },
    { code: 'ET', name: 'Ethiopia' },
    { code: 'TZ', name: 'Tanzania' },
    { code: 'UG', name: 'Uganda' },
    { code: 'GH', name: 'Ghana' },
    { code: 'KE', name: 'Kenya' },
    { code: 'NG', name: 'Nigeria' },
    { code: 'MA', name: 'Morocco' },
    { code: 'EG', name: 'Egypt' },
    { code: 'SA', name: 'Saudi Arabia' },
    { code: 'AE', name: 'United Arab Emirates' },
    { code: 'IL', name: 'Israel' },
    { code: 'TR', name: 'Turkey' },
    { code: 'PT', name: 'Portugal' },
    { code: 'GR', name: 'Greece' },
    { code: 'EE', name: 'Estonia' },
    { code: 'LV', name: 'Latvia' },
    { code: 'LT', name: 'Lithuania' },
    { code: 'SK', name: 'Slovakia' },
    { code: 'SI', name: 'Slovenia' },
    { code: 'HR', name: 'Croatia' },
    { code: 'BG', name: 'Bulgaria' },
    { code: 'RO', name: 'Romania' },
    { code: 'HU', name: 'Hungary' },
    { code: 'CZ', name: 'Czech Republic' },
    { code: 'PL', name: 'Poland' },
    { code: 'RU', name: 'Russia' },
    { code: 'VE', name: 'Venezuela' },
    { code: 'PE', name: 'Peru' },
    { code: 'CO', name: 'Colombia' },
    { code: 'CL', name: 'Chile' },
    { code: 'AR', name: 'Argentina' },
    { code: 'ZA', name: 'South Africa' },
    { code: 'NZ', name: 'New Zealand' },
    { code: 'IE', name: 'Ireland' },
    { code: 'BE', name: 'Belgium' },
    { code: 'AT', name: 'Austria' },
    { code: 'CH', name: 'Switzerland' },
    { code: 'FI', name: 'Finland' },
    { code: 'DK', name: 'Denmark' },
    { code: 'NO', name: 'Norway' },
    { code: 'SE', name: 'Sweden' },
    { code: 'NL', name: 'Netherlands' },
    { code: 'ES', name: 'Spain' },
    { code: 'IT', name: 'Italy' },
    { code: 'PH', name: 'Philippines' },
    { code: 'ID', name: 'Indonesia' },
    { code: 'MY', name: 'Malaysia' },
    { code: 'VN', name: 'Vietnam' },
    { code: 'TH', name: 'Thailand' },
    { code: 'TW', name: 'Taiwan' },
    { code: 'KR', name: 'South Korea' },
    { code: 'SG', name: 'Singapore' },
    { code: 'CN', name: 'China' },
    { code: 'HK', name: 'Hong Kong' }
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
    if (currentStep < 5) {
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
                        {Object.entries(getCategoriesForDirection(formData.direction)).map(([category, items]) => (
                          <div key={category}>
                            <h4 className="font-medium mb-2">{category}:</h4>
                            <p>{items.join(', ')}</p>
                          </div>
                        ))}
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
                          <div className="flex justify-between items-center mt-2">
                            <div className="text-xs text-green-600">
                              Source: {enhancedSources.find(s => s.key === formData.source)?.name}
                            </div>
                            {topic.trending_score && (
                              <div className="text-xs text-blue-600">
                                Trending Score: {topic.trending_score}
                              </div>
                            )}
                          </div>
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
                <p className="text-gray-600 mb-6">Choose the tone for your content</p>
                
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
                        <div className="text-2xl mb-2">{tone.icon}</div>
                        <div className="font-medium">{tone.name}</div>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {currentStep === 5 && (
              <div>
                <h2 className="text-2xl font-bold mb-6">Choose Image Style</h2>
                <p className="text-gray-600 mb-6">Select the visual style for your generated images</p>
                
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
                  {imageStyles.map((style) => (
                    <button
                      key={style.key}
                      onClick={() => handleInputChange('imageStyle', style.key)}
                      className={`p-4 border-2 rounded-lg text-left transition-all duration-200 ${
                        formData.imageStyle === style.key
                          ? 'border-blue-600 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div className="text-2xl mb-2">{style.icon}</div>
                      <div className="font-medium mb-1">{style.name}</div>
                      <div className="text-sm text-gray-600">{style.description}</div>
                    </button>
                  ))}
                </div>

                <div className="bg-gray-50 p-6 rounded-lg mb-6">
                  <h3 className="font-semibold mb-4">Your Settings</h3>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div><strong>Direction:</strong> {contentDirections.find(d => d.key === formData.direction)?.name}</div>
                    <div><strong>Platform:</strong> {enhancedPlatforms.find(p => p.key === formData.platform)?.name}</div>
                    <div><strong>Post Type:</strong> {enhancedPlatforms.find(p => p.key === formData.platform)?.postTypes.find(pt => pt.key === formData.postType)?.name}</div>
                    <div><strong>Source:</strong> {enhancedSources.find(s => s.key === formData.source)?.name}</div>
                    <div><strong>Selected Topic:</strong> {formData.selectedTopic}</div>
                    <div><strong>Tone:</strong> {tones.find(t => t.key === formData.tone)?.name}</div>
                    <div><strong>Image Style:</strong> {imageStyles.find(s => s.key === formData.imageStyle)?.name}</div>
                    <div><strong>Language:</strong> {formData.language === 'en' ? 'English' : 'Chinese'}</div>
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
                        <GeneratedImage imageHash={generatedContent.images.primary} />
                      </div>
                    )}
                    {generatedContent.images.variations && generatedContent.images.variations.map((image, index) => (
                      <div key={index} className="border rounded-lg p-4">
                        <h4 className="font-medium mb-2">Variation {index + 1}</h4>
                        <GeneratedImage imageHash={image} />
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