# Content Creator Pro

An AI-powered content creation platform designed for professionals, businesses, and content creators. Generate engaging social media content, blog articles, and more with intelligent direction-based content generation and regional adaptation.

## 🚀 Features

### Core Features
- **Direction-Based Content Generation**: 18 content directions/niches (Business, Technology, Health, etc.)
- **Multi-Platform Support**: LinkedIn, Facebook, Instagram, Twitter, YouTube Shorts, Blog Articles
- **AI-Powered Generation**: DeepSeek AI integration for high-quality content
- **Regional Adaptation**: Localized content with cultural sensitivity
- **Content Editing**: Rich text editor with version history
- **Social Media Integration**: Direct posting to multiple platforms
- **Quick Start Templates**: Pre-configured content generation workflows

### Content Directions
- Business & Finance
- Technology
- Health & Wellness
- Education
- Entertainment
- Travel & Tourism
- Food & Cooking
- Fashion & Beauty
- Sports & Fitness
- Science & Research
- Politics & Current Events
- Environment & Sustainability
- Personal Development
- Parenting & Family
- Art & Creativity
- Real Estate
- Automotive
- Pet Care

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLAlchemy with SQLite/PostgreSQL
- **AI Services**: DeepSeek API, Stable Diffusion, Runway
- **Authentication**: JWT-based authentication
- **API**: RESTful API with JSON responses

### Frontend
- **Framework**: Bootstrap 5
- **JavaScript**: jQuery with custom modules
- **Styling**: Custom CSS with modern design
- **Icons**: Font Awesome 6

### AI Integration
- **Text Generation**: DeepSeek API
- **Image Generation**: Stable Diffusion
- **Video Generation**: Runway API

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd content-creation
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database Configuration
DATABASE_URL=sqlite:///content_creator_dev.db

# AI Services Configuration
DEEPSEEK_API_KEY=your-deepseek-api-key
DEEPSEEK_API_BASE=https://api.deepseek.com

# Social Media APIs (Optional)
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret
TWITTER_API_KEY=your-twitter-api-key
TWITTER_API_SECRET=your-twitter-api-secret
```

### 5. Initialize Database
```bash
flask init-db
```

### 6. Run the Application
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
content-creation/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models/                  # Database models
│   │   ├── user.py
│   │   ├── content.py
│   │   ├── social_media.py
│   │   └── content_direction.py
│   ├── routes/                  # API routes
│   │   ├── main.py
│   │   ├── api.py
│   │   └── auth.py
│   ├── services/                # Business logic
│   │   ├── content_generator.py
│   │   └── direction_manager.py
│   ├── static/                  # Static files
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/               # HTML templates
│       ├── base.html
│       └── generator.html
├── config/                      # Configuration files
│   ├── development.py
│   ├── production.py
│   └── testing.py
├── docs/                        # Documentation
├── tests/                       # Test files
├── requirements.txt             # Python dependencies
├── run.py                      # Application entry point
└── README.md                   # This file
```

## 🔧 Configuration

### Development Configuration
The application uses different configuration files based on the environment:

- **Development**: `config/development.py`
- **Production**: `config/production.py`
- **Testing**: `config/testing.py`

### Database Configuration
The application supports both SQLite (development) and PostgreSQL (production):

```python
# Development (SQLite)
SQLALCHEMY_DATABASE_URI = 'sqlite:///content_creator_dev.db'

# Production (PostgreSQL)
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/dbname'
```

## 🧪 Testing

Run the test suite:
```bash
flask test
```

Or run with pytest directly:
```bash
pytest tests/
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/profile` - Get user profile
- `PUT /auth/preferences` - Update user preferences

### Content Generation Endpoints
- `POST /api/generate` - Generate content
- `PUT /api/content/<id>` - Update content
- `GET /api/content/<id>/versions` - Get content versions
- `POST /api/content/<id>/revert` - Revert to previous version
- `POST /api/content/<id>/validate` - Validate content

### Direction Management Endpoints
- `GET /api/directions` - Get all content directions
- `GET /api/directions/<key>/sources` - Get direction sources
- `GET /api/directions/<key>/topics` - Get direction topics

## 🎯 Usage Examples

### Content Generation Workflow

1. **Select Content Direction**: Choose from 18 available directions
2. **Choose Content Type**: LinkedIn, Facebook, Instagram, Twitter, YouTube Shorts, or Blog
3. **Select Information Source**: News, Books, Threads, Podcasts, Videos, or Research
4. **Choose Tone**: Professional, Casual, Inspirational, Educational, Humorous, or Serious
5. **Generate Content**: AI-powered content generation with regional adaptation
6. **Edit & Customize**: Use the rich text editor to modify content
7. **Save & Share**: Save to library or post directly to social media

### Quick Start Templates

The platform includes pre-configured templates for common use cases:
- Business News → LinkedIn Post
- Tech Trends → Twitter Update
- Health Tips → Instagram Caption
- Industry Insights → Blog Article

## 🔒 Security

- JWT-based authentication
- Password hashing
- CSRF protection
- Input validation and sanitization
- Rate limiting (planned)
- API key management

## 🚀 Deployment

### Production Deployment

1. **Set Environment Variables**:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret-key
   export DATABASE_URL=your-production-database-url
   ```

2. **Install Production Dependencies**:
   ```bash
   pip install gunicorn
   ```

3. **Run with Gunicorn**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

### Docker Deployment (Planned)
```bash
docker build -t content-creator-pro .
docker run -p 5000:5000 content-creator-pro
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation in the `docs/` folder

## 🔮 Roadmap

### Phase 1 (Current)
- ✅ Basic content generation
- ✅ Direction-based content creation
- ✅ Regional adaptation
- ✅ Content editing interface

### Phase 2 (Planned)
- 🔄 Social media integration
- 🔄 Advanced AI features
- 🔄 Team collaboration
- 🔄 Analytics dashboard

### Phase 3 (Future)
- 📋 Multi-language support
- 📋 Advanced analytics
- 📋 API marketplace
- 📋 Mobile application

## 🙏 Acknowledgments

- DeepSeek for AI text generation
- Stable Diffusion for image generation
- Runway for video generation
- Bootstrap for UI framework
- Flask community for the web framework

---

**Content Creator Pro** - Empowering creators with AI-driven content generation. 