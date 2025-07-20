# Environment Variables Specification for AI Content Generation System

## Overview
This document specifies all environment variables required for both frontend and backend platforms to implement the AI content generation system according to the design specifications.

---

## 🔧 **Backend Environment Variables**

### **Core Flask Configuration**
```bash
# Flask Configuration
SECRET_KEY=your-secret-key-change-in-production
FLASK_ENV=production
FLASK_APP=app.py
```

### **Database Configuration**
```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database_name
```

### **AI Service Configuration**

#### **DeepSeek AI**
```bash
# DeepSeek AI Configuration
DEEPSEEK_API_KEY=your-deepseek-api-key
DEEPSEEK_API_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_MAX_TOKENS=4096
DEEPSEEK_TEMPERATURE=0.7
```

#### **Stable Diffusion**
```bash
# Stable Diffusion Configuration
STABILITY_API_KEY=your-stability-api-key
STABILITY_API_URL=https://api.stability.ai/v1
SD_MODEL=stable-diffusion-xl-1024-v1-0
SD_STEPS=30
SD_CFG_SCALE=7.0
```

#### **Google APIs**
```bash
# Google APIs Configuration
GOOGLE_CUSTOM_SEARCH_API_KEY=your-google-search-api-key
GOOGLE_CUSTOM_SEARCH_ENGINE_ID=your-search-engine-id
GOOGLE_TRENDS_API_KEY=your-google-trends-api-key
GOOGLE_BOOKS_API_KEY=your-google-books-api-key
GOOGLE_NEWS_RSS_ENABLED=true
```

### **Infrastructure Configuration**

#### **Redis & Celery**
```bash
# Redis Configuration (for Celery)
REDIS_URL=redis://username:password@host:port/database_number
CELERY_BROKER_URL=redis://username:password@host:port/database_number
```

#### **Cloudinary (Image Storage)**
```bash
# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### **Security Configuration**
```bash
# Security Configuration
JWT_SECRET_KEY=your_jwt_secret_key
JWT_ACCESS_TOKEN_EXPIRES=3600
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
```

### **Rate Limiting Configuration**
```bash
# Rate Limiting Configuration
RATE_LIMIT_CONTENT_GENERATION=10
RATE_LIMIT_GOOGLE_SEARCH=100
RATE_LIMIT_IMAGE_GENERATION=20
RATE_LIMIT_WINDOW=3600
```

### **Performance Configuration**
```bash
# Performance Configuration
CACHE_CONFIG_GOOGLE_SEARCH=3600
CACHE_CONFIG_CONTENT_GENERATION=300
CACHE_CONFIG_IMAGE_GENERATION=600
CACHE_CONFIG_ANALYTICS=86400
```

### **Monitoring Configuration**
```bash
# Monitoring Configuration
PROMETHEUS_ENABLED=true
METRICS_ENDPOINT=/metrics
LOG_LEVEL=INFO
```

### **Email Configuration (Optional)**
```bash
# Email Configuration (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### **File Upload Configuration**
```bash
# File Upload Configuration
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
```

---

## 🎨 **Frontend Environment Variables**

### **Core Configuration**
```bash
# Backend Configuration
BACKEND_URL=http://localhost:8000

# Environment
NODE_ENV=development

# Frontend Configuration
NEXT_PUBLIC_APP_NAME=Content Creator Pro
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### **AI Feature Flags**
```bash
# AI Content Generation Configuration
NEXT_PUBLIC_DEEPSEEK_ENABLED=true
NEXT_PUBLIC_STABLE_DIFFUSION_ENABLED=true
NEXT_PUBLIC_GOOGLE_SEARCH_ENABLED=true
```

### **Google APIs Configuration (Frontend)**
```bash
# Google APIs Configuration (Frontend)
NEXT_PUBLIC_GOOGLE_CUSTOM_SEARCH_API_KEY=your_google_search_api_key
NEXT_PUBLIC_GOOGLE_CUSTOM_SEARCH_ENGINE_ID=your_search_engine_id
```

### **Feature Flags**
```bash
# Feature Flags
NEXT_PUBLIC_IMAGE_GENERATION_ENABLED=true
NEXT_PUBLIC_GOOGLE_TRENDS_ENABLED=true
NEXT_PUBLIC_GOOGLE_NEWS_ENABLED=true
NEXT_PUBLIC_GOOGLE_BOOKS_ENABLED=true
```

### **UI Configuration**
```bash
# UI Configuration
NEXT_PUBLIC_MAX_TOPICS_PER_REQUEST=5
NEXT_PUBLIC_MAX_IMAGE_VARIATIONS=4
NEXT_PUBLIC_CONTENT_GENERATION_TIMEOUT=30000
NEXT_PUBLIC_IMAGE_GENERATION_TIMEOUT=60000
```

### **Analytics Configuration**
```bash
# Analytics Configuration
NEXT_PUBLIC_ANALYTICS_ENABLED=true
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=your_google_analytics_id
```

### **Error Reporting**
```bash
# Error Reporting
NEXT_PUBLIC_SENTRY_DSN=your_sentry_dsn
```

---

## 📋 **Complete Environment Setup Checklist**

### **Backend Setup (Railway/Heroku)**
- [ ] **Flask Configuration**: SECRET_KEY, FLASK_ENV, FLASK_APP
- [ ] **Database**: DATABASE_URL (PostgreSQL)
- [ ] **DeepSeek AI**: DEEPSEEK_API_KEY, DEEPSEEK_API_URL, DEEPSEEK_MODEL, DEEPSEEK_MAX_TOKENS, DEEPSEEK_TEMPERATURE
- [ ] **Stable Diffusion**: STABILITY_API_KEY, STABILITY_API_URL, SD_MODEL, SD_STEPS, SD_CFG_SCALE
- [ ] **Google APIs**: GOOGLE_CUSTOM_SEARCH_API_KEY, GOOGLE_CUSTOM_SEARCH_ENGINE_ID, GOOGLE_TRENDS_API_KEY, GOOGLE_BOOKS_API_KEY, GOOGLE_NEWS_RSS_ENABLED
- [ ] **Redis**: REDIS_URL, CELERY_BROKER_URL
- [ ] **Cloudinary**: CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
- [ ] **Security**: JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES, CORS_ORIGINS, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS
- [ ] **Rate Limiting**: RATE_LIMIT_CONTENT_GENERATION, RATE_LIMIT_GOOGLE_SEARCH, RATE_LIMIT_IMAGE_GENERATION, RATE_LIMIT_WINDOW
- [ ] **Performance**: CACHE_CONFIG_GOOGLE_SEARCH, CACHE_CONFIG_CONTENT_GENERATION, CACHE_CONFIG_IMAGE_GENERATION, CACHE_CONFIG_ANALYTICS
- [ ] **Monitoring**: PROMETHEUS_ENABLED, METRICS_ENDPOINT, LOG_LEVEL
- [ ] **Optional**: MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD
- [ ] **File Upload**: MAX_CONTENT_LENGTH, UPLOAD_FOLDER

### **Frontend Setup (Vercel)**
- [ ] **Backend**: BACKEND_URL
- [ ] **Environment**: NODE_ENV
- [ ] **App**: NEXT_PUBLIC_APP_NAME, NEXT_PUBLIC_APP_URL
- [ ] **AI Features**: NEXT_PUBLIC_DEEPSEEK_ENABLED, NEXT_PUBLIC_STABLE_DIFFUSION_ENABLED, NEXT_PUBLIC_GOOGLE_SEARCH_ENABLED
- [ ] **Google APIs**: NEXT_PUBLIC_GOOGLE_CUSTOM_SEARCH_API_KEY, NEXT_PUBLIC_GOOGLE_CUSTOM_SEARCH_ENGINE_ID
- [ ] **Feature Flags**: NEXT_PUBLIC_IMAGE_GENERATION_ENABLED, NEXT_PUBLIC_GOOGLE_TRENDS_ENABLED, NEXT_PUBLIC_GOOGLE_NEWS_ENABLED, NEXT_PUBLIC_GOOGLE_BOOKS_ENABLED
- [ ] **UI Config**: NEXT_PUBLIC_MAX_TOPICS_PER_REQUEST, NEXT_PUBLIC_MAX_IMAGE_VARIATIONS, NEXT_PUBLIC_CONTENT_GENERATION_TIMEOUT, NEXT_PUBLIC_IMAGE_GENERATION_TIMEOUT
- [ ] **Analytics**: NEXT_PUBLIC_ANALYTICS_ENABLED, NEXT_PUBLIC_GOOGLE_ANALYTICS_ID
- [ ] **Error Reporting**: NEXT_PUBLIC_SENTRY_DSN

---

## 🔑 **API Keys Required**

### **DeepSeek AI**
- **Service**: DeepSeek AI for content generation
- **URL**: https://api.deepseek.com/
- **Cost**: Pay-per-use
- **Setup**: Sign up and get API key

### **Stability AI (Stable Diffusion)**
- **Service**: Stable Diffusion for image generation
- **URL**: https://platform.stability.ai/
- **Cost**: Pay-per-use
- **Setup**: Sign up and get API key

### **Google APIs**
- **Google Custom Search**: https://developers.google.com/custom-search
- **Google Trends**: https://trends.google.com/trends/
- **Google Books**: https://developers.google.com/books
- **Cost**: Free tier available
- **Setup**: Google Cloud Console

### **Cloudinary**
- **Service**: Image storage and optimization
- **URL**: https://cloudinary.com/
- **Cost**: Free tier available
- **Setup**: Sign up and get credentials

---

## 🚀 **Deployment Configuration**

### **Production Environment Variables**
```bash
# Production Backend (Railway/Heroku)
FLASK_ENV=production
DATABASE_URL=postgresql://production-db-url
REDIS_URL=redis://production-redis-url
BACKEND_URL=https://your-production-backend.railway.app

# Production Frontend (Vercel)
NODE_ENV=production
BACKEND_URL=https://your-production-backend.railway.app
NEXT_PUBLIC_APP_URL=https://your-production-frontend.vercel.app
```

### **Development Environment Variables**
```bash
# Development Backend
FLASK_ENV=development
DATABASE_URL=postgresql://localhost:5432/content_creator_dev
REDIS_URL=redis://localhost:6379/0
BACKEND_URL=http://localhost:8000

# Development Frontend
NODE_ENV=development
BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## ⚠️ **Security Considerations**

### **Sensitive Variables**
- **API Keys**: Never commit to version control
- **Database URLs**: Keep secure and rotate regularly
- **JWT Secrets**: Use strong, unique secrets
- **Cloudinary Credentials**: Keep private

### **Environment-Specific Configuration**
- **Development**: Use local services where possible
- **Staging**: Use separate API keys and databases
- **Production**: Use production-grade services and monitoring

### **Variable Validation**
- Validate all required variables on startup
- Provide clear error messages for missing variables
- Use default values where appropriate
- Log configuration status (without sensitive data)

---

*This specification provides all environment variables needed to implement the AI content generation system according to the design document.* 