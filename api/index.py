import os
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# Set environment variable to indicate serverless mode
os.environ['VERCEL_ENV'] = 'production'

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'  # Required for session management

# Content Management System
class ContentManager:
    def __init__(self):
        self.content_id_counter = 1000
        self.user_content = {}  # Store content by user
    
    def generate_content_id(self):
        """Generate unique content ID"""
        self.content_id_counter += 1
        return f"CC{self.content_id_counter:06d}"
    
    def create_content(self, user_email, direction, platform, source, topic, tone, content_text):
        """Create new content entry"""
        content_id = self.generate_content_id()
        timestamp = datetime.now().isoformat()
        
        content_entry = {
            'id': content_id,
            'user_email': user_email,
            'direction': direction,
            'platform': platform,
            'source': source,
            'topic': topic,
            'tone': tone,
            'content': content_text,
            'created_at': timestamp,
            'performance': {
                'views': 0,
                'likes': 0,
                'shares': 0,
                'comments': 0
            }
        }
        
        if user_email not in self.user_content:
            self.user_content[user_email] = []
        
        self.user_content[user_email].append(content_entry)
        return content_entry
    
    def get_user_content(self, user_email, limit=10):
        """Get user's content sorted by creation date"""
        if user_email not in self.user_content:
            return []
        return sorted(self.user_content[user_email], 
                     key=lambda x: x['created_at'], reverse=True)[:limit]
    
    def get_content_by_direction(self, user_email, direction):
        """Get user's content filtered by direction"""
        if user_email not in self.user_content:
            return []
        return [c for c in self.user_content[user_email] if c['direction'] == direction]
    
    def update_performance(self, content_id, platform, views=None, likes=None, shares=None, comments=None):
        """Update content performance metrics"""
        for user_content in self.user_content.values():
            for content in user_content:
                if content['id'] == content_id and content['platform'] == platform:
                    if views is not None:
                        content['performance']['views'] = views
                    if likes is not None:
                        content['performance']['likes'] = likes
                    if shares is not None:
                        content['performance']['shares'] = shares
                    if comments is not None:
                        content['performance']['comments'] = comments
                    return content
        return None

# Initialize content manager
content_manager = ContentManager()

# Sample content for demo purposes
def initialize_demo_content():
    """Initialize demo content for demonstration"""
    demo_user = "demo@contentcreator.com"
    
    # Create sample content entries
    sample_content = [
        {
            'direction': 'business_finance',
            'platform': 'linkedin',
            'source': 'news',
            'topic': 'Market Analysis: Latest Trends in Financial Markets',
            'tone': 'professional',
            'content': '🚀 Exciting developments in the business world! Based on recent insights, we\'re seeing remarkable growth in key sectors. This represents a significant opportunity for forward-thinking professionals. What are your thoughts on these emerging trends? #BusinessGrowth #Innovation #ProfessionalDevelopment'
        },
        {
            'direction': 'business_finance',
            'platform': 'twitter',
            'source': 'books',
            'topic': 'Key Business Principles from the Book',
            'tone': 'educational',
            'content': '📚 Just finished reading an amazing business book! Key takeaway: Success isn\'t about having all the answers, it\'s about asking the right questions. What\'s the best business advice you\'ve ever received? #BusinessTips #Leadership #Growth'
        },
        {
            'direction': 'technology',
            'platform': 'instagram',
            'source': 'videos',
            'topic': 'Main Takeaways from the Video Content',
            'tone': 'casual',
            'content': '💻 Tech tip of the day! Just learned this amazing productivity hack from a YouTube video. Game changer for anyone working remotely! What\'s your favorite productivity tool? #TechTips #Productivity #RemoteWork'
        },
        {
            'direction': 'business_finance',
            'platform': 'blog',
            'source': 'research',
            'topic': 'Key Findings from the Research Paper',
            'tone': 'professional',
            'content': 'New research reveals fascinating insights into market dynamics. The data shows a clear correlation between innovation investment and long-term growth. This study provides valuable insights for business leaders looking to make strategic decisions.'
        }
    ]
    
    # Add sample content to manager
    for i, content_data in enumerate(sample_content):
        content_entry = content_manager.create_content(
            demo_user,
            content_data['direction'],
            content_data['platform'],
            content_data['source'],
            content_data['topic'],
            content_data['tone'],
            content_data['content']
        )
        
        # Add status information
        if i == 0:  # First post - published
            content_entry['status'] = 'published'
        elif i == 1:  # Second post - scheduled
            content_entry['status'] = 'scheduled'
            content_entry['scheduled_time'] = '2024-07-20 10:00 AM'
        else:  # Other posts - draft
            content_entry['status'] = 'draft'
    
    # Add more sample content for other platforms
    additional_content = [
        {
            'direction': 'technology',
            'platform': 'facebook',
            'source': 'news',
            'topic': 'Latest Tech Trends: AI and Machine Learning',
            'tone': 'casual',
            'content': 'Hey everyone! 👋 Just discovered some amazing new AI developments that are going to change everything! The pace of innovation is incredible. What tech trends are you most excited about? Share your thoughts below! #TechTrends #AI #Innovation #Community'
        },
        {
            'direction': 'health_wellness',
            'platform': 'youtube',
            'source': 'videos',
            'topic': 'Wellness Tips: Mental Health and Productivity',
            'tone': 'educational',
            'content': '🎥 New video alert! Just uploaded a comprehensive guide on maintaining mental wellness while working remotely. The key is finding balance and setting boundaries. Check it out and let me know what wellness tips work best for you! #MentalHealth #Wellness #Productivity #RemoteWork'
        },
        {
            'direction': 'education',
            'platform': 'linkedin',
            'source': 'research',
            'topic': 'Educational Innovation: Online Learning Trends',
            'tone': 'professional',
            'content': '📚 Fascinating research on the evolution of online education! The data shows a 300% increase in digital learning adoption. This represents a fundamental shift in how we approach education. What are your thoughts on the future of learning? #Education #Innovation #OnlineLearning #ProfessionalDevelopment'
        },
        {
            'direction': 'entertainment',
            'platform': 'instagram',
            'source': 'reviews',
            'topic': 'Movie Review: Latest Blockbuster',
            'tone': 'casual',
            'content': '🎬 Just watched the most incredible movie! The cinematography was breathtaking and the story was so compelling. Highly recommend checking it out! What\'s the best movie you\'ve seen recently? Drop your recommendations below! #MovieReview #Entertainment #Cinema #Recommendations'
        }
    ]
    
    # Add additional content
    for i, content_data in enumerate(additional_content):
        content_entry = content_manager.create_content(
            demo_user,
            content_data['direction'],
            content_data['platform'],
            content_data['source'],
            content_data['topic'],
            content_data['tone'],
            content_data['content']
        )
        
        # Add status information
        if i == 0:  # Facebook post - published
            content_entry['status'] = 'published'
        elif i == 1:  # YouTube post - scheduled
            content_entry['status'] = 'scheduled'
            content_entry['scheduled_time'] = '2024-07-22 02:00 PM'
        else:  # Other posts - draft
            content_entry['status'] = 'draft'
    
    # Add performance data for all content
    content_manager.update_performance('CC1001', 'linkedin', views=156, likes=23, shares=5, comments=8)
    content_manager.update_performance('CC1002', 'twitter', views=89, likes=45, shares=12, comments=15)
    content_manager.update_performance('CC1003', 'instagram', views=234, likes=67, shares=8, comments=12)
    content_manager.update_performance('CC1004', 'blog', views=567, likes=89, shares=23, comments=34)
    content_manager.update_performance('CC1005', 'facebook', views=445, likes=78, shares=15, comments=22)
    content_manager.update_performance('CC1006', 'youtube', views=1234, likes=156, shares=45, comments=67)
    content_manager.update_performance('CC1007', 'linkedin', views=289, likes=34, shares=7, comments=12)
    content_manager.update_performance('CC1008', 'instagram', views=567, likes=89, shares=12, comments=18)

# Initialize demo content
initialize_demo_content()

def generate_dashboard_content(user_email, user_content):
    """Generate dynamic dashboard content based on user's content"""
    
    # Get user's name
    user_name = user_email.split('@')[0] if '@' in user_email else user_email
    
    # Calculate stats
    total_content = len(user_content)
    this_month = len([c for c in user_content if c['created_at'].startswith('2024-07')])
    library_items = total_content
    social_posts = len([c for c in user_content if c['platform'] in ['linkedin', 'twitter', 'instagram', 'facebook']])
    
    # Get recent content by direction
    recent_content_html = ""
    for content in user_content[:4]:
        direction_icon = get_direction_icon(content['direction'])
        direction_name = get_direction_name(content['direction'])
        platform_name = get_platform_name(content['platform'])
        time_ago = get_time_ago(content['created_at'])
        badge_color = get_platform_badge_color(content['platform'])
        
        recent_content_html += f"""
        <div class="d-flex align-items-center mb-3">
            {direction_icon}
            <div class="flex-grow-1">
                <strong><span data-translate="{content['direction']}">{direction_name}</span>: {content['topic'][:50]}{'...' if len(content['topic']) > 50 else ''}</strong>
                <br><small class="text-muted">{time_ago}</small>
            </div>
            <span class="badge {badge_color}" data-translate="{content['platform']}">{platform_name}</span>
        </div>
        """
    
    # Generate social media performance
    social_performance_html = generate_social_performance_html(user_content)
    
    # Generate content performance by direction
    direction_performance_html = generate_direction_performance_html(user_content)
    
    return f"""
    <div class="container">
        <!-- Welcome Section -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card bg-primary text-white">
                    <div class="card-body">
                        <h2 class="mb-2"><span data-translate="welcome_back">Welcome back</span>, {user_name}!</h2>
                        <p class="mb-0"><span data-translate="your_focus">Your focus</span>: <strong data-translate="business_finance">Business & Finance</strong></p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Quick Stats -->
        <div class="row mb-4">
            <div class="col-12">
                <h4 class="mb-3"><i class="fas fa-chart-bar me-2"></i><span data-translate="quick_stats">Quick Stats</span></h4>
            </div>
            <div class="col-md-3 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-file-alt fa-2x text-primary mb-2"></i>
                        <h3 class="mb-1">{total_content}</h3>
                        <p class="text-muted mb-0" data-translate="content_generated">Content Generated</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-calendar fa-2x text-success mb-2"></i>
                        <h3 class="mb-1">{this_month}</h3>
                        <p class="text-muted mb-0" data-translate="this_month">This Month</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-folder fa-2x text-warning mb-2"></i>
                        <h3 class="mb-1">{library_items}</h3>
                        <p class="text-muted mb-0" data-translate="library_items">Library Items</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-share-alt fa-2x text-info mb-2"></i>
                        <h3 class="mb-1">{social_posts}</h3>
                        <p class="text-muted mb-0" data-translate="social_posts">Social Posts</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Quick Actions -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0"><i class="fas fa-bolt me-2"></i><span data-translate="quick_actions">Quick Actions</span></h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-2 col-6 mb-2">
                                <a href="/generator" class="btn btn-primary w-100">
                                    <i class="fas fa-plus-circle me-1"></i><span data-translate="generate_new_content">Generate New Content</span>
                                </a>
                            </div>
                            <div class="col-md-2 col-6 mb-2">
                                <a href="/library" class="btn btn-outline-primary w-100">
                                    <i class="fas fa-folder me-1"></i><span data-translate="view_library">View Library</span>
                                </a>
                            </div>
                            <div class="col-md-2 col-6 mb-2">
                                <a href="#" class="btn btn-outline-success w-100">
                                    <i class="fas fa-share-alt me-1"></i><span data-translate="social_media">Social Media</span>
                                </a>
                            </div>
                            <div class="col-md-2 col-6 mb-2">
                                <a href="/settings" class="btn btn-outline-secondary w-100">
                                    <i class="fas fa-cog me-1"></i><span data-translate="settings">Settings</span>
                                </a>
                            </div>
                            <div class="col-md-2 col-6 mb-2">
                                <a href="#" class="btn btn-outline-info w-100">
                                    <i class="fas fa-chart-line me-1"></i><span data-translate="analytics">Analytics</span>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Recent Content by Direction -->
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0"><i class="fas fa-clock me-2"></i><span data-translate="recent_content_by_direction">Recent Content by Direction</span></h5>
                    </div>
                    <div class="card-body">
                        {recent_content_html if recent_content_html else '<p class="text-muted">No content generated yet.</p>'}
                    </div>
                </div>
            </div>
            
            <!-- Social Media Performance -->
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0"><i class="fas fa-chart-pie me-2"></i><span data-translate="social_media_performance">Social Media Performance</span></h5>
                    </div>
                    <div class="card-body">
                        {social_performance_html}
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Content Performance by Direction -->
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0"><i class="fas fa-chart-bar me-2"></i><span data-translate="content_performance_by_direction">Content Performance by Direction</span></h5>
                    </div>
                    <div class="card-body">
                        {direction_performance_html}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

def get_direction_icon(direction):
    """Get icon for content direction"""
    icons = {
        'business_finance': '<i class="fas fa-briefcase text-primary me-3"></i>',
        'technology': '<i class="fas fa-microchip text-success me-3"></i>',
        'health_wellness': '<i class="fas fa-heartbeat text-danger me-3"></i>',
        'education': '<i class="fas fa-graduation-cap text-info me-3"></i>',
        'entertainment': '<i class="fas fa-film text-warning me-3"></i>',
        'travel_tourism': '<i class="fas fa-plane text-primary me-3"></i>',
        'food_cooking': '<i class="fas fa-utensils text-success me-3"></i>',
        'fashion_beauty': '<i class="fas fa-tshirt text-danger me-3"></i>',
        'sports_fitness': '<i class="fas fa-dumbbell text-warning me-3"></i>',
        'science_research': '<i class="fas fa-flask text-info me-3"></i>',
        'politics_news': '<i class="fas fa-newspaper text-primary me-3"></i>',
        'environment': '<i class="fas fa-leaf text-success me-3"></i>',
        'personal_dev': '<i class="fas fa-user-graduate text-info me-3"></i>',
        'parenting_family': '<i class="fas fa-baby text-warning me-3"></i>',
        'art_creativity': '<i class="fas fa-palette text-danger me-3"></i>',
        'real_estate': '<i class="fas fa-home text-primary me-3"></i>',
        'automotive': '<i class="fas fa-car text-secondary me-3"></i>',
        'pet_care': '<i class="fas fa-paw text-warning me-3"></i>'
    }
    return icons.get(direction, '<i class="fas fa-file text-muted me-3"></i>')

def get_direction_name(direction):
    """Get display name for content direction"""
    names = {
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
        'pet_care': 'Pet Care'
    }
    return names.get(direction, direction.replace('_', ' ').title())

def get_platform_name(platform):
    """Get display name for platform"""
    names = {
        'linkedin': 'LinkedIn Post',
        'facebook': 'Facebook Post',
        'instagram': 'Instagram Post',
        'twitter': 'Twitter Post',
        'youtube': 'YouTube Short',
        'blog': 'Blog Article'
    }
    return names.get(platform, platform.title())

def get_platform_badge_color(platform):
    """Get badge color for platform"""
    colors = {
        'linkedin': 'bg-primary',
        'facebook': 'bg-primary',
        'instagram': 'bg-success',
        'twitter': 'bg-info',
        'youtube': 'bg-danger',
        'blog': 'bg-warning'
    }
    return colors.get(platform, 'bg-secondary')

def get_time_ago(timestamp):
    """Get human-readable time ago"""
    try:
        created_time = datetime.fromisoformat(timestamp)
        now = datetime.now()
        diff = now - created_time
        
        if diff.days > 0:
            if diff.days == 1:
                return "1 day ago"
            elif diff.days < 7:
                return f"{diff.days} days ago"
            else:
                weeks = diff.days // 7
                if weeks == 1:
                    return "1 week ago"
                else:
                    return f"{weeks} weeks ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            if hours == 1:
                return "1 hour ago"
            else:
                return f"{hours} hours ago"
        else:
            minutes = diff.seconds // 60
            if minutes < 1:
                return "Just now"
            elif minutes == 1:
                return "1 minute ago"
            else:
                return f"{minutes} minutes ago"
    except:
        return "Recently"

def generate_social_performance_html(user_content):
    """Generate social media performance HTML"""
    platforms = ['linkedin', 'twitter', 'instagram', 'facebook']
    platform_icons = {
        'linkedin': '<i class="fab fa-linkedin text-primary me-2"></i>',
        'twitter': '<i class="fab fa-twitter text-info me-2"></i>',
        'instagram': '<i class="fab fa-instagram text-danger me-2"></i>',
        'facebook': '<i class="fab fa-facebook text-primary me-2"></i>'
    }
    
    html = ""
    for platform in platforms:
        platform_content = [c for c in user_content if c['platform'] == platform]
        total_views = sum(c['performance']['views'] for c in platform_content)
        total_likes = sum(c['performance']['likes'] for c in platform_content)
        post_count = len(platform_content)
        
        if post_count > 0:
            html += f"""
            <div class="d-flex justify-content-between align-items-center mb-3">
                <div>
                    {platform_icons[platform]}
                    <strong data-translate="{platform}">{get_platform_name(platform)}</strong>
                </div>
                <div class="text-end">
                    <div>{total_views} views, {total_likes} likes</div>
                    <small class="text-muted">{post_count} posts</small>
                </div>
            </div>
            """
        else:
            html += f"""
            <div class="d-flex justify-content-between align-items-center mb-3">
                <div>
                    {platform_icons[platform]}
                    <strong data-translate="{platform}">{get_platform_name(platform)}</strong>
                </div>
                <div class="text-end">
                    <div class="text-muted">No posts yet</div>
                </div>
            </div>
            """
    
    return html if html else '<p class="text-muted">No social media content yet.</p>'

def generate_direction_performance_html(user_content):
    """Generate content performance by direction HTML"""
    directions = {}
    for content in user_content:
        direction = content['direction']
        if direction not in directions:
            directions[direction] = {
                'count': 0,
                'total_views': 0,
                'total_likes': 0,
                'total_shares': 0
            }
        directions[direction]['count'] += 1
        directions[direction]['total_views'] += content['performance']['views']
        directions[direction]['total_likes'] += content['performance']['likes']
        directions[direction]['total_shares'] += content['performance']['shares']
    
    if not directions:
        return '<p class="text-muted">No content generated yet.</p>'
    
    html = '<div class="row">'
    for direction, stats in directions.items():
        direction_name = get_direction_name(direction)
        direction_icon = get_direction_icon(direction).replace(' me-3', ' me-2')
        
        html += f"""
        <div class="col-md-4 mb-3">
            <div class="card">
                <div class="card-body text-center">
                    {direction_icon}
                    <h6 class="mb-2">{direction_name}</h6>
                    <div class="row text-center">
                        <div class="col-4">
                            <div class="text-primary"><strong>{stats['count']}</strong></div>
                            <small class="text-muted">Posts</small>
                        </div>
                        <div class="col-4">
                            <div class="text-success"><strong>{stats['total_views']}</strong></div>
                            <small class="text-muted">Views</small>
                        </div>
                        <div class="col-4">
                            <div class="text-info"><strong>{stats['total_likes']}</strong></div>
                            <small class="text-muted">Likes</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    html += '</div>'
    return html

def generate_social_media_manager_content(user_email, social_content, selected_platform='all'):
    """Generate social media manager content for all platforms"""
    user_name = user_email.split('@')[0] if '@' in user_email else user_email
    
    print(f"DEBUG: Generating content for {len(social_content)} social content items")
    
    # Calculate stats for all platforms
    total_posts = len(social_content)
    published_posts = len([c for c in social_content if c.get('status') == 'published'])
    scheduled_posts = len([c for c in social_content if c.get('status') == 'scheduled'])
    draft_posts = len([c for c in social_content if c.get('status') == 'draft'])
    
    # Safely calculate performance metrics
    total_views = sum(c.get('performance', {}).get('views', 0) for c in social_content)
    total_likes = sum(c.get('performance', {}).get('likes', 0) for c in social_content)
    
    print(f"DEBUG: Calculated stats - total: {total_posts}, published: {published_posts}, scheduled: {scheduled_posts}, draft: {draft_posts}")
    print(f"DEBUG: Performance - views: {total_views}, likes: {total_likes}")
    
    # Platform-specific stats
    platform_stats = {}
    for platform in ['linkedin', 'twitter', 'facebook', 'instagram', 'youtube']:
        platform_content = [c for c in social_content if c.get('platform') == platform]
        platform_stats[platform] = {
            'total': len(platform_content),
            'published': len([c for c in platform_content if c.get('status') == 'published']),
            'scheduled': len([c for c in platform_content if c.get('status') == 'scheduled']),
            'draft': len([c for c in platform_content if c.get('status') == 'draft']),
            'views': sum(c.get('performance', {}).get('views', 0) for c in platform_content),
            'likes': sum(c.get('performance', {}).get('likes', 0) for c in platform_content)
        }
    
    # Platform icons and colors
    platform_info = {
        'linkedin': {'icon': 'fab fa-linkedin', 'color': 'primary', 'name': 'LinkedIn'},
        'twitter': {'icon': 'fab fa-twitter', 'color': 'info', 'name': 'Twitter'},
        'facebook': {'icon': 'fab fa-facebook', 'color': 'primary', 'name': 'Facebook'},
        'instagram': {'icon': 'fab fa-instagram', 'color': 'danger', 'name': 'Instagram'},
        'youtube': {'icon': 'fab fa-youtube', 'color': 'danger', 'name': 'YouTube'}
    }
    
    # Generate platform filter buttons
    platform_filters = ''
    for platform, info in platform_info.items():
        active_class = 'active' if selected_platform == platform else ''
        platform_filters += f'''
        <a href="/social-media-manager?platform={platform}" class="btn btn-outline-{info['color']} {active_class}">
            <i class="{info['icon']} me-1"></i>{info['name']} ({platform_stats[platform]['total']})
        </a>'''
    
    return f"""
    <div class="container-fluid">
        <!-- Header -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card bg-primary text-white">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h2 class="mb-2"><i class="fas fa-share-alt me-2"></i>Post Management</h2>
                                <p class="mb-0">Manage and deploy your content across all social media platforms</p>
                            </div>
                            <div class="text-end">
                                <button class="btn btn-light" onclick="openSocialMediaSettings()">
                                    <i class="fas fa-cog me-2"></i>Platform Settings
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Platform Filters -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-body">
                        <h6 class="mb-3"><i class="fas fa-filter me-2"></i>Platform Filters</h6>
                        <div class="d-flex flex-wrap gap-2">
                            <a href="/social-media-manager" class="btn btn-outline-secondary {'active' if selected_platform == 'all' else ''}">
                                <i class="fas fa-globe me-1"></i>All Platforms ({total_posts})
                            </a>
                            {platform_filters}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Quick Stats -->
        <div class="row mb-4">
            <div class="col-md-2 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-file-alt fa-2x text-primary mb-2"></i>
                        <h3 class="mb-1">{total_posts}</h3>
                        <p class="text-muted mb-0">Total Posts</p>
                    </div>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-check-circle fa-2x text-success mb-2"></i>
                        <h3 class="mb-1">{published_posts}</h3>
                        <p class="text-muted mb-0">Published</p>
                    </div>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-clock fa-2x text-warning mb-2"></i>
                        <h3 class="mb-1">{scheduled_posts}</h3>
                        <p class="text-muted mb-0">Scheduled</p>
                    </div>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-edit fa-2x text-info mb-2"></i>
                        <h3 class="mb-1">{draft_posts}</h3>
                        <p class="text-muted mb-0">Drafts</p>
                    </div>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-eye fa-2x text-primary mb-2"></i>
                        <h3 class="mb-1">{total_views:,}</h3>
                        <p class="text-muted mb-0">Total Views</p>
                    </div>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-thumbs-up fa-2x text-success mb-2"></i>
                        <h3 class="mb-1">{total_likes:,}</h3>
                        <p class="text-muted mb-0">Total Likes</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Main Content -->
        <div class="row">
            <!-- Post Management -->
            <div class="col-lg-8">
                <div class="card">
                    <div class="card-header">
                        <div class="d-flex justify-content-between align-items-center">
                            <h5 class="mb-0"><i class="fas fa-list me-2"></i>Post Management</h5>
                            <div>
                                <button class="btn btn-primary btn-sm me-2" onclick="createNewPost()">
                                    <i class="fas fa-plus me-1"></i>New Post
                                </button>
                                <button class="btn btn-outline-secondary btn-sm" onclick="bulkActions()">
                                    <i class="fas fa-tasks me-1"></i>Bulk Actions
                                </button>
                            </div>
                        </div>
                    </div>
                    <div class="card-body">
                        <!-- Filters -->
                        <div class="row mb-3">
                            <div class="col-md-3">
                                <select class="form-select" id="statusFilter">
                                    <option value="">All Status</option>
                                    <option value="draft">Drafts</option>
                                    <option value="scheduled">Scheduled</option>
                                    <option value="published">Published</option>
                                </select>
                            </div>
                            <div class="col-md-3">
                                <select class="form-select" id="directionFilter">
                                    <option value="">All Directions</option>
                                    <option value="business_finance">Business & Finance</option>
                                    <option value="technology">Technology</option>
                                    <option value="health_wellness">Health & Wellness</option>
                                </select>
                            </div>
                            <div class="col-md-3">
                                <input type="date" class="form-control" id="dateFilter" placeholder="Filter by date">
                            </div>
                            <div class="col-md-3">
                                <button class="btn btn-outline-primary w-100" onclick="applyFilters()">
                                    <i class="fas fa-filter me-1"></i>Apply Filters
                                </button>
                            </div>
                        </div>
                        
                        <!-- Posts List -->
                        <div id="postsList">
                            {generate_social_media_posts_list(social_content)}
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Sidebar -->
            <div class="col-lg-4">
                <!-- Quick Actions -->
                <div class="card mb-4">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-bolt me-2"></i>Quick Actions</h6>
                    </div>
                    <div class="card-body">
                        <div class="d-grid gap-2">
                            <button class="btn btn-primary" onclick="schedulePost()">
                                <i class="fas fa-calendar-plus me-2"></i>Schedule Post
                            </button>
                            <button class="btn btn-success" onclick="publishNow()">
                                <i class="fas fa-paper-plane me-2"></i>Publish Now
                            </button>
                            <button class="btn btn-info" onclick="analyzePerformance()">
                                <i class="fas fa-chart-line me-2"></i>Analyze Performance
                            </button>
                            <button class="btn btn-warning" onclick="exportData()">
                                <i class="fas fa-download me-2"></i>Export Data
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- Platform Performance -->
                <div class="card mb-4">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-chart-pie me-2"></i>Platform Performance</h6>
                    </div>
                    <div class="card-body">
                        {generate_platform_performance_summary(platform_stats, platform_info)}
                    </div>
                </div>
                
                <!-- Scheduled Posts -->
                <div class="card mb-4">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-clock me-2"></i>Upcoming Posts</h6>
                    </div>
                    <div class="card-body">
                        {generate_scheduled_posts_list(social_content)}
                    </div>
                </div>
                
                <!-- Performance Insights -->
                <div class="card">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-chart-pie me-2"></i>Performance Insights</h6>
                    </div>
                    <div class="card-body">
                        {generate_performance_insights(social_content)}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

def generate_linkedin_manager_content(user_email, linkedin_content):
    """Generate LinkedIn manager content (legacy function)"""
    return generate_social_media_manager_content(user_email, linkedin_content, 'linkedin')
    
    # Calculate LinkedIn stats
    total_posts = len(linkedin_content)
    published_posts = len([c for c in linkedin_content if c.get('status') == 'published'])
    scheduled_posts = len([c for c in linkedin_content if c.get('status') == 'scheduled'])
    draft_posts = len([c for c in linkedin_content if c.get('status') == 'draft'])
    total_views = sum(c['performance']['views'] for c in linkedin_content)
    total_likes = sum(c['performance']['likes'] for c in linkedin_content)
    
    return f"""
    <div class="container-fluid">
        <!-- Header -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card bg-primary text-white">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h2 class="mb-2"><i class="fab fa-linkedin me-2"></i>LinkedIn Manager</h2>
                                <p class="mb-0">Manage and deploy your LinkedIn content with precision</p>
                            </div>
                            <div class="text-end">
                                <button class="btn btn-light" onclick="openLinkedInSettings()">
                                    <i class="fas fa-cog me-2"></i>LinkedIn Settings
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Quick Stats -->
        <div class="row mb-4">
            <div class="col-md-2 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-file-alt fa-2x text-primary mb-2"></i>
                        <h3 class="mb-1">{total_posts}</h3>
                        <p class="text-muted mb-0">Total Posts</p>
                    </div>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-check-circle fa-2x text-success mb-2"></i>
                        <h3 class="mb-1">{published_posts}</h3>
                        <p class="text-muted mb-0">Published</p>
                    </div>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-clock fa-2x text-warning mb-2"></i>
                        <h3 class="mb-1">{scheduled_posts}</h3>
                        <p class="text-muted mb-0">Scheduled</p>
                    </div>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-edit fa-2x text-info mb-2"></i>
                        <h3 class="mb-1">{draft_posts}</h3>
                        <p class="text-muted mb-0">Drafts</p>
                    </div>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-eye fa-2x text-primary mb-2"></i>
                        <h3 class="mb-1">{total_views:,}</h3>
                        <p class="text-muted mb-0">Total Views</p>
                    </div>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-thumbs-up fa-2x text-success mb-2"></i>
                        <h3 class="mb-1">{total_likes:,}</h3>
                        <p class="text-muted mb-0">Total Likes</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Main Content -->
        <div class="row">
            <!-- Post Management -->
            <div class="col-lg-8">
                <div class="card">
                    <div class="card-header">
                        <div class="d-flex justify-content-between align-items-center">
                            <h5 class="mb-0"><i class="fas fa-list me-2"></i>Post Management</h5>
                            <div>
                                <button class="btn btn-primary btn-sm me-2" onclick="createNewPost()">
                                    <i class="fas fa-plus me-1"></i>New Post
                                </button>
                                <button class="btn btn-outline-secondary btn-sm" onclick="bulkActions()">
                                    <i class="fas fa-tasks me-1"></i>Bulk Actions
                                </button>
                            </div>
                        </div>
                    </div>
                    <div class="card-body">
                        <!-- Filters -->
                        <div class="row mb-3">
                            <div class="col-md-3">
                                <select class="form-select" id="statusFilter">
                                    <option value="">All Status</option>
                                    <option value="draft">Drafts</option>
                                    <option value="scheduled">Scheduled</option>
                                    <option value="published">Published</option>
                                </select>
                            </div>
                            <div class="col-md-3">
                                <select class="form-select" id="directionFilter">
                                    <option value="">All Directions</option>
                                    <option value="business_finance">Business & Finance</option>
                                    <option value="technology">Technology</option>
                                    <option value="health_wellness">Health & Wellness</option>
                                </select>
                            </div>
                            <div class="col-md-3">
                                <input type="date" class="form-control" id="dateFilter" placeholder="Filter by date">
                            </div>
                            <div class="col-md-3">
                                <button class="btn btn-outline-primary w-100" onclick="applyFilters()">
                                    <i class="fas fa-filter me-1"></i>Apply Filters
                                </button>
                            </div>
                        </div>
                        
                        <!-- Posts List -->
                        <div id="postsList">
                            {generate_linkedin_posts_list(linkedin_content)}
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Sidebar -->
            <div class="col-lg-4">
                <!-- Quick Actions -->
                <div class="card mb-4">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-bolt me-2"></i>Quick Actions</h6>
                    </div>
                    <div class="card-body">
                        <div class="d-grid gap-2">
                            <button class="btn btn-primary" onclick="schedulePost()">
                                <i class="fas fa-calendar-plus me-2"></i>Schedule Post
                            </button>
                            <button class="btn btn-success" onclick="publishNow()">
                                <i class="fas fa-paper-plane me-2"></i>Publish Now
                            </button>
                            <button class="btn btn-info" onclick="analyzePerformance()">
                                <i class="fas fa-chart-line me-2"></i>Analyze Performance
                            </button>
                            <button class="btn btn-warning" onclick="exportData()">
                                <i class="fas fa-download me-2"></i>Export Data
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- Scheduled Posts -->
                <div class="card mb-4">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-clock me-2"></i>Upcoming Posts</h6>
                    </div>
                    <div class="card-body">
                        {generate_scheduled_posts_list(linkedin_content)}
                    </div>
                </div>
                
                <!-- Performance Insights -->
                <div class="card">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-chart-pie me-2"></i>Performance Insights</h6>
                    </div>
                    <div class="card-body">
                        {generate_performance_insights(linkedin_content)}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

def generate_social_media_posts_list(social_content):
    """Generate social media posts list HTML for all platforms"""
    if not social_content:
        return '<p class="text-muted text-center">No social media posts found. Create your first post!</p>'
    
    html = ""
    for content in social_content:
        platform = content.get('platform', 'unknown')
        platform_info = {
            'linkedin': {'icon': 'fab fa-linkedin', 'color': 'primary', 'name': 'LinkedIn'},
            'twitter': {'icon': 'fab fa-twitter', 'color': 'info', 'name': 'Twitter'},
            'facebook': {'icon': 'fab fa-facebook', 'color': 'primary', 'name': 'Facebook'},
            'instagram': {'icon': 'fab fa-instagram', 'color': 'danger', 'name': 'Instagram'},
            'youtube': {'icon': 'fab fa-youtube', 'color': 'danger', 'name': 'YouTube'}
        }.get(platform, {'icon': 'fas fa-share-alt', 'color': 'secondary', 'name': platform.title()})
        
        status_badge = get_status_badge(content.get('status', 'draft'))
        direction_icon = get_direction_icon(content.get('direction', 'business_finance'))
        direction_name = get_direction_name(content.get('direction', 'business_finance'))
        time_ago = get_time_ago(content.get('created_at', ''))
        
        html += f"""
        <div class="card mb-3 post-item" data-id="{content.get('id', '')}" data-status="{content.get('status', 'draft')}" data-direction="{content.get('direction', 'business_finance')}" data-platform="{platform}">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <div class="d-flex align-items-center">
                        <i class="{platform_info['icon']} text-{platform_info['color']} me-2"></i>
                        <span class="badge bg-{platform_info['color']} me-2">{platform_info['name']}</span>
                        {status_badge}
                    </div>
                    <div class="dropdown">
                        <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                            <i class="fas fa-ellipsis-v"></i>
                        </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#" onclick="editPost('{content.get('id', '')}')">
                                <i class="fas fa-edit me-2"></i>Edit
                            </a></li>
                            <li><a class="dropdown-item" href="#" onclick="duplicatePost('{content.get('id', '')}')">
                                <i class="fas fa-copy me-2"></i>Duplicate
                            </a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item text-danger" href="#" onclick="deletePost('{content.get('id', '')}')">
                                <i class="fas fa-trash me-2"></i>Delete
                            </a></li>
                        </ul>
                    </div>
                </div>
                
                <div class="row align-items-center">
                    <div class="col-md-8">
                        <p class="mb-2">{content.get('content', '')[:150]}{'...' if len(content.get('content', '')) > 150 else ''}</p>
                        <div class="d-flex gap-2">
                            {direction_icon}
                            <div>
                                <h6 class="mb-1">{content.get('topic', 'Untitled Post')[:60]}{'...' if len(content.get('topic', '')) > 60 else ''}</h6>
                                <small class="text-muted">{direction_name} • {time_ago}</small>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 text-end">
                        <div class="small text-muted">
                            <div><i class="fas fa-eye me-1"></i>{content.get('performance', {}).get('views', 0):,} views</div>
                            <div><i class="fas fa-thumbs-up me-1"></i>{content.get('performance', {}).get('likes', 0):,} likes</div>
                            <div><i class="fas fa-share me-1"></i>{content.get('performance', {}).get('shares', 0):,} shares</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    return html

def generate_platform_performance_summary(platform_stats, platform_info):
    """Generate platform performance summary HTML"""
    html = ""
    for platform, stats in platform_stats.items():
        if stats['total'] > 0:
            info = platform_info.get(platform, {'icon': 'fas fa-share-alt', 'color': 'secondary', 'name': platform.title()})
            html += f"""
            <div class="d-flex justify-content-between align-items-center mb-3">
                <div>
                    <i class="{info['icon']} text-{info['color']} me-2"></i>
                    <strong>{info['name']}</strong>
                </div>
                <div class="text-end">
                    <div>{stats['views']:,} views, {stats['likes']:,} likes</div>
                    <small class="text-muted">{stats['total']} posts</small>
                </div>
            </div>"""
    
    if not html:
        html = '<p class="text-muted text-center">No performance data available</p>'
    
    return html

def generate_linkedin_posts_list(linkedin_content):
    """Generate LinkedIn posts list HTML (legacy function)"""
    return generate_social_media_posts_list(linkedin_content)
    
    html = ""
    for content in linkedin_content:
        status = content.get('status', 'draft')
        status_badge = get_status_badge(status)
        direction_icon = get_direction_icon(content['direction'])
        direction_name = get_direction_name(content['direction'])
        time_ago = get_time_ago(content['created_at'])
        
        html += f"""
        <div class="card mb-3 post-item" data-id="{content['id']}" data-status="{status}" data-direction="{content['direction']}">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <div class="d-flex align-items-center">
                        {direction_icon}
                        <div>
                            <h6 class="mb-1">{content['topic'][:60]}{'...' if len(content['topic']) > 60 else ''}</h6>
                            <small class="text-muted">{direction_name} • {time_ago}</small>
                        </div>
                    </div>
                    <div class="dropdown">
                        <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                            <i class="fas fa-ellipsis-v"></i>
                        </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#" onclick="editPost('{content['id']}')">
                                <i class="fas fa-edit me-2"></i>Edit
                            </a></li>
                            <li><a class="dropdown-item" href="#" onclick="duplicatePost('{content['id']}')">
                                <i class="fas fa-copy me-2"></i>Duplicate
                            </a></li>
                            <li><a class="dropdown-item" href="#" onclick="schedulePost('{content['id']}')">
                                <i class="fas fa-calendar me-2"></i>Schedule
                            </a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item text-danger" href="#" onclick="deletePost('{content['id']}')">
                                <i class="fas fa-trash me-2"></i>Delete
                            </a></li>
                        </ul>
                    </div>
                </div>
                
                <div class="row align-items-center">
                    <div class="col-md-8">
                        <p class="mb-2">{content['content'][:150]}{'...' if len(content['content']) > 150 else ''}</p>
                        <div class="d-flex gap-2">
                            {status_badge}
                            <span class="badge bg-primary">{get_platform_name(content['platform'])}</span>
                        </div>
                    </div>
                    <div class="col-md-4 text-end">
                        <div class="small text-muted">
                            <div><i class="fas fa-eye me-1"></i>{content.get('performance', {}).get('views', 0):,} views</div>
                            <div><i class="fas fa-thumbs-up me-1"></i>{content.get('performance', {}).get('likes', 0):,} likes</div>
                            <div><i class="fas fa-share me-1"></i>{content.get('performance', {}).get('shares', 0):,} shares</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    return html

def generate_scheduled_posts_list(linkedin_content):
    """Generate scheduled posts list HTML"""
    scheduled_posts = [c for c in linkedin_content if c.get('status') == 'scheduled']
    
    if not scheduled_posts:
        return '<p class="text-muted small">No scheduled posts</p>'
    
    html = ""
    for post in scheduled_posts[:3]:  # Show only next 3
        scheduled_time = post.get('scheduled_time', 'TBD')
        html += f"""
        <div class="d-flex align-items-center mb-2">
            <div class="flex-grow-1">
                <div class="small fw-bold">{post['topic'][:40]}{'...' if len(post['topic']) > 40 else ''}</div>
                <div class="small text-muted">{scheduled_time}</div>
            </div>
            <button class="btn btn-sm btn-outline-danger" onclick="cancelSchedule('{post['id']}')">
                <i class="fas fa-times"></i>
            </button>
        </div>
        """
    
    return html

def generate_performance_insights(linkedin_content):
    """Generate performance insights HTML"""
    if not linkedin_content:
        return '<p class="text-muted small">No performance data available</p>'
    
    # Calculate insights with safe division
    total_posts = len(linkedin_content)
    if total_posts == 0:
        return '<p class="text-muted small">No performance data available</p>'
    
    total_views = sum(c.get('performance', {}).get('views', 0) for c in linkedin_content)
    total_likes = sum(c.get('performance', {}).get('likes', 0) for c in linkedin_content)
    
    avg_views = total_views / total_posts if total_posts > 0 else 0
    avg_likes = total_likes / total_posts if total_posts > 0 else 0
    
    # Find best performing post safely
    best_performing = None
    if linkedin_content:
        try:
            best_performing = max(linkedin_content, key=lambda x: x.get('performance', {}).get('views', 0))
        except:
            best_performing = None
    
    # Calculate engagement rate safely
    engagement_rate = (avg_likes / avg_views * 100) if avg_views > 0 else 0
    
    # Prepare best performing display
    best_topic = "No content"
    best_views = 0
    if best_performing and best_performing.get('topic'):
        best_topic = best_performing.get('topic', 'No content')[:30]
        best_views = best_performing.get('performance', {}).get('views', 0)
    
    return f"""
    <div class="small">
        <div class="mb-2">
            <strong>Average Performance:</strong>
            <div class="text-muted">{avg_views:.0f} views per post</div>
            <div class="text-muted">{avg_likes:.0f} likes per post</div>
        </div>
        <div class="mb-2">
            <strong>Best Performing:</strong>
            <div class="text-muted">{best_topic}...</div>
            <div class="text-success">{best_views:,} views</div>
        </div>
        <div>
            <strong>Engagement Rate:</strong>
            <div class="text-muted">{engagement_rate:.1f}%</div>
        </div>
    </div>
    """

def get_status_badge(status):
    """Get status badge HTML"""
    badges = {
        'draft': '<span class="badge bg-secondary">Draft</span>',
        'scheduled': '<span class="badge bg-warning">Scheduled</span>',
        'published': '<span class="badge bg-success">Published</span>',
        'failed': '<span class="badge bg-danger">Failed</span>'
    }
    return badges.get(status, '<span class="badge bg-secondary">Draft</span>')

# Base template with navigation
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Content Creator Pro</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .navbar { 
            background: rgba(255,255,255,0.1) !important; 
            backdrop-filter: blur(10px); 
            position: fixed !important;
            top: 0;
            width: 100%;
            z-index: 1000;
        }
        .navbar-brand { color: #fff !important; font-weight: bold; }
        .nav-link { color: #fff !important; }
        .nav-link:hover { color: #f0f0f0 !important; }
        .main-content { padding: 100px 0 50px 0; color: #fff; }
        .card { background: rgba(255,255,255,0.95); border: none; border-radius: 15px; }
        .btn-primary { background: linear-gradient(45deg, #667eea, #764ba2); border: none; }
        .feature-card { background: #fff; border-radius: 15px; padding: 30px; margin: 20px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.1); color: #222; }
        .feature-card h3, .feature-card p { color: #222 !important; text-shadow: none; }
        h1, h2, h3, p, .lead { color: #fff !important; text-shadow: 0 2px 8px rgba(0,0,0,0.25); }
        
        /* Card text visibility fixes */
        .card h3, .card h4, .card h5, .card h6 { color: #333 !important; text-shadow: none; }
        .card p, .card span, .card div { color: #333 !important; text-shadow: none; }
        .card label { color: #333 !important; font-weight: 600; text-shadow: none; }
        .card .text-muted { color: #666 !important; text-shadow: none; }
        .card .badge { color: #fff !important; text-shadow: none; }
        .card strong { color: #333 !important; text-shadow: none; }
        .card small { color: #666 !important; text-shadow: none; }
        
        /* Form elements visibility */
        .form-control, .form-select { 
            border-radius: 10px; 
            border: 2px solid #e0e0e0; 
            color: #333 !important;
            background: #fff !important;
        }
        .form-control:focus, .form-select:focus { 
            border-color: #667eea; 
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25); 
            color: #333 !important;
        }
        .form-label { color: #333 !important; font-weight: 600; text-shadow: none; }
        
        /* Button text visibility */
        .btn { color: #fff !important; text-shadow: none; }
        .btn-outline-secondary { color: #6c757d !important; border-color: #6c757d; }
        .btn-outline-primary { color: #667eea !important; border-color: #667eea; }
        .btn-outline-success { color: #28a745 !important; border-color: #28a745; }
        .btn-outline-info { color: #17a2b8 !important; border-color: #17a2b8; }
        .btn-outline-warning { color: #ffc107 !important; border-color: #ffc107; }
        .btn-outline-danger { color: #dc3545 !important; border-color: #dc3545; }
        
        /* Direction Cards */
        .direction-card {
            background: #fff;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 15px;
            margin: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
            color: #333 !important;
        }
        .direction-card:hover {
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
        }
        .direction-card.selected {
            border-color: #667eea;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: #fff !important;
        }
        .direction-card i {
            font-size: 24px;
            margin-bottom: 8px;
        }
        .direction-card div {
            color: inherit !important;
            text-shadow: none;
        }
        
        /* Step Progress */
        .step-progress {
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
        }
        .step {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: rgba(255,255,255,0.3);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 10px;
            font-weight: bold;
        }
        .step.active {
            background: #667eea;
        }
        .step.completed {
            background: #28a745;
        }
        
        /* User Welcome */
        .user-welcome {
            color: #fff;
            font-size: 14px;
            margin-right: 15px;
        }
        
        /* Alert and notification visibility */
        .alert { color: #333 !important; text-shadow: none; }
        .alert h5 { color: #333 !important; text-shadow: none; }
        .alert p { color: #333 !important; text-shadow: none; }
        
        /* Input group visibility */
        .input-group-text { 
            background: #f8f9fa !important; 
            color: #495057 !important; 
            border-color: #e0e0e0;
        }
        
        /* Table visibility */
        .table { color: #333 !important; }
        .table th { color: #333 !important; }
        .table td { color: #333 !important; }
        
        /* List visibility */
        .list-group-item { color: #333 !important; }
        
        /* Modal visibility */
        .modal-content { color: #333 !important; }
        .modal-header { color: #333 !important; }
        .modal-body { color: #333 !important; }
        .modal-footer { color: #333 !important; }
        
        /* Dropdown visibility */
        .dropdown-menu { color: #333 !important; }
        .dropdown-item { color: #333 !important; }
        .dropdown-item.active { 
            background-color: #667eea !important; 
            color: #fff !important; 
        }
        
        /* Progress bar visibility */
        .progress { background: rgba(255,255,255,0.3) !important; }
        .progress-bar { color: #fff !important; }
        
        /* Spinner visibility */
        .fa-spinner { color: #667eea !important; }
        
        /* Ensure all text in cards is visible */
        .card * { color: inherit !important; }
        .card .text-primary { color: #667eea !important; }
        .card .text-success { color: #28a745 !important; }
        .card .text-warning { color: #ffc107 !important; }
        .card .text-info { color: #17a2b8 !important; }
        .card .text-danger { color: #dc3545 !important; }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-rocket me-2"></i>Content Creator Pro
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <!-- Language Selector -->
                    <li class="nav-item dropdown me-3">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-globe me-1"></i>
                            <span id="current-language" data-translate="english">English</span>
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item language-option" href="#" data-lang="en">
                                <i class="fas fa-flag me-2"></i><span data-translate="english">English</span>
                            </a></li>
                            <li><a class="dropdown-item language-option" href="#" data-lang="zh">
                                <i class="fas fa-flag me-2"></i><span data-translate="chinese">中文</span>
                            </a></li>
                        </ul>
                    </li>
                    
                    <li class="nav-item">
                        <a class="nav-link" href="/home"><i class="fas fa-home me-1"></i><span data-translate="home">Home</span></a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/generator"><i class="fas fa-magic me-1"></i><span data-translate="generator">Generator</span></a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/dashboard"><i class="fas fa-chart-line me-1"></i><span data-translate="dashboard">Dashboard</span></a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/library"><i class="fas fa-book me-1"></i><span data-translate="library">Library</span></a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/social-media-manager"><i class="fas fa-share-alt me-1"></i><span data-translate="post_management">Post Management</span></a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/settings"><i class="fas fa-cog me-1"></i><span data-translate="settings">Settings</span></a>
                    </li>
                    {% if 'user' in session %}
                    <li class="nav-item">
                        <span class="user-welcome">
                            <i class="fas fa-user me-1"></i><span data-translate="welcome">Welcome</span>, {{ session['user'].split('@')[0] if '@' in session['user'] else session['user'] }}
                        </span>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/logout"><i class="fas fa-sign-out-alt me-1"></i><span data-translate="logout">Logout</span></a>
                    </li>
                    {% else %}
                    <li class="nav-item">
                        <a class="nav-link" href="/login"><i class="fas fa-sign-in-alt me-1"></i><span data-translate="login">Login</span></a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/register"><i class="fas fa-user-plus me-1"></i><span data-translate="register">Register</span></a>
                    </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="main-content">

        
        <!-- Flash Messages -->
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="container mb-4">
                    {% for category, message in messages %}
                        <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show" role="alert">
                            <i class="fas fa-{{ 'exclamation-triangle' if category == 'error' or category == 'danger' else 'check-circle' if category == 'success' else 'info-circle' }} me-2"></i>
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}
        
        {{ content | safe }}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    
    <!-- Translation System -->
    <script>
    // Global variables
    let currentLanguage = '{{ session.get("language", "en") }}';
    
    // Translation dictionary
    const translations = {
        en: {
            // Navigation
            'dashboard': 'Dashboard',
            'generator': 'Generator',
            'library': 'Library',
            'settings': 'Settings',
            'account': 'Account',
            'logout': 'Logout',
            'login': 'Login',
            'register': 'Register',
            'english': 'English',
            'chinese': '中文',
            'home': 'Home',
            'welcome': 'Welcome',
            
            // Common
            'loading': 'Loading...',
            'error': 'Error',
            'success': 'Success',
            'cancel': 'Cancel',
            'save': 'Save',
            'edit': 'Edit',
            'delete': 'Delete',
            'close': 'Close',
            'submit': 'Submit',
            'back': 'Back',
            'next': 'Next',
            'previous': 'Previous',
            'continue': 'Continue',
            'finish': 'Finish',
            
            // Generator page
            'content_generator': 'Content Generator',
            'step_1': 'Step 1',
            'step_2': 'Step 2',
            'step_3': 'Step 3',
            'step_4': 'Step 4',
            'step_5': 'Step 5',
            'choose_direction': 'Choose Your Content Direction',
            'choose_platform': 'Choose Your Platform',
            'what_inspires': 'What Inspires You?',
            'generate_content': 'Generate Content',
            'linkedin': 'LinkedIn',
            'facebook': 'Facebook',
            'instagram': 'Instagram',
            'twitter': 'Twitter',
            'youtube_shorts': 'YouTube Shorts',
            'blog_article': 'Blog Article',
            'professional': 'Professional',
            'casual': 'Casual',
            'inspirational': 'Inspirational',
            'educational': 'Educational',
            'entertaining': 'Entertaining',
            
            // Landing page
            'content_creator_pro': 'Content Creator Pro',
            'ai_powered_platform': 'AI-Powered Content Generation Platform',
            'multi_platform_content': 'Multi-Platform Content',
            'generate_content_for': 'Generate content for',
            'platforms_list': 'LinkedIn, Facebook, Instagram, Twitter, YouTube, and blogs',
            'smart_direction': 'Smart Direction',
            'content_directions_desc': '18 content directions with',
            'regional_context': 'regional and cultural context',
            'ai_powered': 'AI-Powered',
            'advanced_ai_generation': 'Advanced AI content generation with',
            'tone_customization': 'tone and style customization',
            'start_creating': 'Start Creating',
            'try_demo': 'Try Demo',
            
            // Content directions
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
            'personal_dev': 'Personal Dev',
            'parenting_family': 'Parenting & Family',
            'art_creativity': 'Art & Creativity',
            'real_estate': 'Real Estate',
            'automotive': 'Automotive',
            'pet_care': 'Pet Care',
            
            // Generator page
            'create_engaging_content': 'Create engaging content with AI assistance',
            'choose_your_focus': 'Choose Your Focus',
            'next_step': 'Next Step',
            
            // Step titles
            'step_2': 'Step 2',
            'step_3': 'Step 3',
            'step_3_5': 'Step 3.5',
            'step_4': 'Step 4',
            'what_type_content': 'What Type of Content?',
            'what_inspires_you': 'What Inspires You?',
            'choose_your_topic': 'Choose Your Topic',
            'how_should_sound': 'How Should It Sound?',
            
            // Content types
            'linkedin_post': 'LinkedIn Post',
            'facebook_post': 'Facebook Post',
            'instagram_post': 'Instagram Post',
            'twitter_post': 'Twitter Post',
            'youtube_short': 'YouTube Short',
            'blog_article': 'Blog Article',
            
            // Inspiration sources
            'latest_news': 'Latest News',
            'popular_books': 'Popular Books',
            'trending_threads': 'Trending Threads',
            'podcasts': 'Podcasts',
            'youtube_videos': 'YouTube Videos',
            'research_papers': 'Research Papers',
            'case_studies': 'Case Studies',
            'trending_topics': 'Trending Topics',
            
            // Topic selection
            'book_title': 'Book Title',
            'author': 'Author',
            'enter_book_title': 'Enter book title...',
            'enter_author_name': 'Enter author name...',
            'find_topics': 'Find Topics',
            'podcast_link': 'Podcast Link',
            'enter_podcast_url': 'Enter podcast URL...',
            'youtube_video_link': 'YouTube Video Link',
            'enter_youtube_video_url': 'Enter YouTube video URL...',
            'research_paper_pdf': 'Research Paper (PDF)',
            'upload_find_topics': 'Upload & Find Topics',
            'available_topics': 'Available Topics',
            'refresh': 'Refresh',
            'podcast_link': 'Podcast Link',
            'enter_podcast_url': 'Enter podcast URL...',
            'youtube_video_link': 'YouTube Video Link',
            'enter_youtube_video_url': 'Enter YouTube video URL...',
            'research_paper_pdf': 'Research Paper (PDF)',
            'generated_content': 'Generated Content',
            'copy': 'Copy',
            'save_to_library': 'Save to Library',
            'humorous': 'Humorous',
            'serious': 'Serious',
            'welcome_back': 'Welcome back',
            'your_focus': 'Your focus',
            'quick_stats': 'Quick Stats',
            'content_generated': 'Content Generated',
            'this_month': 'This Month',
            'library_items': 'Library Items',
            'social_posts': 'Social Posts',
            'quick_actions': 'Quick Actions',
            'generate_new_content': 'Generate New Content',
            'view_library': 'View Library',
            'social_media': 'Social Media',
            'analytics': 'Analytics',
            'recent_content_by_direction': 'Recent Content by Direction',
            'business': 'Business',
            'tech': 'Tech',
            'twitter_thread': 'Twitter Thread',
            '2_hours_ago': '2 hours ago',
            '1_day_ago': '1 day ago',
            '3_days_ago': '3 days ago',
            '1_week_ago': '1 week ago',
            'linkedin': 'LinkedIn',
            'twitter': 'Twitter',
            'instagram': 'Instagram',
            'blog': 'Blog',
            'email': 'Email',
            'password': 'Password',
            'already_have_account': 'Already have an account?',
            'login_here': 'Login here',
            'dont_have_account': 'Don\'t have an account?',
            'register_here': 'Register here',
            'demo_credentials': 'Demo Credentials:',
            'social_media_performance': 'Social Media Performance',
            'content_performance_by_direction': 'Content Performance by Direction',
            'no_content_generated_yet': 'No content generated yet.',
            'no_social_media_content_yet': 'No social media content yet.',
            'no_posts_yet': 'No posts yet',
            'linkedin_manager': 'LinkedIn Manager',
        'social_media_manager': 'Social Media Manager',
        'post_management': 'Post Management',
        'account_management': 'Account Management',
        'connect_account': 'Connect Account',
        'disconnect_account': 'Disconnect Account',
        'manage_account': 'Manage Account',
        'account_status': 'Account Status',
        'permissions': 'Permissions',
        'security': 'Security',
        'export_data': 'Export Data',
        'revoke_permissions': 'Revoke Permissions',
            'translate_to_chinese': 'Translate to Chinese',
            'translate_to_english': 'Translate to English',
            'step_5': 'Step 5',
            'review_and_generate': 'Review & Generate',
            'your_selections': 'Your Selections',
            'direction': 'Direction',
            'platform': 'Platform',
            'source': 'Source',
            'topic': 'Topic',
            'tone': 'Tone',
            'review_message': 'Review your selections above. Click Generate to create your content.',
            
            // Tone options
            'professional': 'Professional',
            'casual': 'Casual',
            'inspirational': 'Inspirational',
            'educational': 'Educational',
            'humorous': 'Humorous',
            'serious': 'Serious',
            
            // Navigation buttons
            'previous': 'Previous',
            'generate_content': 'Generate Content',
            
            // Result section
            'generated_content': 'Generated Content',
            'copy': 'Copy',
            'save_to_library': 'Save to Library'
        },
        zh: {
            // Navigation
            'dashboard': '仪表板',
            'generator': '生成器',
            'library': '库',
            'settings': '设置',
            'account': '账户',
            'logout': '登出',
            'login': '登录',
            'register': '注册',
            'english': 'English',
            'chinese': '中文',
            'home': '首页',
            'welcome': '欢迎',
            
            // Common
            'loading': '加载中...',
            'error': '错误',
            'success': '成功',
            'cancel': '取消',
            'save': '保存',
            'edit': '编辑',
            'delete': '删除',
            'close': '关闭',
            'submit': '提交',
            'back': '返回',
            'next': '下一步',
            'previous': '上一步',
            'continue': '继续',
            'finish': '完成',
            
            // Generator page
            'content_generator': '内容生成器',
            'step_1': '第1步',
            'step_2': '第2步',
            'step_3': '第3步',
            'step_4': '第4步',
            'step_5': '第5步',
            'choose_direction': '选择您的内容方向',
            'choose_platform': '选择您的平台',
            'what_inspires': '什么激励着您？',
            'generate_content': '生成内容',
            'linkedin': '领英',
            'facebook': '脸书',
            'instagram': 'Instagram',
            'twitter': '推特',
            'youtube_shorts': 'YouTube短视频',
            'blog_article': '博客文章',
            'professional': '专业',
            'casual': '随意',
            'inspirational': '励志',
            'educational': '教育',
            'entertaining': '娱乐',
            
            // Landing page
            'content_creator_pro': '内容创作者专业版',
            'ai_powered_platform': 'AI驱动的内容生成平台',
            'multi_platform_content': '多平台内容',
            'generate_content_for': '为以下平台生成内容',
            'platforms_list': '领英、脸书、Instagram、推特、YouTube和博客',
            'smart_direction': '智能方向',
            'content_directions_desc': '18个内容方向，具有',
            'regional_context': '区域和文化背景',
            'ai_powered': 'AI驱动',
            'advanced_ai_generation': '先进的AI内容生成，具有',
            'tone_customization': '语气和风格定制',
            'start_creating': '开始创作',
            'try_demo': '试用演示',
            
            // Content directions
            'business_finance': '商业与金融',
            'technology': '技术',
            'health_wellness': '健康与保健',
            'education': '教育',
            'entertainment': '娱乐',
            'travel_tourism': '旅游',
            'food_cooking': '美食烹饪',
            'fashion_beauty': '时尚美容',
            'sports_fitness': '运动健身',
            'science_research': '科学研究',
            'politics_news': '政治新闻',
            'environment': '环境',
            'personal_dev': '个人发展',
            'parenting_family': '育儿家庭',
            'art_creativity': '艺术创意',
            'real_estate': '房地产',
            'automotive': '汽车',
            'pet_care': '宠物护理',
            
            // Generator page
            'create_engaging_content': '使用AI辅助创建引人入胜的内容',
            'choose_your_focus': '选择您的重点',
            'next_step': '下一步',
            
            // Step titles
            'step_2': '第2步',
            'step_3': '第3步',
            'step_3_5': '第3.5步',
            'step_4': '第4步',
            'what_type_content': '什么类型的内容？',
            'what_inspires_you': '什么激励着您？',
            'choose_your_topic': '选择您的主题',
            'how_should_sound': '应该听起来如何？',
            
            // Content types
            'linkedin_post': '领英帖子',
            'facebook_post': '脸书帖子',
            'instagram_post': 'Instagram帖子',
            'twitter_post': '推特帖子',
            'youtube_short': 'YouTube短视频',
            'blog_article': '博客文章',
            
            // Inspiration sources
            'latest_news': '最新新闻',
            'popular_books': '热门书籍',
            'trending_threads': '热门讨论',
            'podcasts': '播客',
            'youtube_videos': 'YouTube视频',
            'research_papers': '研究论文',
            'case_studies': '案例研究',
            'trending_topics': '热门话题',
            
            // Topic selection
            'book_title': '书名',
            'author': '作者',
            'enter_book_title': '输入书名...',
            'enter_author_name': '输入作者姓名...',
            'find_topics': '查找主题',
            'podcast_link': '播客链接',
            'enter_podcast_url': '输入播客URL...',
            'youtube_video_link': 'YouTube视频链接',
            'enter_youtube_video_url': '输入YouTube视频URL...',
            'research_paper_pdf': '研究论文(PDF)',
            'upload_find_topics': '上传并查找主题',
            'available_topics': '可用主题',
            'refresh': '刷新',
            'podcast_link': '播客链接',
            'enter_podcast_url': '输入播客网址...',
            'youtube_video_link': 'YouTube视频链接',
            'enter_youtube_video_url': '输入YouTube视频网址...',
            'research_paper_pdf': '研究论文 (PDF)',
            'generated_content': '生成的内容',
            'copy': '复制',
            'save_to_library': '保存到库',
            'humorous': '幽默',
            'serious': '严肃',
            'welcome_back': '欢迎回来',
            'your_focus': '您的重点',
            'quick_stats': '快速统计',
            'content_generated': '生成的内容',
            'this_month': '本月',
            'library_items': '库项目',
            'social_posts': '社交帖子',
            'quick_actions': '快速操作',
            'generate_new_content': '生成新内容',
            'view_library': '查看库',
            'social_media': '社交媒体',
            'analytics': '分析',
            'recent_content_by_direction': '按方向的最新内容',
            'business': '商业',
            'tech': '科技',
            'twitter_thread': 'Twitter线程',
            '2_hours_ago': '2小时前',
            '1_day_ago': '1天前',
            '3_days_ago': '3天前',
            '1_week_ago': '1周前',
            'linkedin': '领英',
            'twitter': '推特',
            'instagram': 'Instagram',
            'blog': '博客',
            'email': '邮箱',
            'password': '密码',
            'already_have_account': '已有账户？',
            'login_here': '在此登录',
            'dont_have_account': '没有账户？',
            'register_here': '在此注册',
            'demo_credentials': '演示凭据：',
            'social_media_performance': '社交媒体表现',
            'content_performance_by_direction': '按方向的内容表现',
            'no_content_generated_yet': '尚未生成内容。',
            'no_social_media_content_yet': '尚无社交媒体内容。',
            'no_posts_yet': '尚无帖子',
            'linkedin_manager': 'LinkedIn管理器',
        'social_media_manager': '社交媒体管理器',
        'post_management': '帖子管理',
        'account_management': '账户管理',
        'connect_account': '连接账户',
        'disconnect_account': '断开连接',
        'manage_account': '管理账户',
        'account_status': '账户状态',
        'permissions': '权限',
        'security': '安全',
        'export_data': '导出数据',
        'revoke_permissions': '撤销权限',
            'translate_to_chinese': '翻译成中文',
            'translate_to_english': '翻译成英文',
            'step_5': '第5步',
            'review_and_generate': '审查和生成',
            'your_selections': '您的选择',
            'direction': '方向',
            'platform': '平台',
            'source': '来源',
            'topic': '主题',
            'tone': '语调',
            'review_message': '查看上面的选择。点击生成来创建您的内容。',
            
            // Tone options
            'professional': '专业',
            'casual': '随意',
            'inspirational': '励志',
            'educational': '教育',
            'humorous': '幽默',
            'serious': '严肃',
            
            // Navigation buttons
            'previous': '上一步',
            'generate_content': '生成内容',
            
            // Result section
            'generated_content': '生成的内容',
            'copy': '复制',
            'save_to_library': '保存到库'
        }
    };
    
    // Translation functions
    function switchLanguage(lang) {
        console.log('Switching language to:', lang);
        currentLanguage = lang;
        
        // Update UI to show current language
        updateLanguageDisplay(lang);
        
        // Translate the entire page
        translatePage(lang);
        
        // Send AJAX request to update server-side language preference
        $.ajax({
            url: '/language/' + lang,
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(response) {
                console.log('Language switch response:', response);
            },
            error: function(xhr, status, error) {
                console.log('Language switch error:', xhr, status, error);
            }
        });
    }
    
    function updateLanguageDisplay(lang) {
        console.log('Updating language display for:', lang);
        const languageNames = {
            'en': 'English',
            'zh': '中文'
        };
        
        $('#current-language').text(languageNames[lang] || 'English');
        
        // Update the dropdown text as well
        $('.language-option').each(function() {
            const optionLang = $(this).data('lang');
            if (optionLang === lang) {
                $(this).addClass('active');
                // Update the dropdown toggle text
                $('#current-language').text(languageNames[optionLang]);
            } else {
                $(this).removeClass('active');
            }
        });
    }
    
    function translatePage(lang) {
        console.log('Translating page to:', lang);
        const langDict = translations[lang] || translations['en'];
        console.log('Translation dictionary keys:', Object.keys(langDict).length);
        console.log('Available translation keys:', Object.keys(langDict));
        
        // Count elements to translate
        const elementsToTranslate = $('[data-translate]');
        console.log('Elements with data-translate attribute found:', elementsToTranslate.length);
        
        // Translate all elements with data-translate attribute
        $('[data-translate]').each(function() {
            const key = $(this).data('translate');
            const translation = langDict[key];
            if (translation) {
                $(this).text(translation);
                console.log('Translated ' + key + ' to:', translation);
            } else {
                console.log('No translation found for key: ' + key);
            }
        });
        
        // Translate placeholders
        $('[data-translate-placeholder]').each(function() {
            const key = $(this).data('translate-placeholder');
            const translation = langDict[key];
            if (translation) {
                $(this).attr('placeholder', translation);
                console.log('Translated placeholder ' + key + ' to:', translation);
            } else {
                console.log('No translation found for placeholder key: ' + key);
            }
        });
        
        // Update HTML lang attribute
        $('html').attr('lang', lang);
        console.log('Page translation completed');
    }
    
    // Initialize on page load
    $(document).ready(function() {
        console.log('Document ready, initializing translation system...');
        
        // Set up event listeners for language selector
        $('.language-option').on('click', function(e) {
            console.log('Language option clicked:', $(this).data('lang'));
            e.preventDefault();
            const lang = $(this).data('lang');
            switchLanguage(lang);
        });
        
        // Test if language options exist
        console.log('Language options found:', $('.language-option').length);
        $('.language-option').each(function() {
            console.log('Language option:', $(this).data('lang'), $(this).text());
        });
        
        // Initialize language system
        console.log('Initializing language system...');
        updateLanguageDisplay(currentLanguage);
        translatePage(currentLanguage);
        
        // Set active language option
        $('.language-option').each(function() {
            const optionLang = $(this).data('lang');
            if (optionLang === currentLanguage) {
                $(this).addClass('active');
            }
        });
        
        console.log('Translation system initialized');
    });
    </script>
    
    {{ scripts | safe if scripts else '' }}
</body>
</html>
"""

# Landing page content
LANDING_CONTENT = """
<div class="container">
    <div class="text-center">
        <h1 class="display-4 mb-4">🚀 <span data-translate="content_creator_pro">Content Creator Pro</span></h1>
        <p class="lead mb-5"><span data-translate="ai_powered_platform">AI-Powered Content Generation Platform</span></p>
        <div class="row">
            <div class="col-md-4">
                <div class="feature-card">
                    <h3><i class="fas fa-share-alt me-2"></i><span data-translate="multi_platform_content">Multi-Platform Content</span></h3>
                    <p><span data-translate="generate_content_for">Generate content for</span> <b><span data-translate="platforms_list">LinkedIn, Facebook, Instagram, Twitter, YouTube, and blogs</span></b>.</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="feature-card">
                    <h3><i class="fas fa-bullseye me-2"></i><span data-translate="smart_direction">Smart Direction</span></h3>
                    <p><span data-translate="content_directions_desc">18 content directions with</span> <b><span data-translate="regional_context">regional and cultural context</span></b>.</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="feature-card">
                    <h3><i class="fas fa-brain me-2"></i><span data-translate="ai_powered">AI-Powered</span></h3>
                    <p><span data-translate="advanced_ai_generation">Advanced AI content generation with</span> <b><span data-translate="tone_customization">tone and style customization</span></b>.</p>
                </div>
            </div>
        </div>
        <div class="mt-5">
            <a href="/generator" class="btn btn-primary btn-lg me-3">
                <i class="fas fa-magic me-2"></i><span data-translate="start_creating">Start Creating</span>
            </a>
            <button class="btn btn-outline-light btn-lg" onclick="showDemo()">
                <i class="fas fa-play me-2"></i><span data-translate="try_demo">Try Demo</span>
            </button>
        </div>
    </div>
</div>
"""

# Generator page content - Updated to match wireframes
GENERATOR_CONTENT = """
<div class="container">
    <div class="row justify-content-center">
        <div class="col-lg-10">
            <div class="text-center mb-5">
                <h1><i class="fas fa-magic me-2"></i><span data-translate="content_generator">Content Generator</span></h1>
                <p class="lead"><span data-translate="create_engaging_content">Create engaging content with AI assistance</span></p>
            </div>
            
            <!-- Step Progress -->
            <div class="step-progress">
                <div class="step active">1</div>
                <div class="step">2</div>
                <div class="step">3</div>
                <div class="step">4</div>
                <div class="step">5</div>
            </div>
            
            <div class="card">
                <div class="card-body p-4">
                    <form id="generatorForm">
                        <!-- Step 1: Content Direction -->
                        <div id="step1" class="step-content">
                            <h3 class="text-center mb-4"><span data-translate="step_1">Step 1</span>: <span data-translate="choose_your_focus">Choose Your Focus</span></h3>
                            <div class="row">
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="business_finance">
                                        <i class="fas fa-briefcase"></i>
                                        <div data-translate="business_finance">Business & Finance</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="technology">
                                        <i class="fas fa-laptop-code"></i>
                                        <div data-translate="technology">Technology</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="health_wellness">
                                        <i class="fas fa-heartbeat"></i>
                                        <div data-translate="health_wellness">Health & Wellness</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="education">
                                        <i class="fas fa-graduation-cap"></i>
                                        <div data-translate="education">Education</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="entertainment">
                                        <i class="fas fa-film"></i>
                                        <div data-translate="entertainment">Entertainment</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="travel_tourism">
                                        <i class="fas fa-plane"></i>
                                        <div data-translate="travel_tourism">Travel & Tourism</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="food_cooking">
                                        <i class="fas fa-utensils"></i>
                                        <div data-translate="food_cooking">Food & Cooking</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="fashion_beauty">
                                        <i class="fas fa-tshirt"></i>
                                        <div data-translate="fashion_beauty">Fashion & Beauty</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="sports_fitness">
                                        <i class="fas fa-dumbbell"></i>
                                        <div data-translate="sports_fitness">Sports & Fitness</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="science_research">
                                        <i class="fas fa-microscope"></i>
                                        <div data-translate="science_research">Science & Research</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="politics_current_events">
                                        <i class="fas fa-newspaper"></i>
                                        <div data-translate="politics_news">Politics & News</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="environment_sustainability">
                                        <i class="fas fa-leaf"></i>
                                        <div data-translate="environment">Environment</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="personal_development">
                                        <i class="fas fa-chart-line"></i>
                                        <div data-translate="personal_dev">Personal Dev</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="parenting_family">
                                        <i class="fas fa-users"></i>
                                        <div data-translate="parenting_family">Parenting & Family</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="art_creativity">
                                        <i class="fas fa-palette"></i>
                                        <div data-translate="art_creativity">Art & Creativity</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="real_estate">
                                        <i class="fas fa-home"></i>
                                        <div data-translate="real_estate">Real Estate</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="automotive">
                                        <i class="fas fa-car"></i>
                                        <div data-translate="automotive">Automotive</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="pet_care">
                                        <i class="fas fa-paw"></i>
                                        <div data-translate="pet_care">Pet Care</div>
                                    </div>
                                </div>
                            </div>
                            <div class="text-center mt-4">
                                <button type="button" class="btn btn-primary btn-lg" onclick="nextStep()" id="step1Next" disabled>
                                    <span data-translate="next_step">Next Step</span> <i class="fas fa-arrow-right ms-2"></i>
                                </button>
                            </div>
                        </div>
                        
                        <!-- Step 2: Content Type -->
                        <div id="step2" class="step-content" style="display: none;">
                            <h3 class="text-center mb-4"><span data-translate="step_2">Step 2</span>: <span data-translate="what_type_content">What Type of Content?</span></h3>
                            <div class="row">
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-platform="linkedin">
                                        <i class="fab fa-linkedin"></i>
                                        <div data-translate="linkedin_post">LinkedIn Post</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-platform="facebook">
                                        <i class="fab fa-facebook"></i>
                                        <div data-translate="facebook_post">Facebook Post</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-platform="instagram">
                                        <i class="fab fa-instagram"></i>
                                        <div data-translate="instagram_post">Instagram Post</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-platform="twitter">
                                        <i class="fab fa-twitter"></i>
                                        <div data-translate="twitter_post">Twitter Post</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-platform="youtube">
                                        <i class="fab fa-youtube"></i>
                                        <div data-translate="youtube_short">YouTube Short</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-platform="blog">
                                        <i class="fas fa-blog"></i>
                                        <div data-translate="blog_article">Blog Article</div>
                                    </div>
                                </div>
                            </div>
                            <div class="text-center mt-4">
                                <button type="button" class="btn btn-secondary btn-lg me-3" onclick="prevStep()">
                                    <i class="fas fa-arrow-left me-2"></i><span data-translate="previous">Previous</span>
                                </button>
                                <button type="button" class="btn btn-primary btn-lg" onclick="nextStep()">
                                    <span data-translate="next_step">Next Step</span> <i class="fas fa-arrow-right ms-2"></i>
                                </button>
                            </div>
                        </div>
                        
                        <!-- Step 3: Inspiration Source -->
                        <div id="step3" class="step-content" style="display: none;">
                            <h3 class="text-center mb-4"><span data-translate="step_3">Step 3</span>: <span data-translate="what_inspires_you">What Inspires You?</span></h3>
                            <div class="row">
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-source="news">
                                        <i class="fas fa-newspaper"></i>
                                        <div data-translate="latest_news">Latest News</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-source="books">
                                        <i class="fas fa-book"></i>
                                        <div data-translate="popular_books">Popular Books</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-source="threads">
                                        <i class="fas fa-comments"></i>
                                        <div data-translate="trending_threads">Trending Threads</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-source="podcasts">
                                        <i class="fas fa-podcast"></i>
                                        <div data-translate="podcasts">Podcasts</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-source="videos">
                                        <i class="fas fa-video"></i>
                                        <div data-translate="youtube_videos">YouTube Videos</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-source="research">
                                        <i class="fas fa-file-alt"></i>
                                        <div data-translate="research_papers">Research Papers</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-source="case_studies">
                                        <i class="fas fa-chart-bar"></i>
                                        <div data-translate="case_studies">Case Studies</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-source="trends">
                                        <i class="fas fa-fire"></i>
                                        <div data-translate="trending_topics">Trending Topics</div>
                                    </div>
                                </div>
                            </div>
                            <div class="text-center mt-4">
                                <button type="button" class="btn btn-secondary btn-lg me-3" onclick="prevStep()">
                                    <i class="fas fa-arrow-left me-2"></i><span data-translate="previous">Previous</span>
                                </button>
                                <button type="button" class="btn btn-primary btn-lg" onclick="nextStep()" id="step3Next" disabled>
                                    <span data-translate="next_step">Next Step</span> <i class="fas fa-arrow-right ms-2"></i>
                                </button>
                            </div>
                        </div>
                        
                        <!-- Step 3.5: Topic Selection -->
                        <div id="step3_5" class="step-content" style="display: none;">
                            <h3 class="text-center mb-4"><span data-translate="step_3_5">Step 3.5</span>: <span data-translate="choose_your_topic">Choose Your Topic</span></h3>
                            
                            <!-- Input fields for specific sources -->
                            <div id="sourceInputs" class="mb-4" style="display: none;">
                                <!-- Books input -->
                                <div id="booksInput" class="source-input" style="display: none;">
                                    <div class="row">
                                        <div class="col-md-6 mb-3">
                                            <label class="form-label" data-translate="book_title">Book Title</label>
                                            <input type="text" class="form-control" id="bookTitle" data-translate-placeholder="enter_book_title" placeholder="Enter book title...">
                                        </div>
                                        <div class="col-md-6 mb-3">
                                            <label class="form-label" data-translate="author">Author</label>
                                            <input type="text" class="form-control" id="bookAuthor" data-translate-placeholder="enter_author_name" placeholder="Enter author name...">
                                        </div>
                                    </div>
                                    <button type="button" class="btn btn-outline-primary" onclick="loadBookTopics()">
                                        <i class="fas fa-search me-2"></i><span data-translate="find_topics">Find Topics</span>
                                    </button>
                                </div>
                                
                                <!-- Podcast input -->
                                <div id="podcastInput" class="source-input" style="display: none;">
                                    <div class="mb-3">
                                        <label class="form-label" data-translate="podcast_link">Podcast Link</label>
                                        <input type="url" class="form-control" id="podcastLink" data-translate-placeholder="enter_podcast_url" placeholder="Enter podcast URL...">
                                    </div>
                                    <button type="button" class="btn btn-outline-primary" onclick="loadPodcastTopics()">
                                        <i class="fas fa-search me-2"></i><span data-translate="find_topics">Find Topics</span>
                                    </button>
                                </div>
                                
                                <!-- Video input -->
                                <div id="videoInput" class="source-input" style="display: none;">
                                    <div class="mb-3">
                                        <label class="form-label" data-translate="youtube_video_link">YouTube Video Link</label>
                                        <input type="url" class="form-control" id="videoLink" data-translate-placeholder="enter_youtube_video_url" placeholder="Enter YouTube video URL...">
                                    </div>
                                    <button type="button" class="btn btn-outline-primary" onclick="loadVideoTopics()">
                                        <i class="fas fa-search me-2"></i><span data-translate="find_topics">Find Topics</span>
                                    </button>
                                </div>
                                
                                <!-- Research paper input -->
                                <div id="researchInput" class="source-input" style="display: none;">
                                    <div class="mb-3">
                                        <label class="form-label" data-translate="research_paper_pdf">Research Paper (PDF)</label>
                                        <input type="file" class="form-control" id="researchFile" accept=".pdf">
                                    </div>
                                    <button type="button" class="btn btn-outline-primary" onclick="loadResearchTopics()">
                                        <i class="fas fa-upload me-2"></i><span data-translate="upload_find_topics">Upload & Find Topics</span>
                                    </button>
                                </div>
                            </div>
                            
                            <!-- Topic choices -->
                            <div id="topicChoices" class="mb-4" style="display: none;">
                                <div class="d-flex justify-content-between align-items-center mb-3">
                                    <h5 id="topicTitle" data-translate="available_topics">Available Topics</h5>
                                    <button type="button" class="btn btn-outline-secondary btn-sm" onclick="refreshTopics()">
                                        <i class="fas fa-sync-alt me-1"></i><span data-translate="refresh">Refresh</span>
                                    </button>
                                </div>
                                <div class="row" id="topicsGrid">
                                    <!-- Topics will be loaded here dynamically -->
                                </div>
                            </div>
                            
                            <div class="text-center mt-4">
                                <button type="button" class="btn btn-secondary btn-lg me-3" onclick="prevStep()">
                                    <i class="fas fa-arrow-left me-2"></i><span data-translate="previous">Previous</span>
                                </button>
                                <button type="button" class="btn btn-primary btn-lg" onclick="nextStep()" id="nextStepBtn" disabled>
                                    <span data-translate="next_step">Next Step</span> <i class="fas fa-arrow-right ms-2"></i>
                                </button>
                            </div>
                        </div>
                        
                        <!-- Step 4: Tone -->
                        <div id="step4" class="step-content" style="display: none;">
                            <h3 class="text-center mb-4"><span data-translate="step_4">Step 4</span>: <span data-translate="how_should_sound">How Should It Sound?</span></h3>
                            <div class="row">
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-tone="professional">
                                        <i class="fas fa-user-tie"></i>
                                        <div data-translate="professional">Professional</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-tone="casual">
                                        <i class="fas fa-smile"></i>
                                        <div data-translate="casual">Casual</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-tone="inspirational">
                                        <i class="fas fa-star"></i>
                                        <div data-translate="inspirational">Inspirational</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-tone="educational">
                                        <i class="fas fa-lightbulb"></i>
                                        <div data-translate="educational">Educational</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-tone="humorous">
                                        <i class="fas fa-laugh"></i>
                                        <div data-translate="humorous">Humorous</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-tone="serious">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <div data-translate="serious">Serious</div>
                                    </div>
                                </div>
                            </div>
                            <div class="text-center mt-4">
                                <button type="button" class="btn btn-secondary btn-lg me-3" onclick="prevStep()">
                                    <i class="fas fa-arrow-left me-2"></i><span data-translate="previous">Previous</span>
                                </button>
                                <button type="submit" class="btn btn-primary btn-lg">
                                    <i class="fas fa-magic me-2"></i><span data-translate="generate_content">Generate Content</span>
                                </button>
                            </div>
                        </div>
                        
                        <!-- Step 5: Review and Generate -->
                        <div id="step5" class="step-content" style="display: none;">
                            <h3 class="text-center mb-4"><span data-translate="step_5">Step 5</span>: <span data-translate="review_and_generate">Review & Generate</span></h3>
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="mb-3"><span data-translate="your_selections">Your Selections</span>:</h5>
                                    <div class="row">
                                        <div class="col-md-6">
                                            <p><strong><span data-translate="direction">Direction</span>:</strong> <span id="reviewDirection"></span></p>
                                            <p><strong><span data-translate="platform">Platform</span>:</strong> <span id="reviewPlatform"></span></p>
                                            <p><strong><span data-translate="source">Source</span>:</strong> <span id="reviewSource"></span></p>
                                        </div>
                                        <div class="col-md-6">
                                            <p><strong><span data-translate="topic">Topic</span>:</strong> <span id="reviewTopic"></span></p>
                                            <p><strong><span data-translate="tone">Tone</span>:</strong> <span id="reviewTone"></span></p>
                                        </div>
                                    </div>
                                    <div class="alert alert-info">
                                        <i class="fas fa-info-circle me-2"></i>
                                        <span data-translate="review_message">Review your selections above. Click Generate to create your content.</span>
                                    </div>
                                </div>
                            </div>
                            <div class="text-center mt-4">
                                <button type="button" class="btn btn-secondary btn-lg me-3" onclick="prevStep()">
                                    <i class="fas fa-arrow-left me-2"></i><span data-translate="previous">Previous</span>
                                </button>
                                <button type="submit" class="btn btn-primary btn-lg">
                                    <i class="fas fa-magic me-2"></i><span data-translate="generate_content">Generate Content</span>
                                </button>
                            </div>
                        </div>
                        
                        <!-- Hidden form fields -->
                        <input type="hidden" id="selectedDirection" name="direction">
                        <input type="hidden" id="selectedPlatform" name="platform">
                        <input type="hidden" id="selectedSource" name="source">
                        <input type="hidden" id="selectedTopic" name="topic">
                        <input type="hidden" id="selectedTone" name="tone">
                        <input type="hidden" id="sourceDetails" name="sourceDetails">
                    </form>
                </div>
            </div>
            
            <div id="result" class="card mt-4" style="display: none;">
                <div class="card-body p-4">
                    <h4><i class="fas fa-file-alt me-2"></i><span data-translate="generated_content">Generated Content</span></h4>
                    <div id="generatedContent" class="mt-3"></div>
                    <div class="mt-3">
                        <button class="btn btn-success me-2" onclick="copyContent()">
                            <i class="fas fa-copy me-1"></i><span data-translate="copy">Copy</span>
                        </button>
                        <button class="btn btn-primary me-2" onclick="saveContent()">
                            <i class="fas fa-save me-1"></i><span data-translate="save_to_library">Save to Library</span>
                        </button>
                        <button class="btn btn-outline-info me-2" id="translateToChinese" onclick="translateToChinese()" style="display: none;">
                            <i class="fas fa-language me-1"></i><span data-translate="translate_to_chinese">Translate to Chinese</span>
                        </button>
                        <button class="btn btn-outline-info me-2" id="translateToEnglish" onclick="translateToEnglish()" style="display: none;">
                            <i class="fas fa-language me-1"></i><span data-translate="translate_to_english">Translate to English</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
let currentStep = 1;
let selectedDirection = '';
let selectedPlatform = '';
let selectedSource = '';
let selectedTopic = '';
let selectedTone = '';
let sourceDetails = {};

// Direction card selection
document.querySelectorAll('[data-direction]').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('[data-direction]').forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
        selectedDirection = this.dataset.direction;
        document.getElementById('selectedDirection').value = selectedDirection;
        
        // Enable next button for step 1
        const step1Next = document.getElementById('step1Next');
        if (step1Next) step1Next.disabled = false;
    });
});

// Platform card selection
document.querySelectorAll('[data-platform]').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('[data-platform]').forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
        selectedPlatform = this.dataset.platform;
        document.getElementById('selectedPlatform').value = selectedPlatform;
        
        // Enable next button for step 2
        const step2Next = document.getElementById('step3Next');
        if (step2Next) step2Next.disabled = false;
    });
});

// Source card selection
document.querySelectorAll('[data-source]').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('[data-source]').forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
        selectedSource = this.dataset.source;
        document.getElementById('selectedSource').value = selectedSource;
        
        // Enable next button for step 3
        const step3Next = document.getElementById('step3Next');
        if (step3Next) step3Next.disabled = false;
    });
});

// Tone card selection
document.querySelectorAll('[data-tone]').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('[data-tone]').forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
        selectedTone = this.dataset.tone;
        document.getElementById('selectedTone').value = selectedTone;
        
        // Enable next button for step 4
        const step4Next = document.querySelector('#step4 button[onclick="nextStep()"]');
        if (step4Next) step4Next.disabled = false;
    });
});

function nextStep() {
    if (currentStep === 3 && selectedSource) {
        // Show topic selection step
        showTopicSelection();
        return;
    }
    
    if (currentStep === 3.5 && selectedTopic) {
        // Move to tone selection
        document.getElementById('step3_5').style.display = 'none';
        document.getElementById('step4').style.display = 'block';
        currentStep = 4;
        updateStepProgress();
        return;
    }
    
    if (currentStep === 4 && selectedTone) {
        // Move to review step
        document.getElementById('step4').style.display = 'none';
        document.getElementById('step5').style.display = 'block';
        currentStep = 5;
        updateStepProgress();
        updateReviewSelections();
        return;
    }
    
    if (currentStep < 4) {
        document.getElementById('step' + currentStep).style.display = 'none';
        currentStep++;
        document.getElementById('step' + currentStep).style.display = 'block';
        updateStepProgress();
    }
}

function prevStep() {
    if (currentStep === 5) {
        // Go back from review to tone selection
        document.getElementById('step5').style.display = 'none';
        document.getElementById('step4').style.display = 'block';
        currentStep = 4;
        updateStepProgress();
        return;
    }
    
    if (currentStep === 4) {
        // Go back from tone to topic selection
        document.getElementById('step4').style.display = 'none';
        document.getElementById('step3_5').style.display = 'block';
        currentStep = 3.5;
        updateStepProgress();
        return;
    }
    
    if (currentStep === 3.5) {
        // Go back from topic selection to source selection
        document.getElementById('step3_5').style.display = 'none';
        document.getElementById('step3').style.display = 'block';
        currentStep = 3;
        updateStepProgress();
        return;
    }
    
    if (currentStep > 1) {
        document.getElementById('step' + currentStep).style.display = 'none';
        currentStep--;
        document.getElementById('step' + currentStep).style.display = 'block';
        updateStepProgress();
    }
}

function showTopicSelection() {
    document.getElementById('step3').style.display = 'none';
    document.getElementById('step3_5').style.display = 'block';
    currentStep = 3.5;
    updateStepProgress();
    
    // Show appropriate input based on source
    showSourceInput();
}

function showSourceInput() {
    // Hide all source inputs
    document.querySelectorAll('.source-input').forEach(input => input.style.display = 'none');
    document.getElementById('sourceInputs').style.display = 'none';
    document.getElementById('topicChoices').style.display = 'none';
    
    // Show appropriate input for the selected source
    switch(selectedSource) {
        case 'books':
            document.getElementById('booksInput').style.display = 'block';
            document.getElementById('sourceInputs').style.display = 'block';
            break;
        case 'podcasts':
            document.getElementById('podcastInput').style.display = 'block';
            document.getElementById('sourceInputs').style.display = 'block';
            break;
        case 'videos':
            document.getElementById('videoInput').style.display = 'block';
            document.getElementById('sourceInputs').style.display = 'block';
            break;
        case 'research':
            document.getElementById('researchInput').style.display = 'block';
            document.getElementById('sourceInputs').style.display = 'block';
            break;
        default:
            // For news, threads, case_studies, trends - load topics directly
            loadTopics();
            break;
    }
}

function loadBookTopics() {
    const bookTitle = document.getElementById('bookTitle').value;
    const bookAuthor = document.getElementById('bookAuthor').value;
    
    if (!bookTitle || !bookAuthor) {
        alert('Please enter both book title and author.');
        return;
    }
    
    sourceDetails = { bookTitle, bookAuthor };
    document.getElementById('sourceDetails').value = JSON.stringify(sourceDetails);
    loadTopics();
}

function loadPodcastTopics() {
    const podcastLink = document.getElementById('podcastLink').value;
    
    if (!podcastLink) {
        alert('Please enter a podcast link.');
        return;
    }
    
    sourceDetails = { podcastLink };
    document.getElementById('sourceDetails').value = JSON.stringify(sourceDetails);
    loadTopics();
}

function loadVideoTopics() {
    const videoLink = document.getElementById('videoLink').value;
    
    if (!videoLink) {
        alert('Please enter a YouTube video link.');
        return;
    }
    
    sourceDetails = { videoLink };
    document.getElementById('sourceDetails').value = JSON.stringify(sourceDetails);
    loadTopics();
}

function loadResearchTopics() {
    const researchFile = document.getElementById('researchFile').files[0];
    
    if (!researchFile) {
        alert('Please select a PDF file.');
        return;
    }
    
    sourceDetails = { fileName: researchFile.name };
    document.getElementById('sourceDetails').value = JSON.stringify(sourceDetails);
    loadTopics();
}

function loadTopics() {
    // Hide source inputs and show topic choices
    document.getElementById('sourceInputs').style.display = 'none';
    document.getElementById('topicChoices').style.display = 'block';
    
    // Generate topics based on direction and source
    const topics = generateTopics(selectedDirection, selectedSource);
    displayTopics(topics);
}

function generateTopics(direction, source) {
    const topicTemplates = {
        'business_finance': {
            'news': [
                'Market Analysis: Latest Trends in Financial Markets',
                'Startup Success: Key Strategies for New Entrepreneurs',
                'Investment Insights: Where to Invest in 2024',
                'Corporate Leadership: Building Effective Teams',
                'Economic Outlook: Global Market Predictions'
            ],
            'books': [
                'Key Business Principles from the Book',
                'Leadership Lessons and Management Insights',
                'Financial Strategies and Investment Tips',
                'Entrepreneurial Mindset and Growth Tactics',
                'Corporate Culture and Team Building'
            ],
            'threads': [
                'Viral Business Tips from Social Media',
                'Entrepreneur Success Stories and Lessons',
                'Investment Strategies Discussed Online',
                'Leadership Insights from Business Leaders',
                'Market Trends and Industry Analysis'
            ],
            'podcasts': [
                'Key Insights from the Podcast Episode',
                'Business Strategies and Best Practices',
                'Leadership Lessons and Management Tips',
                'Industry Trends and Market Analysis',
                'Entrepreneurial Advice and Growth Tactics'
            ],
            'videos': [
                'Main Takeaways from the Video Content',
                'Business Strategies and Implementation Tips',
                'Leadership Insights and Management Lessons',
                'Industry Analysis and Market Trends',
                'Practical Business Advice and Tactics'
            ],
            'research': [
                'Key Findings from the Research Paper',
                'Data-Driven Business Insights and Trends',
                'Statistical Analysis and Market Predictions',
                'Academic Insights Applied to Business',
                'Research-Based Strategic Recommendations'
            ],
            'case_studies': [
                'Success Factors from the Case Study',
                'Strategic Decisions and Their Outcomes',
                'Business Model Analysis and Insights',
                'Lessons Learned and Best Practices',
                'Implementation Strategies and Results'
            ],
            'trends': [
                'Emerging Business Trends and Opportunities',
                'Industry Disruption and Innovation',
                'Market Shifts and Strategic Responses',
                'Technology Impact on Business Models',
                'Future of Work and Leadership'
            ]
        },
        'technology': {
            'news': [
                'Latest Tech Innovations and Breakthroughs',
                'AI and Machine Learning Developments',
                'Cybersecurity Threats and Solutions',
                'Digital Transformation Strategies',
                'Tech Industry Trends and Predictions'
            ],
            'books': [
                'Technology Insights from the Book',
                'Digital Innovation and Future Trends',
                'Tech Leadership and Management',
                'AI and Automation Strategies',
                'Digital Transformation Roadmap'
            ],
            'threads': [
                'Viral Tech Tips and Hacks',
                'Developer Insights and Best Practices',
                'Tech Industry Gossip and Trends',
                'Productivity Tools and Apps',
                'Future Technology Predictions'
            ],
            'podcasts': [
                'Tech Insights from the Podcast',
                'Digital Innovation and Trends',
                'Tech Leadership and Strategy',
                'AI and Automation Discussions',
                'Digital Transformation Insights'
            ],
            'videos': [
                'Tech Tutorials and How-To Guides',
                'Product Reviews and Comparisons',
                'Tech News and Industry Updates',
                'Coding Tips and Best Practices',
                'Future Technology Trends'
            ],
            'research': [
                'Cutting-Edge Research Findings',
                'Technical Innovations and Breakthroughs',
                'AI and ML Algorithm Insights',
                'Digital Technology Trends',
                'Scientific Computing Advances'
            ],
            'case_studies': [
                'Tech Implementation Success Stories',
                'Digital Transformation Case Studies',
                'AI Integration and Results',
                'Cybersecurity Incident Analysis',
                'Technology ROI and Impact'
            ],
            'trends': [
                'Emerging Technology Trends',
                'AI and Automation Developments',
                'Cybersecurity Evolution',
                'Digital Innovation Trends',
                'Future of Technology'
            ]
        }
    };
    
    // Get topics for the selected direction and source, or use default topics
    const directionTopics = topicTemplates[direction] || topicTemplates['business_finance'];
    const sourceTopics = directionTopics[source] || directionTopics['news'];
    
    return sourceTopics;
}

function displayTopics(topics) {
    const topicsGrid = document.getElementById('topicsGrid');
    topicsGrid.innerHTML = '';
    
    topics.forEach((topic, index) => {
        const topicCard = document.createElement('div');
        topicCard.className = 'col-md-6 mb-3';
        topicCard.innerHTML = `
            <div class="direction-card topic-card" data-topic="${index}">
                <i class="fas fa-lightbulb"></i>
                <div>${topic}</div>
            </div>
        `;
        topicsGrid.appendChild(topicCard);
    });
    
    // Add click handlers for topic selection
    document.querySelectorAll('.topic-card').forEach(card => {
        card.addEventListener('click', function() {
            document.querySelectorAll('.topic-card').forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
            selectedTopic = this.dataset.topic;
            document.getElementById('selectedTopic').value = selectedTopic;
            document.getElementById('nextStepBtn').disabled = false;
        });
    });
}

function refreshTopics() {
    loadTopics();
}

function updateStepProgress() {
    document.querySelectorAll('.step').forEach((step, index) => {
        step.classList.remove('active', 'completed');
        
        // Handle step 3.5 (topic selection) - show as step 4
        if (currentStep === 3.5 && index === 3) {
            step.classList.add('active');
        } else if (currentStep === 4 && index === 3) {
            step.classList.add('active');
        } else if (currentStep === 5 && index === 4) {
            step.classList.add('active');
        } else if (currentStep === 5 && index < 4) {
            step.classList.add('completed');
        } else if (currentStep === 4 && index < 3) {
            step.classList.add('completed');
        } else if (currentStep === 3.5 && index < 3) {
            step.classList.add('completed');
        } else if (index + 1 < currentStep) {
            step.classList.add('completed');
        } else if (index + 1 === currentStep) {
            step.classList.add('active');
        }
    });
}

function updateReviewSelections() {
    // Update review display with selected values
    const directionNames = {
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
        'pet_care': 'Pet Care'
    };
    
    const platformNames = {
        'linkedin': 'LinkedIn Post',
        'facebook': 'Facebook Post',
        'instagram': 'Instagram Post',
        'twitter': 'Twitter Post',
        'youtube': 'YouTube Short',
        'blog': 'Blog Article'
    };
    
    const sourceNames = {
        'news': 'Latest News',
        'books': 'Popular Books',
        'threads': 'Trending Threads',
        'podcasts': 'Podcasts',
        'videos': 'YouTube Videos',
        'research': 'Research Papers',
        'case_studies': 'Case Studies',
        'trends': 'Trending Topics'
    };
    
    const toneNames = {
        'professional': 'Professional',
        'casual': 'Casual',
        'inspirational': 'Inspirational',
        'educational': 'Educational',
        'humorous': 'Humorous',
        'serious': 'Serious'
    };
    
    document.getElementById('reviewDirection').textContent = directionNames[selectedDirection] || selectedDirection;
    document.getElementById('reviewPlatform').textContent = platformNames[selectedPlatform] || selectedPlatform;
    document.getElementById('reviewSource').textContent = sourceNames[selectedSource] || selectedSource;
    document.getElementById('reviewTone').textContent = toneNames[selectedTone] || selectedTone;
    
    // Get topic text
    const topics = generateTopics(selectedDirection, selectedSource);
    const topicText = topics[selectedTopic] || selectedTopic;
    document.getElementById('reviewTopic').textContent = topicText;
}

// Form submission
document.getElementById('generatorForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (!selectedDirection || !selectedPlatform || !selectedSource || !selectedTopic || !selectedTone) {
        alert('Please complete all steps before generating content.');
        return;
    }
    
    // Show loading
    document.getElementById('result').style.display = 'block';
    document.getElementById('generatedContent').innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin fa-2x"></i><p>Generating content...</p></div>';
    
    // Simulate content generation (replace with actual API call)
    setTimeout(() => {
        const topics = generateTopics(selectedDirection, selectedSource);
        const selectedTopicText = topics[selectedTopic];
        
        // Generate sample content based on selections
        const sampleContent = generateSampleContent(selectedDirection, selectedPlatform, selectedTopicText, selectedTone);
        
        document.getElementById('generatedContent').innerHTML = `
            <div class="alert alert-success">
                <h5>Generated Content for ${selectedDirection} - ${selectedPlatform}</h5>
                <p><strong>Topic:</strong> ${selectedTopicText}</p>
                <p><strong>Source:</strong> ${selectedSource}</p>
                <p><strong>Tone:</strong> ${selectedTone}</p>
                <div class="mt-3 p-3 bg-light rounded">
                    <h6>Generated Content:</h6>
                    <p>${sampleContent}</p>
                </div>
            </div>
        `;
        
        // Save content to server
        saveGeneratedContent(selectedDirection, selectedPlatform, selectedSource, selectedTopicText, selectedTone, sampleContent);
        
        // Show translation buttons based on current language
        if (currentLanguage === 'zh') {
            document.getElementById('translateToEnglish').style.display = 'inline-block';
        } else {
            document.getElementById('translateToChinese').style.display = 'inline-block';
        }
    }, 2000);
});

function copyContent() {
    // Copy functionality
    alert('Content copied to clipboard!');
}

function saveContent() {
    // Save functionality
    alert('Content saved to library!');
}

function generateSampleContent(direction, platform, topic, tone) {
    // Generate sample content based on direction, platform, topic, and tone
    const contentTemplates = {
        'business_finance': {
            'linkedin': '🚀 Exciting developments in the business world! Based on recent insights, we\'re seeing remarkable growth in key sectors. This represents a significant opportunity for forward-thinking professionals. What are your thoughts on these emerging trends? #BusinessGrowth #Innovation #ProfessionalDevelopment',
            'twitter': '📈 Key insight: Success isn\'t about having all the answers, it\'s about asking the right questions. What\'s the best business advice you\'ve ever received? #BusinessTips #Leadership #Growth',
            'instagram': '💼 Business tip of the day! Just learned this amazing strategy that\'s completely changed how I approach challenges. Game changer for anyone in business! What\'s your favorite business hack? #BusinessTips #Success #Entrepreneur',
            'facebook': 'Hey everyone! 👋 Just wanted to share some amazing insights I\'ve discovered. The way things are evolving in our industry is truly fascinating. What do you think about these changes? Drop a comment below!',
            'youtube': 'In today\'s video, we\'re diving deep into the latest business trends and what they mean for entrepreneurs. This is crucial information that could change your entire approach to business.',
            'blog': 'The landscape of modern business is evolving at an unprecedented pace. Recent developments in market dynamics reveal fascinating insights into what drives success in today\'s competitive environment.'
        },
        'technology': {
            'linkedin': '💻 Fascinating developments in the tech world! The pace of innovation is truly remarkable. These advancements are reshaping how we work and live. What technology trends are you most excited about? #TechInnovation #DigitalTransformation #FutureOfWork',
            'twitter': '🔥 Tech tip: Just discovered this amazing productivity hack that\'s saving me hours every week. What\'s your favorite tech shortcut? #TechTips #Productivity #Innovation',
            'instagram': '⚡ Tech tip of the day! This new tool I found is absolutely incredible. Perfect for anyone working remotely or managing multiple projects. What\'s your go-to tech solution? #TechTips #RemoteWork #Productivity',
            'facebook': 'Tech enthusiasts! 🤖 Just learned about some incredible new developments that are going to change everything. The future is here, and it\'s amazing! What tech are you most excited about?',
            'youtube': 'Today we\'re exploring the cutting-edge technologies that are transforming industries worldwide. This is essential viewing for anyone interested in the future of technology.',
            'blog': 'The rapid evolution of technology continues to reshape our world in profound ways. Understanding these changes is crucial for anyone looking to stay ahead in the digital age.'
        }
    };
    
    // Get template for direction and platform, or use default
    const directionTemplates = contentTemplates[direction] || contentTemplates['business_finance'];
    const content = directionTemplates[platform] || directionTemplates['linkedin'];
    
    // Adjust tone if needed
    if (tone === 'casual') {
        return content.replace(/🚀|💻|🔥|⚡/g, '😊').replace(/Fascinating|Exciting|Remarkable/g, 'Pretty cool');
    } else if (tone === 'professional') {
        return content.replace(/😊|🔥|⚡/g, '📊').replace(/Pretty cool/g, 'Significant');
    }
    
    return content;
}

function saveGeneratedContent(direction, platform, source, topic, tone, content) {
    // Send content to server to save
    fetch('/api/save-content', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            direction: direction,
            platform: platform,
            source: source,
            topic: topic,
            tone: tone,
            content: content
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Content saved successfully:', data.content_id);
        } else {
            console.error('Failed to save content:', data.error);
        }
    })
    .catch(error => {
        console.error('Error saving content:', error);
    });
}

// Content translation functions
function translateToEnglish() {
    const contentElement = document.getElementById('generatedContent');
    if (contentElement) {
        const chineseContent = contentElement.innerHTML;
        // Call translation API
        $.ajax({
            url: '/api/translate',
            method: 'POST',
            data: {
                content: chineseContent,
                target_language: 'en'
            },
            success: function(response) {
                contentElement.innerHTML = response.translated_content;
                document.getElementById('translateToEnglish').style.display = 'none';
                document.getElementById('translateToChinese').style.display = 'inline-block';
            },
            error: function() {
                alert('Translation failed. Please try again.');
            }
        });
    }
}

function translateToChinese() {
    const contentElement = document.getElementById('generatedContent');
    if (contentElement) {
        const englishContent = contentElement.innerHTML;
        // Call translation API
        $.ajax({
            url: '/api/translate',
            method: 'POST',
            data: {
                content: englishContent,
                target_language: 'zh'
            },
            success: function(response) {
                contentElement.innerHTML = response.translated_content;
                document.getElementById('translateToEnglish').style.display = 'inline-block';
                document.getElementById('translateToChinese').style.display = 'none';
            },
            error: function() {
                alert('Translation failed. Please try again.');
            }
        });
    }
}
</script>
"""

# Dashboard page content
DASHBOARD_CONTENT = """
<div class="container">
    <!-- Welcome Section -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card bg-primary text-white">
                <div class="card-body">
                    <h2 class="mb-2"><span data-translate="welcome_back">Welcome back</span>, <span class="user-name">User</span>!</h2>
                    <p class="mb-0"><span data-translate="your_focus">Your focus</span>: <strong data-translate="business_finance">Business & Finance</strong></p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Quick Stats -->
    <div class="row mb-4">
        <div class="col-12">
            <h4 class="mb-3"><i class="fas fa-chart-bar me-2"></i><span data-translate="quick_stats">Quick Stats</span></h4>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card text-center">
                <div class="card-body">
                    <i class="fas fa-file-alt fa-2x text-primary mb-2"></i>
                    <h3 class="mb-1">45</h3>
                    <p class="text-muted mb-0" data-translate="content_generated">Content Generated</p>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card text-center">
                <div class="card-body">
                    <i class="fas fa-calendar fa-2x text-success mb-2"></i>
                    <h3 class="mb-1">12</h3>
                    <p class="text-muted mb-0" data-translate="this_month">This Month</p>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card text-center">
                <div class="card-body">
                    <i class="fas fa-folder fa-2x text-warning mb-2"></i>
                    <h3 class="mb-1">23</h3>
                    <p class="text-muted mb-0" data-translate="library_items">Library Items</p>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card text-center">
                <div class="card-body">
                    <i class="fas fa-share-alt fa-2x text-info mb-2"></i>
                    <h3 class="mb-1">18</h3>
                    <p class="text-muted mb-0" data-translate="social_posts">Social Posts</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Quick Actions -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-bolt me-2"></i><span data-translate="quick_actions">Quick Actions</span></h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-2 col-6 mb-2">
                            <a href="/generator" class="btn btn-primary w-100">
                                <i class="fas fa-plus-circle me-1"></i><span data-translate="generate_new_content">Generate New Content</span>
                            </a>
                        </div>
                        <div class="col-md-2 col-6 mb-2">
                            <a href="/library" class="btn btn-outline-primary w-100">
                                <i class="fas fa-folder me-1"></i><span data-translate="view_library">View Library</span>
                            </a>
                        </div>
                        <div class="col-md-2 col-6 mb-2">
                            <a href="#" class="btn btn-outline-success w-100">
                                <i class="fas fa-share-alt me-1"></i><span data-translate="social_media">Social Media</span>
                            </a>
                        </div>
                        <div class="col-md-2 col-6 mb-2">
                            <a href="/settings" class="btn btn-outline-secondary w-100">
                                <i class="fas fa-cog me-1"></i><span data-translate="settings">Settings</span>
                            </a>
                        </div>
                        <div class="col-md-2 col-6 mb-2">
                            <a href="#" class="btn btn-outline-info w-100">
                                <i class="fas fa-chart-line me-1"></i><span data-translate="analytics">Analytics</span>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Recent Content by Direction -->
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-clock me-2"></i><span data-translate="recent_content_by_direction">Recent Content by Direction</span></h5>
                </div>
                <div class="card-body">
                    <div class="d-flex align-items-center mb-3">
                        <i class="fas fa-briefcase text-primary me-3"></i>
                        <div class="flex-grow-1">
                            <strong><span data-translate="business">Business</span>: <span data-translate="linkedin_post">LinkedIn Post</span></strong>
                            <br><small class="text-muted" data-translate="2_hours_ago">2 hours ago</small>
                        </div>
                        <span class="badge bg-primary" data-translate="linkedin">LinkedIn</span>
                    </div>
                    <div class="d-flex align-items-center mb-3">
                        <i class="fas fa-briefcase text-primary me-3"></i>
                        <div class="flex-grow-1">
                            <strong><span data-translate="business">Business</span>: <span data-translate="twitter_thread">Twitter Thread</span></strong>
                            <br><small class="text-muted" data-translate="1_day_ago">1 day ago</small>
                        </div>
                        <span class="badge bg-info" data-translate="twitter">Twitter</span>
                    </div>
                    <div class="d-flex align-items-center mb-3">
                        <i class="fas fa-microchip text-success me-3"></i>
                        <div class="flex-grow-1">
                            <strong><span data-translate="tech">Tech</span>: <span data-translate="instagram_post">Instagram Post</span></strong>
                            <br><small class="text-muted" data-translate="3_days_ago">3 days ago</small>
                        </div>
                        <span class="badge bg-success" data-translate="instagram">Instagram</span>
                    </div>
                    <div class="d-flex align-items-center">
                        <i class="fas fa-briefcase text-primary me-3"></i>
                        <div class="flex-grow-1">
                            <strong><span data-translate="business">Business</span>: <span data-translate="blog_article">Blog Article</span></strong>
                            <br><small class="text-muted" data-translate="1_week_ago">1 week ago</small>
                        </div>
                        <span class="badge bg-warning" data-translate="blog">Blog</span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Social Media Performance -->
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-chart-pie me-2"></i><span data-translate="social_media_performance">Social Media Performance</span></h5>
                </div>
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <i class="fab fa-linkedin text-primary me-2"></i>
                            <strong data-translate="linkedin">LinkedIn</strong>
                        </div>
                        <div class="text-end">
                            <div><span data-translate="156_views_23_likes">156 views, 23 likes</span></div>
                            <small class="text-muted"><span data-translate="45_posts">45 posts</span></small>
                        </div>
                    </div>
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <i class="fab fa-twitter text-info me-2"></i>
                            <strong data-translate="twitter">Twitter</strong>
                        </div>
                        <div class="text-end">
                            <div><span data-translate="89_retweets_45_likes">89 retweets, 45 likes</span></div>
                            <small class="text-muted"><span data-translate="23_posts">23 posts</span></small>
                        </div>
                    </div>
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <i class="fab fa-instagram text-danger me-2"></i>
                            <strong data-translate="instagram">Instagram</strong>
                        </div>
                        <div class="text-end">
                            <div><span data-translate="234_views_67_likes">234 views, 67 likes</span></div>
                            <small class="text-muted"><span data-translate="34_posts">34 posts</span></small>
                        </div>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <i class="fab fa-facebook text-primary me-2"></i>
                            <strong data-translate="facebook">Facebook</strong>
                        </div>
                        <div class="text-end">
                            <div><span data-translate="567_views_89_likes">567 views, 89 likes</span></div>
                            <small class="text-muted"><span data-translate="12_posts">12 posts</span></small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Content Performance by Direction -->
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-chart-bar me-2"></i><span data-translate="content_performance_by_direction">Content Performance by Direction</span></h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-3 mb-3">
                            <div class="d-flex align-items-center">
                                <i class="fas fa-briefcase text-primary me-2"></i>
                                <div class="flex-grow-1">
                                    <strong data-translate="business">Business</strong>
                                    <br><small class="text-muted"><span data-translate="23_posts_1234_total_views">23 posts, 1,234 total views</span></small>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="d-flex align-items-center">
                                <i class="fas fa-microchip text-success me-2"></i>
                                <div class="flex-grow-1">
                                    <strong data-translate="technology">Technology</strong>
                                    <br><small class="text-muted"><span data-translate="12_posts_567_total_views">12 posts, 567 total views</span></small>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="d-flex align-items-center">
                                <i class="fas fa-heart text-danger me-2"></i>
                                <div class="flex-grow-1">
                                    <strong data-translate="health">Health</strong>
                                    <br><small class="text-muted"><span data-translate="8_posts_345_total_views">8 posts, 345 total views</span></small>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="d-flex align-items-center">
                                <i class="fas fa-graduation-cap text-warning me-2"></i>
                                <div class="flex-grow-1">
                                    <strong data-translate="education">Education</strong>
                                    <br><small class="text-muted"><span data-translate="5_posts_234_total_views">5 posts, 234 total views</span></small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
"""

# Library page content
LIBRARY_CONTENT = """
<div class="container">
    <div class="row">
        <div class="col-12">
            <h1 class="h2 mb-4">
                <i class="fas fa-folder me-2 text-primary"></i><span data-translate="content_library">Content Library</span>
            </h1>
        </div>
    </div>
    
    <!-- Direction Filters -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-filter me-2"></i><span data-translate="direction_filters">Direction Filters</span></h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-primary w-100 direction-filter active" data-direction="all">
                                <i class="fas fa-th me-1"></i><span data-translate="all">All</span>
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-primary w-100 direction-filter" data-direction="business">
                                <i class="fas fa-briefcase me-1"></i><span data-translate="business">Business</span>
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-success w-100 direction-filter" data-direction="technology">
                                <i class="fas fa-microchip me-1"></i><span data-translate="tech">Tech</span>
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-danger w-100 direction-filter" data-direction="health">
                                <i class="fas fa-heart me-1"></i><span data-translate="health">Health</span>
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-warning w-100 direction-filter" data-direction="education">
                                <i class="fas fa-graduation-cap me-1"></i><span data-translate="education">Education</span>
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-info w-100 direction-filter" data-direction="entertainment">
                                <i class="fas fa-film me-1"></i><span data-translate="entertainment">Entertainment</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Platform Filters -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-share-alt me-2"></i><span data-translate="platform_filters">Platform Filters</span></h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-secondary w-100 platform-filter active" data-platform="all">
                                <i class="fas fa-th me-1"></i><span data-translate="all">All</span>
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-primary w-100 platform-filter" data-platform="linkedin">
                                <i class="fab fa-linkedin me-1"></i><span data-translate="linkedin">LinkedIn</span>
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-primary w-100 platform-filter" data-platform="facebook">
                                <i class="fab fa-facebook me-1"></i><span data-translate="facebook">Facebook</span>
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-danger w-100 platform-filter" data-platform="instagram">
                                <i class="fab fa-instagram me-1"></i><span data-translate="instagram">Instagram</span>
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-info w-100 platform-filter" data-platform="twitter">
                                <i class="fab fa-twitter me-1"></i><span data-translate="twitter">Twitter</span>
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-warning w-100 platform-filter" data-platform="blog">
                                <i class="fas fa-blog me-1"></i><span data-translate="blog">Blog</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Search and Actions -->
    <div class="row mb-4">
        <div class="col-md-8">
            <div class="input-group">
                <input type="text" class="form-control" data-translate-placeholder="search_content" placeholder="Search content..." id="searchInput">
                <button class="btn btn-outline-secondary" type="button">
                    <i class="fas fa-search"></i>
                </button>
            </div>
        </div>
        <div class="col-md-4 text-end">
            <button class="btn btn-outline-secondary me-2">
                <i class="fas fa-filter me-1"></i><span data-translate="advanced_search">Advanced Search</span>
            </button>
            <a href="/generator" class="btn btn-primary">
                <i class="fas fa-plus me-1"></i><span data-translate="create_new">Create New</span>
            </a>
        </div>
    </div>
    
    <!-- Content Grid -->
    <div class="row" id="contentGrid">
        <!-- Business LinkedIn Post -->
        <div class="col-md-4 mb-4 content-item" data-direction="business" data-platform="linkedin">
            <div class="card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="badge bg-primary" data-translate="linkedin">LinkedIn</span>
                        <small class="text-muted" data-translate="2_days_ago">2 days ago</small>
                    </div>
                    <div class="d-flex align-items-center mb-2">
                        <i class="fas fa-briefcase text-primary me-2"></i>
                        <h6 class="mb-0" data-translate="business_strategy_insights">Business Strategy Insights</h6>
                    </div>
                    <p class="text-muted small" data-translate="business_strategy_description">Key insights for modern business leaders looking to scale their operations and drive sustainable growth in today's competitive market...</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted" data-translate="business_finance">Business & Finance</small>
                        <div>
                            <button class="btn btn-sm btn-outline-primary me-1">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-success">
                                <i class="fas fa-share"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Business Facebook Post -->
        <div class="col-md-4 mb-4 content-item" data-direction="business" data-platform="facebook">
            <div class="card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="badge bg-primary" data-translate="facebook">Facebook</span>
                        <small class="text-muted" data-translate="1_week_ago">1 week ago</small>
                    </div>
                    <div class="d-flex align-items-center mb-2">
                        <i class="fas fa-briefcase text-primary me-2"></i>
                        <h6 class="mb-0" data-translate="market_analysis_report">Market Analysis Report</h6>
                    </div>
                    <p class="text-muted small" data-translate="market_analysis_description">Comprehensive analysis of current market trends and their implications for business strategy and investment decisions...</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted" data-translate="business_finance">Business & Finance</small>
                        <div>
                            <button class="btn btn-sm btn-outline-primary me-1">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-success">
                                <i class="fas fa-share"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Tech Instagram Post -->
        <div class="col-md-4 mb-4 content-item" data-direction="technology" data-platform="instagram">
            <div class="card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="badge bg-success" data-translate="instagram">Instagram</span>
                        <small class="text-muted" data-translate="3_days_ago">3 days ago</small>
                    </div>
                    <div class="d-flex align-items-center mb-2">
                        <i class="fas fa-microchip text-success me-2"></i>
                        <h6 class="mb-0" data-translate="ai_innovation_trends">AI Innovation Trends</h6>
                    </div>
                    <p class="text-muted small" data-translate="ai_innovation_description">Exploring the latest developments in artificial intelligence and their transformative impact on various industries...</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted" data-translate="technology">Technology</small>
                        <div>
                            <button class="btn btn-sm btn-outline-primary me-1">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-success">
                                <i class="fas fa-share"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Tech Twitter Post -->
        <div class="col-md-4 mb-4 content-item" data-direction="technology" data-platform="twitter">
            <div class="card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="badge bg-info" data-translate="twitter">Twitter</span>
                        <small class="text-muted" data-translate="5_days_ago">5 days ago</small>
                    </div>
                    <div class="d-flex align-items-center mb-2">
                        <i class="fas fa-microchip text-success me-2"></i>
                        <h6 class="mb-0" data-translate="tech_tips_thread">Tech Tips Thread</h6>
                    </div>
                    <p class="text-muted small" data-translate="tech_tips_description">Essential productivity tips and tools for developers and tech professionals to streamline their workflow...</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted" data-translate="technology">Technology</small>
                        <div>
                            <button class="btn btn-sm btn-outline-primary me-1">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-success">
                                <i class="fas fa-share"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Health Blog Article -->
        <div class="col-md-4 mb-4 content-item" data-direction="health" data-platform="blog">
            <div class="card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="badge bg-warning" data-translate="blog">Blog</span>
                        <small class="text-muted" data-translate="2_weeks_ago">2 weeks ago</small>
                    </div>
                    <div class="d-flex align-items-center mb-2">
                        <i class="fas fa-heart text-danger me-2"></i>
                        <h6 class="mb-0" data-translate="wellness_guide">Wellness Guide</h6>
                    </div>
                    <p class="text-muted small" data-translate="wellness_guide_description">Comprehensive guide to maintaining mental and physical health in the modern digital age with practical tips...</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted" data-translate="health_wellness">Health & Wellness</small>
                        <div>
                            <button class="btn btn-sm btn-outline-primary me-1">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-success">
                                <i class="fas fa-share"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Education LinkedIn Post -->
        <div class="col-md-4 mb-4 content-item" data-direction="education" data-platform="linkedin">
            <div class="card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="badge bg-primary" data-translate="linkedin">LinkedIn</span>
                        <small class="text-muted" data-translate="1_month_ago">1 month ago</small>
                    </div>
                    <div class="d-flex align-items-center mb-2">
                        <i class="fas fa-graduation-cap text-warning me-2"></i>
                        <h6 class="mb-0" data-translate="learning_strategies">Learning Strategies</h6>
                    </div>
                    <p class="text-muted small" data-translate="learning_strategies_description">Effective learning strategies and techniques for professionals looking to upskill and stay competitive...</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted" data-translate="education">Education</small>
                        <div>
                            <button class="btn btn-sm btn-outline-primary me-1">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-success">
                                <i class="fas fa-share"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
"""

# Settings page content
SETTINGS_CONTENT = """
<div class="container">
    <div class="row">
        <div class="col-12">
            <h1 class="h2 mb-4">
                <i class="fas fa-cog me-2 text-primary"></i><span data-translate="settings">Settings</span>
            </h1>
        </div>
    </div>
    
    <div class="row">
        <div class="col-lg-8">
            <!-- Profile Settings -->
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-user me-2"></i><span data-translate="profile">Profile</span></h5>
                </div>
                <div class="card-body">
                    <form id="profileForm">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label" data-translate="name">Name</label>
                                <input type="text" class="form-control" value="Demo User" id="userName">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label" data-translate="email">Email</label>
                                <input type="email" class="form-control" value="demo@contentcreator.com" readonly>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label" data-translate="company">Company</label>
                                <input type="text" class="form-control" value="Content Creator Pro" id="userCompany">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label" data-translate="industry">Industry</label>
                                <select class="form-select" id="userIndustry">
                                    <option value="technology" data-translate="technology">Technology</option>
                                    <option value="finance" data-translate="finance">Finance</option>
                                    <option value="healthcare" data-translate="healthcare">Healthcare</option>
                                    <option value="education" data-translate="education">Education</option>
                                    <option value="marketing" data-translate="marketing">Marketing</option>
                                    <option value="consulting" data-translate="consulting">Consulting</option>
                                    <option value="other" data-translate="other">Other</option>
                                </select>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label" data-translate="region">Region</label>
                                <select class="form-select" id="userRegion">
                                    <option value="global" data-translate="global">Global</option>
                                    <option value="us" data-translate="united_states">United States</option>
                                    <option value="eu" data-translate="europe">Europe</option>
                                    <option value="asia" data-translate="asia">Asia</option>
                                    <option value="latin_america" data-translate="latin_america">Latin America</option>
                                    <option value="africa" data-translate="africa">Africa</option>
                                    <option value="oceania" data-translate="oceania">Oceania</option>
                                </select>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label" data-translate="language">Language</label>
                                <select class="form-select" id="userLanguage">
                                    <option value="en" data-translate="english">English</option>
                                    <option value="zh" data-translate="chinese">中文</option>
                                    <option value="es" data-translate="spanish">Spanish</option>
                                    <option value="fr" data-translate="french">French</option>
                                    <option value="de" data-translate="german">German</option>
                                    <option value="ja" data-translate="japanese">Japanese</option>
                                    <option value="ko" data-translate="korean">Korean</option>
                                </select>
                            </div>
                        </div>
                        <div class="text-end">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save me-2"></i><span data-translate="save_profile">Save Profile</span>
                            </button>
                        </div>
                    </form>
                </div>
            </div>
            
            <!-- Content Preferences -->
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-magic me-2"></i><span data-translate="content_preferences">Content Preferences</span></h5>
                </div>
                <div class="card-body">
                    <form id="contentForm">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label" data-translate="primary_direction">Primary Direction</label>
                                <select class="form-select" id="primaryDirection">
                                    <option value="business_finance" data-translate="business_finance">Business & Finance</option>
                                    <option value="technology" data-translate="technology">Technology</option>
                                    <option value="health_wellness" data-translate="health_wellness">Health & Wellness</option>
                                    <option value="education" data-translate="education">Education</option>
                                    <option value="entertainment" data-translate="entertainment">Entertainment</option>
                                    <option value="travel_tourism" data-translate="travel_tourism">Travel & Tourism</option>
                                    <option value="food_cooking" data-translate="food_cooking">Food & Cooking</option>
                                    <option value="fashion_beauty" data-translate="fashion_beauty">Fashion & Beauty</option>
                                </select>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label" data-translate="default_tone">Default Tone</label>
                                <select class="form-select" id="defaultTone">
                                    <option value="professional" data-translate="professional">Professional</option>
                                    <option value="casual" data-translate="casual">Casual</option>
                                    <option value="inspirational" data-translate="inspirational">Inspirational</option>
                                    <option value="educational" data-translate="educational">Educational</option>
                                    <option value="humorous" data-translate="humorous">Humorous</option>
                                    <option value="serious" data-translate="serious">Serious</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label" data-translate="secondary_directions">Secondary Directions</label>
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="technology" id="secTech" checked>
                                        <label class="form-check-label" for="secTech" data-translate="technology">Technology</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="health_wellness" id="secHealth">
                                        <label class="form-check-label" for="secHealth" data-translate="health_wellness">Health & Wellness</label>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="education" id="secEducation">
                                        <label class="form-check-label" for="secEducation" data-translate="education">Education</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="entertainment" id="secEntertainment">
                                        <label class="form-check-label" for="secEntertainment" data-translate="entertainment">Entertainment</label>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="travel_tourism" id="secTravel">
                                        <label class="form-check-label" for="secTravel" data-translate="travel_tourism">Travel & Tourism</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="food_cooking" id="secFood">
                                        <label class="form-check-label" for="secFood" data-translate="food_cooking">Food & Cooking</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label" data-translate="preferred_content_types">Preferred Content Types</label>
                            <div class="row">
                                <div class="col-md-3">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="linkedin" id="prefLinkedIn" checked>
                                        <label class="form-check-label" for="prefLinkedIn" data-translate="linkedin">LinkedIn</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="twitter" id="prefTwitter" checked>
                                        <label class="form-check-label" for="prefTwitter" data-translate="twitter">Twitter</label>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="facebook" id="prefFacebook">
                                        <label class="form-check-label" for="prefFacebook" data-translate="facebook">Facebook</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="instagram" id="prefInstagram">
                                        <label class="form-check-label" for="prefInstagram" data-translate="instagram">Instagram</label>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="youtube" id="prefYouTube">
                                        <label class="form-check-label" for="prefYouTube" data-translate="youtube">YouTube</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="blog" id="prefBlog">
                                        <label class="form-check-label" for="prefBlog" data-translate="blog">Blog</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label" data-translate="favorite_sources">Favorite Sources</label>
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="news" id="sourceNews" checked>
                                        <label class="form-check-label" for="sourceNews" data-translate="news">News</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="books" id="sourceBooks" checked>
                                        <label class="form-check-label" for="sourceBooks" data-translate="books">Books</label>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="research" id="sourceResearch">
                                        <label class="form-check-label" for="sourceResearch" data-translate="research">Research</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="podcasts" id="sourcePodcasts">
                                        <label class="form-check-label" for="sourcePodcasts" data-translate="podcasts">Podcasts</label>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="videos" id="sourceVideos">
                                        <label class="form-check-label" for="sourceVideos" data-translate="videos">Videos</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="threads" id="sourceThreads">
                                        <label class="form-check-label" for="sourceThreads" data-translate="threads">Threads</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="text-end">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save me-2"></i><span data-translate="save_preferences">Save Preferences</span>
                            </button>
                        </div>
                    </form>
                </div>
            </div>
            
            <!-- Social Media Integration -->
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-share-alt me-2"></i><span data-translate="social_media_integration">Social Media Integration</span></h5>
                </div>
                <div class="card-body">
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <div class="d-flex align-items-center mb-2">
                                <i class="fab fa-linkedin text-primary me-2"></i>
                                <span class="me-2" data-translate="linkedin">LinkedIn</span>
                                <span class="badge bg-success" data-translate="connected">Connected</span>
                            </div>
                            <small class="text-muted">John Doe (Personal)</small>
                        </div>
                        <div class="col-md-6 text-end">
                            <button class="btn btn-sm btn-outline-primary" data-translate="manage">Manage</button>
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <div class="d-flex align-items-center mb-2">
                                <i class="fab fa-facebook text-primary me-2"></i>
                                <span class="me-2" data-translate="facebook">Facebook</span>
                                <span class="badge bg-success" data-translate="connected">Connected</span>
                            </div>
                            <small class="text-muted">John Doe</small>
                        </div>
                        <div class="col-md-6 text-end">
                            <button class="btn btn-sm btn-outline-primary" data-translate="manage">Manage</button>
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <div class="d-flex align-items-center mb-2">
                                <i class="fab fa-instagram text-danger me-2"></i>
                                <span class="me-2" data-translate="instagram">Instagram</span>
                                <span class="badge bg-success" data-translate="connected">Connected</span>
                            </div>
                            <small class="text-muted">@johndoe</small>
                        </div>
                        <div class="col-md-6 text-end">
                            <button class="btn btn-sm btn-outline-primary" data-translate="manage">Manage</button>
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <div class="d-flex align-items-center mb-2">
                                <i class="fab fa-twitter text-info me-2"></i>
                                <span class="me-2" data-translate="twitter">Twitter</span>
                                <span class="badge bg-secondary" data-translate="not_connected">Not connected</span>
                            </div>
                            <small class="text-muted" data-translate="connect_twitter_account">Connect your Twitter account</small>
                        </div>
                        <div class="col-md-6 text-end">
                            <button class="btn btn-sm btn-primary" data-translate="connect">Connect</button>
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <div class="d-flex align-items-center mb-2">
                                <i class="fab fa-youtube text-danger me-2"></i>
                                <span class="me-2" data-translate="youtube">YouTube</span>
                                <span class="badge bg-secondary" data-translate="not_connected">Not connected</span>
                            </div>
                            <small class="text-muted" data-translate="connect_youtube_channel">Connect your YouTube channel</small>
                        </div>
                        <div class="col-md-6 text-end">
                            <button class="btn btn-sm btn-primary" data-translate="connect">Connect</button>
                        </div>
                    </div>
                    
                    <hr>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <label class="form-label" data-translate="auto_post_to">Auto-post to</label>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="linkedin" id="autoLinkedIn" checked>
                                <label class="form-check-label" for="autoLinkedIn" data-translate="linkedin">LinkedIn</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="facebook" id="autoFacebook">
                                <label class="form-check-label" for="autoFacebook" data-translate="facebook">Facebook</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="instagram" id="autoInstagram">
                                <label class="form-check-label" for="autoInstagram" data-translate="instagram">Instagram</label>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label" data-translate="default_posting_time">Default posting time</label>
                            <input type="time" class="form-control" value="09:00" id="defaultPostTime">
                            <small class="text-muted" data-translate="local_timezone">Local timezone</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Subscription Sidebar -->
        <div class="col-lg-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-crown me-2"></i><span data-translate="subscription">Subscription</span></h5>
                </div>
                <div class="card-body">
                    <div class="text-center mb-3">
                        <i class="fas fa-crown fa-3x text-warning mb-2"></i>
                        <h5 data-translate="pro_plan">Pro Plan</h5>
                        <h3 class="text-primary">$19/month</h3>
                    </div>
                    
                    <div class="mb-3">
                        <div class="d-flex justify-content-between mb-2">
                            <span data-translate="content_generated">Content Generated</span>
                            <span>67/100</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar" style="width: 67%"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-2">
                            <span data-translate="social_media_posts">Social Media Posts</span>
                            <span>23/50</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar" style="width: 46%"></div>
                        </div>
                    </div>
                    
                    <div class="d-grid gap-2">
                        <button class="btn btn-warning">
                            <i class="fas fa-arrow-up me-2"></i><span data-translate="upgrade_plan">Upgrade Plan</span>
                        </button>
                        <button class="btn btn-outline-danger">
                            <i class="fas fa-times me-2"></i><span data-translate="cancel_subscription">Cancel Subscription</span>
                        </button>
                    </div>
                    
                    <hr>
                    
                    <h6 data-translate="pro_features">Pro Features</h6>
                    <ul class="list-unstyled">
                        <li><i class="fas fa-check text-success me-2"></i><span data-translate="unlimited_content_generation">Unlimited content generation</span></li>
                        <li><i class="fas fa-check text-success me-2"></i><span data-translate="advanced_ai_models">Advanced AI models</span></li>
                        <li><i class="fas fa-check text-success me-2"></i><span data-translate="social_media_scheduling">Social media scheduling</span></li>
                        <li><i class="fas fa-check text-success me-2"></i><span data-translate="analytics_dashboard">Analytics dashboard</span></li>
                        <li><i class="fas fa-check text-success me-2"></i><span data-translate="priority_support">Priority support</span></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
"""

# JavaScript for generator functionality
GENERATOR_SCRIPTS = """
<script>
document.getElementById('generatorForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const direction = document.getElementById('direction').value;
    const platform = document.getElementById('platform').value;
    const tone = document.getElementById('tone').value;
    const length = document.getElementById('length').value;
    const topic = document.getElementById('topic').value;
    
    if (!direction || !platform) {
        alert('Please select both direction and platform');
        return;
    }
    
    // Show loading state
    const submitBtn = document.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating...';
    submitBtn.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
        const sampleContent = generateSampleContent(direction, platform, tone, length, topic);
        
        document.getElementById('generatedContent').innerHTML = sampleContent;
        document.getElementById('result').style.display = 'block';
        
        // Reset button
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
        
        // Scroll to result
        document.getElementById('result').scrollIntoView({ behavior: 'smooth' });
    }, 2000);
});

function generateSampleContent(direction, platform, tone, length, topic) {
    const contents = {
        'business_finance': {
            'linkedin': '🚀 <strong>Business Strategy Insight:</strong><br><br>In today\\'s rapidly evolving market, successful businesses are those that adapt quickly to change while maintaining their core values. The key is not just to react to market shifts, but to anticipate them.<br><br>💡 <strong>Key Takeaway:</strong> Focus on building resilient systems that can weather economic storms while positioning your company for growth opportunities.<br><br>#BusinessStrategy #Leadership #Innovation #Growth',
            'instagram': '💼 <strong>Business Tip of the Day:</strong><br><br>Success isn\\'t about having all the answers—it\\'s about asking the right questions. What problem are you solving? Who are you serving? How can you deliver more value?<br><br>✨ The best businesses focus on creating solutions that make people\\'s lives better.<br><br>#BusinessTips #Entrepreneurship #Success #Innovation',
            'twitter': '💡 Business insight: The most successful companies don\\'t just sell products—they solve problems and create value. What problem are you solving today? #BusinessStrategy #Innovation'
        },
        'technology': {
            'linkedin': '🔮 <strong>The Future of AI in Business:</strong><br><br>Artificial Intelligence is not just a buzzword—it\\'s transforming how we work, think, and create value. From automating routine tasks to generating creative solutions, AI is becoming an essential tool for modern businesses.<br><br>🤖 <strong>What\\'s Next:</strong> We\\'re moving beyond automation to augmentation, where AI enhances human capabilities rather than replacing them.<br><br>#AI #Technology #Innovation #FutureOfWork',
            'instagram': '🚀 <strong>Tech Innovation Spotlight:</strong><br><br>The pace of technological advancement is accelerating exponentially. What seemed impossible yesterday is becoming reality today.<br><br>💻 Remember: Technology should serve humanity, not the other way around. Use it to amplify your impact and reach.<br><br>#TechInnovation #AI #DigitalTransformation #Innovation',
            'twitter': '🚀 Tech is evolving faster than ever. The key is not just to adopt new technology, but to understand how it can serve your mission. #TechInnovation #AI #DigitalTransformation'
        }
    };
    
    const defaultContent = '📝 <strong>Generated Content:</strong><br><br>This is a sample content piece for ' + direction + ' on ' + platform + ' with a ' + tone + ' tone. ' + (topic ? 'Topic: ' + topic : '') + '<br><br>#ContentCreation #AI #Innovation';
    
    return contents[direction]?.[platform] || defaultContent;
}

function copyContent() {
    const content = document.getElementById('generatedContent').innerText;
    navigator.clipboard.writeText(content).then(() => {
        alert('Content copied to clipboard!');
    });
}

function saveContent() {
    alert('Content saved to library! (Demo mode)');
}
</script>
"""

# JavaScript for settings functionality
SETTINGS_SCRIPTS = """
<script>
document.getElementById('settingsForm').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Settings saved successfully! (Demo mode)');
});
</script>
"""

# JavaScript for library functionality
LIBRARY_SCRIPTS = """
<script>
document.getElementById('searchInput').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const cards = document.querySelectorAll('#contentGrid .card');
    
    cards.forEach(card => {
        const title = card.querySelector('h6').textContent.toLowerCase();
        const content = card.querySelector('p').textContent.toLowerCase();
        
        if (title.includes(searchTerm) || content.includes(searchTerm)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
});
</script>
"""

# JavaScript for demo functionality
DEMO_SCRIPTS = """
<script>
function showDemo() {
    alert('Demo mode coming soon! This is a serverless deployment.\\n\\nTry navigating to the Generator page to see the full content creation interface!');
}
</script>
"""

# In-memory user store for demo (replace with DB in production)
USERS = {
    'demo@contentcreator.com': generate_password_hash('demo123'),
    'test@example.com': generate_password_hash('test123')
}

# Expanded content directions (18+)
ALL_DIRECTIONS = [
    ("business_finance", "Business & Finance"),
    ("technology", "Technology"),
    ("health_wellness", "Health & Wellness"),
    ("education", "Education"),
    ("entertainment", "Entertainment"),
    ("travel_tourism", "Travel & Tourism"),
    ("food_cooking", "Food & Cooking"),
    ("fashion_beauty", "Fashion & Beauty"),
    ("sports_fitness", "Sports & Fitness"),
    ("science_research", "Science & Research"),
    ("politics_current_events", "Politics & Current Events"),
    ("environment_sustainability", "Environment & Sustainability"),
    ("personal_development", "Personal Development"),
    ("parenting_family", "Parenting & Family"),
    ("art_creativity", "Art & Creativity"),
    ("real_estate", "Real Estate"),
    ("automotive", "Automotive"),
    ("pet_care", "Pet Care"),
]

# Protect routes (example for dashboard)
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    """Main landing page - redirect to dashboard if logged in"""
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template_string(BASE_TEMPLATE, 
                                title="Home",
                                content=LANDING_CONTENT,
                                scripts=DEMO_SCRIPTS)

@app.route('/home')
def home():
    """Landing page"""
    return render_template_string(BASE_TEMPLATE, 
                                title="Home",
                                content=LANDING_CONTENT,
                                scripts=DEMO_SCRIPTS)

@app.route('/generator')
def generator():
    """Content generator page"""
    return render_template_string(BASE_TEMPLATE,
                                title="Content Generator",
                                content=GENERATOR_CONTENT,
                                scripts=GENERATOR_SCRIPTS)

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard page"""
    user_email = session.get('user', '')
    
    # Get user's content
    user_content = content_manager.get_user_content(user_email, limit=10)
    
    # Generate dashboard content with real data
    dashboard_content = generate_dashboard_content(user_email, user_content)
    
    return render_template_string(BASE_TEMPLATE,
                                title="Dashboard",
                                content=dashboard_content)

@app.route('/library')
def library():
    """Content library page"""
    return render_template_string(BASE_TEMPLATE,
                                title="Content Library",
                                content=LIBRARY_CONTENT,
                                scripts=LIBRARY_SCRIPTS)

@app.route('/linkedin-manager')
@login_required
def linkedin_manager():
    """LinkedIn Manager page (legacy route)"""
    return redirect('/social-media-manager?platform=linkedin')

@app.route('/social-media-manager')
@login_required
def social_media_manager():
    """Post Management page for all platforms"""
    try:
        user_email = session.get('user', 'demo@contentcreator.com')
        platform = request.args.get('platform', 'all')
        
        print(f"DEBUG: Processing social media manager for user: {user_email}, platform: {platform}")
        
        # Get all social media content for the user
        user_content = content_manager.get_user_content(user_email, limit=50)
        print(f"DEBUG: Retrieved {len(user_content)} total content items")
        
        social_content = [c for c in user_content if c.get('platform') in ['linkedin', 'twitter', 'facebook', 'instagram', 'youtube']]
        print(f"DEBUG: Filtered to {len(social_content)} social media content items")
        
        # Filter by platform if specified
        if platform != 'all':
            social_content = [c for c in social_content if c.get('platform') == platform]
            print(f"DEBUG: Further filtered to {len(social_content)} items for platform {platform}")
        
        # Generate social media manager content
        content = generate_social_media_manager_content(user_email, social_content, platform)
        
        return render_template_string(BASE_TEMPLATE,
                                    title="Post Management",
                                    content=content,
                                    scripts=SOCIAL_MEDIA_MANAGER_SCRIPTS)
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"ERROR in social_media_manager: {str(e)}")
        print(f"TRACEBACK: {error_traceback}")
        return render_template_string(BASE_TEMPLATE,
                                    title="Post Management",
                                    content=f"<div class='container'><div class='alert alert-danger'>Error loading Post Management: {str(e)}<br><small>Please try refreshing the page or contact support.</small></div></div>",
                                    scripts="")

@app.route('/settings')
def settings():
    """User settings page"""
    return render_template_string(BASE_TEMPLATE,
                                title="Settings",
                                content=SETTINGS_CONTENT,
                                scripts=SETTINGS_SCRIPTS)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in USERS:
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        USERS[email] = generate_password_hash(password)
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template_string(BASE_TEMPLATE, title="Register", content='''
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body p-4">
                        <h2 class="text-center mb-4"><i class="fas fa-user-plus me-2"></i><span data-translate="register">Register</span></h2>
                        <form method="post">
                            <div class="mb-3">
                                <label class="form-label" data-translate="email">Email</label>
                                <input type="email" name="email" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label" data-translate="password">Password</label>
                                <input type="password" name="password" class="form-control" required>
                            </div>
                            <div class="d-grid">
                                <button type="submit" class="btn btn-primary btn-lg">
                                    <i class="fas fa-user-plus me-2"></i><span data-translate="register">Register</span>
                                </button>
                            </div>
                        </form>
                        <div class="text-center mt-3">
                            <p><span data-translate="already_have_account">Already have an account?</span> <a href="/login" class="text-decoration-none" data-translate="login_here">Login here</a></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_hash = USERS.get(email)
        if user_hash and check_password_hash(user_hash, password):
            session['user'] = email
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        flash('Invalid credentials.', 'danger')
        return redirect(url_for('login'))
    return render_template_string(BASE_TEMPLATE, title="Login", content='''
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body p-4">
                        <h2 class="text-center mb-4"><i class="fas fa-sign-in-alt me-2"></i><span data-translate="login">Login</span></h2>
                        <form method="post">
                            <div class="mb-3">
                                <label class="form-label" data-translate="email">Email</label>
                                <input type="email" name="email" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label" data-translate="password">Password</label>
                                <input type="password" name="password" class="form-control" required>
                            </div>
                            <div class="d-grid">
                                <button type="submit" class="btn btn-primary btn-lg">
                                    <i class="fas fa-sign-in-alt me-2"></i><span data-translate="login">Login</span>
                                </button>
                            </div>
                        </form>
                        <div class="text-center mt-3">
                            <p><span data-translate="dont_have_account">Don't have an account?</span> <a href="/register" class="text-decoration-none" data-translate="register_here">Register here</a></p>
                        </div>
                        <div class="mt-4 p-3 bg-light rounded">
                            <h6 class="text-center mb-2" data-translate="demo_credentials">Demo Credentials:</h6>
                            <p class="small text-center mb-1">Email: demo@contentcreator.com</p>
                            <p class="small text-center mb-0">Password: demo123</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    ''')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/language/<lang>')
def switch_language(lang):
    """Switch application language"""
    if lang in ['en', 'zh']:
        session['language'] = lang
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'language': lang,
                'message': 'Language switched successfully'
            })
    return redirect(request.referrer or url_for('index'))

@app.route('/api/translate', methods=['POST'])
def translate_content():
    """Translate content between English and Chinese"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        target_lang = data.get('target_lang', 'en')
        
        if not content:
            return jsonify({
                'success': False,
                'error': 'No content provided'
            }), 400
        
        # Enhanced mock translation with better Chinese translations
        if target_lang == 'zh':
            translated_content = translate_to_chinese(content)
        else:
            translated_content = translate_to_english(content)
        
        return jsonify({
            'success': True,
            'translated_content': translated_content,
            'target_language': target_lang
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def translate_to_chinese(content):
    """Mock Chinese translation with common patterns"""
    translations = {
        # LinkedIn content
        '🚀 Exciting developments in the business world!': '🚀 商业世界令人兴奋的发展！',
        'Based on recent insights, we\'re seeing remarkable growth in key sectors.': '根据最近的见解，我们看到关键领域出现了显著增长。',
        'This represents a significant opportunity for forward-thinking professionals.': '这为有远见的专业人士提供了重要机会。',
        'What are your thoughts on these emerging trends?': '您对这些新兴趋势有什么看法？',
        '#BusinessGrowth #Innovation #ProfessionalDevelopment': '#商业增长 #创新 #职业发展',
        
        # Facebook content
        'Hey everyone! 👋 Just wanted to share some amazing insights': '大家好！👋 想分享一些令人惊叹的见解',
        'The way things are evolving in our industry is truly fascinating.': '我们行业的发展方式确实令人着迷。',
        'What do you think about these changes?': '您对这些变化有什么看法？',
        'Drop a comment below!': '在下面留言吧！',
        '#Community #Insights #Discussion': '#社区 #见解 #讨论',
        
        # Instagram content
        '✨ Today\'s inspiration comes from some incredible developments': '✨ 今天的灵感来自一些令人难以置信的发展',
        'The possibilities are endless when we embrace innovation and creativity.': '当我们拥抱创新和创造力时，可能性是无限的。',
        'What\'s inspiring you today?': '今天什么激励着您？',
        '#Inspiration #Innovation #Creativity #Motivation #Growth': '#灵感 #创新 #创造力 #动力 #成长',
        
        # Twitter content
        'Breaking: Major developments in the industry!': '突发：行业的重大发展！',
        'This changes everything.': '这改变了一切。',
        'Thoughts?': '想法？',
        '#Innovation #Trending': '#创新 #趋势',
        
        # YouTube content
        '[HOOK: 0-3 seconds] Hey there! Today we\'re diving into something incredible': '[开场：0-3秒] 大家好！今天我们要深入探讨一些令人难以置信的事情',
        'Based on recent research and insights, we\'re seeing remarkable changes': '根据最近的研究和见解，我们看到了一些显著的变化',
        'Here\'s what you need to know and how it impacts you.': '以下是您需要了解的内容以及它如何影响您。',
        'Don\'t forget to like, subscribe, and share your thoughts in the comments below!': '别忘了点赞、订阅，并在下面的评论中分享您的想法！',
        
        # Blog content
        '# The Future of Innovation: What You Need to Know': '# 创新的未来：您需要了解的内容',
        '## Introduction': '## 引言',
        'In today\'s rapidly evolving landscape, understanding the key trends and developments is crucial for success.': '在当今快速发展的环境中，了解关键趋势和发展对成功至关重要。',
        '## Key Insights': '## 关键见解',
        'Recent research and analysis reveal several important developments that are shaping the future of our industry.': '最近的研究和分析揭示了几个正在塑造我们行业未来的重要发展。',
        '## What This Means for You': '## 这对您意味着什么',
        'These changes present both challenges and opportunities for professionals and businesses alike.': '这些变化为专业人士和企业都带来了挑战和机遇。',
        '## Conclusion': '## 结论',
        'Staying informed and adaptable is more important than ever in this dynamic environment.': '在这个动态环境中，保持信息灵通和适应能力比以往任何时候都更重要。'
    }
    
    translated = content
    for english, chinese in translations.items():
        translated = translated.replace(english, chinese)
    
    return translated

def translate_to_english(content):
    """Mock English translation - return original content"""
    # For now, just return the original content since we're translating from Chinese to English
    # In a real implementation, this would translate Chinese back to English
    return content

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "mode": "serverless",
        "message": "Content Creator Pro is running in serverless mode",
        "pages": ["/", "/generator", "/dashboard", "/library", "/settings"]
    })

@app.route('/api/directions')
def get_directions():
    """Get available content directions"""
    directions_data = [
        {
            'id': 1,
            'direction_key': 'business_finance',
            'name': 'Business & Finance',
            'description': 'Content related to business strategies, financial markets, entrepreneurship, and corporate insights.'
        },
        {
            'id': 2,
            'direction_key': 'technology',
            'name': 'Technology',
            'description': 'Latest tech trends, software development, AI, and digital innovation.'
        },
        {
            'id': 3,
            'direction_key': 'health_wellness',
            'name': 'Health & Wellness',
            'description': 'Physical health, mental wellness, nutrition, and lifestyle tips.'
        },
        {
            'id': 4,
            'direction_key': 'education',
            'name': 'Education',
            'description': 'Learning resources, academic insights, and educational content.'
        },
        {
            'id': 5,
            'direction_key': 'entertainment',
            'name': 'Entertainment',
            'description': 'Movies, music, gaming, and pop culture content.'
        },
        {
            'id': 6,
            'direction_key': 'travel_tourism',
            'name': 'Travel & Tourism',
            'description': 'Travel guides, destination reviews, and tourism insights.'
        }
    ]
    return jsonify({
        'success': True,
        'directions': directions_data
    })

@app.route('/api/news-sources')
def get_news_sources():
    """Get available news sources by region"""
    news_sources = {
        'north_america': {
            'general': [
                {'name': 'CNN', 'url': 'cnn.com', 'category': 'General News'},
                {'name': 'Fox News', 'url': 'foxnews.com', 'category': 'General News'},
                {'name': 'NBC News', 'url': 'nbcnews.com', 'category': 'General News'},
                {'name': 'ABC News', 'url': 'abcnews.go.com', 'category': 'General News'}
            ],
            'business': [
                {'name': 'Bloomberg', 'url': 'bloomberg.com', 'category': 'Business News'},
                {'name': 'CNBC', 'url': 'cnbc.com', 'category': 'Business News'},
                {'name': 'Wall Street Journal', 'url': 'wsj.com', 'category': 'Business News'},
                {'name': 'Forbes', 'url': 'forbes.com', 'category': 'Business News'}
            ],
            'tech': [
                {'name': 'TechCrunch', 'url': 'techcrunch.com', 'category': 'Tech News'},
                {'name': 'The Verge', 'url': 'theverge.com', 'category': 'Tech News'},
                {'name': 'Wired', 'url': 'wired.com', 'category': 'Tech News'},
                {'name': 'Ars Technica', 'url': 'arstechnica.com', 'category': 'Tech News'}
            ]
        },
        'europe': {
            'general': [
                {'name': 'BBC', 'url': 'bbc.com', 'category': 'General News'},
                {'name': 'Reuters', 'url': 'reuters.com', 'category': 'General News'},
                {'name': 'The Guardian', 'url': 'theguardian.com', 'category': 'General News'},
                {'name': 'Le Monde', 'url': 'lemonde.fr', 'category': 'General News'}
            ],
            'business': [
                {'name': 'Financial Times', 'url': 'ft.com', 'category': 'Business News'},
                {'name': 'The Economist', 'url': 'economist.com', 'category': 'Business News'},
                {'name': 'Handelsblatt', 'url': 'handelsblatt.com', 'category': 'Business News'}
            ],
            'tech': [
                {'name': 'Tech.eu', 'url': 'tech.eu', 'category': 'Tech News'},
                {'name': 'The Next Web', 'url': 'thenextweb.com', 'category': 'Tech News'},
                {'name': 'EU-Startups', 'url': 'eu-startups.com', 'category': 'Tech News'}
            ]
        },
        'asia_pacific': {
            'general': [
                {'name': 'Nikkei', 'url': 'asia.nikkei.com', 'category': 'General News'},
                {'name': 'South China Morning Post', 'url': 'scmp.com', 'category': 'General News'},
                {'name': 'Straits Times', 'url': 'straitstimes.com', 'category': 'General News'}
            ],
            'business': [
                {'name': 'Bloomberg Asia', 'url': 'bloomberg.com/asia', 'category': 'Business News'},
                {'name': 'CNBC Asia', 'url': 'cnbc.com/asia', 'category': 'Business News'},
                {'name': 'Nikkei Business', 'url': 'business.nikkei.com', 'category': 'Business News'}
            ],
            'tech': [
                {'name': 'Tech in Asia', 'url': 'techinasia.com', 'category': 'Tech News'},
                {'name': 'KrASIA', 'url': 'kr-asia.com', 'category': 'Tech News'},
                {'name': '36Kr', 'url': '36kr.com', 'category': 'Tech News'}
            ]
        },
        'latin_america': {
            'general': [
                {'name': 'El País', 'url': 'elpais.com', 'category': 'General News'},
                {'name': 'Folha de S.Paulo', 'url': 'folha.uol.com.br', 'category': 'General News'},
                {'name': 'Clarín', 'url': 'clarin.com', 'category': 'General News'}
            ],
            'business': [
                {'name': 'América Economía', 'url': 'americaeconomia.com', 'category': 'Business News'},
                {'name': 'Valor Econômico', 'url': 'valor.com.br', 'category': 'Business News'}
            ],
            'tech': [
                {'name': 'TechCrunch Latin America', 'url': 'techcrunch.com/latam', 'category': 'Tech News'},
                {'name': 'Contxto', 'url': 'contxto.com', 'category': 'Tech News'},
                {'name': 'PulsoSocial', 'url': 'pulsosocial.com', 'category': 'Tech News'}
            ]
        },
        'middle_east': {
            'general': [
                {'name': 'Al Jazeera', 'url': 'aljazeera.com', 'category': 'General News'},
                {'name': 'Gulf News', 'url': 'gulfnews.com', 'category': 'General News'},
                {'name': 'The National', 'url': 'thenational.ae', 'category': 'General News'}
            ],
            'business': [
                {'name': 'Arabian Business', 'url': 'arabianbusiness.com', 'category': 'Business News'},
                {'name': 'MEED', 'url': 'meed.com', 'category': 'Business News'},
                {'name': 'Gulf Business', 'url': 'gulfbusiness.com', 'category': 'Business News'}
            ],
            'tech': [
                {'name': 'Wamda', 'url': 'wamda.com', 'category': 'Tech News'},
                {'name': 'MENAbytes', 'url': 'menabytes.com', 'category': 'Tech News'},
                {'name': 'Magnitt', 'url': 'magnitt.com', 'category': 'Tech News'}
            ]
        },
        'africa': {
            'general': [
                {'name': 'Business Day', 'url': 'businessday.ng', 'category': 'General News'},
                {'name': 'Daily Nation', 'url': 'nation.co.ke', 'category': 'General News'},
                {'name': 'The East African', 'url': 'theeastafrican.co.ke', 'category': 'General News'}
            ],
            'business': [
                {'name': 'African Business', 'url': 'africanbusinessmagazine.com', 'category': 'Business News'},
                {'name': 'Ventures Africa', 'url': 'venturesafrica.com', 'category': 'Business News'}
            ],
            'tech': [
                {'name': 'TechCabal', 'url': 'techcabal.com', 'category': 'Tech News'},
                {'name': 'Disrupt Africa', 'url': 'disrupt-africa.com', 'category': 'Tech News'},
                {'name': 'WeeTracker', 'url': 'weetracker.com', 'category': 'Tech News'}
            ]
        }
    }
    
    return jsonify({
        'success': True,
        'news_sources': news_sources
    })

@app.route('/api/save-content', methods=['POST'])
def save_content():
    """Save generated content to user's library"""
    try:
        if 'user' not in session:
            return jsonify({
                'success': False,
                'error': 'User not logged in'
            }), 401
        
        data = request.get_json()
        user_email = session['user']
        
        content_entry = content_manager.create_content(
            user_email=user_email,
            direction=data.get('direction'),
            platform=data.get('platform'),
            source=data.get('source'),
            topic=data.get('topic'),
            tone=data.get('tone'),
            content_text=data.get('content')
        )
        
        return jsonify({
            'success': True,
            'content_id': content_entry['id'],
            'message': 'Content saved successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/linkedin/schedule', methods=['POST'])
def schedule_linkedin_post():
    """Schedule a LinkedIn post"""
    try:
        if 'user' not in session:
            return jsonify({
                'success': False,
                'error': 'User not logged in'
            }), 401
        
        data = request.get_json()
        content_id = data.get('content_id')
        scheduled_time = data.get('scheduled_time')
        account = data.get('account', 'primary')
        
        # Update content status
        for user_content in content_manager.user_content.values():
            for content in user_content:
                if content['id'] == content_id:
                    content['status'] = 'scheduled'
                    content['scheduled_time'] = scheduled_time
                    content['linkedin_account'] = account
                    
                    return jsonify({
                        'success': True,
                        'message': 'Post scheduled successfully',
                        'scheduled_time': scheduled_time
                    })
        
        return jsonify({
            'success': False,
            'error': 'Content not found'
        }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/linkedin/publish', methods=['POST'])
def publish_linkedin_post():
    """Publish a LinkedIn post immediately"""
    try:
        if 'user' not in session:
            return jsonify({
                'success': False,
                'error': 'User not logged in'
            }), 401
        
        data = request.get_json()
        content_id = data.get('content_id')
        account = data.get('account', 'primary')
        
        # Update content status
        for user_content in content_manager.user_content.values():
            for content in user_content:
                if content['id'] == content_id:
                    content['status'] = 'published'
                    content['published_time'] = datetime.now().isoformat()
                    content['linkedin_account'] = account
                    
                    return jsonify({
                        'success': True,
                        'message': 'Post published successfully',
                        'published_time': content['published_time']
                    })
        
        return jsonify({
            'success': False,
            'error': 'Content not found'
        }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/linkedin/update-status', methods=['POST'])
def update_linkedin_post_status():
    """Update LinkedIn post status"""
    try:
        if 'user' not in session:
            return jsonify({
                'success': False,
                'error': 'User not logged in'
            }), 401
        
        data = request.get_json()
        content_id = data.get('content_id')
        status = data.get('status')
        
        # Update content status
        for user_content in content_manager.user_content.values():
            for content in user_content:
                if content['id'] == content_id:
                    content['status'] = status
                    
                    return jsonify({
                        'success': True,
                        'message': f'Post status updated to {status}',
                        'status': status
                    })
        
        return jsonify({
            'success': False,
            'error': 'Content not found'
        }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate', methods=['POST'])
def generate_content():
    """Generate content (demo mode)"""
    data = request.get_json() or {}
    return jsonify({
        'success': True,
        'data': {
            'content': 'This is a demo content generation. Full AI integration coming soon!',
            'message': 'Serverless mode active - AI features will be available in full deployment.',
            'request_data': data
        }
    })

# LinkedIn Manager Scripts
LINKEDIN_MANAGER_SCRIPTS = """
<script>
// LinkedIn Manager JavaScript Functions

// Post Management Functions
function createNewPost() {
    // Redirect to content generator with LinkedIn pre-selected
    window.location.href = '/generator?platform=linkedin';
}

function editPost(postId) {
    // Open edit modal for post
    console.log('Editing post:', postId);
    // Placeholder: Show edit modal
    alert('Edit post functionality - Post ID: ' + postId);
}

function duplicatePost(postId) {
    // Duplicate existing post
    console.log('Duplicating post:', postId);
    // Placeholder: Duplicate post
    alert('Duplicate post functionality - Post ID: ' + postId);
}

function deletePost(postId) {
    if (confirm('Are you sure you want to delete this post?')) {
        console.log('Deleting post:', postId);
        // Placeholder: Delete post
        alert('Delete post functionality - Post ID: ' + postId);
    }
}

// Scheduling Functions
function schedulePost(postId = null) {
    if (postId) {
        // Schedule specific post
        console.log('Scheduling post:', postId);
        showScheduleModal(postId);
    } else {
        // Schedule new post
        console.log('Schedule new post');
        showScheduleModal();
    }
}

function showScheduleModal(postId = null) {
    // Show scheduling modal
    const modalHtml = `
    <div class="modal fade" id="scheduleModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Schedule Post</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label class="form-label">Schedule Date & Time</label>
                        <input type="datetime-local" class="form-control" id="scheduleDateTime">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Post Content</label>
                        <textarea class="form-control" id="scheduleContent" rows="4" placeholder="Enter your post content..."></textarea>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">LinkedIn Account</label>
                        <select class="form-select" id="linkedinAccount">
                            <option value="primary">Primary Account</option>
                            <option value="company">Company Page</option>
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" onclick="confirmSchedule()">Schedule Post</button>
                </div>
            </div>
        </div>
    </div>
    `;
    
    // Remove existing modal if any
    const existingModal = document.getElementById('scheduleModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('scheduleModal'));
    modal.show();
}

function confirmSchedule() {
    const dateTime = document.getElementById('scheduleDateTime').value;
    const content = document.getElementById('scheduleContent').value;
    const account = document.getElementById('linkedinAccount').value;
    
    if (!dateTime || !content) {
        alert('Please fill in all required fields');
        return;
    }
    
    console.log('Scheduling post:', { dateTime, content, account });
    
    // Placeholder: Save schedule
    alert('Post scheduled successfully!');
    
    // Close modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('scheduleModal'));
    modal.hide();
}

function cancelSchedule(postId) {
    if (confirm('Are you sure you want to cancel this scheduled post?')) {
        console.log('Canceling schedule for post:', postId);
        // Placeholder: Cancel schedule
        alert('Schedule canceled for post: ' + postId);
    }
}

// Publishing Functions
function publishNow(postId = null) {
    if (postId) {
        // Publish specific post
        console.log('Publishing post now:', postId);
        confirmPublish(postId);
    } else {
        // Publish new post
        console.log('Publish new post now');
        showPublishModal();
    }
}

function confirmPublish(postId) {
    if (confirm('Are you sure you want to publish this post now?')) {
        console.log('Confirming publish for post:', postId);
        // Placeholder: Publish post
        alert('Post published successfully!');
    }
}

function showPublishModal() {
    // Show publish modal
    const modalHtml = `
    <div class="modal fade" id="publishModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Publish Post Now</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label class="form-label">Post Content</label>
                        <textarea class="form-control" id="publishContent" rows="4" placeholder="Enter your post content..."></textarea>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">LinkedIn Account</label>
                        <select class="form-select" id="publishAccount">
                            <option value="primary">Primary Account</option>
                            <option value="company">Company Page</option>
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-success" onclick="confirmPublishNow()">Publish Now</button>
                </div>
            </div>
        </div>
    </div>
    `;
    
    // Remove existing modal if any
    const existingModal = document.getElementById('publishModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('publishModal'));
    modal.show();
}

function confirmPublishNow() {
    const content = document.getElementById('publishContent').value;
    const account = document.getElementById('publishAccount').value;
    
    if (!content) {
        alert('Please enter post content');
        return;
    }
    
    console.log('Publishing now:', { content, account });
    
    // Placeholder: Publish immediately
    alert('Post published successfully!');
    
    // Close modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('publishModal'));
    modal.hide();
}

// Filter Functions
function applyFilters() {
    const statusFilter = document.getElementById('statusFilter').value;
    const directionFilter = document.getElementById('directionFilter').value;
    const dateFilter = document.getElementById('dateFilter').value;
    
    console.log('Applying filters:', { statusFilter, directionFilter, dateFilter });
    
    // Placeholder: Apply filters
    alert('Filters applied: ' + JSON.stringify({ statusFilter, directionFilter, dateFilter }));
}

// Bulk Actions
function bulkActions() {
    const selectedPosts = document.querySelectorAll('.post-item input[type="checkbox"]:checked');
    
    if (selectedPosts.length === 0) {
        alert('Please select posts for bulk actions');
        return;
    }
    
    const action = prompt('Choose action: schedule, publish, delete');
    if (action) {
        console.log('Bulk action:', action, 'on', selectedPosts.length, 'posts');
        // Placeholder: Perform bulk action
        alert('Bulk action "' + action + '" performed on ' + selectedPosts.length + ' posts');
    }
}

// Analytics Functions
function analyzePerformance() {
    console.log('Opening performance analysis');
    // Placeholder: Open analytics
    alert('Performance analysis - This would open detailed analytics dashboard');
}

function exportData() {
    console.log('Exporting LinkedIn data');
    // Placeholder: Export data
    alert('Data export - This would download LinkedIn performance data as CSV');
}

// Settings Functions
function openLinkedInSettings() {
    console.log('Opening LinkedIn settings');
    // Placeholder: Open settings
    alert('LinkedIn Settings - This would open account connection and preferences');
}

// Initialize LinkedIn Manager
document.addEventListener('DOMContentLoaded', function() {
    console.log('LinkedIn Manager initialized');
    
    // Add event listeners for checkboxes
    document.querySelectorAll('.post-item input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateBulkActionsVisibility();
        });
    });
});

function updateBulkActionsVisibility() {
    const selectedPosts = document.querySelectorAll('.post-item input[type="checkbox"]:checked');
    const bulkActionsBtn = document.querySelector('button[onclick="bulkActions()"]');
    
    if (bulkActionsBtn) {
        bulkActionsBtn.disabled = selectedPosts.length === 0;
    }
}
</script>
"""

# Social Media Manager Scripts
SOCIAL_MEDIA_MANAGER_SCRIPTS = """
<script>
// Social Media Manager JavaScript Functions

// Post Management Functions
function createNewPost() {
    // Redirect to content generator
    window.location.href = '/generator';
}

function editPost(postId) {
    // Open edit modal for post
    console.log('Editing post:', postId);
    // Placeholder: Show edit modal
    alert('Edit post functionality - Post ID: ' + postId);
}

function duplicatePost(postId) {
    // Duplicate existing post
    console.log('Duplicating post:', postId);
    // Placeholder: Duplicate post
    alert('Duplicate post functionality - Post ID: ' + postId);
}

function deletePost(postId) {
    if (confirm('Are you sure you want to delete this post?')) {
        console.log('Deleting post:', postId);
        // Placeholder: Delete post
        alert('Delete post functionality - Post ID: ' + postId);
    }
}

// Scheduling Functions
function schedulePost(postId = null) {
    if (postId) {
        // Schedule specific post
        console.log('Scheduling post:', postId);
        showScheduleModal(postId);
    } else {
        // Schedule new post
        console.log('Schedule new post');
        showScheduleModal();
    }
}

function showScheduleModal(postId = null) {
    // Show scheduling modal
    const modalHtml = `
    <div class="modal fade" id="scheduleModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Schedule Post</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label class="form-label">Platform</label>
                        <select class="form-select" id="schedulePlatform">
                            <option value="linkedin">LinkedIn</option>
                            <option value="twitter">Twitter</option>
                            <option value="facebook">Facebook</option>
                            <option value="instagram">Instagram</option>
                            <option value="youtube">YouTube</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Schedule Date & Time</label>
                        <input type="datetime-local" class="form-control" id="scheduleDateTime">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Post Content</label>
                        <textarea class="form-control" id="scheduleContent" rows="4" placeholder="Enter your post content..."></textarea>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Account</label>
                        <select class="form-select" id="scheduleAccount">
                            <option value="primary">Primary Account</option>
                            <option value="company">Company Page</option>
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" onclick="confirmSchedule()">Schedule Post</button>
                </div>
            </div>
        </div>
    </div>
    `;
    
    // Remove existing modal if any
    const existingModal = document.getElementById('scheduleModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('scheduleModal'));
    modal.show();
}

function confirmSchedule() {
    const platform = document.getElementById('schedulePlatform').value;
    const dateTime = document.getElementById('scheduleDateTime').value;
    const content = document.getElementById('scheduleContent').value;
    const account = document.getElementById('scheduleAccount').value;
    
    if (!dateTime || !content) {
        alert('Please fill in all required fields');
        return;
    }
    
    console.log('Scheduling post:', { platform, dateTime, content, account });
    
    // Placeholder: Save schedule
    alert('Post scheduled successfully for ' + platform + '!');
    
    // Close modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('scheduleModal'));
    modal.hide();
}

function cancelSchedule(postId) {
    if (confirm('Are you sure you want to cancel this scheduled post?')) {
        console.log('Canceling schedule for post:', postId);
        // Placeholder: Cancel schedule
        alert('Schedule canceled for post: ' + postId);
    }
}

// Publishing Functions
function publishNow(postId = null) {
    if (postId) {
        // Publish specific post
        console.log('Publishing post now:', postId);
        confirmPublish(postId);
    } else {
        // Publish new post
        console.log('Publish new post now');
        showPublishModal();
    }
}

function confirmPublish(postId) {
    if (confirm('Are you sure you want to publish this post now?')) {
        console.log('Confirming publish for post:', postId);
        // Placeholder: Publish post
        alert('Post published successfully!');
    }
}

function showPublishModal() {
    // Show publish modal
    const modalHtml = `
    <div class="modal fade" id="publishModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Publish Post Now</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label class="form-label">Platform</label>
                        <select class="form-select" id="publishPlatform">
                            <option value="linkedin">LinkedIn</option>
                            <option value="twitter">Twitter</option>
                            <option value="facebook">Facebook</option>
                            <option value="instagram">Instagram</option>
                            <option value="youtube">YouTube</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Post Content</label>
                        <textarea class="form-control" id="publishContent" rows="4" placeholder="Enter your post content..."></textarea>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Account</label>
                        <select class="form-select" id="publishAccount">
                            <option value="primary">Primary Account</option>
                            <option value="company">Company Page</option>
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-success" onclick="confirmPublishNow()">Publish Now</button>
                </div>
            </div>
        </div>
    </div>
    `;
    
    // Remove existing modal if any
    const existingModal = document.getElementById('publishModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('publishModal'));
    modal.show();
}

function confirmPublishNow() {
    const platform = document.getElementById('publishPlatform').value;
    const content = document.getElementById('publishContent').value;
    const account = document.getElementById('publishAccount').value;
    
    if (!content) {
        alert('Please enter post content');
        return;
    }
    
    console.log('Publishing now:', { platform, content, account });
    
    // Placeholder: Publish immediately
    alert('Post published successfully on ' + platform + '!');
    
    // Close modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('publishModal'));
    modal.hide();
}

// Filter Functions
function applyFilters() {
    const statusFilter = document.getElementById('statusFilter').value;
    const directionFilter = document.getElementById('directionFilter').value;
    const dateFilter = document.getElementById('dateFilter').value;
    
    console.log('Applying filters:', { statusFilter, directionFilter, dateFilter });
    
    // Placeholder: Apply filters
    alert('Filters applied: ' + JSON.stringify({ statusFilter, directionFilter, dateFilter }));
}

// Bulk Actions
function bulkActions() {
    const selectedPosts = document.querySelectorAll('.post-item input[type="checkbox"]:checked');
    
    if (selectedPosts.length === 0) {
        alert('Please select posts for bulk actions');
        return;
    }
    
    const action = prompt('Choose action: schedule, publish, delete');
    if (action) {
        console.log('Bulk action:', action, 'on', selectedPosts.length, 'posts');
        // Placeholder: Perform bulk action
        alert('Bulk action "' + action + '" performed on ' + selectedPosts.length + ' posts');
    }
}

// Analytics Functions
function analyzePerformance() {
    console.log('Opening performance analysis');
    // Placeholder: Open analytics
    alert('Performance analysis - This would open detailed analytics dashboard');
}

function exportData() {
    console.log('Exporting social media data');
    // Placeholder: Export data
    alert('Data export - This would download social media performance data as CSV');
}

// Settings Functions
function openSocialMediaSettings() {
    console.log('Opening social media settings');
    // Placeholder: Open settings
    alert('Social Media Settings - This would open account connections and preferences for all platforms');
}

// Initialize Social Media Manager
document.addEventListener('DOMContentLoaded', function() {
    console.log('Social Media Manager initialized');
    
    // Add event listeners for checkboxes
    document.querySelectorAll('.post-item input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateBulkActionsVisibility();
        });
    });
});

function updateBulkActionsVisibility() {
    const selectedPosts = document.querySelectorAll('.post-item input[type="checkbox"]:checked');
    const bulkActionsBtn = document.querySelector('button[onclick="bulkActions()"]');
    
    if (bulkActionsBtn) {
        bulkActionsBtn.disabled = selectedPosts.length === 0;
    }
}
</script>
"""

if __name__ == '__main__':
    app.run(debug=True) 