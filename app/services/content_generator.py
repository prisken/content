import requests
import json
from flask import current_app

class ContentGenerator:
    """Content generation service using DeepSeek AI"""
    
    def __init__(self):
        self.api_key = current_app.config.get('DEEPSEEK_API_KEY')
        self.api_base = current_app.config.get('DEEPSEEK_API_BASE', 'https://api.deepseek.com')
        
        # Content templates for different platforms
        self.content_templates = {
            'linkedin': {
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
            },
            'facebook': {
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
            },
            'instagram': {
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
            },
            'twitter': {
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
            },
            'youtube_shorts': {
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
            },
            'blog': {
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
        }
    
    def generate_content(self, content_direction, content_type, source_type, specific_content, 
                        tone, region='global', language='en', direction_context=None):
        """Generate content using DeepSeek AI with direction and regional context"""
        
        # Get template for content type
        template_config = self.content_templates.get(content_type.lower())
        if not template_config:
            raise ValueError(f"Unsupported content type: {content_type}")
        
        # Build prompt with context
        prompt = self._build_prompt(
            template_config['template'],
            source_data=specific_content,
            tone=tone,
            region=region,
            content_direction=content_direction,
            language=language,
            direction_context=direction_context
        )
        
        # Generate content using DeepSeek
        generated_text = self._call_deepseek_api(prompt, template_config['max_length'])
        
        # Generate variations
        variations = self._generate_variations(prompt, template_config['max_length'])
        
        # Generate media suggestions
        media_suggestions = self._generate_media_suggestions(content_type, content_direction, specific_content)
        
        return {
            'content': generated_text,
            'variations': variations,
            'media_suggestions': media_suggestions,
            'cultural_context': self._get_cultural_context(region, content_direction),
            'direction_context': direction_context or {},
            'content_type': content_type,
            'max_length': template_config['max_length']
        }
    
    def _build_prompt(self, template, **kwargs):
        """Build the complete prompt for AI generation"""
        # Format the template with provided parameters
        prompt = template.format(**kwargs)
        
        # Add direction-specific instructions
        if kwargs.get('direction_context'):
            direction_context = kwargs['direction_context']
            prompt += f"\n\nDirection Context:\n"
            prompt += f"- Industry: {direction_context.get('direction_name', '')}\n"
            prompt += f"- Language Style: {direction_context.get('language_style', '')}\n"
            prompt += f"- Recommended Hashtags: {', '.join(direction_context.get('hashtags', []))}\n"
            prompt += f"- Subcategories: {', '.join(direction_context.get('subcategories', []))}\n"
        
        # Add regional context
        if kwargs.get('region') and kwargs['region'] != 'global':
            prompt += f"\nRegional Considerations:\n"
            prompt += f"- Region: {kwargs['region']}\n"
            prompt += f"- Language: {kwargs['language']}\n"
            prompt += "- Ensure cultural sensitivity and local relevance\n"
        
        return prompt
    
    def _call_deepseek_api(self, prompt, max_length):
        """Call DeepSeek API for content generation"""
        if not self.api_key:
            # Fallback to mock response for development
            return self._generate_mock_content(prompt, max_length)
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'deepseek-chat',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a professional content creator specializing in social media and blog content. Generate high-quality, engaging content that follows the provided specifications exactly.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': min(max_length * 2, 2000),  # Estimate tokens needed
                'temperature': 0.7,
                'top_p': 0.9
            }
            
            response = requests.post(
                f'{self.api_base}/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                # Fallback to mock response
                return self._generate_mock_content(prompt, max_length)
                
        except Exception as e:
            # Fallback to mock response
            return self._generate_mock_content(prompt, max_length)
    
    def _generate_mock_content(self, prompt, max_length):
        """Generate mock content for development/testing"""
        # Extract content type from prompt
        if 'LinkedIn' in prompt:
            return f"🚀 Exciting developments in the business world! Based on recent insights, we're seeing remarkable growth in key sectors. This represents a significant opportunity for forward-thinking professionals. What are your thoughts on these emerging trends? #BusinessGrowth #Innovation #ProfessionalDevelopment"
        elif 'Facebook' in prompt:
            return f"Hey everyone! 👋 Just wanted to share some amazing insights I came across today. The way things are evolving in our industry is truly fascinating. What do you think about these changes? Drop a comment below! #Community #Insights #Discussion"
        elif 'Instagram' in prompt:
            return f"✨ Today's inspiration comes from some incredible developments in our field. The possibilities are endless when we embrace innovation and creativity. What's inspiring you today? 💫 #Inspiration #Innovation #Creativity #Motivation #Growth"
        elif 'Twitter' in prompt:
            return f"Breaking: Major developments in the industry! This changes everything. Thoughts? #Innovation #Trending"
        elif 'YouTube' in prompt:
            return f"[HOOK: 0-3 seconds] Hey there! Today we're diving into something incredible that's happening right now.\n\n[CONTENT: 3-40 seconds] Based on recent research and insights, we're seeing remarkable changes that affect everyone. Here's what you need to know and how it impacts you.\n\n[CALL TO ACTION: 40-45 seconds] Don't forget to like, subscribe, and share your thoughts in the comments below!"
        elif 'blog' in prompt.lower():
            return f"# The Future of Innovation: What You Need to Know\n\n## Introduction\nIn today's rapidly evolving landscape, understanding the key trends and developments is crucial for success.\n\n## Key Insights\nRecent research and analysis reveal several important developments that are shaping the future of our industry.\n\n## What This Means for You\nThese changes present both challenges and opportunities for professionals and businesses alike.\n\n## Conclusion\nStaying informed and adaptable is more important than ever in this dynamic environment."
        else:
            return f"Generated content based on: {prompt[:100]}... (Mock response for development)"
    
    def _generate_variations(self, prompt, max_length):
        """Generate content variations"""
        variations = []
        
        # Generate 3 variations with different approaches
        variation_prompts = [
            prompt + "\n\nVariation 1: Focus on storytelling and personal connection",
            prompt + "\n\nVariation 2: Emphasize data and statistics",
            prompt + "\n\nVariation 3: Use humor and lighthearted approach"
        ]
        
        for i, var_prompt in enumerate(variation_prompts, 1):
            try:
                variation_content = self._call_deepseek_api(var_prompt, max_length)
                variations.append({
                    'id': i,
                    'content': variation_content,
                    'style': ['Storytelling', 'Data-driven', 'Humorous'][i-1]
                })
            except Exception:
                # Add mock variation
                variations.append({
                    'id': i,
                    'content': f"Variation {i}: {self._generate_mock_content(prompt, max_length)}",
                    'style': ['Storytelling', 'Data-driven', 'Humorous'][i-1]
                })
        
        return variations
    
    def _generate_media_suggestions(self, content_type, content_direction, source_content):
        """Generate media suggestions for the content"""
        media_suggestions = {
            'images': [],
            'videos': [],
            'graphics': []
        }
        
        # Generate image suggestions based on content type and direction
        if content_type.lower() in ['linkedin', 'facebook', 'instagram']:
            media_suggestions['images'].extend([
                f"Professional {content_direction} related image",
                f"Infographic about {content_direction} trends",
                f"Quote card with {content_direction} insights"
            ])
        
        if content_type.lower() == 'youtube_shorts':
            media_suggestions['videos'].extend([
                f"Animated explainer about {content_direction}",
                f"Talking head video discussing {content_direction}",
                f"Screen recording with {content_direction} insights"
            ])
        
        if content_type.lower() == 'blog':
            media_suggestions['graphics'].extend([
                f"Featured image related to {content_direction}",
                f"Charts and graphs for {content_direction} data",
                f"Infographic summarizing {content_direction} key points"
            ])
        
        return media_suggestions
    
    def _get_cultural_context(self, region, content_direction):
        """Get cultural context for the region and content direction"""
        cultural_contexts = {
            'global': {
                'sensitivity': 'general',
                'recommendations': ['Use inclusive language', 'Avoid cultural stereotypes']
            },
            'north_america': {
                'sensitivity': 'western',
                'recommendations': ['Use American business terminology', 'Consider US holidays and events']
            },
            'europe': {
                'sensitivity': 'european',
                'recommendations': ['Use European business practices', 'Consider EU regulations and trends']
            },
            'asia_pacific': {
                'sensitivity': 'asian',
                'recommendations': ['Use respectful language', 'Consider Asian business customs']
            }
        }
        
        return cultural_contexts.get(region, cultural_contexts['global']) 