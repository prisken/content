# Environment Variables Specification for AI Content Generation System

## Overview
This document specifies all environment variables required for both frontend and backend platforms to implement the AI content generation system according to the design specifications.

---

## 🔧 **Backend Environment Variables**

### **Core Flask Configuration**
```bash
# Flask Configuration
SECRET_KEY=dba4712bba83d7be5688812bffaa65b4309af94acc2cb5a29dbf03a1439a2447
FLASK_ENV=production
FLASK_APP=app.py
```

### **Database Configuration**
```bash
# Database Configuration (Railway PostgreSQL - Get from Railway Dashboard)
DATABASE_URL=postgresql://username:password@host:port/database_name
```

### **AI Service Configuration**

#### **DeepSeek AI** ✅ (Already Configured)
```bash
# DeepSeek AI Configuration
DEEPSEEK_API_KEY=sk-9d217f003dd24fd1bc1ce4e5440b11e9
DEEPSEEK_API_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_MAX_TOKENS=4096
DEEPSEEK_TEMPERATURE=0.7
```

#### **Stable Diffusion** ✅ (Already Configured)
```bash
# Stable Diffusion Configuration
STABILITY_API_KEY=sk-4LYzKcgv6IQ5qVtXBNTZD6j8oeo3NVToOWAar2ykfD8Ux5IW
STABILITY_API_URL=https://api.stability.ai/v1
SD_MODEL=stable-diffusion-xl-1024-v1-0
SD_STEPS=30
SD_CFG_SCALE=7.0
```

#### **Google APIs** ❌ (Need to Obtain)
```bash
# Google APIs Configuration
GOOGLE_CUSTOM_SEARCH_API_KEY=your_google_search_api_key  # Get from Google Cloud Console
GOOGLE_CUSTOM_SEARCH_ENGINE_ID=your_search_engine_id     # Get from https://programmablesearchengine.google.com/
GOOGLE_TRENDS_API_KEY=your_google_trends_api_key         # Optional - Using mock data
GOOGLE_BOOKS_API_KEY=your_google_books_api_key           # Same as Custom Search API key
GOOGLE_NEWS_RSS_ENABLED=true
```

### **Infrastructure Configuration**

#### **Redis & Celery** ❌ (Need to Set Up)
```bash
# Redis Configuration (for Celery) - Get from Railway Dashboard
REDIS_URL=redis://username:password@host:port/database_number
CELERY_BROKER_URL=redis://username:password@host:port/database_number
```

#### **Cloudinary (Image Storage)** ✅ (Already Configured)
```bash
# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=117158686154364
CLOUDINARY_API_SECRET=QkWKsPdbREy6Ox86kpncl6q4KbI
```

### **Security Configuration**
```bash
# Security Configuration
JWT_SECRET_KEY=a5308400690e449e632a50f4004ffeacc662cb24b9cdf7708811e7da069cb247
JWT_ACCESS_TOKEN_EXPIRES=3600
CORS_ORIGINS=https://content-gray-nu.vercel.app,https://www.content-gray-nu.vercel.app
ALLOWED_HOSTS=content-gray-nu.vercel.app,www.content-gray-nu.vercel.app
CSRF_TRUSTED_ORIGINS=https://content-gray-nu.vercel.app
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
BACKEND_URL=https://content-contentmaker.up.railway.app

# Environment
NODE_ENV=production

# Frontend Configuration
NEXT_PUBLIC_APP_NAME=Content Creator Pro
NEXT_PUBLIC_APP_URL=https://content-gray-nu.vercel.app
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
NEXT_PUBLIC_GOOGLE_CUSTOM_SEARCH_API_KEY=your_google_search_api_key  # Same as backend
NEXT_PUBLIC_GOOGLE_CUSTOM_SEARCH_ENGINE_ID=your_search_engine_id     # Same as backend
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

## 🔑 **How to Obtain Missing API Keys and Configuration**

### **✅ Already Configured**
- **DeepSeek AI**: `sk-9d217f003dd24fd1bc1ce4e5440b11e9`
- **Stability AI**: `sk-4LYzKcgv6IQ5qVtXBNTZD6j8oeo3NVToOWAar2ykfD8Ux5IW`
- **Cloudinary**: API Key and Secret provided
- **Secret Keys**: Generated and ready to use

### **❌ Need to Obtain**

#### **1. Google Custom Search API - For Topic Generation**

**Step-by-Step Guide:**
1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create/Select Project**: Create new or select existing project
3. **Enable Custom Search API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Custom Search API"
   - Click "Enable"
4. **Create Credentials**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy the API key
5. **Create Search Engine**:
   - Go to: https://programmablesearchengine.google.com/
   - Click "Create a search engine"
   - Enter any site (e.g., `www.google.com`)
   - Get your Search Engine ID (looks like: `012345678901234567890:abcdefghijk`)
6. **Set in Environment**:
   ```bash
   GOOGLE_CUSTOM_SEARCH_API_KEY=your-google-api-key
   GOOGLE_CUSTOM_SEARCH_ENGINE_ID=your-search-engine-id
   ```

#### **3. Database Configuration (PostgreSQL)**

**Option A: Railway PostgreSQL (Recommended)**
1. **Go to Railway**: https://railway.app/
2. **Create New Project**
3. **Add PostgreSQL Database**:
   - Click "New Service" → "Database" → "PostgreSQL"
   - Railway will provide connection string
4. **Get Connection String**:
   - Go to database service
   - Click "Connect" → "PostgreSQL"
   - Copy the connection string
5. **Set in Environment**:
   ```bash
   DATABASE_URL=postgresql://username:password@host:port/database_name
   ```

**Option B: Local PostgreSQL**
1. **Install PostgreSQL**: https://www.postgresql.org/download/
2. **Create Database**:
   ```bash
   createdb content_creator
   ```
3. **Set in Environment**:
   ```bash
   DATABASE_URL=postgresql://localhost:5432/content_creator
   ```

#### **4. Redis Configuration (For Background Tasks)**

**Option A: Railway Redis**
1. **Go to Railway**: https://railway.app/
2. **Add Redis Service**:
   - Click "New Service" → "Database" → "Redis"
3. **Get Connection String**:
   - Go to Redis service
   - Click "Connect" → "Redis"
   - Copy the connection string
4. **Set in Environment**:
   ```bash
   REDIS_URL=redis://username:password@host:port/database_number
   CELERY_BROKER_URL=redis://username:password@host:port/database_number
   ```

**Option B: Local Redis**
1. **Install Redis**: https://redis.io/download
2. **Start Redis**:
   ```bash
   redis-server
   ```
3. **Set in Environment**:
   ```bash
   REDIS_URL=redis://localhost:6379/0
   CELERY_BROKER_URL=redis://localhost:6379/0
   ```

#### **5. Domain Configuration**

**Get Your Deployment URLs:**
1. **Vercel Domain**: Check your Vercel dashboard for your app URL
2. **Railway Domain**: Check your Railway dashboard for your backend URL
3. **Update Environment Variables**:
   ```bash
   # Replace with your actual domains
   CORS_ORIGINS=https://content-gray-nu.vercel.app
   ALLOWED_HOSTS=content-gray-nu.vercel.app
   CSRF_TRUSTED_ORIGINS=https://content-gray-nu.vercel.app
   BACKEND_URL=https://content-contentmaker.up.railway.app
   NEXT_PUBLIC_APP_URL=https://content-gray-nu.vercel.app
   ```

---

## 📋 **Complete Environment Setup Checklist**

### **Backend Setup (Railway/Heroku)**
- [x] **Flask Configuration**: SECRET_KEY, FLASK_ENV, FLASK_APP
- [ ] **Database**: DATABASE_URL (PostgreSQL) - Get from Railway
- [x] **DeepSeek AI**: DEEPSEEK_API_KEY, DEEPSEEK_API_URL, DEEPSEEK_MODEL, DEEPSEEK_MAX_TOKENS, DEEPSEEK_TEMPERATURE
- [x] **Stable Diffusion**: STABILITY_API_KEY, STABILITY_API_URL, SD_MODEL, SD_STEPS, SD_CFG_SCALE
- [ ] **Google APIs**: GOOGLE_CUSTOM_SEARCH_API_KEY, GOOGLE_CUSTOM_SEARCH_ENGINE_ID, GOOGLE_TRENDS_API_KEY, GOOGLE_BOOKS_API_KEY, GOOGLE_NEWS_RSS_ENABLED - Get from Google Cloud Console
- [ ] **Redis**: REDIS_URL, CELERY_BROKER_URL - Get from Railway
- [x] **Cloudinary**: CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
- [x] **Security**: JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES, CORS_ORIGINS, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS
- [x] **Rate Limiting**: RATE_LIMIT_CONTENT_GENERATION, RATE_LIMIT_GOOGLE_SEARCH, RATE_LIMIT_IMAGE_GENERATION, RATE_LIMIT_WINDOW
- [x] **Performance**: CACHE_CONFIG_GOOGLE_SEARCH, CACHE_CONFIG_CONTENT_GENERATION, CACHE_CONFIG_IMAGE_GENERATION, CACHE_CONFIG_ANALYTICS
- [x] **Monitoring**: PROMETHEUS_ENABLED, METRICS_ENDPOINT, LOG_LEVEL
- [ ] **Optional**: MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD
- [x] **File Upload**: MAX_CONTENT_LENGTH, UPLOAD_FOLDER

### **Frontend Setup (Vercel)**
- [ ] **Backend**: BACKEND_URL - Get from Railway
- [x] **Environment**: NODE_ENV
- [ ] **App**: NEXT_PUBLIC_APP_NAME, NEXT_PUBLIC_APP_URL - Get from Vercel
- [x] **AI Features**: NEXT_PUBLIC_DEEPSEEK_ENABLED, NEXT_PUBLIC_STABLE_DIFFUSION_ENABLED, NEXT_PUBLIC_GOOGLE_SEARCH_ENABLED
- [ ] **Google APIs**: NEXT_PUBLIC_GOOGLE_CUSTOM_SEARCH_API_KEY, NEXT_PUBLIC_GOOGLE_CUSTOM_SEARCH_ENGINE_ID - Same as backend
- [x] **Feature Flags**: NEXT_PUBLIC_IMAGE_GENERATION_ENABLED, NEXT_PUBLIC_GOOGLE_TRENDS_ENABLED, NEXT_PUBLIC_GOOGLE_NEWS_ENABLED, NEXT_PUBLIC_GOOGLE_BOOKS_ENABLED
- [x] **UI Config**: NEXT_PUBLIC_MAX_TOPICS_PER_REQUEST, NEXT_PUBLIC_MAX_IMAGE_VARIATIONS, NEXT_PUBLIC_CONTENT_GENERATION_TIMEOUT, NEXT_PUBLIC_IMAGE_GENERATION_TIMEOUT
- [ ] **Analytics**: NEXT_PUBLIC_ANALYTICS_ENABLED, NEXT_PUBLIC_GOOGLE_ANALYTICS_ID
- [ ] **Error Reporting**: NEXT_PUBLIC_SENTRY_DSN

---

## 🚀 **Quick Setup Commands**

### **Test API Keys**
```bash
# Test DeepSeek AI (Already Working)
curl -H "Authorization: Bearer sk-9d217f003dd24fd1bc1ce4e5440b11e9" \
     -H "Content-Type: application/json" \
     -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"Hello"}]}' \
     https://api.deepseek.com/v1/chat/completions

# Test Stability AI (Already Working)
curl -H "Authorization: Bearer sk-4LYzKcgv6IQ5qVtXBNTZD6j8oeo3NVToOWAar2ykfD8Ux5IW" \
     -H "Content-Type: application/json" \
     -d '{"text_prompts":[{"text":"a beautiful landscape"}],"cfg_scale":7,"height":1024,"width":1024,"samples":1,"steps":30}' \
     https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image

# Test Google Custom Search (After getting key)
curl "https://www.googleapis.com/customsearch/v1?key=YOUR_API_KEY&cx=YOUR_SEARCH_ENGINE_ID&q=test"
```

### **Priority Order for Setup**
1. **Google Custom Search API** (for topic generation)
2. **Database URL** (PostgreSQL from Railway)
3. **Redis URL** (from Railway)
4. **Domain Configuration** (from Vercel/Railway dashboards)

---

## ⚠️ **Security Considerations**

### **Sensitive Variables**
- **API Keys**: Never commit to version control
- **Database URLs**: Keep secure and rotate regularly
- **JWT Secrets**: Use strong, unique secrets (✅ Generated)
- **Cloudinary Credentials**: Keep private (✅ Configured)

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