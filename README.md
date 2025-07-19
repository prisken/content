# Content Creator Pro

AI-powered content generation platform for social media and marketing.

## 🚀 Deployment Status

**Last Updated**: $(date)
**Status**: Ready for deployment

## 🚀 Features

### Core Features
- **Direction-Based Content Generation**: 18 content directions/niches (Business, Technology, Health, etc.)
- **Multi-Platform Support**: LinkedIn, Facebook, Instagram, Twitter, YouTube Shorts, Blog Articles
- **AI-Powered Generation**: DeepSeek AI integration for high-quality content
- **Regional Adaptation**: Localized content with cultural sensitivity
- **Content Editing**: Rich text editor with version history
- **Social Media Integration**: Direct posting to multiple platforms
- **Quick Start Templates**: Pre-configured content generation workflows
- **User Management**: Admin panel for user management and role-based access

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
- **Database**: SQLAlchemy with PostgreSQL (production)
- **AI Services**: DeepSeek API, Stable Diffusion, Runway
- **Authentication**: JWT-based authentication
- **API**: RESTful API with JSON responses
- **Deployment**: Railway

### Frontend
- **Framework**: Next.js (React)
- **Styling**: Tailwind CSS
- **State Management**: React Context
- **Deployment**: Vercel

### AI Integration
- **Text Generation**: DeepSeek API
- **Image Generation**: Stable Diffusion
- **Video Generation**: Runway API

## 🚀 Quick Start

### Option 1: Deploy to Production (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd content-creation
   ```

2. **Run automated deployment**:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **Follow the prompts** to deploy to Vercel and Railway.

### Option 2: Local Development

#### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- Git

#### Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp env.example .env
# Edit .env with your configuration

# Initialize database
flask init-db

# Run backend
python run.py
```

#### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment
cp env.production.example .env.local
# Edit .env.local with your backend URL

# Run frontend
npm run dev
```

## 🌐 Deployment

### Production Deployment
- **Frontend**: Deployed on Vercel
- **Backend**: Deployed on Railway
- **Database**: PostgreSQL (Railway)

### Environment Variables

#### Backend (Railway)
```env
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://...
CORS_ORIGINS=https://your-app.vercel.app
JWT_SECRET_KEY=your-jwt-secret
```

#### Frontend (Vercel)
```env
BACKEND_URL=https://your-railway-app.railway.app
NEXT_PUBLIC_APP_NAME=Content Creator Pro
```

For detailed deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md).

## 📁 Project Structure

```
content-creation/
├── app/                         # Flask backend
│   ├── __init__.py
│   ├── models/                  # Database models
│   ├── routes/                  # API routes
│   ├── services/                # Business logic
│   └── utils/                   # Utilities
├── frontend/                    # Next.js frontend
│   ├── components/              # React components
│   ├── pages/                   # Next.js pages
│   ├── contexts/                # React contexts
│   ├── lib/                     # Utilities
│   └── styles/                  # CSS styles
├── config/                      # Configuration files
├── docs/                        # Documentation
├── tests/                       # Test files
├── requirements.txt             # Python dependencies
├── run.py                      # Flask entry point
├── deploy.sh                   # Deployment script
├── railway.json                # Railway configuration
├── vercel.json                 # Vercel configuration
└── README.md                   # This file
```

## 🔧 Configuration

### Development vs Production
- **Development**: Uses SQLite database, debug mode enabled
- **Production**: Uses PostgreSQL, optimized for performance

### Database Configuration
```python
# Development (SQLite)
SQLALCHEMY_DATABASE_URI = 'sqlite:///content_creator_dev.db'

# Production (PostgreSQL)
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@host/dbname'
```

## 🧪 Testing

### Backend Tests
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_api.py
```

### Frontend Tests
```bash
cd frontend
npm test
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
- `DELETE /api/content/<id>` - Delete content

### Admin Endpoints
- `GET /api/admin/users` - List all users
- `PUT /api/admin/users/<id>` - Update user
- `DELETE /api/admin/users/<id>` - Delete user
- `POST /api/admin/users/<id>/toggle-status` - Toggle user status

## 🔐 Security

- JWT-based authentication
- Role-based access control
- CORS protection
- Environment variable protection
- HTTPS enforcement in production

## 📊 Monitoring

- **Health Checks**: `/health` endpoint for Railway
- **Logs**: Available in Railway and Vercel dashboards
- **Analytics**: Built-in Vercel analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Issues**: Create an issue in the GitHub repository
- **Email**: support@contentcreatorpro.com

---

**Built with ❤️ for content creators worldwide** 