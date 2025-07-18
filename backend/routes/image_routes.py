from flask import Blueprint, request, jsonify, session
from models import db, Image, User
from datetime import datetime
import uuid
import cloudinary
import cloudinary.uploader
import cloudinary.api
from PIL import Image as PILImage, ImageDraw, ImageFont
import io
import os

image_routes = Blueprint('images', __name__)

def generate_image_id():
    """Generate unique image ID"""
    return f"IMG{uuid.uuid4().hex[:8].upper()}"

@image_routes.route('/generate', methods=['POST'])
def generate_image():
    """Generate AI image based on content and style"""
    try:
        if 'user' not in session:
            return jsonify({
                'success': False,
                'error': 'User not logged in'
            }), 401
        
        data = request.get_json()
        user_email = session['user']
        user = User.query.get(user_email)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Check user image limits
        current_image_count = Image.query.filter_by(user_email=user_email).count()
        if current_image_count >= user.image_limit:
            return jsonify({
                'success': False,
                'error': f'Image limit reached ({user.image_limit}). Upgrade your subscription for more images.'
            }), 403
        
        # Extract parameters
        content_text = data.get('content', '')
        image_style = data.get('image_style', 'modern')
        platform = data.get('platform', 'linkedin')
        direction = data.get('direction', 'business_finance')
        
        # Generate image prompt
        image_prompt = generate_image_prompt(content_text, image_style, platform, direction)
        
        # Create mock image (replace with actual AI generation)
        image_url = create_mock_image(image_prompt, image_style, user_email)
        
        return jsonify({
            'success': True,
            'image_url': image_url,
            'prompt': image_prompt,
            'style': image_style,
            'message': 'Image generated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def generate_image_prompt(content_text, image_style, platform, direction):
    """Generate image prompt based on content and style"""
    # Extract key themes from content
    themes = extract_content_themes(content_text, direction)
    
    # Style-specific prompts
    style_prompts = {
        'modern': 'modern, clean, minimalist design with',
        'vintage': 'vintage, retro, classic aesthetic with',
        'abstract': 'abstract, artistic, creative composition with',
        'photorealistic': 'photorealistic, detailed, high-quality image of',
        'cartoon': 'cartoon, illustrated, animated style with',
        'corporate': 'professional, corporate, business setting with',
        'nature': 'natural, organic, earthy elements with',
        'tech': 'futuristic, digital, technological aesthetic with',
        'elegant': 'elegant, sophisticated, luxury feel with'
    }
    
    style_prompt = style_prompts.get(image_style, 'modern, clean design with')
    
    # Platform-specific adjustments
    platform_adjustments = {
        'linkedin': 'professional business context',
        'facebook': 'social, friendly context',
        'instagram': 'visual, aesthetic context',
        'twitter': 'concise, impactful context',
        'youtube': 'dynamic, engaging context',
        'blog': 'detailed, informative context'
    }
    
    platform_context = platform_adjustments.get(platform, 'general context')
    
    # Combine into final prompt
    prompt = f"{style_prompt} {themes} in {platform_context}, high quality, trending on artstation"
    
    return prompt

def extract_content_themes(content_text, direction):
    """Extract key themes from content for image generation"""
    direction_themes = {
        'business_finance': 'business charts, financial graphs, professional office setting',
        'technology': 'digital technology, computer screens, innovation concepts',
        'health_wellness': 'health and wellness, fitness, medical concepts',
        'education': 'learning, books, academic setting',
        'entertainment': 'entertainment, media, creative arts',
        'travel_tourism': 'travel destinations, tourism, adventure',
        'food_cooking': 'food, cooking, culinary arts',
        'fashion_beauty': 'fashion, beauty, style',
        'sports_fitness': 'sports, fitness, athletic activities',
        'science_research': 'scientific research, laboratory, innovation',
        'politics_news': 'news, politics, current events',
        'environment': 'environmental protection, nature, sustainability',
        'personal_dev': 'personal development, growth, self-improvement',
        'parenting_family': 'family, parenting, children',
        'art_creativity': 'art, creativity, artistic expression',
        'real_estate': 'real estate, property, architecture',
        'automotive': 'automotive, cars, transportation',
        'pet_care': 'pets, animals, pet care'
    }
    
    return direction_themes.get(direction, 'general business concept')

def create_mock_image(prompt, style, user_email):
    """Create a mock image and upload to Cloudinary"""
    try:
        # Create a simple placeholder image using PIL
        img = PILImage.new('RGB', (1200, 630), color='#667EEA')
        draw = ImageDraw.Draw(img)
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Draw title
        draw.text((600, 200), "AI Generated Image", fill='white', anchor='mm', font=font)
        draw.text((600, 280), f"Style: {style.title()}", fill='white', anchor='mm', font=font)
        draw.text((600, 360), "Content Creator Pro", fill='white', anchor='mm', font=font)
        
        # Save to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            img_bytes,
            folder=f"content_creator/{user_email.replace('@', '_at_')}",
            public_id=f"generated_{style}_{uuid.uuid4().hex[:8]}",
            overwrite=True
        )
        
        # Create database record
        image_record = Image(
            id=generate_image_id(),
            user_email=user_email,
            filename=result['public_id'],
            original_filename=f"generated_{style}.png",
            file_path=result['secure_url'],
            file_size=result['bytes'],
            mime_type='image/png',
            width=1200,
            height=630,
            alt_text=f"AI generated image in {style} style",
            caption=prompt[:100] + "..." if len(prompt) > 100 else prompt
        )
        
        db.session.add(image_record)
        db.session.commit()
        
        return result['secure_url']
        
    except Exception as e:
        # Fallback: return a placeholder URL
        return "https://via.placeholder.com/1200x630/667EEA/FFFFFF?text=AI+Generated+Image"

@image_routes.route('/upload', methods=['POST'])
def upload_image():
    """Upload image file"""
    try:
        if 'user' not in session:
            return jsonify({
                'success': False,
                'error': 'User not logged in'
            }), 401
        
        user_email = session['user']
        user = User.query.get(user_email)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Check if file was uploaded
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No image file selected'
            }), 400
        
        # Check user image limits
        current_image_count = Image.query.filter_by(user_email=user_email).count()
        if current_image_count >= user.image_limit:
            return jsonify({
                'success': False,
                'error': f'Image limit reached ({user.image_limit}). Upgrade your subscription for more images.'
            }), 403
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file,
            folder=f"content_creator/{user_email.replace('@', '_at_')}",
            public_id=f"uploaded_{uuid.uuid4().hex[:8]}",
            overwrite=True
        )
        
        # Create database record
        image_record = Image(
            id=generate_image_id(),
            user_email=user_email,
            filename=result['public_id'],
            original_filename=file.filename,
            file_path=result['secure_url'],
            file_size=result['bytes'],
            mime_type=result['format'],
            width=result.get('width'),
            height=result.get('height')
        )
        
        db.session.add(image_record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'image_id': image_record.id,
            'image_url': result['secure_url'],
            'filename': file.filename,
            'file_size': result['bytes'],
            'width': result.get('width'),
            'height': result.get('height'),
            'message': 'Image uploaded successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@image_routes.route('/list', methods=['GET'])
def list_images():
    """Get user's images"""
    try:
        if 'user' not in session:
            return jsonify({
                'success': False,
                'error': 'User not logged in'
            }), 401
        
        user_email = session['user']
        images = Image.query.filter_by(user_email=user_email).order_by(Image.created_at.desc()).all()
        
        image_list = []
        for img in images:
            image_list.append({
                'id': img.id,
                'filename': img.original_filename,
                'file_size': img.file_size,
                'width': img.width,
                'height': img.height,
                'mime_type': img.mime_type,
                'created_at': img.created_at.isoformat(),
                'content_id': img.content_id,
                'alt_text': img.alt_text,
                'caption': img.caption,
                'url': img.file_path
            })
        
        return jsonify({
            'success': True,
            'images': image_list,
            'total': len(image_list)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 