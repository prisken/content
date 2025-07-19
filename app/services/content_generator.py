import requests
import json
from flask import current_app
from .stable_diffusion import StableDiffusionService

class ContentGenerator:
    """Content generation service using DeepSeek AI and Stable Diffusion"""
    
    def __init__(self):
        self.api_key = current_app.config.get('DEEPSEEK_API_KEY')
        self.api_base = current_app.config.get('DEEPSEEK_API_BASE', 'https://api.deepseek.com')
        self.stable_diffusion = StableDiffusionService()
        
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
                        tone, region='global', language='en', direction_context=None, generate_images=True):
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
        
        # Generate images if requested
        generated_images = []
        if generate_images:
            try:
                generated_images = self._generate_images(content_type, content_direction, specific_content, tone, language)
            except Exception as e:
                current_app.logger.error(f"Error generating images: {str(e)}")
                generated_images = []
        
        # Format response according to documentation
        response = self._format_response(
            content=generated_text,
            variations=variations,
            media_suggestions=media_suggestions,
            generated_images=generated_images,
            content_type=content_type,
            content_direction=content_direction,
            source_type=source_type,
            specific_content=specific_content,
            tone=tone,
            region=region,
            language=language,
            direction_context=direction_context,
            max_length=template_config['max_length']
        )
        
        return response
    
    def _format_response(self, **kwargs):
        """Format response according to documentation specifications"""
        return {
            # Content Information
            'content': {
                'text': kwargs['content'],
                'length': len(kwargs['content']),
                'max_length': kwargs['max_length'],
                'hashtags': self._extract_hashtags(kwargs['content']),
                'call_to_action': self._extract_call_to_action(kwargs['content'])
            },
            
            # Content Variations
            'variations': kwargs['variations'],
            
            # Generated Images
            'images': kwargs['generated_images'],
            
            # Media Suggestions
            'media_suggestions': kwargs['media_suggestions'],
            
            # Platform Specifications
            'platform_specs': self._get_platform_specifications(kwargs['content_type']),
            
            # Content Metadata
            'metadata': {
                'content_direction': kwargs['content_direction'],
                'content_type': kwargs['content_type'],
                'source_type': kwargs['source_type'],
                'topic': kwargs['specific_content'],
                'tone': kwargs['tone'],
                'region': kwargs['region'],
                'language': kwargs['language'],
                'generated_at': self._get_current_timestamp()
            },
            
            # Cultural and Direction Context
            'cultural_context': self._get_cultural_context(kwargs['region'], kwargs['content_direction']),
            'direction_context': kwargs['direction_context'] or {},
            
            # Analytics Data
            'analytics': self._generate_analytics_data(kwargs['content_type'], kwargs['content_direction'], kwargs['tone'])
        }
    
    def _generate_images(self, content_type, content_direction, topic, tone, language):
        """Generate images using Stable Diffusion"""
        try:
            # Generate primary image
            primary_image = self.stable_diffusion.generate_image(
                platform=content_type,
                content_direction=content_direction,
                topic=topic,
                tone=tone,
                language=language
            )
            
            # Generate additional variations
            variations = self.stable_diffusion.generate_multiple_images(
                platform=content_type,
                content_direction=content_direction,
                topic=topic,
                tone=tone,
                count=2
            )
            
            return {
                'primary': primary_image,
                'variations': variations,
                'total_count': len(variations) + 1
            }
            
        except Exception as e:
            current_app.logger.error(f"Error in image generation: {str(e)}")
            return {
                'primary': None,
                'variations': [],
                'total_count': 0,
                'error': str(e)
            }
    
    def _get_platform_specifications(self, content_type):
        """Get platform-specific specifications from documentation"""
        specs = {
            'linkedin': {
                'content_format': {
                    'max_length': 1300,
                    'hashtag_limit': '1-2',
                    'tone': 'Professional and authoritative',
                    'focus': 'Thought leadership and insights'
                },
                'image_format': {
                    'dimensions': '1024 x 576 pixels (16:9 ratio)',
                    'aspect_ratio': '16:9',
                    'file_types': 'JPG, PNG, GIF',
                    'max_file_size': '5MB',
                    'stable_diffusion_note': 'Uses 16:9 ratio (closest to LinkedIn\'s 1.91:1)'
                },
                'content_structure': [
                    'Professional hook or insight',
                    'Main content with industry expertise',
                    'Data or example when relevant',
                    'Thought-provoking conclusion',
                    'Call-to-action for engagement',
                    '1-2 Professional Hashtags'
                ]
            },
            'facebook': {
                'content_format': {
                    'max_length': 63206,
                    'optimal_length': '40-80 words',
                    'hashtag_limit': '3-5',
                    'tone': 'Conversational and relatable',
                    'focus': 'Community and connection'
                },
                'image_format': {
                    'dimensions': '1024 x 576 pixels (16:9 ratio)',
                    'aspect_ratio': '16:9',
                    'file_types': 'JPG, PNG, GIF',
                    'max_file_size': '4MB',
                    'stable_diffusion_note': 'Uses 16:9 ratio (closest to Facebook\'s 1.91:1)'
                },
                'content_structure': [
                    'Engaging Hook/Question',
                    'Main Content - 2-3 sentences',
                    'Personal touch or story',
                    'Call-to-Action',
                    '3-5 Relevant Hashtags'
                ]
            },
            'instagram': {
                'content_format': {
                    'max_length': 2200,
                    'hashtag_limit': '5-10',
                    'tone': 'Visual and inspirational',
                    'focus': 'Visual storytelling'
                },
                'image_format': {
                    'dimensions': '1024 x 1024 pixels (1:1 ratio)',
                    'aspect_ratio': '1:1',
                    'file_types': 'JPG, PNG',
                    'max_file_size': '8MB',
                    'stable_diffusion_note': 'Perfect square ratio for Instagram posts'
                },
                'content_structure': [
                    'Eye-catching first line',
                    'Main content with line breaks',
                    'Personal insight or tip',
                    'Question or call-to-action',
                    '5-10 Relevant Hashtags'
                ]
            },
            'twitter': {
                'content_format': {
                    'max_length': 280,
                    'hashtag_limit': '1-2',
                    'tone': 'Concise and impactful',
                    'focus': 'Trending and engaging'
                },
                'image_format': {
                    'dimensions': '1024 x 576 pixels (16:9 ratio)',
                    'aspect_ratio': '16:9',
                    'file_types': 'JPG, PNG, GIF, WebP',
                    'max_file_size': '5MB',
                    'stable_diffusion_note': 'Perfect 16:9 ratio for Twitter'
                },
                'content_structure': [
                    'Concise, impactful message',
                    'Clear call-to-action',
                    '1-2 Relevant Hashtags'
                ]
            },
            'youtube_shorts': {
                'content_format': {
                    'length': '30-45 seconds (150-200 words)',
                    'tone': 'Educational and engaging',
                    'focus': 'Hook in first 3 seconds',
                    'structure': 'Problem → Solution → Call to Action'
                },
                'image_format': {
                    'dimensions': '576 x 1024 pixels (9:16 ratio)',
                    'aspect_ratio': '9:16',
                    'file_types': 'MP4, MOV, AVI',
                    'max_file_size': '256GB',
                    'stable_diffusion_note': 'Perfect 9:16 ratio for YouTube Shorts thumbnails'
                },
                'content_structure': [
                    'Hook - First 3 seconds',
                    'Problem identification',
                    'Solution or insight',
                    'Call-to-action',
                    'Voiceover instructions'
                ]
            },
            'blog': {
                'content_format': {
                    'length': '1,500-2,500 words',
                    'tone': 'Educational and informative',
                    'focus': 'SEO and value',
                    'structure': 'Introduction + Body + Conclusion'
                },
                'image_format': {
                    'dimensions': '1024 x 576 pixels (16:9 ratio)',
                    'aspect_ratio': '16:9',
                    'file_types': 'JPG, PNG, WebP',
                    'max_file_size': '5MB',
                    'stable_diffusion_note': 'Uses 16:9 ratio (closest to blog\'s 1.91:1)'
                },
                'content_structure': [
                    'SEO-optimized title',
                    'Introduction with hook',
                    'Main content with headings',
                    'Subheadings for organization',
                    'Conclusion with takeaways',
                    'Call-to-action'
                ]
            }
        }
        
        return specs.get(content_type.lower(), {})
    
    def _generate_analytics_data(self, content_type, content_direction, tone):
        """Generate analytics data for content performance tracking"""
        return {
            'content_metrics': {
                'character_count': 0,  # Will be updated with actual content
                'word_count': 0,       # Will be updated with actual content
                'hashtag_count': 0,    # Will be updated with actual content
                'readability_score': 0, # Will be calculated
                'engagement_potential': 'medium'  # Will be calculated
            },
            'platform_optimization': {
                'optimal_posting_time': self._get_optimal_posting_time(content_type),
                'recommended_frequency': self._get_recommended_frequency(content_type),
                'audience_demographics': self._get_audience_demographics(content_type),
                'content_lifecycle': self._get_content_lifecycle(content_type)
            },
            'performance_predictions': {
                'estimated_reach': 'medium',
                'estimated_engagement': 'medium',
                'estimated_clicks': 'low',
                'viral_potential': 'low'
            }
        }
    
    def _extract_hashtags(self, content):
        """Extract hashtags from content"""
        import re
        hashtags = re.findall(r'#\w+', content)
        return hashtags
    
    def _extract_call_to_action(self, content):
        """Extract call-to-action from content"""
        cta_indicators = [
            'click', 'visit', 'learn more', 'get started', 'sign up', 'download',
            'share', 'comment', 'like', 'follow', 'subscribe', 'join', 'try',
            'discover', 'explore', 'find out', 'check out', 'see more'
        ]
        
        sentences = content.split('.')
        cta_sentences = []
        
        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in cta_indicators):
                cta_sentences.append(sentence.strip())
        
        return cta_sentences
    
    def _get_current_timestamp(self):
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'
    
    def _get_optimal_posting_time(self, content_type):
        """Get optimal posting time for content type"""
        times = {
            'linkedin': 'Tuesday-Thursday, 8-10 AM or 5-6 PM',
            'facebook': 'Tuesday-Thursday, 1-3 PM or 7-9 PM',
            'instagram': 'Wednesday, 11 AM-1 PM or 7-9 PM',
            'twitter': 'Monday-Thursday, 8-10 AM or 6-9 PM',
            'youtube_shorts': 'Monday-Thursday, 2-4 PM or 7-9 PM',
            'blog': 'Tuesday-Thursday, 9-11 AM'
        }
        return times.get(content_type, 'Varies by platform')
    
    def _get_recommended_frequency(self, content_type):
        """Get recommended posting frequency"""
        frequencies = {
            'linkedin': '1-2 times per week',
            'facebook': '1-2 times per day',
            'instagram': '1-2 times per day',
            'twitter': '3-5 times per day',
            'youtube_shorts': '1-2 times per day',
            'blog': '1-2 times per week'
        }
        return frequencies.get(content_type, 'Varies by platform')
    
    def _get_audience_demographics(self, content_type):
        """Get audience demographics for content type"""
        demographics = {
            'linkedin': 'Professionals, 25-54, B2B focus',
            'facebook': 'General audience, 25-65, diverse interests',
            'instagram': 'Young adults, 18-34, visual content lovers',
            'twitter': 'News followers, 18-49, real-time engagement',
            'youtube_shorts': 'Young audience, 13-34, video content consumers',
            'blog': 'Professionals, 25-54, in-depth content seekers'
        }
        return demographics.get(content_type, 'Varies by platform')
    
    def _get_content_lifecycle(self, content_type):
        """Get content lifecycle for platform"""
        lifecycles = {
            'linkedin': '48-72 hours',
            'facebook': '24-48 hours',
            'instagram': '24-48 hours',
            'twitter': '2-4 hours',
            'youtube_shorts': '24-48 hours',
            'blog': '1-2 weeks'
        }
        return lifecycles.get(content_type, 'Varies by platform')
    
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