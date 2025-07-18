# Content Creator Pro - Backend API

This is the backend API for Content Creator Pro, designed to be deployed on Railway.

## Features

- **User Authentication**: Register, login, logout, and profile management
- **Content Generation**: AI-powered content generation with multiple directions and platforms
- **Image Generation**: AI image generation with style selection
- **Content Management**: Save, retrieve, and manage generated content
- **Multi-language Support**: English and Chinese translation
- **Social Media Integration**: Platform-specific content formatting
- **Database Storage**: PostgreSQL database for persistent data
- **File Storage**: Cloudinary integration for image storage

## Tech Stack

- **Framework**: Flask
- **Database**: PostgreSQL (via SQLAlchemy)
- **File Storage**: Cloudinary
- **Background Jobs**: Celery + Redis
- **Deployment**: Railway
- **Image Processing**: Pillow (PIL)

## Setup Instructions

### 1. Railway Deployment

1. **Create Railway Account**: Sign up at [railway.app](https://railway.app)

2. **Deploy from GitHub**:
   - Connect your GitHub repository
   - Select the `backend` folder as the source
   - Railway will automatically detect the Python app

3. **Add PostgreSQL Database**:
   - In Railway dashboard, click "New"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically set the `DATABASE_URL` environment variable

4. **Add Redis** (optional, for background jobs):
   - In Railway dashboard, click "New"
   - Select "Database" → "Redis"
   - Railway will automatically set the `REDIS_URL` environment variable

5. **Configure Environment Variables**:
   - Go to your app's "Variables" tab
   - Add the following variables:
     ```
     SECRET_KEY=your-secure-secret-key
     FLASK_ENV=production
     CLOUDINARY_CLOUD_NAME=your-cloud-name
     CLOUDINARY_API_KEY=your-api-key
     CLOUDINARY_API_SECRET=your-api-secret
     ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
     ```

### 2. Cloudinary Setup

1. **Create Cloudinary Account**: Sign up at [cloudinary.com](https://cloudinary.com)
2. **Get Credentials**: Copy your cloud name, API key, and API secret
3. **Add to Environment Variables**: Add these to your Railway app variables

### 3. Database Migration

The database tables will be created automatically on first request. For manual migration:

```bash
# Connect to Railway shell
railway shell

# Run migrations
flask db upgrade
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/profile` - Get user profile

### Content Management
- `POST /api/content/save` - Save generated content
- `GET /api/content/list` - List user's content
- `GET /api/content/<id>` - Get specific content
- `DELETE /api/content/<id>` - Delete content

### Image Management
- `POST /api/images/generate` - Generate AI image
- `POST /api/images/upload` - Upload image file
- `GET /api/images/list` - List user's images

### API
- `POST /api/generate` - Generate content
- `POST /api/translate` - Translate content
- `GET /api/directions` - Get content directions
- `GET /api/translations` - Get translations
- `GET /health` - Health check

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | Yes |
| `CLOUDINARY_API_KEY` | Cloudinary API key | Yes |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | Yes |
| `REDIS_URL` | Redis connection string | No |
| `ALLOWED_ORIGINS` | CORS allowed origins | Yes |
| `FLASK_ENV` | Flask environment | No |

## Local Development

1. **Clone the repository**:
   ```bash
   git clone <your-repo>
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp env.example .env
   # Edit .env with your values
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

## Deployment Notes

- The app uses `gunicorn` as the WSGI server for production
- Database migrations run automatically on startup
- CORS is configured for frontend integration
- Health check endpoint available at `/health`

## Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Check `DATABASE_URL` environment variable
   - Ensure PostgreSQL is running and accessible

2. **Cloudinary Upload Error**:
   - Verify Cloudinary credentials
   - Check internet connectivity

3. **CORS Error**:
   - Update `ALLOWED_ORIGINS` with your frontend domain
   - Ensure frontend is making requests to correct backend URL

### Logs

View logs in Railway dashboard:
1. Go to your app in Railway
2. Click on "Deployments"
3. Select the latest deployment
4. View logs for debugging

## Support

For issues and questions:
1. Check Railway logs
2. Verify environment variables
3. Test endpoints with Postman or similar tool
4. Contact support with specific error messages 