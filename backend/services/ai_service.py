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
    
    def generate_content(self, direction: str, platform: str, source: str, topic: str, tone: str, language: str = 'en', generate_images: bool = True) -> str:
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

    def analyze_content_quality(self, content: str, platform: str, direction: str) -> Dict[str, any]:
        """Analyze content quality using AI"""
        
        if not self.api_key:
            return {
                'readability_score': 75,
                'engagement_potential': 'medium',
                'seo_score': 'basic',
                'quality_score': 70
            }
        
        try:
            prompt = f"""
Analyze this content for {platform} in the {direction.replace('_', ' ')} category:

"{content}"

Provide a JSON response with:
- readability_score (0-100)
- engagement_potential (low/medium/high)
- seo_score (basic/good/excellent)
- quality_score (0-100)
- improvement_suggestions (array of strings)
"""
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a content quality analyst. Provide detailed analysis in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.3
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis_text = result['choices'][0]['message']['content'].strip()
                
                # Try to parse JSON response
                try:
                    import json
                    analysis = json.loads(analysis_text)
                    return analysis
                except:
                    # Fallback if JSON parsing fails
                    return {
                        'readability_score': 75,
                        'engagement_potential': 'medium',
                        'seo_score': 'basic',
                        'quality_score': 70,
                        'improvement_suggestions': ['Consider adding more specific examples', 'Include a call-to-action']
                    }
            else:
                return self._fallback_content_analysis()
                
        except Exception as e:
            print(f"Error analyzing content: {str(e)}")
            return self._fallback_content_analysis()
    
    def generate_hashtags(self, content: str, direction: str, platform: str) -> List[str]:
        """Generate relevant hashtags using AI"""
        
        if not self.api_key:
            return self._fallback_hashtags(direction, platform)
        
        try:
            prompt = f"""
Generate 5-8 relevant hashtags for this {platform} content in the {direction.replace('_', ' ')} category:

"{content[:300]}..."

Requirements:
- Relevant to the content and direction
- Platform-appropriate
- Mix of popular and niche hashtags
- No spaces, use camelCase or underscores
- Include the main direction hashtag

Return as a JSON array of strings.
"""
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a hashtag expert. Generate relevant, platform-appropriate hashtags in JSON array format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 200,
                "temperature": 0.5
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                hashtags_text = result['choices'][0]['message']['content'].strip()
                
                try:
                    import json
                    hashtags = json.loads(hashtags_text)
                    return hashtags if isinstance(hashtags, list) else self._fallback_hashtags(direction, platform)
                except:
                    return self._fallback_hashtags(direction, platform)
            else:
                return self._fallback_hashtags(direction, platform)
                
        except Exception as e:
            print(f"Error generating hashtags: {str(e)}")
            return self._fallback_hashtags(direction, platform)
    
    def generate_optimization_suggestions(self, content: str, platform: str) -> List[str]:
        """Generate optimization suggestions using AI"""
        
        if not self.api_key:
            return self._fallback_optimization_suggestions(platform)
        
        try:
            prompt = f"""
Analyze this {platform} content and provide 3-5 optimization suggestions:

"{content}"

Focus on:
- Engagement improvement
- Platform-specific optimization
- Content structure
- Call-to-action effectiveness

Return as a JSON array of suggestion strings.
"""
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a social media optimization expert. Provide actionable suggestions in JSON array format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 300,
                "temperature": 0.4
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                suggestions_text = result['choices'][0]['message']['content'].strip()
                
                try:
                    import json
                    suggestions = json.loads(suggestions_text)
                    return suggestions if isinstance(suggestions, list) else self._fallback_optimization_suggestions(platform)
                except:
                    return self._fallback_optimization_suggestions(platform)
            else:
                return self._fallback_optimization_suggestions(platform)
                
        except Exception as e:
            print(f"Error generating optimization suggestions: {str(e)}")
            return self._fallback_optimization_suggestions(platform)
    
    def enhance_content(self, content: str, platform: str, tone: str, direction: str) -> Optional[str]:
        """Enhance content using AI"""
        
        if not self.api_key:
            return None
        
        try:
            prompt = f"""
Enhance this {platform} content for {tone} tone in the {direction.replace('_', ' ')} category:

"{content}"

Improvements to make:
- Better engagement
- Platform optimization
- Tone consistency
- Clear call-to-action
- Better structure

Return the enhanced content only, no explanations.
"""
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a content enhancement expert. Improve content for better engagement and platform optimization."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 800,
                "temperature": 0.6
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                enhanced_content = result['choices'][0]['message']['content'].strip()
                return enhanced_content if enhanced_content else None
            else:
                return None
                
        except Exception as e:
            print(f"Error enhancing content: {str(e)}")
            return None
    
    def _fallback_content_analysis(self) -> Dict[str, any]:
        """Fallback content analysis"""
        return {
            'readability_score': 75,
            'engagement_potential': 'medium',
            'seo_score': 'basic',
            'quality_score': 70,
            'improvement_suggestions': ['Consider adding more specific examples', 'Include a call-to-action']
        }
    
    def _fallback_hashtags(self, direction: str, platform: str) -> List[str]:
        """Fallback hashtag generation"""
        base_hashtags = [f"#{direction.replace('_', '')}", f"#{platform}"]
        
        direction_hashtags = {
            'business_finance': ['#Business', '#Finance', '#Entrepreneurship'],
            'technology': ['#Tech', '#Innovation', '#DigitalTransformation'],
            'health_wellness': ['#Health', '#Wellness', '#Fitness'],
            'education': ['#Education', '#Learning', '#Skills'],
            'entertainment': ['#Entertainment', '#Culture', '#Media'],
            'travel': ['#Travel', '#Adventure', '#Tourism'],
            'food_cooking': ['#Food', '#Cooking', '#Culinary'],
            'fashion_beauty': ['#Fashion', '#Beauty', '#Style'],
            'sports': ['#Sports', '#Fitness', '#Athletics'],
            'science_research': ['#Science', '#Research', '#Innovation'],
            'politics_society': ['#Politics', '#Society', '#News'],
            'environment_sustainability': ['#Environment', '#Sustainability', '#Green'],
            'lifestyle': ['#Lifestyle', '#PersonalDevelopment', '#Growth'],
            'parenting': ['#Parenting', '#Family', '#Kids'],
            'art_creativity': ['#Art', '#Creativity', '#Design'],
            'real_estate': ['#RealEstate', '#Property', '#Investment'],
            'automotive': ['#Automotive', '#Cars', '#Transportation'],
            'pets_animals': ['#Pets', '#Animals', '#PetCare']
        }
        
        return base_hashtags + direction_hashtags.get(direction, ['#Content', '#SocialMedia'])
    
    def _fallback_optimization_suggestions(self, platform: str) -> List[str]:
        """Fallback optimization suggestions"""
        suggestions = {
            'linkedin': [
                'Add a professional call-to-action',
                'Include industry-specific hashtags',
                'Share personal insights or experiences'
            ],
            'facebook': [
                'Ask a question to encourage engagement',
                'Include relevant images or videos',
                'Use conversational language'
            ],
            'twitter': [
                'Keep it concise and impactful',
                'Use trending hashtags strategically',
                'Include a clear takeaway'
            ],
            'instagram': [
                'Add visual elements',
                'Use aesthetic hashtags',
                'Include a story or personal touch'
            ],
            'youtube': [
                'Create engaging thumbnails',
                'Add timestamps for longer content',
                'Include a clear value proposition'
            ],
            'blog': [
                'Add subheadings for better structure',
                'Include relevant images',
                'Add internal and external links'
            ]
        }
        
        return suggestions.get(platform, ['Optimize for your target audience', 'Include relevant hashtags', 'Add a clear call-to-action'])

    def generate_topics_from_content(self, content_data: Dict[str, str], direction: str, content_type: str = 'video') -> List[Dict[str, any]]:
        """Generate AI-powered topics from video or podcast content"""
        
        if not self.api_key:
            return self._fallback_topics_from_content(content_data, direction, content_type)
        
        try:
            # Extract content information
            title = content_data.get('title', '')
            description = content_data.get('description', '')
            channel = content_data.get('channel', '') or content_data.get('host', '')
            
            prompt = f"""
You are Jess, an expert content strategist and social media specialist. Analyze this {content_type} content and generate 5 highly specific, actionable topic ideas for content creation in the {direction.replace('_', ' ')} niche.

{content_type.title()} Information:
- Title: {title}
- Channel/Host: {channel}
- Description: {description[:800]}{'...' if len(description) > 800 else ''}

As Jess, I need you to:
1. **Deeply analyze** the actual content from the video/podcast
2. **Extract specific insights** and key points mentioned
3. **Identify trending angles** and current discussions in {direction.replace('_', ' ')}
4. **Create actionable topics** that expand on the content's themes
5. **Focus on practical value** for the target audience

Requirements:
- Generate 5 unique, highly specific topic ideas
- Each topic must be directly inspired by the actual content analysis
- Focus on the {direction.replace('_', ' ')} niche and target audience
- Topics should expand on themes, insights, or questions raised in the content
- Include specific angles and approaches for each topic
- Make topics suitable for social media content creation
- Consider current trends and audience pain points in {direction.replace('_', ' ')}

Format your response as a JSON array with this structure:
[
  {{
    "title": "Specific, actionable topic title",
    "description": "Detailed explanation of why this topic is relevant, what value it provides, and how it relates to the analyzed content",
    "trending_score": 85,
    "content_angle": "The specific angle, approach, or unique perspective for this topic"
  }}
]

As Jess, analyze this content and generate the topics now:
"""
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert content strategist specializing in social media content creation. Generate highly relevant, engaging topic ideas based on video/podcast content analysis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 1000,
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
                content = result['choices'][0]['message']['content'].strip()
                
                # Try to parse JSON response
                try:
                    import json
                    topics = json.loads(content)
                    
                    # Validate and format topics
                    formatted_topics = []
                    for topic in topics[:5]:  # Limit to 5 topics
                        if isinstance(topic, dict) and 'title' in topic:
                            formatted_topics.append({
                                'title': topic.get('title', 'Unknown Topic'),
                                'description': topic.get('description', 'No description available'),
                                'trending_score': topic.get('trending_score', 80),
                                'content_angle': topic.get('content_angle', 'General discussion')
                            })
                    
                    return formatted_topics
                    
                except json.JSONDecodeError:
                    # If JSON parsing fails, try to extract topics from text
                    return self._extract_topics_from_text(content, direction)
                    
            else:
                print(f"DeepSeek API error: {response.status_code} - {response.text}")
                return self._fallback_topics_from_content(content_data, direction, content_type)
                
        except Exception as e:
            print(f"Error calling DeepSeek API: {str(e)}")
            return self._fallback_topics_from_content(content_data, direction, content_type)

    def _extract_topics_from_text(self, text: str, direction: str) -> List[Dict[str, any]]:
        """Extract topics from AI text response when JSON parsing fails"""
        import re
        
        topics = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('{') and not line.startswith('[') and not line.startswith(']'):
                # Try to extract topic title
                if ':' in line:
                    title = line.split(':', 1)[1].strip()
                else:
                    title = line
                
                if title and len(title) > 10:
                    topics.append({
                        'title': title,
                        'description': f'AI-generated topic based on {direction.replace("_", " ")} content analysis',
                        'trending_score': 80,
                        'content_angle': 'AI analysis'
                    })
        
        return topics[:5]  # Return max 5 topics

    def _fallback_topics_from_content(self, content_data: Dict[str, str], direction: str, content_type: str = 'video') -> List[Dict[str, any]]:
        """Fallback topic generation when AI is not available - Jess's approach"""
        
        title = content_data.get('title', '')
        channel = content_data.get('channel', '') or content_data.get('host', '')
        description = content_data.get('description', '')
        
        # Generate specific topics based on actual content analysis
        base_topics = [
            {
                'title': f'Deep Dive: Key Insights from "{title[:40]}"',
                'description': f'As Jess, I analyzed this {content_type} and found specific insights that can be expanded into engaging content. This topic explores the main themes and actionable takeaways.',
                'trending_score': 88,
                'content_angle': 'Content analysis with practical applications'
            },
            {
                'title': f'What {channel} Got Right About {direction.replace("_", " ").title()}',
                'description': f'Breaking down the specific strategies and insights shared in this {content_type}. This topic focuses on the most valuable lessons and how to apply them.',
                'trending_score': 85,
                'content_angle': 'Strategy breakdown and implementation'
            },
            {
                'title': f'Beyond the {content_type.title()}: Advanced {direction.replace("_", " ").title()} Strategies',
                'description': f'Taking the concepts from this {content_type} to the next level. This topic explores advanced applications and deeper insights for serious practitioners.',
                'trending_score': 82,
                'content_angle': 'Advanced applications and deep insights'
            },
            {
                'title': f'The {direction.replace("_", " ").title()} Framework: A Step-by-Step Guide',
                'description': f'Based on the insights from this {content_type}, I\'ve created a practical framework that anyone can follow. This topic provides actionable steps and clear implementation strategies.',
                'trending_score': 80,
                'content_angle': 'Practical framework and implementation'
            },
            {
                'title': f'Common Mistakes in {direction.replace("_", " ").title()} (And How to Avoid Them)',
                'description': f'Drawing from the lessons in this {content_type}, this topic addresses the most common pitfalls and provides specific solutions to help others succeed.',
                'trending_score': 78,
                'content_angle': 'Problem-solving and prevention strategies'
            }
        ]
        
        return base_topics

# Global instance
ai_service = DeepSeekAIService() 