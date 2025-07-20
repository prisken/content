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
        # Calculate actual content metrics
        content_text = kwargs['content']
        character_count = len(content_text)
        word_count = len(content_text.split())
        hashtags = self._extract_hashtags(content_text)
        hashtag_count = len(hashtags)
        
        # Get platform specifications
        platform_specs = self._get_platform_specifications(kwargs['content_type'])
        
        # Generate analytics with actual content data
        analytics_data = self._generate_analytics_data(kwargs['content_type'], kwargs['content_direction'], kwargs['tone'])
        analytics_data['content_metrics'].update({
            'character_count': character_count,
            'word_count': word_count,
            'hashtag_count': hashtag_count,
            'readability_score': self._calculate_readability_score(content_text),
            'engagement_potential': self._calculate_engagement_potential(content_text, kwargs['content_type']),
            'content_quality_score': self._calculate_content_quality_score(content_text, kwargs['content_type']),
            'seo_score': self._calculate_seo_score(content_text) if kwargs['content_type'] == 'blog' else 0,
            'visual_appeal_score': self._calculate_visual_appeal_score(content_text, kwargs['content_type'])
        })
        
        # Update content validation
        analytics_data['content_validation'].update({
            'length_compliance': self._check_length_compliance(character_count, kwargs['content_type']),
            'hashtag_optimization': self._check_hashtag_optimization(hashtag_count, kwargs['content_type']),
            'tone_consistency': self._check_tone_consistency(content_text, kwargs['tone']),
            'cultural_sensitivity': self._check_cultural_sensitivity(content_text, kwargs['region']),
            'brand_consistency': True,  # Placeholder for brand checking
            'accessibility_score': self._calculate_accessibility_score(content_text)
        })
        
        return {
            # Content Information
            'content': {
                'text': content_text,
                'length': character_count,
                'max_length': kwargs['max_length'],
                'hashtags': hashtags,
                'call_to_action': self._extract_call_to_action(content_text),
                'word_count': word_count,
                'readability_score': analytics_data['content_metrics']['readability_score']
            },
            
            # Content Variations
            'variations': kwargs['variations'],
            
            # Generated Images
            'images': kwargs['generated_images'],
            
            # Media Suggestions
            'media_suggestions': kwargs['media_suggestions'],
            
            # Platform Specifications (Comprehensive)
            'platform_specifications': {
                'content_format': platform_specs.get('content_format', {}),
                'image_format': platform_specs.get('image_format', {}),
                'content_structure': platform_specs.get('content_structure', []),
                'best_practices': platform_specs.get('best_practices', []),
                'technical_requirements': {
                    'character_limits': platform_specs.get('content_format', {}).get('max_length', 0),
                    'hashtag_limits': platform_specs.get('content_format', {}).get('hashtag_limit', '0'),
                    'image_dimensions': platform_specs.get('image_format', {}),
                    'file_size_limits': platform_specs.get('image_format', {}),
                    'supported_formats': platform_specs.get('image_format', {})
                }
            },
            
            # Content Metadata
            'metadata': {
                'content_direction': kwargs['content_direction'],
                'content_type': kwargs['content_type'],
                'source_type': kwargs['source_type'],
                'topic': kwargs['specific_content'],
                'tone': kwargs['tone'],
                'region': kwargs['region'],
                'language': kwargs['language'],
                'generated_at': self._get_current_timestamp(),
                'platform': kwargs['content_type'].upper(),
                'content_category': kwargs['content_direction']
            },
            
            # Cultural and Direction Context
            'cultural_context': self._get_cultural_context(kwargs['region'], kwargs['content_direction']),
            'direction_context': kwargs['direction_context'] or {},
            
            # Enhanced Analytics Data
            'analytics': analytics_data,
            
            # Content Validation Results
            'validation': {
                'compliance_check': analytics_data['content_validation'],
                'quality_score': analytics_data['content_metrics']['content_quality_score'],
                'optimization_suggestions': self._generate_optimization_suggestions(content_text, kwargs['content_type'], analytics_data),
                'performance_insights': self._generate_performance_insights(kwargs['content_type'], analytics_data)
            },
            
            # Export Formats
            'export_formats': {
                'social_media_ready': True,
                'copy_paste_text': content_text,
                'hashtag_list': hashtags,
                'image_specifications': platform_specs.get('image_format', {}),
                'scheduling_recommendations': {
                    'optimal_time': analytics_data['platform_optimization']['optimal_posting_time'],
                    'best_days': analytics_data['platform_optimization']['best_posting_days'],
                    'frequency': analytics_data['platform_optimization']['recommended_frequency']
                }
            }
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
                    'post_images': {
                        'dimensions': '1024 x 576 pixels (16:9 aspect ratio)',
                        'stable_diffusion_dimensions': '1024 x 576',
                        'minimum': '200 x 200 pixels',
                        'file_types': 'JPG, PNG, GIF',
                        'max_file_size': '5MB',
                        'optimal_format': 'JPG for photos, PNG for infographics',
                        'stable_diffusion_note': 'Uses 16:9 ratio (closest to LinkedIn\'s 1.91:1)'
                    },
                    'profile_pictures': {
                        'dimensions': '400 x 400 pixels (square)',
                        'stable_diffusion_dimensions': '512 x 512',
                        'display_size': '300 x 300 pixels',
                        'file_types': 'JPG, PNG',
                        'max_file_size': '8MB'
                    },
                    'cover_images': {
                        'dimensions': '1584 x 396 pixels (4:1 aspect ratio)',
                        'stable_diffusion_dimensions': '1024 x 256',
                        'file_types': 'JPG, PNG',
                        'max_file_size': '8MB'
                    },
                    'company_logos': {
                        'dimensions': '300 x 300 pixels (square)',
                        'stable_diffusion_dimensions': '512 x 512',
                        'file_types': 'JPG, PNG',
                        'max_file_size': '4MB'
                    }
                },
                'content_structure': [
                    'Professional hook or insight',
                    'Main content with industry expertise',
                    'Data or example when relevant',
                    'Thought-provoking conclusion',
                    'Call-to-action for engagement',
                    '1-2 Professional Hashtags'
                ],
                'best_practices': [
                    'Lead with industry insights',
                    'Use professional language',
                    'Include data or statistics when possible',
                    'Focus on thought leadership',
                    'Keep hashtags minimal and professional',
                    'Encourage meaningful discussions'
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
                    'post_images': {
                        'dimensions': '1200 x 630 pixels (1.91:1 aspect ratio)',
                        'stable_diffusion_dimensions': '1024 x 576',
                        'minimum': '600 x 315 pixels',
                        'file_types': 'JPG, PNG, GIF',
                        'max_file_size': '4MB',
                        'optimal_format': 'JPG for photos, PNG for graphics with text',
                        'stable_diffusion_note': 'Uses 16:9 ratio (closest to Facebook\'s 1.91:1)'
                    },
                    'profile_pictures': {
                        'dimensions': '170 x 170 pixels (square)',
                        'stable_diffusion_dimensions': '512 x 512',
                        'display_size': '128 x 128 pixels',
                        'file_types': 'JPG, PNG',
                        'max_file_size': '4MB'
                    },
                    'cover_photos': {
                        'dimensions': '851 x 315 pixels (2.7:1 aspect ratio)',
                        'stable_diffusion_dimensions': '1024 x 384',
                        'mobile_display': '640 x 360 pixels',
                        'file_types': 'JPG, PNG',
                        'max_file_size': '4MB'
                    }
                },
                'content_structure': [
                    'Engaging Hook/Question',
                    'Main Content - 2-3 sentences',
                    'Personal touch or story',
                    'Call-to-Action',
                    '3-5 Relevant Hashtags'
                ],
                'best_practices': [
                    'Start with questions to encourage engagement',
                    'Use conversational language',
                    'Include personal anecdotes when relevant',
                    'End with questions to spark discussion',
                    'Use emojis strategically (2-3 per post)',
                    'Use high-quality, relevant visuals'
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
                    'square_posts': {
                        'dimensions': '1080 x 1080 pixels (1:1 aspect ratio)',
                        'stable_diffusion_dimensions': '1024 x 1024',
                        'minimum': '320 x 320 pixels',
                        'file_types': 'JPG, PNG',
                        'max_file_size': '8MB',
                        'optimal_format': 'JPG for photos, PNG for graphics',
                        'stable_diffusion_note': 'Perfect square ratio for Instagram posts'
                    },
                    'portrait_posts': {
                        'dimensions': '1080 x 1350 pixels (4:5 aspect ratio)',
                        'stable_diffusion_dimensions': '768 x 1024',
                        'minimum': '320 x 400 pixels',
                        'file_types': 'JPG, PNG',
                        'max_file_size': '8MB'
                    },
                    'landscape_posts': {
                        'dimensions': '1080 x 566 pixels (1.91:1 aspect ratio)',
                        'stable_diffusion_dimensions': '1024 x 576',
                        'minimum': '320 x 168 pixels',
                        'file_types': 'JPG, PNG',
                        'max_file_size': '8MB'
                    },
                    'stories': {
                        'dimensions': '1080 x 1920 pixels (9:16 aspect ratio)',
                        'stable_diffusion_dimensions': '576 x 1024',
                        'file_types': 'JPG, PNG, MP4',
                        'max_file_size': '4MB for images, 50MB for videos',
                        'duration': '1-15 seconds for videos'
                    },
                    'reels': {
                        'dimensions': '1080 x 1920 pixels (9:16 aspect ratio)',
                        'stable_diffusion_dimensions': '576 x 1024',
                        'file_types': 'MP4, MOV',
                        'max_file_size': '4GB',
                        'duration': '15-90 seconds',
                        'aspect_ratio': '9:16 (vertical)'
                    },
                    'igtv': {
                        'dimensions': '1080 x 1920 pixels (9:16) or 1920 x 1080 pixels (16:9)',
                        'stable_diffusion_dimensions': '576 x 1024 or 1024 x 576',
                        'file_types': 'MP4',
                        'max_file_size': '650MB',
                        'duration': '15 seconds - 60 minutes'
                    }
                },
                'content_structure': [
                    'Eye-catching first line',
                    'Main content with line breaks',
                    'Personal insight or tip',
                    'Question or call-to-action',
                    '5-10 Relevant Hashtags'
                ],
                'best_practices': [
                    'Use line breaks for readability',
                    'Include emojis throughout (5-8 per post)',
                    'Focus on visual descriptions',
                    'Use aesthetic and inspirational language',
                    'Include location tags when relevant',
                    'End with engaging questions',
                    'Use high-quality, visually appealing images',
                    'Maintain consistent brand colors'
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
                    'tweet_images': {
                        'dimensions': '1200 x 675 pixels (16:9 aspect ratio)',
                        'stable_diffusion_dimensions': '1024 x 576',
                        'minimum': '300 x 157 pixels',
                        'file_types': 'JPG, PNG, GIF, WebP',
                        'max_file_size': '5MB',
                        'optimal_format': 'JPG for photos, PNG for graphics',
                        'stable_diffusion_note': 'Perfect 16:9 ratio for Twitter'
                    },
                    'profile_pictures': {
                        'dimensions': '400 x 400 pixels (square)',
                        'stable_diffusion_dimensions': '512 x 512',
                        'display_size': '200 x 200 pixels',
                        'file_types': 'JPG, PNG, GIF',
                        'max_file_size': '2MB'
                    },
                    'header_images': {
                        'dimensions': '1500 x 500 pixels (3:1 aspect ratio)',
                        'stable_diffusion_dimensions': '1024 x 384',
                        'file_types': 'JPG, PNG, GIF',
                        'max_file_size': '5MB'
                    },
                    'gifs': {
                        'max_file_size': '15MB',
                        'duration': 'Up to 5 seconds',
                        'dimensions': 'Same as regular images'
                    }
                },
                'content_structure': [
                    'Concise, impactful message',
                    'Clear call-to-action',
                    '1-2 Relevant Hashtags'
                ],
                'best_practices': [
                    'Be concise and direct',
                    'Use trending hashtags when relevant',
                    'Include clear calls-to-action',
                    'Focus on shareable content',
                    'Use abbreviations when necessary',
                    'Keep hashtags to minimum',
                    'Use eye-catching, shareable visuals',
                    'Use animated content for higher engagement'
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
                    'shorts': {
                        'dimensions': '1080 x 1920 pixels (9:16 aspect ratio)',
                        'file_types': 'MP4, MOV, AVI',
                        'max_file_size': '256GB',
                        'duration': '15-60 seconds',
                        'frame_rate': '24-60 fps',
                        'resolution': '720p minimum, 1080p recommended'
                    },
                    'thumbnails': {
                        'dimensions': '1280 x 720 pixels (16:9 aspect ratio)',
                        'stable_diffusion_dimensions': '1024 x 576',
                        'file_types': 'JPG, PNG',
                        'max_file_size': '2MB',
                        'optimal_format': 'JPG for photos, PNG for graphics with text',
                        'stable_diffusion_note': 'Perfect 16:9 ratio for YouTube thumbnails'
                    },
                    'channel_icons': {
                        'dimensions': '800 x 800 pixels (square)',
                        'stable_diffusion_dimensions': '512 x 512',
                        'display_size': '98 x 98 pixels',
                        'file_types': 'JPG, PNG, GIF',
                        'max_file_size': '2MB'
                    },
                    'channel_banners': {
                        'dimensions': '2560 x 1440 pixels (16:9 aspect ratio)',
                        'stable_diffusion_dimensions': '1024 x 576',
                        'file_types': 'JPG, PNG',
                        'max_file_size': '6MB'
                    }
                },
                'content_structure': [
                    'Hook - First 3 seconds',
                    'Problem identification',
                    'Solution or insight',
                    'Call-to-action',
                    'Voiceover instructions'
                ],
                'best_practices': [
                    'Start with a strong hook',
                    'Keep sentences short and clear',
                    'Include clear voiceover instructions',
                    'Focus on one main point',
                    'End with strong call-to-action',
                    'Use conversational tone',
                    'Use high-resolution footage',
                    'Ensure clear, high-quality audio',
                    'Create compelling, clickable thumbnails'
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
                    'featured_images': {
                        'dimensions': '1200 x 630 pixels (1.91:1 aspect ratio)',
                        'stable_diffusion_dimensions': '1024 x 576',
                        'minimum': '600 x 315 pixels',
                        'file_types': 'JPG, PNG, WebP',
                        'max_file_size': '5MB',
                        'optimal_format': 'JPG for photos, PNG for graphics',
                        'stable_diffusion_note': 'Uses 16:9 ratio (closest to blog\'s 1.91:1)'
                    },
                    'inline_images': {
                        'dimensions': '800 x 600 pixels (4:3 aspect ratio)',
                        'stable_diffusion_dimensions': '768 x 576',
                        'file_types': 'JPG, PNG, WebP',
                        'max_file_size': '2MB',
                        'responsive': 'Should scale well on mobile'
                    },
                    'infographics': {
                        'dimensions': '1200 x 800 pixels (3:2 aspect ratio)',
                        'stable_diffusion_dimensions': '1024 x 768',
                        'file_types': 'PNG, SVG',
                        'max_file_size': '5MB',
                        'optimal_format': 'PNG for web, SVG for scalable graphics'
                    },
                    'social_media_previews': {
                        'dimensions': '1200 x 630 pixels (1.91:1 aspect ratio)',
                        'stable_diffusion_dimensions': '1024 x 576',
                        'file_types': 'JPG, PNG',
                        'max_file_size': '5MB'
                    }
                },
                'content_structure': [
                    'SEO-optimized title',
                    'Introduction with hook',
                    'Main content with headings',
                    'Subheadings for organization',
                    'Conclusion with takeaways',
                    'Call-to-action'
                ],
                'best_practices': [
                    'Use SEO-optimized headings',
                    'Include relevant keywords naturally',
                    'Break content into digestible sections',
                    'Provide actionable insights',
                    'Include internal and external links',
                    'Use bullet points and lists',
                    'Use high-quality, relevant visuals',
                    'Include descriptive alt text for SEO',
                    'Compress images for faster loading'
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
                'engagement_potential': 'medium',  # Will be calculated
                'content_quality_score': 0,  # Will be calculated
                'seo_score': 0,  # For blog content
                'visual_appeal_score': 0  # For image-heavy platforms
            },
            'platform_optimization': {
                'optimal_posting_time': self._get_optimal_posting_time(content_type),
                'recommended_frequency': self._get_recommended_frequency(content_type),
                'audience_demographics': self._get_audience_demographics(content_type),
                'content_lifecycle': self._get_content_lifecycle(content_type),
                'best_posting_days': self._get_best_posting_days(content_type),
                'peak_engagement_hours': self._get_peak_engagement_hours(content_type)
            },
            'performance_predictions': {
                'estimated_reach': 'medium',
                'estimated_engagement': 'medium',
                'estimated_clicks': 'low',
                'viral_potential': 'low',
                'conversion_potential': 'low',
                'brand_awareness_impact': 'medium'
            },
            'content_validation': {
                'length_compliance': True,  # Check against platform limits
                'hashtag_optimization': 'optimal',  # optimal, good, needs_improvement
                'tone_consistency': True,  # Check against selected tone
                'cultural_sensitivity': True,  # Regional appropriateness
                'brand_consistency': True,  # Style alignment
                'accessibility_score': 0  # Inclusive content practices
            },
            'visual_performance': {
                'image_load_time': 'fast',  # fast, medium, slow
                'visual_engagement_potential': 'medium',
                'brand_recognition_score': 0,
                'accessibility_compliance': True,  # Alt text, screen reader support
                'mobile_optimization': True,
                'responsive_design_score': 0
            },
            'engagement_optimization': {
                'click_through_rate_potential': 'medium',
                'engagement_rate_potential': 'medium',
                'reach_optimization': 'medium',
                'conversion_tracking_ready': True,
                'call_to_action_effectiveness': 'medium',
                'shareability_score': 0
            },
            'quality_assurance': {
                'content_uniqueness': True,  # Plagiarism checking
                'brand_consistency': True,  # Tone and style alignment
                'seo_optimization': True,  # Search engine visibility
                'accessibility': True,  # Inclusive content practices
                'cultural_relevance': True,  # Regional appropriateness
                'technical_compliance': True  # Platform requirements
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
    
    def _get_best_posting_days(self, content_type):
        """Get best posting days for content type"""
        days = {
            'linkedin': 'Tuesday, Wednesday, Thursday',
            'facebook': 'Tuesday, Wednesday, Thursday, Friday',
            'instagram': 'Wednesday, Thursday, Friday',
            'twitter': 'Monday, Tuesday, Wednesday, Thursday',
            'youtube_shorts': 'Monday, Tuesday, Wednesday, Thursday',
            'blog': 'Tuesday, Wednesday, Thursday'
        }
        return days.get(content_type, 'Varies by platform')
    
    def _get_peak_engagement_hours(self, content_type):
        """Get peak engagement hours for content type"""
        hours = {
            'linkedin': '8-10 AM, 5-6 PM (EST)',
            'facebook': '1-3 PM, 7-9 PM (EST)',
            'instagram': '11 AM-1 PM, 7-9 PM (EST)',
            'twitter': '8-10 AM, 6-9 PM (EST)',
            'youtube_shorts': '2-4 PM, 7-9 PM (EST)',
            'blog': '9-11 AM (EST)'
        }
        return hours.get(content_type, 'Varies by platform')
    
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
        """Get cultural context for region and content direction"""
        # Placeholder for cultural context logic
        return {
            'region': region,
            'content_direction': content_direction,
            'cultural_considerations': 'Standard global content',
            'local_relevance': 'High',
            'sensitivity_notes': 'None'
        }
    
    def _calculate_readability_score(self, content):
        """Calculate readability score for content"""
        # Simple Flesch Reading Ease approximation
        words = content.split()
        sentences = content.split('.')
        syllables = sum(self._count_syllables(word) for word in words)
        
        if len(words) == 0 or len(sentences) == 0:
            return 0
        
        # Flesch Reading Ease formula approximation
        score = 206.835 - (1.015 * (len(words) / len(sentences))) - (84.6 * (syllables / len(words)))
        return max(0, min(100, score))
    
    def _count_syllables(self, word):
        """Count syllables in a word (approximation)"""
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        on_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not on_vowel:
                count += 1
            on_vowel = is_vowel
        
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count = 1
        return count
    
    def _calculate_engagement_potential(self, content, content_type):
        """Calculate engagement potential score"""
        score = 50  # Base score
        
        # Factors that increase engagement
        if '?' in content:  # Questions
            score += 15
        if any(word in content.lower() for word in ['you', 'your', 'we', 'us']):  # Personal pronouns
            score += 10
        if any(word in content.lower() for word in ['amazing', 'incredible', 'awesome', 'fantastic']):  # Emotional words
            score += 10
        if len(self._extract_hashtags(content)) > 0:  # Hashtags
            score += 5
        
        # Platform-specific adjustments
        if content_type == 'instagram':
            if content.count('\n') > 3:  # Line breaks
                score += 10
        elif content_type == 'linkedin':
            if any(word in content.lower() for word in ['industry', 'professional', 'business']):
                score += 10
        
        return min(100, score)
    
    def _calculate_content_quality_score(self, content, content_type):
        """Calculate content quality score"""
        score = 70  # Base score
        
        # Length appropriateness
        if content_type == 'twitter' and len(content) <= 280:
            score += 10
        elif content_type == 'linkedin' and len(content) <= 1300:
            score += 10
        elif content_type == 'instagram' and len(content) <= 2200:
            score += 10
        
        # Hashtag optimization
        hashtags = self._extract_hashtags(content)
        if content_type == 'twitter' and 1 <= len(hashtags) <= 2:
            score += 10
        elif content_type == 'instagram' and 5 <= len(hashtags) <= 10:
            score += 10
        
        # Call-to-action presence
        if self._extract_call_to_action(content):
            score += 10
        
        return min(100, score)
    
    def _calculate_seo_score(self, content):
        """Calculate SEO score for blog content"""
        score = 60  # Base score
        
        # Word count (blog should be 1500-2500 words)
        word_count = len(content.split())
        if 1500 <= word_count <= 2500:
            score += 20
        elif 1000 <= word_count < 1500:
            score += 10
        
        # Headings presence
        if '#' in content or any(word in content for word in ['Introduction', 'Conclusion', 'Summary']):
            score += 10
        
        # Keywords (basic check)
        if any(word in content.lower() for word in ['how', 'what', 'why', 'when', 'where']):
            score += 10
        
        return min(100, score)
    
    def _calculate_visual_appeal_score(self, content, content_type):
        """Calculate visual appeal score"""
        score = 50  # Base score
        
        # Emoji usage
        emoji_count = content.count('😀') + content.count('😃') + content.count('😄') + content.count('😁')
        if content_type == 'instagram' and emoji_count >= 5:
            score += 20
        elif emoji_count >= 2:
            score += 10
        
        # Line breaks for visual appeal
        if content.count('\n') >= 3:
            score += 10
        
        # Visual descriptive words
        visual_words = ['beautiful', 'stunning', 'amazing', 'incredible', 'gorgeous', 'perfect']
        if any(word in content.lower() for word in visual_words):
            score += 10
        
        return min(100, score)
    
    def _check_length_compliance(self, character_count, content_type):
        """Check if content length complies with platform limits"""
        limits = {
            'linkedin': 1300,
            'facebook': 63206,
            'instagram': 2200,
            'twitter': 280,
            'youtube_shorts': 200,
            'blog': 2500
        }
        return character_count <= limits.get(content_type, float('inf'))
    
    def _check_hashtag_optimization(self, hashtag_count, content_type):
        """Check hashtag optimization for platform"""
        optimal_ranges = {
            'linkedin': (1, 2),
            'facebook': (3, 5),
            'instagram': (5, 10),
            'twitter': (1, 2),
            'youtube_shorts': (0, 3),
            'blog': (0, 5)
        }
        
        min_hashtags, max_hashtags = optimal_ranges.get(content_type, (0, 5))
        
        if min_hashtags <= hashtag_count <= max_hashtags:
            return 'optimal'
        elif hashtag_count < min_hashtags:
            return 'needs_more_hashtags'
        else:
            return 'too_many_hashtags'
    
    def _check_tone_consistency(self, content, tone):
        """Check if content tone is consistent with selected tone"""
        # Basic tone checking logic
        professional_words = ['industry', 'professional', 'business', 'strategy', 'leadership']
        casual_words = ['awesome', 'cool', 'amazing', 'great', 'love']
        inspirational_words = ['inspire', 'motivate', 'dream', 'achieve', 'success']
        
        content_lower = content.lower()
        
        if tone == 'professional' and any(word in content_lower for word in professional_words):
            return True
        elif tone == 'casual' and any(word in content_lower for word in casual_words):
            return True
        elif tone == 'inspirational' and any(word in content_lower for word in inspirational_words):
            return True
        
        return True  # Default to True for now
    
    def _check_cultural_sensitivity(self, content, region):
        """Check cultural sensitivity for region"""
        # Placeholder for cultural sensitivity checking
        return True
    
    def _calculate_accessibility_score(self, content):
        """Calculate accessibility score"""
        score = 70  # Base score
        
        # Check for clear language
        if len(content.split()) <= 20:  # Short, clear content
            score += 15
        
        # Check for simple sentence structure
        sentences = content.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        if avg_sentence_length <= 15:
            score += 15
        
        return min(100, score)
    
    def _generate_optimization_suggestions(self, content, content_type, analytics_data):
        """Generate optimization suggestions"""
        suggestions = []
        
        # Length suggestions
        if not analytics_data['content_validation']['length_compliance']:
            suggestions.append(f"Content exceeds {content_type} character limit")
        
        # Hashtag suggestions
        hashtag_status = analytics_data['content_validation']['hashtag_optimization']
        if hashtag_status == 'needs_more_hashtags':
            suggestions.append(f"Add more hashtags for better {content_type} reach")
        elif hashtag_status == 'too_many_hashtags':
            suggestions.append(f"Reduce hashtag count for better {content_type} performance")
        
        # Engagement suggestions
        if analytics_data['content_metrics']['engagement_potential'] == 'low':
            suggestions.append("Add questions or call-to-action to increase engagement")
        
        return suggestions
    
    def _generate_performance_insights(self, content_type, analytics_data):
        """Generate performance insights"""
        insights = []
        
        # Platform-specific insights
        if content_type == 'linkedin':
            insights.append("Professional tone and industry insights perform best")
        elif content_type == 'instagram':
            insights.append("Visual descriptions and emojis increase engagement")
        elif content_type == 'twitter':
            insights.append("Concise, trending content gets more retweets")
        
        # Timing insights
        optimal_time = analytics_data['platform_optimization']['optimal_posting_time']
        insights.append(f"Post during {optimal_time} for maximum reach")
        
        return insights 