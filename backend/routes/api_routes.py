from flask import Blueprint, request, jsonify, session
from models import db, User, Content
import uuid
import random
from sqlalchemy import text

# Import AI service
try:
    from services.ai_service import ai_service
    AI_SERVICE_AVAILABLE = True
except ImportError:
    AI_SERVICE_AVAILABLE = False
    print("Warning: AI service not available. Using fallback content generation.")

api_routes = Blueprint('api', __name__)

# Content directions mapping
CONTENT_DIRECTIONS = {
    'business_finance': {
        'name': 'Business & Finance',
        'topics': ['Market Analysis', 'Investment Strategies', 'Business Growth', 'Financial Planning', 'Entrepreneurship', 'Corporate Strategy', 'Economic Trends', 'Startup Advice']
    },
    'technology': {
        'name': 'Technology',
        'topics': ['AI & Machine Learning', 'Software Development', 'Cybersecurity', 'Cloud Computing', 'Digital Transformation', 'Tech Trends', 'Programming', 'Innovation']
    },
    'health_wellness': {
        'name': 'Health & Wellness',
        'topics': ['Mental Health', 'Physical Fitness', 'Nutrition', 'Wellness Tips', 'Medical Advances', 'Healthy Living', 'Mindfulness', 'Work-Life Balance']
    },
    'education': {
        'name': 'Education',
        'topics': ['Learning Strategies', 'Online Education', 'Skill Development', 'Academic Success', 'Teaching Methods', 'Educational Technology', 'Career Development', 'Lifelong Learning']
    },
    'entertainment': {
        'name': 'Entertainment',
        'topics': ['Movies & TV', 'Music', 'Gaming', 'Celebrity News', 'Streaming Services', 'Pop Culture', 'Arts & Culture', 'Entertainment Industry']
    },
    'travel_tourism': {
        'name': 'Travel & Tourism',
        'topics': ['Travel Destinations', 'Travel Tips', 'Adventure Travel', 'Cultural Experiences', 'Budget Travel', 'Luxury Travel', 'Travel Planning', 'Tourism Industry']
    },
    'food_cooking': {
        'name': 'Food & Cooking',
        'topics': ['Recipes', 'Cooking Tips', 'Food Trends', 'Restaurant Reviews', 'Healthy Eating', 'Culinary Arts', 'Food Culture', 'Kitchen Gadgets']
    },
    'fashion_beauty': {
        'name': 'Fashion & Beauty',
        'topics': ['Fashion Trends', 'Beauty Tips', 'Style Advice', 'Skincare', 'Makeup Tutorials', 'Sustainable Fashion', 'Fashion Industry', 'Personal Style']
    },
    'sports_fitness': {
        'name': 'Sports & Fitness',
        'topics': ['Sports News', 'Fitness Tips', 'Athletic Performance', 'Sports Analysis', 'Workout Routines', 'Sports Industry', 'Athlete Profiles', 'Sports Technology']
    },
    'science_research': {
        'name': 'Science & Research',
        'topics': ['Scientific Discoveries', 'Research Findings', 'Space Exploration', 'Climate Science', 'Medical Research', 'Technology Innovation', 'Scientific Breakthroughs', 'Research Methods']
    },
    'politics_news': {
        'name': 'Politics & News',
        'topics': ['Current Events', 'Political Analysis', 'Policy Issues', 'International Relations', 'Election Coverage', 'Government News', 'Social Issues', 'Political Commentary']
    },
    'environment': {
        'name': 'Environment',
        'topics': ['Climate Change', 'Sustainability', 'Environmental Protection', 'Green Technology', 'Conservation', 'Renewable Energy', 'Environmental Policy', 'Eco-friendly Living']
    },
    'personal_dev': {
        'name': 'Personal Development',
        'topics': ['Self-Improvement', 'Goal Setting', 'Productivity Tips', 'Leadership Skills', 'Communication', 'Time Management', 'Motivation', 'Success Stories']
    },
    'parenting_family': {
        'name': 'Parenting & Family',
        'topics': ['Parenting Tips', 'Child Development', 'Family Activities', 'Education', 'Health & Safety', 'Family Relationships', 'Work-Life Balance', 'Parenting Challenges']
    },
    'art_creativity': {
        'name': 'Art & Creativity',
        'topics': ['Artistic Inspiration', 'Creative Process', 'Art Techniques', 'Design Trends', 'Creative Business', 'Art History', 'Digital Art', 'Creative Expression']
    },
    'real_estate': {
        'name': 'Real Estate',
        'topics': ['Property Market', 'Investment Properties', 'Home Buying', 'Real Estate Tips', 'Market Analysis', 'Property Development', 'Mortgage Advice', 'Real Estate Technology']
    },
    'automotive': {
        'name': 'Automotive',
        'topics': ['Car Reviews', 'Automotive Technology', 'Electric Vehicles', 'Car Maintenance', 'Auto Industry', 'Driving Tips', 'Vehicle Safety', 'Car Culture']
    },
    'pet_care': {
        'name': 'Pet Care',
        'topics': ['Pet Health', 'Training Tips', 'Pet Nutrition', 'Pet Behavior', 'Veterinary Care', 'Pet Products', 'Pet Adoption', 'Pet Lifestyle']
    }
}

# Translation dictionary
TRANSLATIONS = {
    'en': {
        'welcome': 'Content Creator Pro',
        'home': 'Home',
        'dashboard': 'Dashboard',
        'generator': 'Content Generator',
        'library': 'Content Library',
        'settings': 'Settings',
        'post_management': 'Post Management',
        'setup': 'Setup',
        'user_management': 'User Management',
        'login': 'Login',
        'logout': 'Logout',
        'register': 'Register',
        'language': 'Language',
        'english': 'English',
        'chinese': 'Chinese',
        'username': 'Username',
        'password': 'Password',
        'email': 'Email',
        'submit': 'Submit',
        'cancel': 'Cancel',
        'save': 'Save',
        'delete': 'Delete',
        'edit': 'Edit',
        'view': 'View',
        'create': 'Create',
        'update': 'Update',
        'search': 'Search',
        'filter': 'Filter',
        'sort': 'Sort',
        'refresh': 'Refresh',
        'loading': 'Loading...',
        'error': 'Error',
        'success': 'Success',
        'warning': 'Warning',
        'info': 'Information',
        'confirm': 'Confirm',
        'yes': 'Yes',
        'no': 'No',
        'ok': 'OK',
        'close': 'Close',
        'back': 'Back',
        'next': 'Next',
        'previous': 'Previous',
        'finish': 'Finish',
        'step': 'Step',
        'of': 'of',
        'content_generated': 'Content Generated Successfully!',
        'content_saved': 'Content saved to your library',
        'image_generated': 'Image Generated Successfully!',
        'select_direction': 'Select Content Direction',
        'what_inspires_you': 'What Inspires You?',
        'choose_topic': 'Choose Your Topic',
        'select_style': 'Select Image Style',
        'review_publish': 'Review & Publish',
        'business_finance': 'Business & Finance',
        'technology': 'Technology',
        'health_wellness': 'Health & Wellness',
        'education': 'Education',
        'entertainment': 'Entertainment',
        'travel_tourism': 'Travel & Tourism',
        'food_cooking': 'Food & Cooking',
        'fashion_beauty': 'Fashion & Beauty',
        'sports_fitness': 'Sports & Fitness',
        'science_research': 'Science & Research',
        'politics_news': 'Politics & News',
        'environment': 'Environment',
        'personal_dev': 'Personal Development',
        'parenting_family': 'Parenting & Family',
        'art_creativity': 'Art & Creativity',
        'real_estate': 'Real Estate',
        'automotive': 'Automotive',
        'pet_care': 'Pet Care',
        'footer_description': 'Generate professional social media posts, blog articles, and more with our AI-powered platform.',
        'features': 'Features',
        'ai_content_generation': 'AI Content Generation',
        'multi_platform_support': 'Multi-Platform Support',
        'regional_adaptation': 'Regional Adaptation',
        'content_library': 'Content Library',
        'platforms': 'Platforms',
        'all_rights_reserved': 'All rights reserved'
    },
    'zh': {
        'welcome': '内容创作专家',
        'home': '首页',
        'dashboard': '仪表板',
        'generator': '内容生成器',
        'library': '内容库',
        'settings': '设置',
        'post_management': '帖子管理',
        'setup': '设置',
        'user_management': '用户管理',
        'login': '登录',
        'logout': '登出',
        'register': '注册',
        'language': '语言',
        'english': '英语',
        'chinese': '中文',
        'username': '用户名',
        'password': '密码',
        'email': '邮箱',
        'submit': '提交',
        'cancel': '取消',
        'save': '保存',
        'delete': '删除',
        'edit': '编辑',
        'view': '查看',
        'create': '创建',
        'update': '更新',
        'search': '搜索',
        'filter': '筛选',
        'sort': '排序',
        'refresh': '刷新',
        'loading': '加载中...',
        'error': '错误',
        'success': '成功',
        'warning': '警告',
        'info': '信息',
        'confirm': '确认',
        'yes': '是',
        'no': '否',
        'ok': '确定',
        'close': '关闭',
        'back': '返回',
        'next': '下一步',
        'previous': '上一步',
        'finish': '完成',
        'step': '步骤',
        'of': '共',
        'content_generated': '内容生成成功！',
        'content_saved': '内容已保存到您的库中',
        'image_generated': '图片生成成功！',
        'select_direction': '选择内容方向',
        'what_inspires_you': '什么启发您？',
        'choose_topic': '选择您的主题',
        'select_style': '选择图片风格',
        'review_publish': '审查和发布',
        'business_finance': '商业与金融',
        'technology': '技术',
        'health_wellness': '健康与保健',
        'education': '教育',
        'entertainment': '娱乐',
        'travel_tourism': '旅游',
        'food_cooking': '美食与烹饪',
        'fashion_beauty': '时尚与美容',
        'sports_fitness': '运动与健身',
        'science_research': '科学与研究',
        'politics_news': '政治与新闻',
        'environment': '环境',
        'personal_dev': '个人发展',
        'parenting_family': '育儿与家庭',
        'art_creativity': '艺术与创意',
        'real_estate': '房地产',
        'automotive': '汽车',
        'pet_care': '宠物护理',
        'footer_description': '使用我们的AI驱动平台生成专业的社交媒体帖子、博客文章等。',
        'features': '功能',
        'ai_content_generation': 'AI内容生成',
        'multi_platform_support': '多平台支持',
        'regional_adaptation': '区域适配',
        'content_library': '内容库',
        'platforms': '平台',
        'all_rights_reserved': '版权所有'
    }
}

@api_routes.route('/generate', methods=['POST'])
def generate_content():
    """Generate content based on user input"""
    try:
        data = request.get_json()
        
        # Extract parameters
        direction = data.get('direction', 'business_finance')
        platform = data.get('platform', 'linkedin')
        source = data.get('source', 'personal_experience')
        topic = data.get('topic', 'Business Strategy')
        tone = data.get('tone', 'professional')
        language = data.get('language', 'en')
        
        # Generate content using AI service or fallback
        if AI_SERVICE_AVAILABLE:
            content = ai_service.generate_content(direction, platform, source, topic, tone, language)
        else:
            content = generate_content_text(direction, platform, source, topic, tone, language)
        
        return jsonify({
            'success': True,
            'content': content,
            'direction': direction,
            'platform': platform,
            'source': source,
            'topic': topic,
            'tone': tone,
            'language': language
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def generate_content_text(direction, platform, source, topic, tone, language):
    """Generate content text based on parameters"""
    
    # Platform-specific templates
    platform_templates = {
        'linkedin': {
            'professional': [
                "🚀 {topic} Insights: {content}",
                "💡 Key Takeaway: {content}",
                "📈 {topic} Analysis: {content}",
                "🎯 {topic} Strategy: {content}",
                "🔍 {topic} Deep Dive: {content}"
            ],
            'casual': [
                "Hey there! 👋 {content}",
                "Quick thought on {topic}: {content}",
                "Just sharing some insights on {topic}: {content}",
                "What do you think about {topic}? {content}",
                "Here's my take on {topic}: {content}"
            ]
        },
        'facebook': {
            'professional': [
                "📊 {topic} Update: {content}",
                "💼 {topic} Discussion: {content}",
                "📋 {topic} Summary: {content}",
                "🎯 {topic} Focus: {content}",
                "🔍 {topic} Overview: {content}"
            ],
            'casual': [
                "Hey friends! 😊 {content}",
                "What's your opinion on {topic}? {content}",
                "Sharing some thoughts on {topic}: {content}",
                "Anyone else thinking about {topic}? {content}",
                "Quick update on {topic}: {content}"
            ]
        },
        'twitter': {
            'professional': [
                "📈 {topic}: {content}",
                "💡 {topic} insight: {content}",
                "🎯 {topic} key point: {content}",
                "🔍 {topic} analysis: {content}",
                "📊 {topic} data: {content}"
            ],
            'casual': [
                "🤔 {topic} thoughts: {content}",
                "💭 {topic} musing: {content}",
                "👀 {topic} observation: {content}",
                "💪 {topic} take: {content}",
                "🎉 {topic} update: {content}"
            ]
        },
        'instagram': {
            'professional': [
                "📸 {topic} Spotlight: {content}",
                "🎨 {topic} Visual: {content}",
                "📱 {topic} Story: {content}",
                "✨ {topic} Highlight: {content}",
                "🌟 {topic} Feature: {content}"
            ],
            'casual': [
                "📸 {topic} vibes: {content}",
                "🎨 {topic} moment: {content}",
                "📱 {topic} share: {content}",
                "✨ {topic} feels: {content}",
                "🌟 {topic} energy: {content}"
            ]
        },
        'youtube': {
            'professional': [
                "🎥 {topic} Analysis: {content}",
                "📺 {topic} Discussion: {content}",
                "🎬 {topic} Review: {content}",
                "📹 {topic} Tutorial: {content}",
                "🎭 {topic} Showcase: {content}"
            ],
            'casual': [
                "🎥 {topic} chat: {content}",
                "📺 {topic} thoughts: {content}",
                "🎬 {topic} review: {content}",
                "📹 {topic} tutorial: {content}",
                "🎭 {topic} showcase: {content}"
            ]
        },
        'blog': {
            'professional': [
                "## {topic}\n\n{content}\n\n### Key Takeaways\n\n- {content}\n- {content}\n- {content}",
                "# {topic} Analysis\n\n{content}\n\n## Summary\n\n{content}",
                "## {topic} Guide\n\n{content}\n\n### Best Practices\n\n{content}",
                "# {topic} Insights\n\n{content}\n\n## Conclusion\n\n{content}",
                "## {topic} Strategy\n\n{content}\n\n### Implementation\n\n{content}"
            ],
            'casual': [
                "## {topic}\n\n{content}\n\n### My Thoughts\n\n{content}",
                "# {topic} Chat\n\n{content}\n\n## What I Learned\n\n{content}",
                "## {topic} Experience\n\n{content}\n\n### Tips & Tricks\n\n{content}",
                "# {topic} Journey\n\n{content}\n\n## Lessons Learned\n\n{content}",
                "## {topic} Adventure\n\n{content}\n\n### Key Insights\n\n{content}"
            ]
        }
    }
    
    # Direction-specific content
    direction_content = {
        'business_finance': [
            "The key to sustainable business growth lies in understanding market dynamics and customer needs. Companies that adapt quickly to changing conditions often outperform their competitors.",
            "Financial planning is crucial for both personal and business success. Diversification and risk management should be at the core of any investment strategy.",
            "Market analysis shows that businesses focusing on customer experience and digital transformation are seeing significant growth in today's competitive landscape.",
            "Entrepreneurship requires a balance of innovation, risk-taking, and strategic planning. The most successful startups often solve real problems with scalable solutions.",
            "Corporate strategy must evolve with market conditions. Companies that invest in technology and employee development tend to have better long-term outcomes."
        ],
        'technology': [
            "AI and machine learning are transforming industries across the board. Companies that embrace these technologies early are gaining significant competitive advantages.",
            "Software development is becoming more collaborative and agile. Teams that focus on user experience and rapid iteration are delivering better products.",
            "Cybersecurity is more important than ever. Organizations need to implement comprehensive security strategies to protect against evolving threats.",
            "Cloud computing has revolutionized how businesses operate. The flexibility and scalability it provides are essential for modern digital transformation.",
            "Digital transformation isn't just about technology—it's about changing how organizations think and operate in the digital age."
        ],
        'health_wellness': [
            "Mental health awareness is growing, and it's crucial to prioritize self-care in our busy lives. Small daily practices can make a significant difference.",
            "Physical fitness goes beyond just exercise—it's about creating sustainable habits that support overall well-being and energy levels.",
            "Nutrition plays a fundamental role in our health and performance. Understanding how food affects our bodies can transform our daily lives.",
            "Wellness is a holistic approach that combines physical, mental, and emotional health. Balance is key to long-term well-being.",
            "Mindfulness practices can help reduce stress and improve focus. Even a few minutes of daily meditation can have profound effects."
        ]
    }
    
    # Get content based on direction
    content_pool = direction_content.get(direction, direction_content['business_finance'])
    base_content = random.choice(content_pool)
    
    # Get template based on platform and tone
    templates = platform_templates.get(platform, platform_templates['linkedin'])
    tone_templates = templates.get(tone, templates['professional'])
    template = random.choice(tone_templates)
    
    # Generate final content
    if platform == 'blog':
        # For blog posts, use longer format
        content = template.format(topic=topic, content=base_content)
    else:
        # For social media, use shorter format
        content = template.format(topic=topic, content=base_content[:200] + "..." if len(base_content) > 200 else base_content)
    
    return content

@api_routes.route('/translate', methods=['POST'])
def translate_content():
    """Translate content between languages"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        target_language = data.get('language', 'en')
        
        # Mock translation (replace with actual translation service)
        if target_language == 'zh':
            # Simple mock Chinese translation
            translations = {
                'Welcome to Content Creator Pro': '欢迎使用内容创作专家',
                'Dashboard': '仪表板',
                'Content Generator': '内容生成器',
                'Content Library': '内容库',
                'Settings': '设置',
                'Login': '登录',
                'Logout': '登出',
                'Register': '注册',
                'Business & Finance': '商业与金融',
                'Technology': '技术',
                'Health & Wellness': '健康与保健',
                'Education': '教育',
                'Entertainment': '娱乐',
                'Travel & Tourism': '旅游',
                'Food & Cooking': '美食与烹饪',
                'Fashion & Beauty': '时尚与美容',
                'Sports & Fitness': '运动与健身',
                'Science & Research': '科学与研究',
                'Politics & News': '政治与新闻',
                'Environment': '环境',
                'Personal Development': '个人发展',
                'Parenting & Family': '育儿与家庭',
                'Art & Creativity': '艺术与创意',
                'Real Estate': '房地产',
                'Automotive': '汽车',
                'Pet Care': '宠物护理'
            }
            
            # Simple word replacement for demo
            translated_content = content
            for eng, chn in translations.items():
                translated_content = translated_content.replace(eng, chn)
            
            return jsonify({
                'success': True,
                'translated_content': translated_content,
                'original_content': content,
                'target_language': target_language
            })
        else:
            # Return original content for English
            return jsonify({
                'success': True,
                'translated_content': content,
                'original_content': content,
                'target_language': target_language
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_routes.route('/directions', methods=['GET'])
def get_directions():
    """Get available content directions"""
    return jsonify({
        'success': True,
        'directions': CONTENT_DIRECTIONS
    })

@api_routes.route('/translations', methods=['GET'])
def get_translations():
    """Get translation dictionary"""
    language = request.args.get('language', 'en')
    return jsonify({
        'success': True,
        'translations': TRANSLATIONS.get(language, TRANSLATIONS['en'])
    }) 

@api_routes.route('/migrate', methods=['POST'])
def migrate_database():
    """Run database migrations"""
    try:
        # Add role column if it doesn't exist
        with db.engine.connect() as connection:
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT 'user'
            """))
            
            # Update admin user role
            connection.execute(text("""
                UPDATE users 
                SET role = 'admin' 
                WHERE email = 'admin@contentcreator.com'
            """))
            
            connection.commit()
        
        return jsonify({
            'success': True,
            'message': 'Database migration completed successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 