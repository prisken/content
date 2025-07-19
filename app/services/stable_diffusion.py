import requests
import base64
import json
from flask import current_app
import os

class StableDiffusionService:
    """Stable Diffusion image generation service"""
    
    def __init__(self):
        self.api_key = "sk-4LYzKcgv6IQ5qVtXBNTZD6j8oeo3NVToOWAar2ykfD8Ux5IW"
        self.api_base = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        
        # Stable Diffusion supported aspect ratios and dimensions
        self.supported_ratios = {
            '1:1': {'width': 1024, 'height': 1024},      # Square
            '16:9': {'width': 1024, 'height': 576},      # Landscape
            '9:16': {'width': 576, 'height': 1024}       # Portrait
        }
        
        # Platform-specific image configurations (adjusted to supported ratios)
        self.platform_configs = {
            'facebook': {
                'width': 1024,
                'height': 576,
                'aspect_ratio': '16:9',
                'style': 'social media post, professional, engaging',
                'format': 'JPG',
                'note': 'Uses 16:9 ratio (closest to Facebook\'s 1.91:1)'
            },
            'instagram': {
                'width': 1024,
                'height': 1024,
                'aspect_ratio': '1:1',
                'style': 'aesthetic, visual storytelling, inspirational',
                'format': 'JPG',
                'note': 'Perfect square ratio for Instagram posts'
            },
            'linkedin': {
                'width': 1024,
                'height': 576,
                'aspect_ratio': '16:9',
                'style': 'professional, business, corporate',
                'format': 'JPG',
                'note': 'Uses 16:9 ratio (closest to LinkedIn\'s 1.91:1)'
            },
            'twitter': {
                'width': 1024,
                'height': 576,
                'aspect_ratio': '16:9',
                'style': 'trending, engaging, shareable',
                'format': 'JPG',
                'note': 'Perfect 16:9 ratio for Twitter'
            },
            'youtube_shorts': {
                'width': 576,
                'height': 1024,
                'aspect_ratio': '9:16',
                'style': 'video thumbnail, clickable, engaging',
                'format': 'JPG',
                'note': 'Perfect 9:16 ratio for YouTube Shorts'
            },
            'blog': {
                'width': 1024,
                'height': 576,
                'aspect_ratio': '16:9',
                'style': 'featured image, professional, informative',
                'format': 'JPG',
                'note': 'Uses 16:9 ratio (closest to blog\'s 1.91:1)'
            }
        }
        
        # Content direction to visual style mapping
        self.direction_styles = {
            'business_finance': 'professional business setting, corporate environment, financial charts, modern office',
            'technology': 'digital technology, futuristic, computer screens, innovation, tech workspace',
            'health_wellness': 'healthy lifestyle, wellness, fitness, natural environment, medical professional',
            'education': 'learning environment, books, classroom, academic setting, knowledge sharing',
            'entertainment': 'creative arts, entertainment industry, performance, media, cultural events',
            'travel_tourism': 'travel destinations, landscapes, tourism, adventure, cultural experiences',
            'food_cooking': 'culinary arts, food preparation, restaurant, cooking, delicious meals',
            'fashion_beauty': 'fashion industry, beauty, style, runway, trendy clothing',
            'sports_fitness': 'athletic activities, sports equipment, fitness training, competition',
            'science_research': 'scientific research, laboratory, experiments, discovery, innovation',
            'politics_current_events': 'political events, news, current affairs, government, social issues',
            'environment_sustainability': 'environmental protection, sustainability, nature, green technology',
            'personal_development': 'self-improvement, motivation, growth, personal success, achievement',
            'parenting_family': 'family life, parenting, children, home environment, family activities',
            'art_creativity': 'artistic expression, creativity, design, artistic process, creative workspace',
            'real_estate': 'real estate, property, architecture, home design, construction',
            'automotive': 'automotive industry, cars, vehicles, transportation, automotive technology',
            'pet_care': 'pet care, animals, veterinary, pet health, animal companionship'
        }
        
        # Tone to visual style mapping
        self.tone_styles = {
            'professional': 'clean, sophisticated, corporate, polished',
            'casual': 'relaxed, friendly, approachable, comfortable',
            'inspirational': 'uplifting, motivational, bright, positive energy',
            'educational': 'informative, clear, organized, learning-focused',
            'entertaining': 'fun, vibrant, engaging, playful'
        }
    
    def generate_image(self, platform, content_direction, topic, tone, language='en'):
        """Generate image based on platform and content specifications"""
        try:
            # Get platform configuration
            platform_config = self.platform_configs.get(platform, self.platform_configs['facebook'])
            
            # Validate aspect ratio is supported
            if platform_config['aspect_ratio'] not in self.supported_ratios:
                # Fallback to 16:9 if unsupported
                platform_config = self.platform_configs['facebook']
            
            # Build prompt based on content direction and topic
            base_prompt = self._build_image_prompt(content_direction, topic, tone, platform)
            
            # Generate image using Stable Diffusion API
            image_data = self._call_stable_diffusion_api(
                prompt=base_prompt,
                width=platform_config['width'],
                height=platform_config['height']
            )
            
            # Create response with platform-specific metadata
            response = {
                'image_data': image_data,
                'platform': platform,
                'dimensions': {
                    'width': platform_config['width'],
                    'height': platform_config['height'],
                    'aspect_ratio': platform_config['aspect_ratio']
                },
                'format': platform_config['format'],
                'file_size': len(image_data) if image_data else 0,
                'prompt_used': base_prompt,
                'content_direction': content_direction,
                'topic': topic,
                'tone': tone,
                'language': language,
                'stable_diffusion_note': platform_config['note']
            }
            
            return response
            
        except Exception as e:
            current_app.logger.error(f"Error generating image: {str(e)}")
            return {
                'error': f"Failed to generate image: {str(e)}",
                'platform': platform,
                'content_direction': content_direction,
                'topic': topic
            }
    
    def _build_image_prompt(self, content_direction, topic, tone, platform):
        """Build image generation prompt based on content specifications"""
        # Get base style from content direction
        direction_style = self.direction_styles.get(content_direction, 'professional business setting')
        
        # Get tone style
        tone_style = self.tone_styles.get(tone, 'professional')
        
        # Get platform style
        platform_style = self.platform_configs[platform]['style']
        
        # Build comprehensive prompt
        prompt = f"High-quality {platform_style} image featuring {direction_style}, {tone_style} style, related to {topic}, professional photography, 4K resolution, detailed, realistic"
        
        # Add negative prompt to avoid unwanted elements
        negative_prompt = "blurry, low quality, distorted, unrealistic, cartoon, anime, text overlay, watermark, logo"
        
        return {
            'text_prompts': [
                {
                    'text': prompt,
                    'weight': 1.0
                },
                {
                    'text': negative_prompt,
                    'weight': -1.0
                }
            ]
        }
    
    def _call_stable_diffusion_api(self, prompt, width, height):
        """Call Stable Diffusion API to generate image"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            data = {
                'text_prompts': prompt['text_prompts'],
                'cfg_scale': 7,
                'height': height,
                'width': width,
                'samples': 1,
                'steps': 30,
                'style_preset': 'photographic'
            }
            
            response = requests.post(
                self.api_base,
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'artifacts' in result and len(result['artifacts']) > 0:
                    # Return base64 encoded image data
                    image_data = result['artifacts'][0]['base64']
                    return image_data
                else:
                    raise Exception("No image generated in response")
            else:
                error_data = response.json() if response.content else {}
                raise Exception(f"API Error: {response.status_code} - {error_data.get('message', 'Unknown error')}")
                
        except Exception as e:
            current_app.logger.error(f"Stable Diffusion API error: {str(e)}")
            raise e
    
    def generate_multiple_images(self, platform, content_direction, topic, tone, count=3):
        """Generate multiple image variations"""
        images = []
        
        for i in range(count):
            try:
                # Slightly vary the prompt for each image
                varied_topic = f"{topic} - variation {i+1}"
                image_result = self.generate_image(platform, content_direction, varied_topic, tone)
                images.append(image_result)
            except Exception as e:
                current_app.logger.error(f"Error generating image variation {i+1}: {str(e)}")
                continue
        
        return images
    
    def get_platform_image_specs(self, platform):
        """Get image specifications for a specific platform"""
        return self.platform_configs.get(platform, {})
    
    def get_supported_ratios(self):
        """Get list of supported aspect ratios"""
        return list(self.supported_ratios.keys())
    
    def validate_image_requirements(self, platform, image_data):
        """Validate if generated image meets platform requirements"""
        platform_config = self.platform_configs.get(platform, {})
        
        if not image_data:
            return False, "No image data provided"
        
        # Check if aspect ratio is supported
        if platform_config.get('aspect_ratio') not in self.supported_ratios:
            return False, f"Aspect ratio {platform_config.get('aspect_ratio')} not supported by Stable Diffusion"
        
        # Check file size (approximate for base64)
        file_size = len(image_data) * 0.75  # Base64 to bytes approximation
        max_size = {
            'facebook': 4 * 1024 * 1024,  # 4MB
            'instagram': 8 * 1024 * 1024,  # 8MB
            'linkedin': 5 * 1024 * 1024,   # 5MB
            'twitter': 5 * 1024 * 1024,    # 5MB
            'youtube_shorts': 2 * 1024 * 1024,  # 2MB
            'blog': 5 * 1024 * 1024        # 5MB
        }.get(platform, 5 * 1024 * 1024)
        
        if file_size > max_size:
            return False, f"Image file size ({file_size:.2f}MB) exceeds platform limit ({max_size/1024/1024:.0f}MB)"
        
        return True, "Image meets platform requirements" 