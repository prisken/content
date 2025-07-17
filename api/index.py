import os
from flask import Flask, render_template_string, jsonify

# Set environment variable to indicate serverless mode
os.environ['VERCEL_ENV'] = 'production'

app = Flask(__name__)

# Improved HTML template for the landing page with better text visibility
LANDING_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Content Creator Pro</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .hero {
            position: relative;
            padding: 100px 0;
            color: #fff;
            z-index: 1;
        }
        .hero::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(30, 30, 30, 0.55);
            z-index: -1;
            border-radius: 20px;
        }
        .feature-card {
            background: #fff;
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            color: #222;
        }
        .btn-primary {
            background: linear-gradient(45deg, #667eea, #764ba2);
            border: none;
            padding: 12px 30px;
            font-weight: bold;
        }
        h1, h3, p, .lead {
            color: #fff !important;
            text-shadow: 0 2px 8px rgba(0,0,0,0.25);
        }
        .feature-card h3, .feature-card p {
            color: #222 !important;
            text-shadow: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero text-center">
            <h1 class="display-4 mb-4">🚀 Content Creator Pro</h1>
            <p class="lead mb-5">AI-Powered Content Generation Platform</p>
            <div class="row">
                <div class="col-md-4">
                    <div class="feature-card">
                        <h3>📝 Multi-Platform Content</h3>
                        <p>Generate content for <b>LinkedIn, Facebook, Instagram, Twitter, YouTube, and blogs</b>.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-card">
                        <h3>🎯 Smart Direction</h3>
                        <p>18 content directions with <b>regional and cultural context</b>.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-card">
                        <h3>🤖 AI-Powered</h3>
                        <p>Advanced AI content generation with <b>tone and style customization</b>.</p>
                    </div>
                </div>
            </div>
            <div class="mt-5">
                <button class="btn btn-primary btn-lg" onclick="showDemo()">Try Demo</button>
            </div>
        </div>
    </div>
    
    <script>
        function showDemo() {
            alert('Demo mode coming soon! This is a serverless deployment.');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main landing page"""
    return render_template_string(LANDING_HTML)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "mode": "serverless",
        "message": "Content Creator Pro is running in serverless mode"
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
    return jsonify({
        'success': True,
        'data': {
            'content': 'This is a demo content generation. Full AI integration coming soon!',
            'message': 'Serverless mode active - AI features will be available in full deployment.'
        }
    })

if __name__ == '__main__':
    app.run(debug=True) 