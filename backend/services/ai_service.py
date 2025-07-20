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
        """Create a detailed prompt for content generation following platform-specific formats"""
        
        # Platform-specific formats and requirements
        platform_formats = {
            'linkedin': {
                'character_limit': 1300,
                'structure': '[Professional hook or insight]\n[Main content with industry expertise]\n[Data or example when relevant]\n[Thought-provoking conclusion]\n[Call-to-action for engagement]\n[1-2 Professional Hashtags]',
                'guidelines': 'Professional tone, business-focused, thought leadership, include industry insights, use professional language, keep hashtags minimal and professional, encourage meaningful discussions',
                'hashtags': '1-2 relevant hashtags'
            },
            'facebook': {
                'character_limit': 632,
                'structure': '[Engaging Hook/Question]\n[Main Content - 2-3 sentences]\n[Personal touch or story]\n[Call-to-Action]\n[3-5 Relevant Hashtags]',
                'guidelines': 'Conversational and relatable tone, focus on community and connection, encourage comments and discussion, use conversational language, include personal anecdotes when relevant, end with questions to spark discussion, use emojis strategically (2-3 per post)',
                'hashtags': '3-5 relevant hashtags'
            },
            'twitter': {
                'character_limit': 280,
                'structure': '[Concise, impactful message]\n[Clear call-to-action]\n[1-2 Relevant Hashtags]',
                'guidelines': 'Concise and impactful tone, focus on trending and engaging content, be concise and direct, use trending hashtags when relevant, include clear calls-to-action, focus on shareable content, use abbreviations when necessary, keep hashtags to minimum',
                'hashtags': '1-2 relevant hashtags'
            },
            'instagram': {
                'character_limit': 2200,
                'structure': '[Eye-catching first line]\n[Main content with line breaks]\n[Personal insight or tip]\n[Question or call-to-action]\n[5-10 Relevant Hashtags]',
                'guidelines': 'Visual and inspirational tone, focus on visual storytelling, use line breaks for readability, include emojis throughout (5-8 per post), focus on visual descriptions, use aesthetic and inspirational language, include location tags when relevant, end with engaging questions',
                'hashtags': '5-10 relevant hashtags'
            },
            'youtube': {
                'character_limit': 5000,
                'structure': '[Hook - First 3 seconds]\n[Problem identification]\n[Solution or insight]\n[Call-to-action]\n[Voiceover instructions]',
                'guidelines': 'Educational and engaging tone, detailed and informative content, include timestamps if relevant, start with a strong hook, keep sentences short and clear, include clear voiceover instructions, focus on one main point, end with strong call-to-action, use conversational tone',
                'hashtags': 'Include relevant hashtags in description'
            },
            'blog': {
                'character_limit': 2500,
                'structure': '[SEO-optimized title]\n[Introduction with hook]\n[Main content with headings]\n[Subheadings for organization]\n[Conclusion with takeaways]\n[Call-to-action]',
                'guidelines': 'Educational and informative tone, comprehensive and well-structured content, include headings, use SEO-optimized headings, include relevant keywords naturally, break content into digestible sections, provide actionable insights, include internal and external links, use bullet points and lists',
                'hashtags': 'Include relevant hashtags in meta description'
            }
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
        
        # Get platform format
        platform_format = platform_formats.get(platform, platform_formats['linkedin'])
        
        # Language-specific instructions
        language_instruction = f"Write in {language.upper()} language." if language != 'en' else ""
        
        prompt = f"""
Create a {platform} post about "{topic}" in the {direction.replace('_', ' ')} category.

PLATFORM REQUIREMENTS:
- Character Limit: {platform_format['character_limit']} characters
- Structure: {platform_format['structure']}
- Guidelines: {platform_format['guidelines']}
- Hashtags: {platform_format['hashtags']}

CONTENT DIRECTION: {direction_context.get(direction, 'Professional and informative content')}
TONE: {tone_guidelines.get(tone, 'Professional and engaging')}
SOURCE INSPIRATION: {source.replace('_', ' ')}

{language_instruction}

CRITICAL REQUIREMENTS:
- Follow the exact structure provided above
- Stay within character limits
- Use the specified tone throughout
- Include appropriate hashtags
- Make it engaging and shareable
- Ensure platform-specific formatting
- Make it actionable and valuable to the audience

Generate the content following the exact format:
"""
        
        return prompt.strip()
    
    def _fallback_content_generation(self, direction: str, platform: str, source: str, topic: str, tone: str, language: str) -> str:
        """Fallback content generation when DeepSeek API is not available - following platform formats"""
        
        # Platform-specific fallback templates following the formats
        templates = {
            'linkedin': {
                'professional': f"🚀 {topic}\n\nBased on {source.replace('_', ' ')} insights, here's what you need to know about {direction.replace('_', ' ')}.\n\nKey takeaways:\n• Understanding {topic} is crucial for success\n• Focus on practical applications in {direction.replace('_', ' ')}\n• Continuous learning drives innovation\n\nWhat's your experience with {topic}? Share your thoughts below! 👇\n\n#{direction.replace('_', '')} #{topic.replace(' ', '')}",
                'casual': f"Hey there! 👋\n\nQuick thought on {topic} - inspired by some great {source.replace('_', ' ')} content I've been consuming.\n\nHere's what I've learned:\n• There's always something new to discover about {topic}\n• Community insights are invaluable\n\nWhat do you think? Any tips to share? 🤔\n\n#{direction.replace('_', '')} #{topic.replace(' ', '')}"
            },
            'facebook': {
                'professional': f"📊 {topic} Update\n\nSharing insights from {source.replace('_', ' ')} about {direction.replace('_', ' ')}.\n\nKey points:\n• Current trends in {direction.replace('_', ' ')}\n• Future implications for {topic}\n\nWhat's your take on this? Comment below!\n\n#{direction.replace('_', '')} #{topic.replace(' ', '')} #Technology #Innovation",
                'casual': f"Hey friends! 😊\n\nJust wanted to share some thoughts on {topic} that I picked up from {source.replace('_', ' ')}.\n\nHere's what caught my attention:\n• How {topic} affects our daily lives\n• Ways to improve our approach to {direction.replace('_', ' ')}\n\nAnyone else thinking about this? Let's discuss! 💬\n\n#{direction.replace('_', '')} #{topic.replace(' ', '')} #TechTalk #Innovation"
            },
            'twitter': {
                'professional': f"💡 {topic}\n\nKey insights from {source.replace('_', ' ')}:\n\n• Understanding {topic} is crucial for success\n• Focus on practical applications\n\n#{direction.replace('_', '')} #{topic.replace(' ', '')}",
                'casual': f"🤔 {topic}\n\nJust learned from {source.replace('_', ' ')}:\n\n• There's always something new to discover\n• Community insights are invaluable\n\nThoughts? #{direction.replace('_', '')} #{topic.replace(' ', '')}"
            },
            'instagram': {
                'professional': f"🚀 {topic}\n\nBased on {source.replace('_', ' ')} insights, here's what you need to know about {direction.replace('_', ' ')}.\n\nKey takeaways:\n• Understanding {topic} is crucial for success\n• Focus on practical applications in {direction.replace('_', ' ')}\n• Continuous learning drives innovation\n\nWhat's your experience with {topic}? Share your thoughts below! 👇\n\n#Technology #Innovation #{direction.replace('_', '')} #{topic.replace(' ', '')} #TechTrends #DigitalTransformation #FutureTech #AI #Innovation #TechLife",
                'casual': f"Hey there! 👋\n\nQuick thought on {topic} - inspired by some great {source.replace('_', ' ')} content I've been consuming.\n\nHere's what I've learned:\n• There's always something new to discover about {topic}\n• Community insights are invaluable\n\nWhat do you think? Any tips to share? 🤔\n\n#TechTalk #Innovation #{direction.replace('_', '')} #{topic.replace(' ', '')} #TechCommunity #Learning #Growth #TechTrends #DigitalLife"
            },
            'youtube': {
                'professional': f"🎬 {topic}\n\nHook: Discover the secrets behind {topic} that most people miss!\n\nProblem: Many struggle with understanding {topic} in {direction.replace('_', ' ')}.\n\nSolution: In this video, we'll break down the key insights from {source.replace('_', ' ')} and show you practical applications.\n\nCall-to-Action: Subscribe for more insights on {direction.replace('_', ' ')}!\n\nVoiceover: Start with 'Have you ever wondered about {topic}?' and end with 'Don't forget to like and subscribe!'",
                'casual': f"🎬 {topic}\n\nHook: Let's talk about {topic} - it's more interesting than you think!\n\nProblem: People often overlook the importance of {topic}.\n\nSolution: We'll explore how {topic} impacts our daily lives and share some cool insights.\n\nCall-to-Action: Hit that subscribe button for more awesome content!\n\nVoiceover: Start with 'Hey everyone!' and end with 'Thanks for watching!'"
            },
            'blog': {
                'professional': f"# {topic}: A Comprehensive Guide to {direction.replace('_', ' ').title()}\n\n## Introduction\n\nIn today's rapidly evolving {direction.replace('_', ' ')} landscape, understanding {topic} has become more crucial than ever. Based on insights from {source.replace('_', ' ')}, this comprehensive guide will provide you with actionable strategies and practical applications.\n\n## Key Insights from {source.replace('_', ' ').title()}\n\n### Understanding {topic}\n{topic} represents a fundamental shift in how we approach {direction.replace('_', ' ')}. The insights from {source.replace('_', ' ')} reveal several key aspects:\n\n- **Practical Applications**: How {topic} can be implemented in real-world scenarios\n- **Industry Impact**: The broader implications for {direction.replace('_', ' ')}\n- **Future Trends**: What to expect in the coming years\n\n### Implementation Strategies\n\nBased on {source.replace('_', ' ')} research, here are the most effective strategies:\n\n1. **Start Small**: Begin with basic applications of {topic}\n2. **Scale Gradually**: Build upon initial successes\n3. **Measure Results**: Track progress and adjust accordingly\n\n## Conclusion\n\n{topic} offers tremendous opportunities for those willing to embrace change and innovation. By following the insights from {source.replace('_', ' ')} and implementing the strategies outlined above, you can position yourself for success in the evolving {direction.replace('_', ' ')} landscape.\n\n**Ready to get started?** Take the first step today and explore how {topic} can transform your approach to {direction.replace('_', ' ')}.",
                'casual': f"# {topic}: What You Need to Know About {direction.replace('_', ' ').title()}\n\n## Hey there! 👋\n\nSo, you've probably heard about {topic} and wondered what all the fuss is about. Well, you're in the right place! Based on some really interesting {source.replace('_', ' ')} content I've been exploring, I'm here to break it down for you in a way that actually makes sense.\n\n## What's the Deal with {topic}?\n\n### The Basics\n{topic} is basically changing how we think about {direction.replace('_', ' ')}. Here's what you need to know:\n\n- **What it is**: A fresh approach to {direction.replace('_', ' ')}\n- **Why it matters**: It's making waves in the industry\n- **How to use it**: Practical tips that actually work\n\n### Cool Things I Learned\n\nFrom diving into {source.replace('_', ' ')} content, here are some really cool insights:\n\n1. **It's More Accessible Than You Think**: You don't need to be an expert to get started\n2. **Community is Key**: There are tons of people exploring this together\n3. **Small Steps Lead to Big Results**: Start simple and build from there\n\n## Wrapping Up\n\n{topic} is definitely worth your attention if you're interested in {direction.replace('_', ' ')}. The insights from {source.replace('_', ' ')} show that it's not just a trend - it's here to stay.\n\n**Want to learn more?** Check out the resources below and join the conversation!"
            }
        }
        
        # Get appropriate template
        platform_templates = templates.get(platform, templates['linkedin'])
        template = platform_templates.get(tone, platform_templates['professional'])
        
        return template
    
    def generate_image_prompt(self, content: str, direction: str, platform: str) -> str:
        """Generate image prompt based on content and context following Stable Diffusion best practices"""
        
        if not self.api_key:
            return self._fallback_image_prompt(direction, platform)
        
        try:
            # Platform-specific image requirements
            platform_image_specs = {
                'linkedin': {
                    'dimensions': '1200 x 627 pixels (1.91:1 aspect ratio)',
                    'style': 'professional, corporate, business-focused',
                    'format': 'infographics, charts, professional photography'
                },
                'facebook': {
                    'dimensions': '1200 x 630 pixels (1.91:1 aspect ratio)',
                    'style': 'social, friendly, community-focused',
                    'format': 'lifestyle photography, social scenes, relatable imagery'
                },
                'twitter': {
                    'dimensions': '1200 x 675 pixels (16:9 aspect ratio)',
                    'style': 'clean, impactful, shareable',
                    'format': 'minimalist design, bold graphics, eye-catching visuals'
                },
                'instagram': {
                    'dimensions': '1080 x 1080 pixels (1:1 aspect ratio)',
                    'style': 'visual, aesthetic, inspirational',
                    'format': 'high-quality photography, artistic composition, trending aesthetics'
                },
                'youtube': {
                    'dimensions': '1280 x 720 pixels (16:9 aspect ratio)',
                    'style': 'dynamic, engaging, educational',
                    'format': 'video thumbnails, action shots, educational graphics'
                },
                'blog': {
                    'dimensions': '1200 x 630 pixels (1.91:1 aspect ratio)',
                    'style': 'detailed, informative, professional',
                    'format': 'featured images, infographics, professional photography'
                }
            }
            
            platform_specs = platform_image_specs.get(platform, platform_image_specs['linkedin'])
            
            prompt = f"""
Based on this content: "{content[:200]}..."

Generate a Stable Diffusion image prompt for a {platform} post in the {direction.replace('_', ' ')} category.

PLATFORM REQUIREMENTS:
- Dimensions: {platform_specs['dimensions']}
- Style: {platform_specs['style']}
- Format: {platform_specs['format']}

STABLE DIFFUSION BEST PRACTICES:
- Use specific, descriptive language
- Include style modifiers (photorealistic, digital art, etc.)
- Specify lighting and mood
- Include composition details
- Use quality boosters (high quality, detailed, 4k, etc.)
- Avoid negative prompts in the main prompt

FORMAT: Create a detailed, specific prompt that follows Stable Diffusion conventions and includes:
1. Main subject/theme
2. Style and aesthetic
3. Lighting and mood
4. Composition and framing
5. Quality modifiers
6. Platform-specific elements

Generate the image prompt now:
"""
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert at creating Stable Diffusion image prompts for social media content. Generate specific, actionable prompts that follow Stable Diffusion best practices and platform requirements."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 400,
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
                image_prompt = result['choices'][0]['message']['content'].strip()
                return image_prompt
            else:
                return self._fallback_image_prompt(direction, platform)
                
        except Exception as e:
            print(f"Error generating image prompt: {str(e)}")
            return self._fallback_image_prompt(direction, platform)
    
    def _fallback_image_prompt(self, direction: str, platform: str) -> str:
        """Fallback image prompt generation following Stable Diffusion best practices"""
        
        # Direction-specific base prompts
        direction_prompts = {
            'business_finance': 'professional business executive in modern office with charts, graphs, financial data, corporate environment',
            'technology': 'futuristic digital interface, holographic displays, technology elements, innovation concepts, digital transformation',
            'health_wellness': 'clean modern wellness center, natural lighting, healthy lifestyle imagery, fitness equipment, wellness atmosphere',
            'education': 'modern learning environment, books, technology, educational materials, student collaboration, knowledge sharing',
            'entertainment': 'vibrant entertainment venue, media elements, creative atmosphere, stage lighting, performance energy',
            'travel_tourism': 'beautiful travel destination, scenic landscapes, adventure elements, cultural landmarks, wanderlust',
            'food_cooking': 'appetizing food presentation, culinary elements, kitchen setting, fresh ingredients, gourmet preparation',
            'fashion_beauty': 'stylish fashion runway, modern aesthetics, beauty elements, designer clothing, fashion photography',
            'sports_fitness': 'dynamic sports arena, athletic equipment, fitness motivation, action shots, competitive spirit',
            'science_research': 'scientific laboratory, research equipment, innovation, microscope, test tubes, breakthrough discovery',
            'politics_news': 'professional news studio, current events, political elements, journalism, media coverage',
            'environment': 'natural environmental landscape, sustainability, green living elements, renewable energy, eco-friendly',
            'personal_dev': 'inspiring personal development workshop, growth mindset, motivation elements, self-improvement, success',
            'parenting_family': 'warm family home, parenting elements, child-friendly environment, family bonding, nurturing atmosphere',
            'art_creativity': 'creative art studio, artistic elements, creative inspiration, paintbrushes, canvas, artistic expression',
            'real_estate': 'modern luxury home, property elements, architectural design, real estate showcase, dream house',
            'automotive': 'modern automotive showroom, car elements, transportation technology, luxury vehicles, automotive innovation',
            'pet_care': 'warm pet-friendly home, animal care elements, pet lifestyle, happy pets, veterinary care'
        }
        
        base_prompt = direction_prompts.get(direction, 'professional modern setting with business elements')
        
        # Platform-specific style modifiers
        platform_styles = {
            'linkedin': 'professional corporate photography, business environment, executive style, professional lighting',
            'facebook': 'social lifestyle photography, friendly atmosphere, community focus, warm lighting',
            'instagram': 'aesthetic photography, trending visual style, artistic composition, high contrast',
            'twitter': 'clean minimalist design, bold graphics, eye-catching visuals, sharp focus',
            'youtube': 'dynamic action photography, engaging composition, educational graphics, vibrant colors',
            'blog': 'detailed professional photography, informative graphics, high resolution, editorial style'
        }
        
        platform_style = platform_styles.get(platform, 'professional photography')
        
        # Stable Diffusion quality boosters
        quality_modifiers = 'high quality, detailed, 4k resolution, professional photography, sharp focus, perfect lighting, photorealistic'
        
        return f"{base_prompt}, {platform_style}, {quality_modifiers}, trending on artstation, masterpiece"

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
You are Jess, a creative content strategist. Based on this {content_type} content, generate 5 fresh and engaging topic ideas for the {direction.replace('_', ' ')} niche.

Content Info:
- Title: {title}
- Channel/Host: {channel}
- Description: {description[:500]}{'...' if len(description) > 500 else ''}

Be creative and think outside the box! Generate topics that are:
- Engaging and interesting
- Relevant to {direction.replace('_', ' ')}
- Suitable for social media
- Unique and fresh perspectives

Format as JSON array:
[
  {{
    "title": "Creative topic title",
    "description": "Brief explanation of the topic",
    "trending_score": 85,
    "content_angle": "Creative angle or approach"
  }}
]

Generate 5 creative topics now:
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
                    # Clean up the content to remove extra quotes and commas
                    cleaned_content = content.strip()
                    if cleaned_content.startswith('```json'):
                        cleaned_content = cleaned_content[7:]
                    if cleaned_content.endswith('```'):
                        cleaned_content = cleaned_content[:-3]
                    cleaned_content = cleaned_content.strip()
                    
                    topics = json.loads(cleaned_content)
                    
                    # Validate and format topics
                    formatted_topics = []
                    for topic in topics[:5]:  # Limit to 5 topics
                        if isinstance(topic, dict) and 'title' in topic:
                            # Clean up title (remove extra quotes and commas)
                            title = topic.get('title', 'Unknown Topic')
                            if isinstance(title, str):
                                title = title.strip().strip('"').strip(',').strip()
                            
                            formatted_topics.append({
                                'title': title,
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
        
        # Generate creative topics based on content
        base_topics = [
            {
                'title': f'🎯 Hidden Gems from "{title[:30]}"',
                'description': f'Discover the unexpected insights and creative angles from this {content_type} that most people miss.',
                'trending_score': 88,
                'content_angle': 'Creative insights'
            },
            {
                'title': f'🚀 {direction.replace("_", " ").title()} Hacks That Actually Work',
                'description': f'Real-world strategies and practical tips that you can implement immediately.',
                'trending_score': 85,
                'content_angle': 'Practical hacks'
            },
            {
                'title': f'💡 The Future of {direction.replace("_", " ").title()}',
                'description': f'Explore emerging trends and innovative approaches that are shaping the future.',
                'trending_score': 82,
                'content_angle': 'Future trends'
            },
            {
                'title': f'🔥 {direction.replace("_", " ").title()} Secrets Revealed',
                'description': f'Behind-the-scenes insights and insider knowledge that give you the edge.',
                'trending_score': 80,
                'content_angle': 'Insider knowledge'
            },
            {
                'title': f'⚡ Quick Wins in {direction.replace("_", " ").title()}',
                'description': f'Fast, actionable strategies that deliver immediate results and boost your success.',
                'trending_score': 78,
                'content_angle': 'Quick results'
            }
        ]
        
        return base_topics

# Global instance
ai_service = DeepSeekAIService() 