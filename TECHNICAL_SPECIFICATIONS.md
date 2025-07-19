# Technical Specifications - Content Generation API

## Overview
This document provides detailed technical specifications for the Content Creator Pro API, including request/response formats, platform-specific configurations, and integration details.

---

## 🔌 **API Endpoints**

### **Base URL**
```
Production: https://your-backend-url.com
Development: http://localhost:8000
```

### **Content Generation Endpoint**
```
POST /api/generate
```

---

## 📤 **Request Format**

### **Standard Request Body**
```json
{
  "content_direction": "business_finance",
  "content_type": "linkedin",
  "source_type": "industry_trends",
  "specific_content": "AI in business transformation",
  "tone": "professional",
  "region": "global",
  "language": "en",
  "user_id": "user123"
}
```

### **Field Descriptions**

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `content_direction` | string | Yes | Content category/industry | `"business_finance"` |
| `content_type` | string | Yes | Target platform | `"linkedin"` |
| `source_type` | string | Yes | Content inspiration source | `"industry_trends"` |
| `specific_content` | string | Yes | Main topic/content focus | `"AI in business transformation"` |
| `tone` | string | Yes | Content tone/style | `"professional"` |
| `region` | string | No | Geographic region | `"global"` |
| `language` | string | No | Content language | `"en"` |
| `user_id` | string | No | User identifier | `"user123"` |

---

## 📥 **Response Format**

### **Standard Response Body**
```json
{
  "content": "Generated content text...",
  "variations": [
    "Alternative version 1...",
    "Alternative version 2...",
    "Alternative version 3..."
  ],
  "media_suggestions": [
    "Professional headshot",
    "Infographic with key statistics",
    "Team collaboration image"
  ],
  "cultural_context": {
    "region": "global",
    "sensitivity_notes": "Universal business content"
  },
  "direction_context": {
    "direction_name": "Business & Finance",
    "language_style": "Professional and authoritative",
    "hashtags": ["#Business", "#Finance", "#Leadership"],
    "subcategories": ["Entrepreneurship", "Investment", "Management"]
  },
  "content_type": "linkedin",
  "max_length": 1300,
  "generated_at": "2024-01-15T10:30:00Z"
}
```

---

## 🎯 **Platform-Specific Configurations**

### **LinkedIn Configuration**
```python
{
    'max_length': 1300,
    'template': """Create a professional LinkedIn post based on: {source_data}
Requirements:
- Length: 1,300 characters max
- Tone: {tone}
- Include 1-2 relevant hashtags
- Focus on thought leadership and insights
- Regional Context: {region}
- Direction Focus: {content_direction}
- Language: {language}
- Professional and authoritative tone
- Include a call-to-action for engagement"""
}
```

### **Facebook Configuration**
```python
{
    'max_length': 63206,
    'template': """Create an engaging Facebook post based on: {source_data}
Requirements:
- Length: 40-80 words optimal
- Tone: {tone}
- Include 3-5 relevant hashtags
- Focus on community and connection
- Regional Context: {region}
- Direction Focus: {content_direction}
- Language: {language}
- Conversational and relatable tone
- Encourage comments and discussion"""
}
```

### **Instagram Configuration**
```python
{
    'max_length': 2200,
    'template': """Create an engaging Instagram caption based on: {source_data}
Requirements:
- Length: 2,200 characters max
- Tone: {tone}
- Include 5-10 relevant hashtags
- Focus on visual storytelling
- Regional Context: {region}
- Direction Focus: {content_direction}
- Language: {language}
- Visual and inspirational tone
- Include emojis and aesthetic language"""
}
```

### **Twitter Configuration**
```python
{
    'max_length': 280,
    'template': """Create a concise Twitter post based on: {source_data}
Requirements:
- Length: 280 characters max
- Tone: {tone}
- Include 1-2 relevant hashtags
- Focus on trending and engaging
- Regional Context: {region}
- Direction Focus: {content_direction}
- Language: {language}
- Concise and impactful tone
- Encourage retweets and engagement"""
}
```

### **YouTube Shorts Configuration**
```python
{
    'max_length': 200,
    'template': """Create a YouTube Shorts script based on: {source_data}
Requirements:
- Length: 30-45 seconds (150-200 words)
- Tone: {tone}
- Focus on educational and engaging
- Regional Context: {region}
- Direction Focus: {content_direction}
- Language: {language}
- Hook in first 3 seconds
- Structure: Problem → Solution → Call to Action
- Include clear voiceover instructions"""
}
```

### **Blog Configuration**
```python
{
    'max_length': 2500,
    'template': """Create a comprehensive blog article based on: {source_data}
Requirements:
- Length: 1,500-2,500 words
- Tone: {tone}
- Focus on SEO and value
- Regional Context: {region}
- Direction Focus: {content_direction}
- Language: {language}
- Structure: Introduction + Body + Conclusion
- Include headings and subheadings
- SEO-optimized with relevant keywords
- Provide actionable insights and value"""
}
```

---

## 🎨 **Content Direction Mappings**

### **Available Directions**
```python
content_directions = [
    {'key': 'business_finance', 'name': 'Business & Finance', 'icon': '💼'},
    {'key': 'technology', 'name': 'Technology', 'icon': '💻'},
    {'key': 'health_wellness', 'name': 'Health & Wellness', 'icon': '🏥'},
    {'key': 'education', 'name': 'Education', 'icon': '📚'},
    {'key': 'entertainment', 'name': 'Entertainment', 'icon': '🎬'},
    {'key': 'travel_tourism', 'name': 'Travel & Tourism', 'icon': '✈️'},
    {'key': 'food_cooking', 'name': 'Food & Cooking', 'icon': '🍳'},
    {'key': 'fashion_beauty', 'name': 'Fashion & Beauty', 'icon': '👗'},
    {'key': 'sports_fitness', 'name': 'Sports & Fitness', 'icon': '⚽'},
    {'key': 'science_research', 'name': 'Science & Research', 'icon': '🔬'},
    {'key': 'politics_current_events', 'name': 'Politics & Current Events', 'icon': '📰'},
    {'key': 'environment_sustainability', 'name': 'Environment & Sustainability', 'icon': '🌱'},
    {'key': 'personal_development', 'name': 'Personal Development', 'icon': '🧠'},
    {'key': 'parenting_family', 'name': 'Parenting & Family', 'icon': '👨‍👩‍👧‍👦'},
    {'key': 'art_creativity', 'name': 'Art & Creativity', 'icon': '🎨'},
    {'key': 'real_estate', 'name': 'Real Estate', 'icon': '🏠'},
    {'key': 'automotive', 'name': 'Automotive', 'icon': '🚗'},
    {'key': 'pet_care', 'name': 'Pet Care', 'icon': '🐕'}
]
```

### **Direction-Specific Contexts**
```python
direction_contexts = {
    'business_finance': {
        'language_style': 'Professional and authoritative',
        'hashtags': ['#Business', '#Finance', '#Leadership', '#Entrepreneurship'],
        'subcategories': ['Entrepreneurship', 'Investment', 'Management', 'Strategy']
    },
    'technology': {
        'language_style': 'Innovative and forward-thinking',
        'hashtags': ['#Tech', '#Innovation', '#AI', '#DigitalTransformation'],
        'subcategories': ['AI/ML', 'Software', 'Hardware', 'Cybersecurity']
    }
    # ... additional directions
}
```

---

## 🎭 **Tone Configurations**

### **Available Tones**
```python
tones = [
    {'key': 'professional', 'name': 'Professional'},
    {'key': 'casual', 'name': 'Casual'},
    {'key': 'inspirational', 'name': 'Inspirational'},
    {'key': 'educational', 'name': 'Educational'},
    {'key': 'entertaining', 'name': 'Entertaining'}
]
```

### **Tone-Specific Instructions**
```python
tone_instructions = {
    'professional': 'Use formal language, industry terminology, authoritative voice',
    'casual': 'Use conversational language, relatable examples, friendly tone',
    'inspirational': 'Use motivational language, uplifting stories, encouraging voice',
    'educational': 'Use clear explanations, step-by-step guidance, helpful tone',
    'entertaining': 'Use humor, engaging stories, fun and lighthearted tone'
}
```

---

## 📊 **Source Type Configurations**

### **Available Sources**
```python
sources = [
    {'key': 'personal_experience', 'name': 'Personal Experience'},
    {'key': 'industry_trends', 'name': 'Industry Trends'},
    {'key': 'customer_feedback', 'name': 'Customer Feedback'},
    {'key': 'market_research', 'name': 'Market Research'},
    {'key': 'competitor_analysis', 'name': 'Competitor Analysis'},
    {'key': 'expert_interviews', 'name': 'Expert Interviews'},
    {'key': 'case_studies', 'name': 'Case Studies'},
    {'key': 'data_analytics', 'name': 'Data Analytics'},
    {'key': 'trending_topics', 'name': 'Trending Topics'},
    {'key': 'seasonal_events', 'name': 'Seasonal Events'}
]
```

---

## 🌍 **Regional and Language Support**

### **Supported Languages**
```python
supported_languages = {
    'en': 'English',
    'zh': 'Chinese (中文)'
}
```

### **Regional Contexts**
```python
regional_contexts = {
    'global': 'Universal content suitable for international audience',
    'north_america': 'US/Canada specific cultural references and terminology',
    'europe': 'European market focus with regional considerations',
    'asia_pacific': 'APAC region focus with cultural sensitivity'
}
```

---

## 🔧 **AI Integration**

### **DeepSeek AI Configuration**
```python
ai_config = {
    'api_base': 'https://api.deepseek.com',
    'model': 'deepseek-chat',
    'max_tokens': 2000,
    'temperature': 0.7,
    'top_p': 0.9,
    'timeout': 30
}
```

### **Prompt Engineering**
```python
system_prompt = """You are a professional content creator specializing in social media and blog content. Generate high-quality, engaging content that follows the provided specifications exactly."""
```

---

## 📈 **Content Validation**

### **Platform-Specific Validation Rules**
```python
validation_rules = {
    'linkedin': {
        'max_length': 1300,
        'hashtag_limit': 2,
        'tone_requirements': ['professional', 'authoritative']
    },
    'facebook': {
        'max_length': 63206,
        'optimal_length': '40-80 words',
        'hashtag_limit': 5,
        'tone_requirements': ['conversational', 'relatable']
    },
    'instagram': {
        'max_length': 2200,
        'hashtag_minimum': 5,
        'hashtag_maximum': 10,
        'tone_requirements': ['visual', 'inspirational']
    },
    'twitter': {
        'max_length': 280,
        'hashtag_limit': 2,
        'tone_requirements': ['concise', 'impactful']
    },
    'youtube_shorts': {
        'max_length': 200,
        'duration': '30-45 seconds',
        'structure': 'Problem → Solution → Call to Action'
    },
    'blog': {
        'min_length': 1500,
        'max_length': 2500,
        'structure': 'Introduction + Body + Conclusion'
    }
}
```

---

## 🚨 **Error Handling**

### **Common Error Responses**
```json
{
  "error": "Validation failed",
  "details": {
    "field": "content_type",
    "message": "Unsupported content type: invalid_platform"
  },
  "status_code": 400
}
```

### **Error Codes**
- `400` - Bad Request (Invalid parameters)
- `401` - Unauthorized (Missing/invalid API key)
- `422` - Validation Error (Content validation failed)
- `500` - Internal Server Error (AI service unavailable)
- `503` - Service Unavailable (Rate limiting)

---

## 📊 **Rate Limiting**

### **Limits**
- **Free Tier**: 10 requests/hour
- **Pro Tier**: 100 requests/hour
- **Enterprise**: Custom limits

### **Headers**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642233600
```

---

## 🔐 **Authentication**

### **API Key Authentication**
```http
Authorization: Bearer your-api-key-here
Content-Type: application/json
```

### **User Context Headers**
```http
X-User-Email: user@example.com
X-User-Role: admin
```

---

## 📝 **Example Implementations**

### **JavaScript/Node.js**
```javascript
const generateContent = async (data) => {
  const response = await fetch('/api/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    },
    body: JSON.stringify(data)
  });
  
  return response.json();
};
```

### **Python**
```python
import requests

def generate_content(data, api_key):
    response = requests.post(
        'https://api.example.com/generate',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        },
        json=data
    )
    return response.json()
```

### **cURL**
```bash
curl -X POST https://api.example.com/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "content_direction": "business_finance",
    "content_type": "linkedin",
    "source_type": "industry_trends",
    "specific_content": "AI in business transformation",
    "tone": "professional",
    "language": "en"
  }'
```

---

*This technical specification is maintained by Content Creator Pro and updated with each API version release.* 