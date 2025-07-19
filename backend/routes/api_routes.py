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
        'all_rights_reserved': 'All rights reserved',
        # Login page translations
        'sign_in_description': 'Sign in to Content Creator Pro',
        'sign_in_to_account': 'Sign in to your account',
        'enter_email': 'Enter your email',
        'enter_password': 'Enter your password',
        'signing_in': 'Signing in...',
        'sign_in': 'Sign in',
        'creating': 'Creating...',
        'demo_accounts': 'Demo Accounts',
        'demo_accounts_description': 'Use these demo accounts to test the platform:',
        'demo_user': 'Demo User',
        'demo_user_description': 'Regular user account',
        'admin_user': 'Admin User',
        'admin_user_description': 'Administrator account',
        'use': 'Use',
        'getting_started': 'Getting Started',
        'getting_started_step1': 'Click "Use" on any demo account above',
        'getting_started_step2': 'Click "Sign in" to login',
        'getting_started_step3': 'Explore the platform features',
        'getting_started_step4': 'Try generating content in the Generator',
        'dont_have_account': "Don't have an account?",
        'register_here': 'Register here',
        'filled_credentials': 'Filled {name} credentials',
        'login_successful': 'Login successful!',
        'login_failed': 'Login failed',
        'registration_successful': 'Registration successful! Please login.',
        'registration_failed': 'Registration failed',
        # Dashboard translations
        'dashboard_description': 'Your content creation dashboard and analytics',
        'dashboard_welcome': 'Welcome back! Here\'s an overview of your content performance.',
        'total_content': 'Total Content',
        'this_month': 'This Month',
        'engagement_rate': 'Engagement Rate',
        'top_platform': 'Top Platform',
        'recent_content': 'Recent Content',
        'view_all': 'View All',
        'engagement': 'Engagement',
        'platform_performance': 'Platform Performance',
        'posts': 'posts',
        'sample_content_1': 'AI in Business: The Future is Now',
        'sample_content_2': 'Digital Marketing Trends 2024',
        'sample_content_3': 'Healthy Work-Life Balance Tips',
        # Home page translations
        'home_title': 'Content Creator Pro - AI-Powered Content Generation',
        'home_description': 'Generate professional social media posts, blog articles, and more with our AI-powered platform. Choose from 18 content directions and create content that resonates with your audience.',
        'hero_title': 'Create Engaging Content with',
        'ai_power': 'AI Power',
        'hero_description': 'Generate professional social media posts, blog articles, and more with our AI-powered platform. Choose from 18 content directions and create content that resonates with your audience.',
        'start_creating': 'Start Creating',
        'view_dashboard': 'View Dashboard',
        'why_choose_title': 'Why Choose Content Creator Pro?',
        'why_choose_subtitle': 'Everything you need to create engaging content',
        'feature_ai_title': 'AI-Powered Generation',
        'feature_ai_description': 'Advanced AI models create high-quality, engaging content tailored to your needs.',
        'feature_regional_title': 'Regional Adaptation',
        'feature_regional_description': 'Content automatically adapts to your region with cultural sensitivity and local relevance.',
        'feature_platform_title': 'Multi-Platform Support',
        'feature_platform_description': 'Create content for LinkedIn, Facebook, Instagram, Twitter, YouTube, and blogs.',
        'feature_directions_title': 'Content Directions',
        'feature_directions_description': 'Choose from 18 specialized content directions for targeted content creation.',
        'cta_title': 'Ready to Create Amazing Content?',
        'cta_description': 'Join thousands of creators who are already using Content Creator Pro to generate engaging content.',
        'get_started_now': 'Get Started Now',
        # Register page translations
        'register_description': 'Create your Content Creator Pro account',
        'create_account': 'Create Account',
        'join_today': 'Join Content Creator Pro today',
        'full_name': 'Full Name',
        'enter_full_name': 'Enter your full name',
        'email_address': 'Email Address',
        'enter_email_address': 'Enter your email address',
        'create_strong_password': 'Create a strong password',
        'confirm_password': 'Confirm Password',
        'region': 'Region',
        'global': 'Global',
        'united_states': 'United States',
        'europe': 'Europe',
        'asia': 'Asia',
        'australia': 'Australia',
        'spanish': 'Español (Spanish)',
        'french': 'Français (French)',
        'creating_account': 'Creating Account...',
        'already_have_account': 'Already have an account?',
        'sign_in_here': 'Sign in here',
        'why_join_content_creator_pro': 'Why Join Content Creator Pro?',
        'ai_powered_content_generation': 'AI-powered content generation',
        'multi_platform_social_media_support': 'Multi-platform social media support',
        'regional_content_adaptation': 'Regional content adaptation',
        'content_library_and_management': 'Content library and management',
        'post_scheduling_and_analytics': 'Post scheduling and analytics',
        # Form validation translations
        'name_required': 'Name is required',
        'name_min_length': 'Name must be at least 2 characters',
        'email_required': 'Email is required',
        'email_invalid': 'Please enter a valid email address',
        'password_required': 'Password is required',
        'password_min_length': 'Password must be at least 6 characters',
        'password_complexity': 'Password must contain uppercase, lowercase, and number',
        'confirm_password_required': 'Please confirm your password',
        'passwords_not_match': 'Passwords do not match',
        'fix_form_errors': 'Please fix the errors in the form',
        'email_already_exists': 'An account with this email already exists',
        'network_error': 'Network error. Please check your connection and try again.',
        'server_error': 'Server error. Please try again later.',
        'invalid_data': 'Invalid data. Please check your information.',
        'password_weak': 'Weak',
        'password_fair': 'Fair',
        'password_strong': 'Strong',
        # Generator page translations
        'content_generator': 'Content Generator',
        'generator_description': 'Generate AI-powered content for your social media platforms',
        'generator_subtitle': 'Create engaging content with AI in just a few steps',
        'choose_direction': 'Choose Your Content Direction',
        'direction_description': 'Select the primary focus for your content',
        'choose_platform': 'Choose Your Platform',
        'platform_description': 'Select where you\'ll share your content',
        'what_inspires_you': 'What Inspires You?',
        'inspiration_description': 'Tell us what\'s driving your content creation',
        'select_topics_tone': 'Select Topics & Tone',
        'topics_tone_description': 'Choose specific topics and tone for your content',
        'topic_label': 'Topic *',
        'topic_placeholder': 'e.g., AI in Business, Digital Marketing Trends...',
        'tone_label': 'Tone *',
        'language_label': 'Language',
        'generate_content': 'Generate Content',
        'review_settings': 'Review your settings and generate your content',
        'your_settings': 'Your Settings:',
        'direction_label': 'Direction:',
        'platform_label': 'Platform:',
        'source_label': 'Source:',
        'tone_label_settings': 'Tone:',
        'topic_label_settings': 'Topic:',
        'language_label_settings': 'Language:',
        'generating': 'Generating...',
        'generate_content_button': 'Generate Content',
        'previous': 'Previous',
        'next': 'Next',
        'generated_content_title': 'Generated Content',
        'copy': 'Copy',
        'download': 'Download',
        'regenerate': 'Regenerate',
        'content_label': 'Content:',
        'hashtags_label': 'Hashtags:',
        'login_required': 'Please login to generate content',
        'fill_all_fields': 'Please fill in all required fields',
        'generation_failed': 'Failed to generate content',
        'copied_to_clipboard': 'Copied to clipboard!',
        'copy_failed': 'Failed to copy to clipboard',
        'content_creator_pro': 'Content Creator Pro',
        'generated_content': 'Generated Content',
        'direction': 'Direction',
        'platform': 'Platform',
        'topic': 'Topic',
        'tone': 'Tone',
        'content': 'Content',
        'hashtags': 'Hashtags',
        'generated_on': 'Generated on',
        'content_downloaded': 'Content downloaded!',
        # Library page translations
        'content_library': 'Content Library',
        'library_description': 'Browse and manage your generated content',
        'library_subtitle': 'View and manage all your generated content',
        'search_content': 'Search content...',
        'all_platforms': 'All Platforms',
        'all_directions': 'All Directions',
        'newest_first': 'Newest First',
        'oldest_first': 'Oldest First',
        'most_engaged': 'Most Engaged',
        'least_engaged': 'Least Engaged',
        'no_content_found': 'No content found',
        'try_adjusting_filters': 'Try adjusting your filters or search terms',
        'copy_content': 'Copy content',
        'download_content': 'Download content',
        'edit_content': 'Edit content',
        'delete_content': 'Delete content',
        'showing_results_summary': 'Showing {count} of {total} content items',
        'created': 'Created',
        # Sample content translations
        'sample_content_1_text': 'Artificial Intelligence is revolutionizing how businesses operate...',
        'sample_content_2_text': 'The landscape of digital marketing continues to evolve...',
        'sample_content_3_text': 'Maintaining a healthy work-life balance is crucial...',
        'sample_content_4': 'The Future of Remote Work',
        'sample_content_4_text': 'Remote work has become the new normal...',
        'sample_content_5': 'Sustainable Living Practices',
        'sample_content_5_text': 'Small changes in our daily lives can make a big impact...',
        'environment': 'Environment & Sustainability',
        # Settings page translations
        'settings_description': 'Configure your Content Creator Pro settings',
        'settings_subtitle': 'Configure your account and preferences',
        'settings_saved': 'Settings saved successfully!',
        'settings_save_failed': 'Failed to save settings',
        'confirm_reset_settings': 'Are you sure you want to reset all settings to default?',
        'settings_reset': 'Settings reset to default',
        'reset': 'Reset',
        'saving': 'Saving...',
        'save_settings': 'Save Settings',
        'profile': 'Profile',
        'preferences': 'Preferences',
        'social_media': 'Social Media',
        'appearance': 'Appearance',
        'notifications': 'Notifications',
        'security': 'Security',
        'profile_settings': 'Profile Settings',
        'content_preferences': 'Content Preferences',
        'default_direction': 'Default Direction',
        'default_platform': 'Default Platform',
        'default_tone': 'Default Tone',
        'linkedin': 'LinkedIn',
        'facebook': 'Facebook',
        'instagram': 'Instagram',
        'twitter': 'Twitter',
        'youtube_shorts': 'YouTube Shorts',
        'professional': 'Professional',
        'casual': 'Casual',
        'inspirational': 'Inspirational',
        'educational': 'Educational',
        'entertaining': 'Entertaining',
        'auto_save_drafts': 'Auto-save drafts',
        'email_notifications': 'Email notifications',
        'social_media_connections': 'Social Media Connections',
        'connected': 'Connected',
        'not_connected': 'Not connected',
        'disconnect': 'Disconnect',
        'connect': 'Connect',
        'theme': 'Theme',
        'light': 'Light',
        'dark': 'Dark',
        'auto_system': 'Auto (System)',
        'font_size': 'Font Size',
        'small': 'Small',
        'medium': 'Medium',
        'large': 'Large',
        'compact_mode': 'Compact mode',
        # Post management translations
        'post_management': 'Post Management',
        'post_management_description': 'Schedule and manage your social media posts',
        'post_management_subtitle': 'Schedule and manage your social media content',
        'new_post': 'New Post',
        'total_posts': 'Total Posts',
        'published': 'Published',
        'drafts': 'Drafts',
        'search_posts': 'Search posts...',
        'all_status': 'All Status',
        'posts': 'Posts',
        'created_at': 'Created',
        'scheduled_at': 'Scheduled',
        'published_at': 'Published',
        'likes': 'Likes',
        'publish_now': 'Publish now',
        'edit_post': 'Edit post',
        'delete_post': 'Delete post',
        'no_posts_found': 'No posts found',
        'create_first_post': 'Create your first post to get started',
        'schedule_new_post': 'Schedule New Post',
        'title': 'Title',
        'schedule_date': 'Schedule Date',
        'schedule': 'Schedule',
        'confirm_delete_post': 'Are you sure you want to delete this post?',
        'post_deleted': 'Post deleted successfully',
        'post_scheduled': 'Post scheduled successfully',
        'post_published': 'Post published successfully',
        # Sample post translations
        'sample_post_1_title': 'AI Trends in 2024',
        'sample_post_1_content': '🚀 Exciting developments in the business world! Based on recent insights, we\'re seeing remarkable growth in key sectors...',
        'sample_post_2_title': 'Digital Marketing Tips',
        'sample_post_2_content': '💡 Want to boost your social media presence? Here are 5 proven strategies that actually work...',
        'sample_post_3_title': 'Business Growth Strategies',
        'sample_post_3_content': '📈 The key to sustainable business growth isn\'t just about increasing revenue...',
        'youtube': 'YouTube',
        # Setup page translations
        'setup': 'Setup',
        'setup_description': 'Complete your account setup',
        'welcome_to_content_creator_pro': 'Welcome to Content Creator Pro',
        'setup_subtitle': 'Let\'s set up your account for the best experience',
        'tell_us_about_yourself': 'Tell us about yourself',
        'company_organization': 'Company/Organization',
        'enter_company_name': 'Enter your company name',
        'industry': 'Industry',
        'select_your_industry': 'Select your industry',
        'your_role': 'Your Role',
        'e_g_marketing_manager_ceo_content_creator': 'e.g., Marketing Manager, CEO, Content Creator',
        'primary_platform': 'Primary Platform',
        'select_your_primary_platform': 'Select your primary platform',
        'content_frequency': 'Content Frequency',
        'select_frequency': 'Select frequency',
        'daily': 'Daily',
        'weekly': 'Weekly',
        'biweekly': 'Bi-weekly',
        'monthly': 'Monthly',
        'your_goals': 'Your Goals',
        'select_all_that_apply': 'Select all that apply',
        'increase_brand_awareness': 'Increase brand awareness',
        'generate_leads': 'Generate leads',
        'drive_website_traffic': 'Drive website traffic',
        'build_community': 'Build community',
        'share_thought_leadership': 'Share thought leadership',
        'promote_products_services': 'Promote products/services',
        'connect_your_social_media': 'Connect Your Social Media',
        'select_the_platforms_you_want_to_create_content_for': 'Select the platforms you want to create content for',
        'notification_preferences': 'Notification Preferences',
        'choose_how_you_d_like_to_stay_updated': 'Choose how you\'d like to stay updated',
        'push_notifications': 'Push notifications',
        'weekly_performance_reports': 'Weekly performance reports',
        'previous': 'Previous',
        'next': 'Next',
        'complete_setup': 'Complete Setup',
        'setup_completed': 'Setup completed successfully!',
        'setup_failed': 'Failed to complete setup',
        # Industry translations
        'healthcare': 'Healthcare',
        'real_estate': 'Real Estate',
        'ecommerce': 'E-commerce',
        'consulting': 'Consulting',
        'manufacturing': 'Manufacturing',
        'other': 'Other',
        # Admin translations
        'failed_to_fetch_users': '获取用户失败',
        'user_updated_successfully': '用户更新成功',
        'failed_to_update_user': '更新用户失败',
        'user_deleted_successfully': '用户删除成功',
        'failed_to_delete_user': '删除用户失败',
        'failed_to_toggle_user_status': '切换用户状态失败',
        'password_reset_successfully': '密码重置成功',
        'failed_to_reset_password': '重置密码失败',
        'active': '活跃',
        'inactive': '非活跃'
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
        'all_rights_reserved': '版权所有',
        # Login page translations
        'sign_in_description': '登录内容创作专家',
        'sign_in_to_account': '登录您的账户',
        'enter_email': '输入您的邮箱',
        'enter_password': '输入您的密码',
        'signing_in': '登录中...',
        'sign_in': '登录',
        'creating': '创建中...',
        'demo_accounts': '演示账户',
        'demo_accounts_description': '使用这些演示账户来测试平台：',
        'demo_user': '演示用户',
        'demo_user_description': '普通用户账户',
        'admin_user': '管理员用户',
        'admin_user_description': '管理员账户',
        'use': '使用',
        'getting_started': '开始使用',
        'getting_started_step1': '点击上方任意演示账户的"使用"按钮',
        'getting_started_step2': '点击"登录"按钮登录',
        'getting_started_step3': '探索平台功能',
        'getting_started_step4': '在生成器中尝试生成内容',
        'dont_have_account': '没有账户？',
        'register_here': '在此注册',
        'filled_credentials': '已填入{name}的凭据',
        'login_successful': '登录成功！',
        'login_failed': '登录失败',
        'registration_successful': '注册成功！请登录。',
        'registration_failed': '注册失败',
        # Dashboard translations
        'dashboard_description': '您的内容创作仪表板和分析',
        'dashboard_welcome': '欢迎回来！这是您内容表现概览。',
        'total_content': '总内容',
        'this_month': '本月',
        'engagement_rate': '参与率',
        'top_platform': '主要平台',
        'recent_content': '最近内容',
        'view_all': '查看全部',
        'engagement': '参与度',
        'platform_performance': '平台表现',
        'posts': '帖子',
        'sample_content_1': '商业：未来已来',
        'sample_content_2': '2024年数字营销趋势',
        'sample_content_3': '健康工作与生活平衡技巧',
        # Home page translations
        'home_title': '内容创作专家 - AI驱动内容生成',
        'home_description': '使用我们的AI驱动平台生成专业的社交媒体帖子、博客文章等。选择18个内容方向，为您的受众创作内容。',
        'hero_title': '创建引人入胜的内容与',
        'ai_power': 'AI力量',
        'hero_description': '使用我们的AI驱动平台生成专业的社交媒体帖子、博客文章等。选择18个内容方向，为您的受众创作内容。',
        'start_creating': '开始创作',
        'view_dashboard': '查看仪表板',
        'why_choose_title': '为什么选择内容创作专家？',
        'why_choose_subtitle': '您所需的一切，以创建引人入胜的内容',
        'feature_ai_title': 'AI驱动生成',
        'feature_ai_description': '先进的AI模型为您量身定制高质量、引人入胜的内容。',
        'feature_regional_title': '区域适配',
        'feature_regional_description': '内容自动适应您的区域，具有文化敏感性和本地相关性。',
        'feature_platform_title': '多平台支持',
        'feature_platform_description': '为LinkedIn、Facebook、Instagram、Twitter、YouTube和博客创建内容。',
        'feature_directions_title': '内容方向',
        'feature_directions_description': '从18个专业内容方向中选择，以实现有针对性的内容创作。',
        'cta_title': '准备好创作精彩内容？',
        'cta_description': '成千上万的创作者已经在使用内容创作专家来生成引人入胜的内容。',
        'get_started_now': '立即开始',
        # Register page translations
        'register_description': '创建您的内容创作专家账户',
        'create_account': '创建账户',
        'join_today': '今天加入内容创作专家',
        'full_name': '全名',
        'enter_full_name': '输入您的全名',
        'email_address': '电子邮件地址',
        'enter_email_address': '输入您的电子邮件地址',
        'create_strong_password': '创建强密码',
        'confirm_password': '确认密码',
        'region': '地区',
        'global': '全球',
        'united_states': '美国',
        'europe': '欧洲',
        'asia': '亚洲',
        'australia': '澳大利亚',
        'spanish': '西班牙语 (Spanish)',
        'french': '法语 (French)',
        'creating_account': '创建账户中...',
        'already_have_account': '已有账户？',
        'sign_in_here': '在此登录',
        'why_join_content_creator_pro': '为什么加入内容创作专家？',
        'ai_powered_content_generation': 'AI驱动内容生成',
        'multi_platform_social_media_support': '多平台社交媒体支持',
        'regional_content_adaptation': '区域内容适配',
        'content_library_and_management': '内容库和资产管理',
        'post_scheduling_and_analytics': '帖子排程和分析',
        # Form validation translations
        'name_required': '名称是必需的',
        'name_min_length': '名称必须至少2个字符',
        'email_required': '电子邮件是必需的',
        'email_invalid': '请输入有效的电子邮件地址',
        'password_required': '密码是必需的',
        'password_min_length': '密码必须至少6个字符',
        'password_complexity': '密码必须包含大写、小写和数字',
        'confirm_password_required': '请确认您的密码',
        'passwords_not_match': '密码不匹配',
        'fix_form_errors': '请修复表单中的错误',
        'email_already_exists': '此电子邮件已存在账户',
        'network_error': '网络错误。请检查您的连接并重试。',
        'server_error': '服务器错误。请稍后再试。',
        'invalid_data': '无效数据。请检查您的信息。',
        'password_weak': '弱',
        'password_fair': '一般',
        'password_strong': '强',
        # Generator page translations
        'content_generator': '内容生成器',
        'generator_description': '生成AI驱动的社交媒体内容',
        'generator_subtitle': '只需几个步骤即可使用AI创建引人入胜的内容',
        'choose_direction': '选择您的内容方向',
        'direction_description': '选择您内容的主要焦点',
        'choose_platform': '选择您的平台',
        'platform_description': '选择您将在哪里分享内容',
        'what_inspires_you': '什么激励着您？',
        'inspiration_description': '告诉我们什么在推动您的内容创作',
        'select_topics_tone': '选择主题和语气',
        'topics_tone_description': '为您的内容选择特定主题和语气',
        'topic_label': '主题 *',
        'topic_placeholder': '例如，商业中的AI，数字营销趋势...',
        'tone_label': '语气 *',
        'language_label': '语言',
        'generate_content': '生成内容',
        'review_settings': '查看您的设置并生成内容',
        'your_settings': '您的设置：',
        'direction_label': '方向：',
        'platform_label': '平台：',
        'source_label': '来源：',
        'tone_label_settings': '语气：',
        'topic_label_settings': '主题：',
        'language_label_settings': '语言：',
        'generating': '生成中...',
        'generate_content_button': '生成内容',
        'previous': '上一步',
        'next': '下一步',
        'generated_content_title': '已生成内容',
        'copy': '复制',
        'download': '下载',
        'regenerate': '重新生成',
        'content_label': '内容：',
        'hashtags_label': '话题标签：',
        'login_required': '请登录以生成内容',
        'fill_all_fields': '请填写所有必填字段',
        'generation_failed': '内容生成失败',
        'copied_to_clipboard': '已复制到剪贴板！',
        'copy_failed': '复制失败',
        'content_creator_pro': '内容创作专家',
        'generated_content': '已生成内容',
        'direction': '方向',
        'platform': '平台',
        'topic': '主题',
        'tone': '语气',
        'content': '内容',
        'hashtags': '话题标签',
        'generated_on': '生成于',
        'content_downloaded': '内容已下载！',
        # Library page translations
        'content_library': '内容库',
        'library_description': '浏览和管理您生成的内容',
        'library_subtitle': '查看和管理所有您生成的内容',
        'search_content': '搜索内容...',
        'all_platforms': '所有平台',
        'all_directions': '所有方向',
        'newest_first': '最新优先',
        'oldest_first': '最旧优先',
        'most_engaged': '最受欢迎',
        'least_engaged': '最不受欢迎',
        'no_content_found': '未找到内容',
        'try_adjusting_filters': '请调整您的筛选条件或搜索词',
        'copy_content': '复制内容',
        'download_content': '下载内容',
        'edit_content': '编辑内容',
        'delete_content': '删除内容',
        'showing_results_summary': '显示 {count} 个内容项中的 {total}',
        'created': '创建于',
        # Sample content translations
        'sample_content_1_text': '人工智能正在改变企业运营方式...',
        'sample_content_2_text': '数字营销领域继续发展...',
        'sample_content_3_text': '保持健康的工作与生活平衡至关重要...',
        'sample_content_4': '远程工作未来',
        'sample_content_4_text': '远程工作已成为新常态...',
        'sample_content_5': '可持续生活实践',
        'sample_content_5_text': '我们日常生活中的小小改变可以产生巨大影响...',
        'environment': '环境与可持续发展',
        # Settings page translations
        'settings_description': '配置您的内容创作专家设置',
        'settings_subtitle': '配置您的账户和偏好设置',
        'settings_saved': '设置保存成功！',
        'settings_save_failed': '设置保存失败',
        'confirm_reset_settings': '您确定要将所有设置重置为默认值吗？',
        'settings_reset': '设置已重置为默认值',
        'reset': '重置',
        'saving': '保存中...',
        'save_settings': '保存设置',
        'profile': '个人资料',
        'preferences': '偏好设置',
        'social_media': '社交媒体',
        'appearance': '外观',
        'notifications': '通知',
        'security': '安全',
        'profile_settings': '个人资料设置',
        'content_preferences': '内容偏好设置',
        'default_direction': '默认方向',
        'default_platform': '默认平台',
        'default_tone': '默认语气',
        'linkedin': 'LinkedIn',
        'facebook': 'Facebook',
        'instagram': 'Instagram',
        'twitter': 'Twitter',
        'youtube_shorts': 'YouTube Shorts',
        'professional': '专业',
        'casual': '随意',
        'inspirational': '鼓舞人心',
        'educational': '教育性',
        'entertaining': '娱乐性',
        'auto_save_drafts': '自动保存草稿',
        'email_notifications': '电子邮件通知',
        'social_media_connections': '社交媒体连接',
        'connected': '已连接',
        'not_connected': '未连接',
        'disconnect': '断开连接',
        'connect': '连接',
        'theme': '主题',
        'light': '浅色',
        'dark': '深色',
        'auto_system': '自动（系统）',
        'font_size': '字体大小',
        'small': '小',
        'medium': '中',
        'large': '大',
        'compact_mode': '紧凑模式',
        # Post management translations
        'post_management': '帖子管理',
        'post_management_description': '安排和管理您的社交媒体帖子',
        'post_management_subtitle': '安排和管理您的社交媒体内容',
        'new_post': '新帖子',
        'total_posts': '总帖子',
        'published': '已发布',
        'drafts': '草稿',
        'search_posts': '搜索帖子...',
        'all_status': '所有状态',
        'posts': '帖子',
        'created_at': '创建于',
        'scheduled_at': '安排于',
        'published_at': '已发布于',
        'likes': '点赞',
        'publish_now': '立即发布',
        'edit_post': '编辑帖子',
        'delete_post': '删除帖子',
        'no_posts_found': '未找到帖子',
        'create_first_post': '创建您的第一个帖子以开始',
        'schedule_new_post': '安排新帖子',
        'title': '标题',
        'schedule_date': '安排日期',
        'schedule': '安排',
        'confirm_delete_post': '您确定要删除此帖子吗？',
        'post_deleted': '帖子删除成功',
        'post_scheduled': '帖子安排成功',
        'post_published': '帖子发布成功',
        # Sample post translations
        'sample_post_1_title': '2024年AI趋势',
        'sample_post_1_content': '🚀 商业世界令人振奋的发展！根据最近的研究，我们看到了关键领域令人瞩目的增长...',
        'sample_post_2_title': '数字营销技巧',
        'sample_post_2_content': '💡 想要提升您的社交媒体影响力？这里有5个行之有效的策略...',
        'sample_post_3_title': '商业增长策略',
        'sample_post_3_content': '📈 可持续商业增长的关键不仅仅是增加收入...',
        'youtube': 'YouTube',
        # Setup page translations
        'setup': '设置',
        'setup_description': '完成您的账户设置',
        'welcome_to_content_creator_pro': '欢迎使用内容创作专家',
        'setup_subtitle': '让我们为您设置最佳体验',
        'tell_us_about_yourself': '请告诉我们您的信息',
        'company_organization': '公司/组织',
        'enter_company_name': '输入您的公司名称',
        'industry': '行业',
        'select_your_industry': '选择您的行业',
        'your_role': '您的角色',
        'e_g_marketing_manager_ceo_content_creator': '例如，营销经理、首席执行官、内容创作者',
        'primary_platform': '主要平台',
        'select_your_primary_platform': '选择您的主要平台',
        'content_frequency': '内容频率',
        'select_frequency': '选择频率',
        'daily': '每日',
        'weekly': '每周',
        'biweekly': '每两周',
        'monthly': '每月',
        'your_goals': '您的目标',
        'select_all_that_apply': '选择所有适用的',
        'increase_brand_awareness': '提高品牌知名度',
        'generate_leads': '生成线索',
        'drive_website_traffic': '驱动网站流量',
        'build_community': '建立社区',
        'share_thought_leadership': '分享思想领导力',
        'promote_products_services': '推广产品/服务',
        'connect_your_social_media': '连接您的社交媒体',
        'select_the_platforms_you_want_to_create_content_for': '选择您想要创建内容的平台',
        'notification_preferences': '通知偏好',
        'choose_how_you_d_like_to_stay_updated': '选择您希望如何保持更新',
        'push_notifications': '推送通知',
        'weekly_performance_reports': '每周性能报告',
        'previous': '上一步',
        'next': '下一步',
        'complete_setup': '完成设置',
        'setup_completed': '设置成功完成！',
        'setup_failed': '设置完成失败',
        # Industry translations
        'healthcare': '医疗保健',
        'real_estate': '房地产',
        'ecommerce': '电子商务',
        'consulting': '咨询',
        'manufacturing': '制造业',
        'other': '其他',
        # Admin translations
        'failed_to_fetch_users': '获取用户失败',
        'user_updated_successfully': '用户更新成功',
        'failed_to_update_user': '更新用户失败',
        'user_deleted_successfully': '用户删除成功',
        'failed_to_delete_user': '删除用户失败',
        'failed_to_toggle_user_status': '切换用户状态失败',
        'password_reset_successfully': '密码重置成功',
        'failed_to_reset_password': '重置密码失败',
        'active': '活跃',
        'inactive': '非活跃'
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
        generate_images = data.get('generate_images', True)  # New parameter
        
        # Generate content using AI service or fallback
        if AI_SERVICE_AVAILABLE:
            content = ai_service.generate_content(
                direction, platform, source, topic, tone, language, 
                generate_images=generate_images
            )
        else:
            content = generate_content_text(direction, platform, source, topic, tone, language)
            # Add basic structure for non-AI content
            content = {
                'content': {
                    'text': content,
                    'length': len(content),
                    'max_length': 1300,
                    'hashtags': [],
                    'call_to_action': []
                },
                'variations': [],
                'images': {'primary': None, 'variations': [], 'total_count': 0},
                'media_suggestions': {'images': [], 'videos': [], 'graphics': []},
                'platform_specs': {},
                'metadata': {
                    'content_direction': direction,
                    'content_type': platform,
                    'source_type': source,
                    'topic': topic,
                    'tone': tone,
                    'region': 'global',
                    'language': language,
                    'generated_at': '2024-01-15T10:30:00Z'
                },
                'cultural_context': {'sensitivity': 'general', 'recommendations': []},
                'direction_context': {},
                'analytics': {
                    'content_metrics': {'character_count': len(content), 'word_count': len(content.split()), 'hashtag_count': 0, 'readability_score': 0, 'engagement_potential': 'medium'},
                    'platform_optimization': {'optimal_posting_time': 'Varies', 'recommended_frequency': 'Varies', 'audience_demographics': 'Varies', 'content_lifecycle': 'Varies'},
                    'performance_predictions': {'estimated_reach': 'medium', 'estimated_engagement': 'medium', 'estimated_clicks': 'low', 'viral_potential': 'low'}
                }
            }
        
        return jsonify({
            'success': True,
            'data': content
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

@api_routes.route('/generate-image', methods=['POST'])
def generate_image():
    """Generate image using Stable Diffusion"""
    try:
        data = request.get_json()
        
        # Extract parameters
        platform = data.get('platform', 'facebook')
        content_direction = data.get('content_direction', 'business_finance')
        topic = data.get('topic', 'Business Strategy')
        tone = data.get('tone', 'professional')
        language = data.get('language', 'en')
        
        # Import Stable Diffusion service
        from app.services.stable_diffusion import StableDiffusionService
        stable_diffusion = StableDiffusionService()
        
        # Generate image
        image_result = stable_diffusion.generate_image(
            platform=platform,
            content_direction=content_direction,
            topic=topic,
            tone=tone,
            language=language
        )
        
        return jsonify({
            'success': True,
            'data': image_result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_routes.route('/image-specs/<platform>', methods=['GET'])
def get_image_specs(platform):
    """Get image specifications for a specific platform"""
    try:
        from app.services.stable_diffusion import StableDiffusionService
        stable_diffusion = StableDiffusionService()
        
        specs = stable_diffusion.get_platform_image_specs(platform)
        supported_ratios = stable_diffusion.get_supported_ratios()
        
        return jsonify({
            'success': True,
            'data': {
                'platform': platform,
                'specifications': specs,
                'supported_ratios': supported_ratios
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 