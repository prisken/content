import os
from flask import Flask, render_template_string, jsonify, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# Set environment variable to indicate serverless mode
os.environ['VERCEL_ENV'] = 'production'

app = Flask(__name__)

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
        .navbar { background: rgba(255,255,255,0.1) !important; backdrop-filter: blur(10px); }
        .navbar-brand { color: #fff !important; font-weight: bold; }
        .nav-link { color: #fff !important; }
        .nav-link:hover { color: #f0f0f0 !important; }
        .main-content { padding: 50px 0; color: #fff; }
        .card { background: rgba(255,255,255,0.95); border: none; border-radius: 15px; }
        .btn-primary { background: linear-gradient(45deg, #667eea, #764ba2); border: none; }
        .feature-card { background: #fff; border-radius: 15px; padding: 30px; margin: 20px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.1); color: #222; }
        .feature-card h3, .feature-card p { color: #222 !important; text-shadow: none; }
        h1, h2, h3, p, .lead { color: #fff !important; text-shadow: 0 2px 8px rgba(0,0,0,0.25); }
        .card h3, .card p { color: #222 !important; text-shadow: none; }
        .form-control { border-radius: 10px; border: 2px solid #e0e0e0; }
        .form-control:focus { border-color: #667eea; box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25); }
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
                    <li class="nav-item">
                        <a class="nav-link" href="/"><i class="fas fa-home me-1"></i>Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/generator"><i class="fas fa-magic me-1"></i>Generator</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/dashboard"><i class="fas fa-chart-line me-1"></i>Dashboard</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/library"><i class="fas fa-book me-1"></i>Library</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/settings"><i class="fas fa-cog me-1"></i>Settings</a>
                    </li>
                    {% if 'user' in session %}
                    <li class="nav-item">
                        <a class="nav-link" href="/logout"><i class="fas fa-sign-out-alt me-1"></i>Logout</a>
                    </li>
                    {% else %}
                    <li class="nav-item">
                        <a class="nav-link" href="/login"><i class="fas fa-sign-in-alt me-1"></i>Login</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/register"><i class="fas fa-user-plus me-1"></i>Register</a>
                    </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="main-content">
        {{ content | safe }}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    {{ scripts | safe if scripts else '' }}
</body>
</html>
"""

# Landing page content
LANDING_CONTENT = """
<div class="container">
    <div class="text-center">
        <h1 class="display-4 mb-4">🚀 Content Creator Pro</h1>
        <p class="lead mb-5">AI-Powered Content Generation Platform</p>
        <div class="row">
            <div class="col-md-4">
                <div class="feature-card">
                    <h3><i class="fas fa-share-alt me-2"></i>Multi-Platform Content</h3>
                    <p>Generate content for <b>LinkedIn, Facebook, Instagram, Twitter, YouTube, and blogs</b>.</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="feature-card">
                    <h3><i class="fas fa-bullseye me-2"></i>Smart Direction</h3>
                    <p>18 content directions with <b>regional and cultural context</b>.</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="feature-card">
                    <h3><i class="fas fa-brain me-2"></i>AI-Powered</h3>
                    <p>Advanced AI content generation with <b>tone and style customization</b>.</p>
                </div>
            </div>
        </div>
        <div class="mt-5">
            <a href="/generator" class="btn btn-primary btn-lg me-3">
                <i class="fas fa-magic me-2"></i>Start Creating
            </a>
            <button class="btn btn-outline-light btn-lg" onclick="showDemo()">
                <i class="fas fa-play me-2"></i>Try Demo
            </button>
        </div>
    </div>
</div>
"""

# Generator page content
GENERATOR_CONTENT = """
<div class="container">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="text-center mb-5">
                <h1><i class="fas fa-magic me-2"></i>Content Generator</h1>
                <p class="lead">Create engaging content with AI assistance</p>
            </div>
            
            <div class="card">
                <div class="card-body p-4">
                    <form id="generatorForm">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Content Direction</label>
                                <select class="form-select" id="direction" required>
                                    <option value="">Choose direction...</option>
                                    {% for direction_key, direction_name in ALL_DIRECTIONS %}
                                    <option value="{{ direction_key }}">{{ direction_name }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Platform</label>
                                <select class="form-select" id="platform" required>
                                    <option value="">Choose platform...</option>
                                    <option value="linkedin">LinkedIn</option>
                                    <option value="facebook">Facebook</option>
                                    <option value="instagram">Instagram</option>
                                    <option value="twitter">Twitter</option>
                                    <option value="youtube">YouTube</option>
                                    <option value="blog">Blog</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Tone</label>
                                <select class="form-select" id="tone">
                                    <option value="professional">Professional</option>
                                    <option value="casual">Casual</option>
                                    <option value="inspirational">Inspirational</option>
                                    <option value="educational">Educational</option>
                                    <option value="humorous">Humorous</option>
                                </select>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Length</label>
                                <select class="form-select" id="length">
                                    <option value="short">Short</option>
                                    <option value="medium">Medium</option>
                                    <option value="long">Long</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Topic/Keywords</label>
                            <textarea class="form-control" id="topic" rows="3" placeholder="Enter your topic or keywords..."></textarea>
                        </div>
                        
                        <div class="text-center">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-magic me-2"></i>Generate Content
                            </button>
                        </div>
                    </form>
                </div>
            </div>
            
            <div id="result" class="card mt-4" style="display: none;">
                <div class="card-body p-4">
                    <h4><i class="fas fa-file-alt me-2"></i>Generated Content</h4>
                    <div id="generatedContent" class="mt-3"></div>
                    <div class="mt-3">
                        <button class="btn btn-success me-2" onclick="copyContent()">
                            <i class="fas fa-copy me-1"></i>Copy
                        </button>
                        <button class="btn btn-primary" onclick="saveContent()">
                            <i class="fas fa-save me-1"></i>Save to Library
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
"""

# Dashboard page content
DASHBOARD_CONTENT = """
<div class="container">
    <div class="text-center mb-5">
        <h1><i class="fas fa-chart-line me-2"></i>Dashboard</h1>
        <p class="lead">Your content creation overview</p>
    </div>
    
    <div class="row">
        <div class="col-md-3 mb-4">
            <div class="card text-center">
                <div class="card-body">
                    <i class="fas fa-file-alt fa-3x text-primary mb-3"></i>
                    <h4>24</h4>
                    <p class="text-muted">Total Content</p>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-4">
            <div class="card text-center">
                <div class="card-body">
                    <i class="fas fa-calendar fa-3x text-success mb-3"></i>
                    <h4>7</h4>
                    <p class="text-muted">This Week</p>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-4">
            <div class="card text-center">
                <div class="card-body">
                    <i class="fas fa-thumbs-up fa-3x text-warning mb-3"></i>
                    <h4>156</h4>
                    <p class="text-muted">Total Likes</p>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-4">
            <div class="card text-center">
                <div class="card-body">
                    <i class="fas fa-share fa-3x text-info mb-3"></i>
                    <h4>89</h4>
                    <p class="text-muted">Total Shares</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header">
                    <h5><i class="fas fa-chart-pie me-2"></i>Content by Platform</h5>
                </div>
                <div class="card-body">
                    <div class="d-flex justify-content-between mb-2">
                        <span>LinkedIn</span>
                        <span class="badge bg-primary">45%</span>
                    </div>
                    <div class="d-flex justify-content-between mb-2">
                        <span>Instagram</span>
                        <span class="badge bg-success">30%</span>
                    </div>
                    <div class="d-flex justify-content-between mb-2">
                        <span>Twitter</span>
                        <span class="badge bg-info">15%</span>
                    </div>
                    <div class="d-flex justify-content-between">
                        <span>Facebook</span>
                        <span class="badge bg-warning">10%</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header">
                    <h5><i class="fas fa-clock me-2"></i>Recent Activity</h5>
                </div>
                <div class="card-body">
                    <div class="d-flex align-items-center mb-3">
                        <i class="fas fa-file-alt text-primary me-3"></i>
                        <div>
                            <strong>Business Post</strong>
                            <br><small class="text-muted">2 hours ago</small>
                        </div>
                    </div>
                    <div class="d-flex align-items-center mb-3">
                        <i class="fas fa-image text-success me-3"></i>
                        <div>
                            <strong>Instagram Caption</strong>
                            <br><small class="text-muted">1 day ago</small>
                        </div>
                    </div>
                    <div class="d-flex align-items-center">
                        <i class="fas fa-video text-warning me-3"></i>
                        <div>
                            <strong>YouTube Script</strong>
                            <br><small class="text-muted">3 days ago</small>
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
    <div class="text-center mb-5">
        <h1><i class="fas fa-book me-2"></i>Content Library</h1>
        <p class="lead">Your saved content collection</p>
    </div>
    
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="input-group">
                <input type="text" class="form-control" placeholder="Search content..." id="searchInput">
                <button class="btn btn-outline-secondary" type="button">
                    <i class="fas fa-search"></i>
                </button>
            </div>
        </div>
        <div class="col-md-6 text-end">
            <button class="btn btn-primary">
                <i class="fas fa-plus me-2"></i>Create New
            </button>
        </div>
    </div>
    
    <div class="row" id="contentGrid">
        <div class="col-md-4 mb-4">
            <div class="card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="badge bg-primary">LinkedIn</span>
                        <small class="text-muted">2 hours ago</small>
                    </div>
                    <h6>Business Strategy Insights</h6>
                    <p class="text-muted small">Key insights for modern business leaders looking to scale their operations...</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">Business & Finance</small>
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
        
        <div class="col-md-4 mb-4">
            <div class="card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="badge bg-success">Instagram</span>
                        <small class="text-muted">1 day ago</small>
                    </div>
                    <h6>Tech Innovation Trends</h6>
                    <p class="text-muted small">Exploring the latest developments in AI and machine learning...</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">Technology</small>
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
        
        <div class="col-md-4 mb-4">
            <div class="card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="badge bg-info">Twitter</span>
                        <small class="text-muted">3 days ago</small>
                    </div>
                    <h6>Health & Wellness Tips</h6>
                    <p class="text-muted small">Simple daily habits that can transform your health and wellbeing...</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">Health & Wellness</small>
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
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="text-center mb-5">
                <h1><i class="fas fa-cog me-2"></i>Settings</h1>
                <p class="lead">Customize your content creation experience</p>
            </div>
            
            <div class="card">
                <div class="card-body p-4">
                    <form id="settingsForm">
                        <h5 class="mb-4"><i class="fas fa-user me-2"></i>Profile Settings</h5>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Name</label>
                                <input type="text" class="form-control" value="Demo User" id="userName">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Email</label>
                                <input type="email" class="form-control" value="demo@contentcreator.com" readonly>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Region</label>
                                <select class="form-select" id="region">
                                    <option value="global">Global</option>
                                    <option value="us">United States</option>
                                    <option value="eu">Europe</option>
                                    <option value="asia">Asia</option>
                                </select>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Language</label>
                                <select class="form-select" id="language">
                                    <option value="en">English</option>
                                    <option value="es">Spanish</option>
                                    <option value="fr">French</option>
                                    <option value="de">German</option>
                                </select>
                            </div>
                        </div>
                        
                        <hr class="my-4">
                        
                        <h5 class="mb-4"><i class="fas fa-magic me-2"></i>Content Preferences</h5>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Default Tone</label>
                                <select class="form-select" id="defaultTone">
                                    <option value="professional">Professional</option>
                                    <option value="casual">Casual</option>
                                    <option value="inspirational">Inspirational</option>
                                    <option value="educational">Educational</option>
                                </select>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Default Length</label>
                                <select class="form-select" id="defaultLength">
                                    <option value="medium">Medium</option>
                                    <option value="short">Short</option>
                                    <option value="long">Long</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Preferred Content Directions</label>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="business_finance" id="pref1" checked>
                                <label class="form-check-label" for="pref1">Business & Finance</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="technology" id="pref2" checked>
                                <label class="form-check-label" for="pref2">Technology</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="health_wellness" id="pref3">
                                <label class="form-check-label" for="pref3">Health & Wellness</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="education" id="pref4">
                                <label class="form-check-label" for="pref4">Education</label>
                            </div>
                        </div>
                        
                        <div class="text-center">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-save me-2"></i>Save Settings
                            </button>
                        </div>
                    </form>
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
            'linkedin': '🚀 <strong>Business Strategy Insight:</strong><br><br>In today\'s rapidly evolving market, successful businesses are those that adapt quickly to change while maintaining their core values. The key is not just to react to market shifts, but to anticipate them.<br><br>💡 <strong>Key Takeaway:</strong> Focus on building resilient systems that can weather economic storms while positioning your company for growth opportunities.<br><br>#BusinessStrategy #Leadership #Innovation #Growth',
            'instagram': '💼 <strong>Business Tip of the Day:</strong><br><br>Success isn\'t about having all the answers—it\'s about asking the right questions. What problem are you solving? Who are you serving? How can you deliver more value?<br><br>✨ The best businesses focus on creating solutions that make people\'s lives better.<br><br>#BusinessTips #Entrepreneurship #Success #Innovation',
            'twitter': '💡 Business insight: The most successful companies don\'t just sell products—they solve problems and create value. What problem are you solving today? #BusinessStrategy #Innovation'
        },
        'technology': {
            'linkedin': '🔮 <strong>The Future of AI in Business:</strong><br><br>Artificial Intelligence is not just a buzzword—it\'s transforming how we work, think, and create value. From automating routine tasks to generating creative solutions, AI is becoming an essential tool for modern businesses.<br><br>🤖 <strong>What\'s Next:</strong> We\'re moving beyond automation to augmentation, where AI enhances human capabilities rather than replacing them.<br><br>#AI #Technology #Innovation #FutureOfWork',
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
    """Main landing page"""
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
    return render_template_string(BASE_TEMPLATE,
                                title="Dashboard",
                                content=DASHBOARD_CONTENT)

@app.route('/library')
def library():
    """Content library page"""
    return render_template_string(BASE_TEMPLATE,
                                title="Content Library",
                                content=LIBRARY_CONTENT,
                                scripts=LIBRARY_SCRIPTS)

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
    <div class="container"><div class="row justify-content-center"><div class="col-md-6">
    <h2>Register</h2>
    <form method="post">
      <div class="mb-3"><label>Email</label><input type="email" name="email" class="form-control" required></div>
      <div class="mb-3"><label>Password</label><input type="password" name="password" class="form-control" required></div>
      <button type="submit" class="btn btn-primary">Register</button>
    </form></div></div></div>
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
    <div class="container"><div class="row justify-content-center"><div class="col-md-6">
    <h2>Login</h2>
    <form method="post">
      <div class="mb-3"><label>Email</label><input type="email" name="email" class="form-control" required></div>
      <div class="mb-3"><label>Password</label><input type="password" name="password" class="form-control" required></div>
      <button type="submit" class="btn btn-primary">Login</button>
    </form></div></div></div>
    ''')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out.', 'info')
    return redirect(url_for('index'))

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

if __name__ == '__main__':
    app.run(debug=True) 