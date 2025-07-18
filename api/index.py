import os
from flask import Flask, render_template_string, jsonify, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# Set environment variable to indicate serverless mode
os.environ['VERCEL_ENV'] = 'production'

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'  # Required for session management

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
                            <span id="current-language">English</span>
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item language-option" href="/language/en">
                                <i class="fas fa-flag me-2"></i>English
                            </a></li>
                            <li><a class="dropdown-item language-option" href="/language/zh">
                                <i class="fas fa-flag me-2"></i>中文
                            </a></li>
                        </ul>
                    </li>
                    
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
                        <span class="user-welcome">
                            <i class="fas fa-user me-1"></i>Welcome, {{ session['user'] }}
                        </span>
                    </li>
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
    <script>
    // Language switching functionality
    document.addEventListener('DOMContentLoaded', function() {
        // Update language display based on session
        const currentLang = '{{ session.get("language", "en") }}';
        const languageNames = {
            'en': 'English',
            'zh': '中文'
        };
        
        const currentLanguageSpan = document.getElementById('current-language');
        if (currentLanguageSpan) {
            currentLanguageSpan.textContent = languageNames[currentLang] || 'English';
        }
        
        // Highlight current language in dropdown
        const languageOptions = document.querySelectorAll('.language-option');
        languageOptions.forEach(option => {
            if (option.getAttribute('href').includes(currentLang)) {
                option.classList.add('active');
            }
        });
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

# Generator page content - Updated to match wireframes
GENERATOR_CONTENT = """
<div class="container">
    <div class="row justify-content-center">
        <div class="col-lg-10">
            <div class="text-center mb-5">
                <h1><i class="fas fa-magic me-2"></i>Content Generator</h1>
                <p class="lead">Create engaging content with AI assistance</p>
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
                            <h3 class="text-center mb-4">Step 1: Choose Your Focus</h3>
                            <div class="row">
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="business_finance">
                                        <i class="fas fa-briefcase"></i>
                                        <div>Business & Finance</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="technology">
                                        <i class="fas fa-laptop-code"></i>
                                        <div>Technology</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="health_wellness">
                                        <i class="fas fa-heartbeat"></i>
                                        <div>Health & Wellness</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="education">
                                        <i class="fas fa-graduation-cap"></i>
                                        <div>Education</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="entertainment">
                                        <i class="fas fa-film"></i>
                                        <div>Entertainment</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="travel_tourism">
                                        <i class="fas fa-plane"></i>
                                        <div>Travel & Tourism</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="food_cooking">
                                        <i class="fas fa-utensils"></i>
                                        <div>Food & Cooking</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="fashion_beauty">
                                        <i class="fas fa-tshirt"></i>
                                        <div>Fashion & Beauty</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="sports_fitness">
                                        <i class="fas fa-dumbbell"></i>
                                        <div>Sports & Fitness</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="science_research">
                                        <i class="fas fa-microscope"></i>
                                        <div>Science & Research</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="politics_current_events">
                                        <i class="fas fa-newspaper"></i>
                                        <div>Politics & News</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="environment_sustainability">
                                        <i class="fas fa-leaf"></i>
                                        <div>Environment</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="personal_development">
                                        <i class="fas fa-chart-line"></i>
                                        <div>Personal Dev</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="parenting_family">
                                        <i class="fas fa-users"></i>
                                        <div>Parenting & Family</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="art_creativity">
                                        <i class="fas fa-palette"></i>
                                        <div>Art & Creativity</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="real_estate">
                                        <i class="fas fa-home"></i>
                                        <div>Real Estate</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="automotive">
                                        <i class="fas fa-car"></i>
                                        <div>Automotive</div>
                                    </div>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <div class="direction-card" data-direction="pet_care">
                                        <i class="fas fa-paw"></i>
                                        <div>Pet Care</div>
                                    </div>
                                </div>
                            </div>
                            <div class="text-center mt-4">
                                <button type="button" class="btn btn-primary btn-lg" onclick="nextStep()">
                                    Next Step <i class="fas fa-arrow-right ms-2"></i>
                                </button>
                            </div>
                        </div>
                        
                        <!-- Step 2: Content Type -->
                        <div id="step2" class="step-content" style="display: none;">
                            <h3 class="text-center mb-4">Step 2: What Type of Content?</h3>
                            <div class="row">
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-platform="linkedin">
                                        <i class="fab fa-linkedin"></i>
                                        <div>LinkedIn Post</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-platform="facebook">
                                        <i class="fab fa-facebook"></i>
                                        <div>Facebook Post</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-platform="instagram">
                                        <i class="fab fa-instagram"></i>
                                        <div>Instagram Post</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-platform="twitter">
                                        <i class="fab fa-twitter"></i>
                                        <div>Twitter Post</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-platform="youtube">
                                        <i class="fab fa-youtube"></i>
                                        <div>YouTube Short</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-platform="blog">
                                        <i class="fas fa-blog"></i>
                                        <div>Blog Article</div>
                                    </div>
                                </div>
                            </div>
                            <div class="text-center mt-4">
                                <button type="button" class="btn btn-secondary btn-lg me-3" onclick="prevStep()">
                                    <i class="fas fa-arrow-left me-2"></i>Previous
                                </button>
                                <button type="button" class="btn btn-primary btn-lg" onclick="nextStep()">
                                    Next Step <i class="fas fa-arrow-right ms-2"></i>
                                </button>
                            </div>
                        </div>
                        
                        <!-- Step 3: Inspiration Source -->
                        <div id="step3" class="step-content" style="display: none;">
                            <h3 class="text-center mb-4">Step 3: What Inspires You?</h3>
                            <div class="row">
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-source="news">
                                        <i class="fas fa-newspaper"></i>
                                        <div>Latest News</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-source="books">
                                        <i class="fas fa-book"></i>
                                        <div>Popular Books</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-source="threads">
                                        <i class="fas fa-comments"></i>
                                        <div>Trending Threads</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-source="podcasts">
                                        <i class="fas fa-podcast"></i>
                                        <div>Podcasts</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-source="videos">
                                        <i class="fas fa-video"></i>
                                        <div>YouTube Videos</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-source="research">
                                        <i class="fas fa-file-alt"></i>
                                        <div>Research Papers</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-source="case_studies">
                                        <i class="fas fa-chart-bar"></i>
                                        <div>Case Studies</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-source="trends">
                                        <i class="fas fa-fire"></i>
                                        <div>Trending Topics</div>
                                    </div>
                                </div>
                            </div>
                            <div class="text-center mt-4">
                                <button type="button" class="btn btn-secondary btn-lg me-3" onclick="prevStep()">
                                    <i class="fas fa-arrow-left me-2"></i>Previous
                                </button>
                                <button type="button" class="btn btn-primary btn-lg" onclick="nextStep()">
                                    Next Step <i class="fas fa-arrow-right ms-2"></i>
                                </button>
                            </div>
                        </div>
                        
                        <!-- Step 3.5: Topic Selection -->
                        <div id="step3_5" class="step-content" style="display: none;">
                            <h3 class="text-center mb-4">Step 3.5: Choose Your Topic</h3>
                            
                            <!-- Input fields for specific sources -->
                            <div id="sourceInputs" class="mb-4" style="display: none;">
                                <!-- Books input -->
                                <div id="booksInput" class="source-input" style="display: none;">
                                    <div class="row">
                                        <div class="col-md-6 mb-3">
                                            <label class="form-label">Book Title</label>
                                            <input type="text" class="form-control" id="bookTitle" placeholder="Enter book title...">
                                        </div>
                                        <div class="col-md-6 mb-3">
                                            <label class="form-label">Author</label>
                                            <input type="text" class="form-control" id="bookAuthor" placeholder="Enter author name...">
                                        </div>
                                    </div>
                                    <button type="button" class="btn btn-outline-primary" onclick="loadBookTopics()">
                                        <i class="fas fa-search me-2"></i>Find Topics
                                    </button>
                                </div>
                                
                                <!-- Podcast input -->
                                <div id="podcastInput" class="source-input" style="display: none;">
                                    <div class="mb-3">
                                        <label class="form-label">Podcast Link</label>
                                        <input type="url" class="form-control" id="podcastLink" placeholder="Enter podcast URL...">
                                    </div>
                                    <button type="button" class="btn btn-outline-primary" onclick="loadPodcastTopics()">
                                        <i class="fas fa-search me-2"></i>Find Topics
                                    </button>
                                </div>
                                
                                <!-- Video input -->
                                <div id="videoInput" class="source-input" style="display: none;">
                                    <div class="mb-3">
                                        <label class="form-label">YouTube Video Link</label>
                                        <input type="url" class="form-control" id="videoLink" placeholder="Enter YouTube video URL...">
                                    </div>
                                    <button type="button" class="btn btn-outline-primary" onclick="loadVideoTopics()">
                                        <i class="fas fa-search me-2"></i>Find Topics
                                    </button>
                                </div>
                                
                                <!-- Research paper input -->
                                <div id="researchInput" class="source-input" style="display: none;">
                                    <div class="mb-3">
                                        <label class="form-label">Research Paper (PDF)</label>
                                        <input type="file" class="form-control" id="researchFile" accept=".pdf">
                                    </div>
                                    <button type="button" class="btn btn-outline-primary" onclick="loadResearchTopics()">
                                        <i class="fas fa-upload me-2"></i>Upload & Find Topics
                                    </button>
                                </div>
                            </div>
                            
                            <!-- Topic choices -->
                            <div id="topicChoices" class="mb-4" style="display: none;">
                                <div class="d-flex justify-content-between align-items-center mb-3">
                                    <h5 id="topicTitle">Available Topics</h5>
                                    <button type="button" class="btn btn-outline-secondary btn-sm" onclick="refreshTopics()">
                                        <i class="fas fa-sync-alt me-1"></i>Refresh
                                    </button>
                                </div>
                                <div class="row" id="topicsGrid">
                                    <!-- Topics will be loaded here dynamically -->
                                </div>
                            </div>
                            
                            <div class="text-center mt-4">
                                <button type="button" class="btn btn-secondary btn-lg me-3" onclick="prevStep()">
                                    <i class="fas fa-arrow-left me-2"></i>Previous
                                </button>
                                <button type="button" class="btn btn-primary btn-lg" onclick="nextStep()" id="nextStepBtn" disabled>
                                    Next Step <i class="fas fa-arrow-right ms-2"></i>
                                </button>
                            </div>
                        </div>
                        
                        <!-- Step 4: Tone -->
                        <div id="step4" class="step-content" style="display: none;">
                            <h3 class="text-center mb-4">Step 4: How Should It Sound?</h3>
                            <div class="row">
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-tone="professional">
                                        <i class="fas fa-user-tie"></i>
                                        <div>Professional</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-tone="casual">
                                        <i class="fas fa-smile"></i>
                                        <div>Casual</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-tone="inspirational">
                                        <i class="fas fa-star"></i>
                                        <div>Inspirational</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-tone="educational">
                                        <i class="fas fa-lightbulb"></i>
                                        <div>Educational</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-tone="humorous">
                                        <i class="fas fa-laugh"></i>
                                        <div>Humorous</div>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-6 mb-3">
                                    <div class="direction-card" data-tone="serious">
                                        <i class="fas fa-exclamation-triangle"></i>
                                        <div>Serious</div>
                                    </div>
                                </div>
                            </div>
                            <div class="text-center mt-4">
                                <button type="button" class="btn btn-secondary btn-lg me-3" onclick="prevStep()">
                                    <i class="fas fa-arrow-left me-2"></i>Previous
                                </button>
                                <button type="submit" class="btn btn-primary btn-lg">
                                    <i class="fas fa-magic me-2"></i>Generate Content
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
    });
});

// Platform card selection
document.querySelectorAll('[data-platform]').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('[data-platform]').forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
        selectedPlatform = this.dataset.platform;
        document.getElementById('selectedPlatform').value = selectedPlatform;
    });
});

// Source card selection
document.querySelectorAll('[data-source]').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('[data-source]').forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
        selectedSource = this.dataset.source;
        document.getElementById('selectedSource').value = selectedSource;
    });
});

// Tone card selection
document.querySelectorAll('[data-tone]').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('[data-tone]').forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
        selectedTone = this.dataset.tone;
        document.getElementById('selectedTone').value = selectedTone;
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
    
    if (currentStep < 4) {
        document.getElementById('step' + currentStep).style.display = 'none';
        currentStep++;
        document.getElementById('step' + currentStep).style.display = 'block';
        updateStepProgress();
    }
}

function prevStep() {
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
        if (currentStep === 3.5 && index === 3) {
            step.classList.add('active');
        } else if (index + 1 < currentStep || (currentStep === 3.5 && index < 3)) {
            step.classList.add('completed');
        } else if (index + 1 === currentStep) {
            step.classList.add('active');
        }
    });
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
        
        document.getElementById('generatedContent').innerHTML = `
            <div class="alert alert-success">
                <h5>Generated Content for ${selectedDirection} - ${selectedPlatform}</h5>
                <p><strong>Topic:</strong> ${selectedTopicText}</p>
                <p><strong>Source:</strong> ${selectedSource}</p>
                <p><strong>Tone:</strong> ${selectedTone}</p>
                <p>This is a sample generated content based on your selections. In the full implementation, this would be AI-generated content from the selected source with the chosen tone.</p>
            </div>
        `;
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
                    <h2 class="mb-2">Welcome back, <span class="user-name">User</span>!</h2>
                    <p class="mb-0">Your focus: <strong>Business & Finance</strong></p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Quick Stats -->
    <div class="row mb-4">
        <div class="col-12">
            <h4 class="mb-3"><i class="fas fa-chart-bar me-2"></i>Quick Stats</h4>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card text-center">
                <div class="card-body">
                    <i class="fas fa-file-alt fa-2x text-primary mb-2"></i>
                    <h3 class="mb-1">45</h3>
                    <p class="text-muted mb-0">Content Generated</p>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card text-center">
                <div class="card-body">
                    <i class="fas fa-calendar fa-2x text-success mb-2"></i>
                    <h3 class="mb-1">12</h3>
                    <p class="text-muted mb-0">This Month</p>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card text-center">
                <div class="card-body">
                    <i class="fas fa-folder fa-2x text-warning mb-2"></i>
                    <h3 class="mb-1">23</h3>
                    <p class="text-muted mb-0">Library Items</p>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card text-center">
                <div class="card-body">
                    <i class="fas fa-share-alt fa-2x text-info mb-2"></i>
                    <h3 class="mb-1">18</h3>
                    <p class="text-muted mb-0">Social Posts</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Quick Actions -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-bolt me-2"></i>Quick Actions</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-2 col-6 mb-2">
                            <a href="/generator" class="btn btn-primary w-100">
                                <i class="fas fa-plus-circle me-1"></i>Generate New Content
                            </a>
                        </div>
                        <div class="col-md-2 col-6 mb-2">
                            <a href="/library" class="btn btn-outline-primary w-100">
                                <i class="fas fa-folder me-1"></i>View Library
                            </a>
                        </div>
                        <div class="col-md-2 col-6 mb-2">
                            <a href="#" class="btn btn-outline-success w-100">
                                <i class="fas fa-share-alt me-1"></i>Social Media
                            </a>
                        </div>
                        <div class="col-md-2 col-6 mb-2">
                            <a href="/settings" class="btn btn-outline-secondary w-100">
                                <i class="fas fa-cog me-1"></i>Settings
                            </a>
                        </div>
                        <div class="col-md-2 col-6 mb-2">
                            <a href="#" class="btn btn-outline-info w-100">
                                <i class="fas fa-chart-line me-1"></i>Analytics
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
                    <h5 class="mb-0"><i class="fas fa-clock me-2"></i>Recent Content by Direction</h5>
                </div>
                <div class="card-body">
                    <div class="d-flex align-items-center mb-3">
                        <i class="fas fa-briefcase text-primary me-3"></i>
                        <div class="flex-grow-1">
                            <strong>Business: LinkedIn Post</strong>
                            <br><small class="text-muted">2 hours ago</small>
                        </div>
                        <span class="badge bg-primary">LinkedIn</span>
                    </div>
                    <div class="d-flex align-items-center mb-3">
                        <i class="fas fa-briefcase text-primary me-3"></i>
                        <div class="flex-grow-1">
                            <strong>Business: Twitter Thread</strong>
                            <br><small class="text-muted">1 day ago</small>
                        </div>
                        <span class="badge bg-info">Twitter</span>
                    </div>
                    <div class="d-flex align-items-center mb-3">
                        <i class="fas fa-microchip text-success me-3"></i>
                        <div class="flex-grow-1">
                            <strong>Tech: Instagram Post</strong>
                            <br><small class="text-muted">3 days ago</small>
                        </div>
                        <span class="badge bg-success">Instagram</span>
                    </div>
                    <div class="d-flex align-items-center">
                        <i class="fas fa-briefcase text-primary me-3"></i>
                        <div class="flex-grow-1">
                            <strong>Business: Blog Article</strong>
                            <br><small class="text-muted">1 week ago</small>
                        </div>
                        <span class="badge bg-warning">Blog</span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Social Media Performance -->
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-chart-pie me-2"></i>Social Media Performance</h5>
                </div>
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <i class="fab fa-linkedin text-primary me-2"></i>
                            <strong>LinkedIn</strong>
                        </div>
                        <div class="text-end">
                            <div>156 views, 23 likes</div>
                            <small class="text-muted">45 posts</small>
                        </div>
                    </div>
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <i class="fab fa-twitter text-info me-2"></i>
                            <strong>Twitter</strong>
                        </div>
                        <div class="text-end">
                            <div>89 retweets, 45 likes</div>
                            <small class="text-muted">23 posts</small>
                        </div>
                    </div>
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <i class="fab fa-instagram text-danger me-2"></i>
                            <strong>Instagram</strong>
                        </div>
                        <div class="text-end">
                            <div>234 views, 67 likes</div>
                            <small class="text-muted">34 posts</small>
                        </div>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <i class="fab fa-facebook text-primary me-2"></i>
                            <strong>Facebook</strong>
                        </div>
                        <div class="text-end">
                            <div>567 views, 89 likes</div>
                            <small class="text-muted">12 posts</small>
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
                    <h5 class="mb-0"><i class="fas fa-chart-bar me-2"></i>Content Performance by Direction</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-3 mb-3">
                            <div class="d-flex align-items-center">
                                <i class="fas fa-briefcase text-primary me-2"></i>
                                <div class="flex-grow-1">
                                    <strong>Business</strong>
                                    <br><small class="text-muted">23 posts, 1,234 total views</small>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="d-flex align-items-center">
                                <i class="fas fa-microchip text-success me-2"></i>
                                <div class="flex-grow-1">
                                    <strong>Technology</strong>
                                    <br><small class="text-muted">12 posts, 567 total views</small>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="d-flex align-items-center">
                                <i class="fas fa-heart text-danger me-2"></i>
                                <div class="flex-grow-1">
                                    <strong>Health</strong>
                                    <br><small class="text-muted">8 posts, 345 total views</small>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="d-flex align-items-center">
                                <i class="fas fa-graduation-cap text-warning me-2"></i>
                                <div class="flex-grow-1">
                                    <strong>Education</strong>
                                    <br><small class="text-muted">5 posts, 234 total views</small>
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
                <i class="fas fa-folder me-2 text-primary"></i>Content Library
            </h1>
        </div>
    </div>
    
    <!-- Direction Filters -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-filter me-2"></i>Direction Filters</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-primary w-100 direction-filter active" data-direction="all">
                                <i class="fas fa-th me-1"></i>All
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-primary w-100 direction-filter" data-direction="business">
                                <i class="fas fa-briefcase me-1"></i>Business
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-success w-100 direction-filter" data-direction="technology">
                                <i class="fas fa-microchip me-1"></i>Tech
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-danger w-100 direction-filter" data-direction="health">
                                <i class="fas fa-heart me-1"></i>Health
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-warning w-100 direction-filter" data-direction="education">
                                <i class="fas fa-graduation-cap me-1"></i>Education
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-info w-100 direction-filter" data-direction="entertainment">
                                <i class="fas fa-film me-1"></i>Entertainment
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
                    <h5 class="mb-0"><i class="fas fa-share-alt me-2"></i>Platform Filters</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-secondary w-100 platform-filter active" data-platform="all">
                                <i class="fas fa-th me-1"></i>All
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-primary w-100 platform-filter" data-platform="linkedin">
                                <i class="fab fa-linkedin me-1"></i>LinkedIn
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-primary w-100 platform-filter" data-platform="facebook">
                                <i class="fab fa-facebook me-1"></i>Facebook
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-danger w-100 platform-filter" data-platform="instagram">
                                <i class="fab fa-instagram me-1"></i>Instagram
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-info w-100 platform-filter" data-platform="twitter">
                                <i class="fab fa-twitter me-1"></i>Twitter
                            </button>
                        </div>
                        <div class="col-md-2 col-4 mb-2">
                            <button class="btn btn-outline-warning w-100 platform-filter" data-platform="blog">
                                <i class="fas fa-blog me-1"></i>Blog
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
                <input type="text" class="form-control" placeholder="Search content..." id="searchInput">
                <button class="btn btn-outline-secondary" type="button">
                    <i class="fas fa-search"></i>
                </button>
            </div>
        </div>
        <div class="col-md-4 text-end">
            <button class="btn btn-outline-secondary me-2">
                <i class="fas fa-filter me-1"></i>Advanced Search
            </button>
            <a href="/generator" class="btn btn-primary">
                <i class="fas fa-plus me-1"></i>Create New
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
                        <span class="badge bg-primary">LinkedIn</span>
                        <small class="text-muted">2 days ago</small>
                    </div>
                    <div class="d-flex align-items-center mb-2">
                        <i class="fas fa-briefcase text-primary me-2"></i>
                        <h6 class="mb-0">Business Strategy Insights</h6>
                    </div>
                    <p class="text-muted small">Key insights for modern business leaders looking to scale their operations and drive sustainable growth in today's competitive market...</p>
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
        
        <!-- Business Facebook Post -->
        <div class="col-md-4 mb-4 content-item" data-direction="business" data-platform="facebook">
            <div class="card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="badge bg-primary">Facebook</span>
                        <small class="text-muted">1 week ago</small>
                    </div>
                    <div class="d-flex align-items-center mb-2">
                        <i class="fas fa-briefcase text-primary me-2"></i>
                        <h6 class="mb-0">Market Analysis Report</h6>
                    </div>
                    <p class="text-muted small">Comprehensive analysis of current market trends and their implications for business strategy and investment decisions...</p>
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
        
        <!-- Tech Instagram Post -->
        <div class="col-md-4 mb-4 content-item" data-direction="technology" data-platform="instagram">
            <div class="card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="badge bg-success">Instagram</span>
                        <small class="text-muted">3 days ago</small>
                    </div>
                    <div class="d-flex align-items-center mb-2">
                        <i class="fas fa-microchip text-success me-2"></i>
                        <h6 class="mb-0">AI Innovation Trends</h6>
                    </div>
                    <p class="text-muted small">Exploring the latest developments in artificial intelligence and their transformative impact on various industries...</p>
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
        
        <!-- Tech Twitter Post -->
        <div class="col-md-4 mb-4 content-item" data-direction="technology" data-platform="twitter">
            <div class="card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="badge bg-info">Twitter</span>
                        <small class="text-muted">5 days ago</small>
                    </div>
                    <div class="d-flex align-items-center mb-2">
                        <i class="fas fa-microchip text-success me-2"></i>
                        <h6 class="mb-0">Tech Tips Thread</h6>
                    </div>
                    <p class="text-muted small">Essential productivity tips and tools for developers and tech professionals to streamline their workflow...</p>
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
        
        <!-- Health Blog Article -->
        <div class="col-md-4 mb-4 content-item" data-direction="health" data-platform="blog">
            <div class="card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="badge bg-warning">Blog</span>
                        <small class="text-muted">2 weeks ago</small>
                    </div>
                    <div class="d-flex align-items-center mb-2">
                        <i class="fas fa-heart text-danger me-2"></i>
                        <h6 class="mb-0">Wellness Guide</h6>
                    </div>
                    <p class="text-muted small">Comprehensive guide to maintaining mental and physical health in the modern digital age with practical tips...</p>
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
        
        <!-- Education LinkedIn Post -->
        <div class="col-md-4 mb-4 content-item" data-direction="education" data-platform="linkedin">
            <div class="card h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <span class="badge bg-primary">LinkedIn</span>
                        <small class="text-muted">1 month ago</small>
                    </div>
                    <div class="d-flex align-items-center mb-2">
                        <i class="fas fa-graduation-cap text-warning me-2"></i>
                        <h6 class="mb-0">Learning Strategies</h6>
                    </div>
                    <p class="text-muted small">Effective learning strategies and techniques for professionals looking to upskill and stay competitive...</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">Education</small>
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
                <i class="fas fa-cog me-2 text-primary"></i>Settings
            </h1>
        </div>
    </div>
    
    <div class="row">
        <div class="col-lg-8">
            <!-- Profile Settings -->
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-user me-2"></i>Profile</h5>
                </div>
                <div class="card-body">
                    <form id="profileForm">
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
                                <label class="form-label">Company</label>
                                <input type="text" class="form-control" value="Content Creator Pro" id="userCompany">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Industry</label>
                                <select class="form-select" id="userIndustry">
                                    <option value="technology">Technology</option>
                                    <option value="finance">Finance</option>
                                    <option value="healthcare">Healthcare</option>
                                    <option value="education">Education</option>
                                    <option value="marketing">Marketing</option>
                                    <option value="consulting">Consulting</option>
                                    <option value="other">Other</option>
                                </select>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Region</label>
                                <select class="form-select" id="userRegion">
                                    <option value="global">Global</option>
                                    <option value="us">United States</option>
                                    <option value="eu">Europe</option>
                                    <option value="asia">Asia</option>
                                    <option value="latin_america">Latin America</option>
                                    <option value="africa">Africa</option>
                                    <option value="oceania">Oceania</option>
                                </select>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Language</label>
                                <select class="form-select" id="userLanguage">
                                    <option value="en">English</option>
                                    <option value="zh">中文</option>
                                    <option value="es">Spanish</option>
                                    <option value="fr">French</option>
                                    <option value="de">German</option>
                                    <option value="ja">Japanese</option>
                                    <option value="ko">Korean</option>
                                </select>
                            </div>
                        </div>
                        <div class="text-end">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save me-2"></i>Save Profile
                            </button>
                        </div>
                    </form>
                </div>
            </div>
            
            <!-- Content Preferences -->
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-magic me-2"></i>Content Preferences</h5>
                </div>
                <div class="card-body">
                    <form id="contentForm">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Primary Direction</label>
                                <select class="form-select" id="primaryDirection">
                                    <option value="business_finance">Business & Finance</option>
                                    <option value="technology">Technology</option>
                                    <option value="health_wellness">Health & Wellness</option>
                                    <option value="education">Education</option>
                                    <option value="entertainment">Entertainment</option>
                                    <option value="travel_tourism">Travel & Tourism</option>
                                    <option value="food_cooking">Food & Cooking</option>
                                    <option value="fashion_beauty">Fashion & Beauty</option>
                                </select>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Default Tone</label>
                                <select class="form-select" id="defaultTone">
                                    <option value="professional">Professional</option>
                                    <option value="casual">Casual</option>
                                    <option value="inspirational">Inspirational</option>
                                    <option value="educational">Educational</option>
                                    <option value="humorous">Humorous</option>
                                    <option value="serious">Serious</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Secondary Directions</label>
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="technology" id="secTech" checked>
                                        <label class="form-check-label" for="secTech">Technology</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="health_wellness" id="secHealth">
                                        <label class="form-check-label" for="secHealth">Health & Wellness</label>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="education" id="secEducation">
                                        <label class="form-check-label" for="secEducation">Education</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="entertainment" id="secEntertainment">
                                        <label class="form-check-label" for="secEntertainment">Entertainment</label>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="travel_tourism" id="secTravel">
                                        <label class="form-check-label" for="secTravel">Travel & Tourism</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="food_cooking" id="secFood">
                                        <label class="form-check-label" for="secFood">Food & Cooking</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Preferred Content Types</label>
                            <div class="row">
                                <div class="col-md-3">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="linkedin" id="prefLinkedIn" checked>
                                        <label class="form-check-label" for="prefLinkedIn">LinkedIn</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="twitter" id="prefTwitter" checked>
                                        <label class="form-check-label" for="prefTwitter">Twitter</label>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="facebook" id="prefFacebook">
                                        <label class="form-check-label" for="prefFacebook">Facebook</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="instagram" id="prefInstagram">
                                        <label class="form-check-label" for="prefInstagram">Instagram</label>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="youtube" id="prefYouTube">
                                        <label class="form-check-label" for="prefYouTube">YouTube</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="blog" id="prefBlog">
                                        <label class="form-check-label" for="prefBlog">Blog</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Favorite Sources</label>
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="news" id="sourceNews" checked>
                                        <label class="form-check-label" for="sourceNews">News</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="books" id="sourceBooks" checked>
                                        <label class="form-check-label" for="sourceBooks">Books</label>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="research" id="sourceResearch">
                                        <label class="form-check-label" for="sourceResearch">Research</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="podcasts" id="sourcePodcasts">
                                        <label class="form-check-label" for="sourcePodcasts">Podcasts</label>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="videos" id="sourceVideos">
                                        <label class="form-check-label" for="sourceVideos">Videos</label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="threads" id="sourceThreads">
                                        <label class="form-check-label" for="sourceThreads">Threads</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="text-end">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save me-2"></i>Save Preferences
                            </button>
                        </div>
                    </form>
                </div>
            </div>
            
            <!-- Social Media Integration -->
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-share-alt me-2"></i>Social Media Integration</h5>
                </div>
                <div class="card-body">
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <div class="d-flex align-items-center mb-2">
                                <i class="fab fa-linkedin text-primary me-2"></i>
                                <span class="me-2">LinkedIn</span>
                                <span class="badge bg-success">Connected</span>
                            </div>
                            <small class="text-muted">John Doe (Personal)</small>
                        </div>
                        <div class="col-md-6 text-end">
                            <button class="btn btn-sm btn-outline-primary">Manage</button>
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <div class="d-flex align-items-center mb-2">
                                <i class="fab fa-facebook text-primary me-2"></i>
                                <span class="me-2">Facebook</span>
                                <span class="badge bg-success">Connected</span>
                            </div>
                            <small class="text-muted">John Doe</small>
                        </div>
                        <div class="col-md-6 text-end">
                            <button class="btn btn-sm btn-outline-primary">Manage</button>
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <div class="d-flex align-items-center mb-2">
                                <i class="fab fa-instagram text-danger me-2"></i>
                                <span class="me-2">Instagram</span>
                                <span class="badge bg-success">Connected</span>
                            </div>
                            <small class="text-muted">@johndoe</small>
                        </div>
                        <div class="col-md-6 text-end">
                            <button class="btn btn-sm btn-outline-primary">Manage</button>
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <div class="d-flex align-items-center mb-2">
                                <i class="fab fa-twitter text-info me-2"></i>
                                <span class="me-2">Twitter</span>
                                <span class="badge bg-secondary">Not connected</span>
                            </div>
                            <small class="text-muted">Connect your Twitter account</small>
                        </div>
                        <div class="col-md-6 text-end">
                            <button class="btn btn-sm btn-primary">Connect</button>
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <div class="d-flex align-items-center mb-2">
                                <i class="fab fa-youtube text-danger me-2"></i>
                                <span class="me-2">YouTube</span>
                                <span class="badge bg-secondary">Not connected</span>
                            </div>
                            <small class="text-muted">Connect your YouTube channel</small>
                        </div>
                        <div class="col-md-6 text-end">
                            <button class="btn btn-sm btn-primary">Connect</button>
                        </div>
                    </div>
                    
                    <hr>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <label class="form-label">Auto-post to</label>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="linkedin" id="autoLinkedIn" checked>
                                <label class="form-check-label" for="autoLinkedIn">LinkedIn</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="facebook" id="autoFacebook">
                                <label class="form-check-label" for="autoFacebook">Facebook</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="instagram" id="autoInstagram">
                                <label class="form-check-label" for="autoInstagram">Instagram</label>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Default posting time</label>
                            <input type="time" class="form-control" value="09:00" id="defaultPostTime">
                            <small class="text-muted">Local timezone</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Subscription Sidebar -->
        <div class="col-lg-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-crown me-2"></i>Subscription</h5>
                </div>
                <div class="card-body">
                    <div class="text-center mb-3">
                        <i class="fas fa-crown fa-3x text-warning mb-2"></i>
                        <h5>Pro Plan</h5>
                        <h3 class="text-primary">$19/month</h3>
                    </div>
                    
                    <div class="mb-3">
                        <div class="d-flex justify-content-between mb-2">
                            <span>Content Generated</span>
                            <span>67/100</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar" style="width: 67%"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-2">
                            <span>Social Media Posts</span>
                            <span>23/50</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar" style="width: 46%"></div>
                        </div>
                    </div>
                    
                    <div class="d-grid gap-2">
                        <button class="btn btn-warning">
                            <i class="fas fa-arrow-up me-2"></i>Upgrade Plan
                        </button>
                        <button class="btn btn-outline-danger">
                            <i class="fas fa-times me-2"></i>Cancel Subscription
                        </button>
                    </div>
                    
                    <hr>
                    
                    <h6>Pro Features</h6>
                    <ul class="list-unstyled">
                        <li><i class="fas fa-check text-success me-2"></i>Unlimited content generation</li>
                        <li><i class="fas fa-check text-success me-2"></i>Advanced AI models</li>
                        <li><i class="fas fa-check text-success me-2"></i>Social media scheduling</li>
                        <li><i class="fas fa-check text-success me-2"></i>Analytics dashboard</li>
                        <li><i class="fas fa-check text-success me-2"></i>Priority support</li>
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
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body p-4">
                        <h2 class="text-center mb-4"><i class="fas fa-user-plus me-2"></i>Register</h2>
                        <form method="post">
                            <div class="mb-3">
                                <label class="form-label">Email</label>
                                <input type="email" name="email" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Password</label>
                                <input type="password" name="password" class="form-control" required>
                            </div>
                            <div class="d-grid">
                                <button type="submit" class="btn btn-primary btn-lg">
                                    <i class="fas fa-user-plus me-2"></i>Register
                                </button>
                            </div>
                        </form>
                        <div class="text-center mt-3">
                            <p>Already have an account? <a href="/login" class="text-decoration-none">Login here</a></p>
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
                        <h2 class="text-center mb-4"><i class="fas fa-sign-in-alt me-2"></i>Login</h2>
                        <form method="post">
                            <div class="mb-3">
                                <label class="form-label">Email</label>
                                <input type="email" name="email" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Password</label>
                                <input type="password" name="password" class="form-control" required>
                            </div>
                            <div class="d-grid">
                                <button type="submit" class="btn btn-primary btn-lg">
                                    <i class="fas fa-sign-in-alt me-2"></i>Login
                                </button>
                            </div>
                        </form>
                        <div class="text-center mt-3">
                            <p>Don't have an account? <a href="/register" class="text-decoration-none">Register here</a></p>
                        </div>
                        <div class="mt-4 p-3 bg-light rounded">
                            <h6 class="text-center mb-2">Demo Credentials:</h6>
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