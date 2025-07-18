import os
import requests
import json
from typing import Dict, List, Optional

class DeepSeekAIService:
    """Service for interacting with DeepSeek AI API"""
    
    def __init__(self):
        self.api_key = os.environ.get('DEEPSEEK_API_KEY')
        self.base_url = "https://api.deepseek.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_content(self, direction: str, platform: str, source: str, topic: str, tone: str, language: str = 'en') -> str:
        """Generate content using DeepSeek AI"""
        
        if not self.api_key:
            return self._fallback_content_generation(direction, platform, source, topic, tone, language)
        
        try:
            # Create a detailed prompt for better content generation
            prompt = self._create_content_prompt(direction, platform, source, topic, tone, language)
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a professional content creator specializing in social media content generation. Create engaging, platform-specific content that resonates with the target audience."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                return content
            else:
                print(f"DeepSeek API error: {response.status_code} - {response.text}")
                return self._fallback_content_generation(direction, platform, source, topic, tone, language)
                
        except Exception as e:
            print(f"Error calling DeepSeek API: {str(e)}")
            return self._fallback_content_generation(direction, platform, source, topic, tone, language)
    
    def _create_content_prompt(self, direction: str, platform: str, source: str, topic: str, tone: str, language: str) -> str:
        """Create a detailed prompt for content generation"""
        
        # Platform-specific guidelines
        platform_guidelines = {
            'linkedin': 'Professional tone, business-focused, include hashtags, 1300 characters max',
            'facebook': 'Engaging and conversational, encourage interaction, 632 characters max',
            'twitter': 'Concise and impactful, use hashtags strategically, 280 characters max',
            'instagram': 'Visual and engaging, use emojis, include call-to-action, 2200 characters max',
            'youtube': 'Detailed and informative, include timestamps if relevant, 5000 characters max',
            'blog': 'Comprehensive and well-structured, include headings, 2000+ words'
        }
        
        # Direction-specific context
        direction_context = {
            'business_finance': 'Focus on business insights, financial tips, market analysis, and professional growth',
            'technology': 'Cover tech trends, software development, AI, cybersecurity, and digital transformation',
            'health_wellness': 'Emphasize mental health, physical fitness, nutrition, and overall well-being',
            'education': 'Focus on learning strategies, skill development, and educational insights',
            'entertainment': 'Cover movies, music, gaming, and pop culture trends',
            'travel_tourism': 'Share travel tips, destination guides, and tourism insights',
            'food_cooking': 'Provide recipes, cooking tips, and culinary inspiration',
            'fashion_beauty': 'Cover style trends, beauty tips, and fashion advice',
            'sports_fitness': 'Focus on athletic performance, fitness tips, and sports analysis',
            'science_research': 'Share scientific discoveries, research findings, and innovation',
            'politics_news': 'Cover current events, political analysis, and news commentary',
            'environment': 'Focus on sustainability, environmental protection, and green living',
            'personal_dev': 'Emphasize self-improvement, productivity, and personal growth',
            'parenting_family': 'Share parenting tips, family activities, and child development',
            'art_creativity': 'Cover artistic inspiration, creative processes, and design trends',
            'real_estate': 'Focus on property market, investment advice, and real estate tips',
            'automotive': 'Cover car reviews, automotive technology, and driving tips',
            'pet_care': 'Share pet health, training tips, and pet lifestyle advice'
        }
        
        # Tone guidelines
        tone_guidelines = {
            'professional': 'Formal, authoritative, and business-focused',
            'casual': 'Friendly, conversational, and approachable',
            'enthusiastic': 'Energetic, positive, and motivating',
            'educational': 'Informative, clear, and instructional',
            'humorous': 'Witty, entertaining, and light-hearted'
        }
        
        # Language-specific instructions
        language_instruction = f"Write in {language.upper()} language." if language != 'en' else ""
        
        prompt = f"""
Create a {platform} post about "{topic}" in the {direction.replace('_', ' ')} category.

Platform Guidelines: {platform_guidelines.get(platform, 'Engaging and relevant content')}
Content Direction: {direction_context.get(direction, 'Professional and informative content')}
Tone: {tone_guidelines.get(tone, 'Professional and engaging')}
Source Inspiration: {source.replace('_', ' ')}
{language_instruction}

Requirements:
- Make it engaging and shareable
- Include relevant hashtags if appropriate for the platform
- Ensure it fits the platform's character limits
- Make it actionable and valuable to the audience
- Use the specified tone throughout

Generate the content now:
"""
        
        return prompt.strip()
    
    def _fallback_content_generation(self, direction: str, platform: str, source: str, topic: str, tone: str, language: str) -> str:
        """Fallback content generation when DeepSeek API is not available"""
        
        # Simple template-based content generation
        templates = {
            'linkedin': {
                'professional': f"🚀 {topic}\n\nBased on {source.replace('_', ' ')} insights, here's what you need to know about {direction.replace('_', ' ')}.\n\nKey takeaways:\n• [Insight 1]\n• [Insight 2]\n• [Insight 3]\n\nWhat's your experience with {topic}? Share your thoughts below! 👇\n\n#{direction.replace('_', '')} #{topic.replace(' ', '')} #ProfessionalDevelopment",
                'casual': f"Hey there! 👋\n\nQuick thought on {topic} - inspired by some great {source.replace('_', ' ')} content I've been consuming.\n\nHere's what I've learned:\n• [Learning 1]\n• [Learning 2]\n\nWhat do you think? Any tips to share? 🤔\n\n#{direction.replace('_', '')} #{topic.replace(' ', '')} #Learning"
            },
            'facebook': {
                'professional': f"📊 {topic} Update\n\nSharing insights from {source.replace('_', ' ')} about {direction.replace('_', ' ')}.\n\nKey points:\n• [Point 1]\n• [Point 2]\n\nWhat's your take on this? Comment below!\n\n#{direction.replace('_', '')} #{topic.replace(' ', '')}",
                'casual': f"Hey friends! 😊\n\nJust wanted to share some thoughts on {topic} that I picked up from {source.replace('_', ' ')}.\n\nHere's what caught my attention:\n• [Thought 1]\n• [Thought 2]\n\nAnyone else thinking about this? Let's discuss! 💬\n\n#{direction.replace('_', '')} #{topic.replace(' ', '')}"
            },
            'twitter': {
                'professional': f"💡 {topic}\n\nKey insights from {source.replace('_', ' ')}:\n\n• [Insight 1]\n• [Insight 2]\n\n#{direction.replace('_', '')} #{topic.replace(' ', '')}",
                'casual': f"🤔 {topic}\n\nJust learned from {source.replace('_', ' ')}:\n\n• [Learning 1]\n• [Learning 2]\n\nThoughts? #{direction.replace('_', '')} #{topic.replace(' ', '')}"
            }
        }
        
        # Get appropriate template
        platform_templates = templates.get(platform, templates['linkedin'])
        template = platform_templates.get(tone, platform_templates['professional'])
        
        # Replace placeholders with actual content
        content = template.replace('[Insight 1]', f'Understanding {topic} is crucial for success')
        content = content.replace('[Insight 2]', f'Focus on practical applications in {direction.replace("_", " ")}')
        content = content.replace('[Insight 3]', f'Continuous learning drives innovation')
        content = content.replace('[Learning 1]', f'There\'s always something new to discover about {topic}')
        content = content.replace('[Learning 2]', f'Community insights are invaluable')
        content = content.replace('[Point 1]', f'Current trends in {direction.replace("_", " ")}')
        content = content.replace('[Point 2]', f'Future implications for {topic}')
        content = content.replace('[Thought 1]', f'How {topic} affects our daily lives')
        content = content.replace('[Thought 2]', f'Ways to improve our approach to {direction.replace("_", " ")}')
        
        return content
    
    def generate_image_prompt(self, content: str, direction: str, platform: str) -> str:
        """Generate image prompt based on content and context"""
        
        if not self.api_key:
            return self._fallback_image_prompt(direction, platform)
        
        try:
            prompt = f"""
Based on this content: "{content[:200]}..."

Generate a detailed image prompt for a {platform} post in the {direction.replace('_', ' ')} category.

Requirements:
- Professional and visually appealing
- Suitable for {platform} dimensions
- Relevant to the content theme
- Include style, mood, and composition details
- Make it specific and actionable for image generation

Format: Describe the image in detail, including style, colors, composition, and mood.
"""
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert at creating detailed image prompts for social media content. Generate specific, actionable prompts that will create engaging visuals."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 300,
                "temperature": 0.8
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                image_prompt = result['choices'][0]['message']['content'].strip()
                return image_prompt
            else:
                return self._fallback_image_prompt(direction, platform)
                
        except Exception as e:
            print(f"Error generating image prompt: {str(e)}")
            return self._fallback_image_prompt(direction, platform)
    
    def _fallback_image_prompt(self, direction: str, platform: str) -> str:
        """Fallback image prompt generation"""
        
        direction_prompts = {
            'business_finance': 'professional business setting with charts, graphs, and modern office environment',
            'technology': 'futuristic digital interface with technology elements and innovation concepts',
            'health_wellness': 'clean, modern wellness setting with natural elements and healthy lifestyle imagery',
            'education': 'modern learning environment with books, technology, and educational materials',
            'entertainment': 'vibrant entertainment setting with media elements and creative atmosphere',
            'travel_tourism': 'beautiful travel destination with scenic landscapes and adventure elements',
            'food_cooking': 'appetizing food presentation with culinary elements and kitchen setting',
            'fashion_beauty': 'stylish fashion setting with modern aesthetics and beauty elements',
            'sports_fitness': 'dynamic sports environment with athletic equipment and fitness motivation',
            'science_research': 'scientific laboratory setting with research equipment and innovation',
            'politics_news': 'professional news setting with current events and political elements',
            'environment': 'natural environmental setting with sustainability and green living elements',
            'personal_dev': 'inspiring personal development setting with growth and motivation elements',
            'parenting_family': 'warm family setting with parenting elements and child-friendly environment',
            'art_creativity': 'creative artistic setting with artistic elements and creative inspiration',
            'real_estate': 'modern real estate setting with property elements and architectural design',
            'automotive': 'modern automotive setting with car elements and transportation technology',
            'pet_care': 'warm pet-friendly setting with animal care elements and pet lifestyle'
        }
        
        base_prompt = direction_prompts.get(direction, 'professional modern setting')
        
        platform_adjustments = {
            'linkedin': 'professional and corporate',
            'facebook': 'social and friendly',
            'instagram': 'visual and aesthetic',
            'twitter': 'clean and impactful',
            'youtube': 'dynamic and engaging',
            'blog': 'detailed and informative'
        }
        
        platform_style = platform_adjustments.get(platform, 'professional')
        
        return f"{platform_style} {base_prompt}, high quality, trending on artstation, 4k resolution"

# Global instance
ai_service = DeepSeekAIService() 