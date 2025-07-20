# Deployment Configuration for Content Creator Pro

## 🚀 **Deployed Applications**

### **Frontend (Vercel)**
- **URL**: https://content-gray-nu.vercel.app/
- **Platform**: Vercel
- **Status**: ✅ Deployed

### **Backend (Railway)**
- **URL**: https://content-contentmaker.up.railway.app
- **Platform**: Railway
- **Status**: ✅ Deployed

---

## 🔧 **Environment Variables Setup**

### **Backend Environment Variables (Railway)**

Go to your Railway dashboard and add these environment variables:

```bash
# Core Flask Configuration
SECRET_KEY=dba4712bba83d7be5688812bffaa65b4309af94acc2cb5a29dbf03a1439a2447
FLASK_ENV=production
FLASK_APP=app.py

# Database Configuration (Get from Railway PostgreSQL)
DATABASE_URL=postgresql://username:password@host:port/database_name

# AI Service Configuration
DEEPSEEK_API_KEY=sk-9d217f003dd24fd1bc1ce4e5440b11e9
DEEPSEEK_API_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_MAX_TOKENS=4096
DEEPSEEK_TEMPERATURE=0.7

# Stable Diffusion (Stability AI)
STABILITY_API_KEY=sk-4LYzKcgv6IQ5qVtXBNTZD6j8oeo3NVToOWAar2ykfD8Ux5IW
STABILITY_API_URL=https://api.stability.ai/v1
SD_MODEL=stable-diffusion-xl-1024-v1-0
SD_STEPS=30
SD_CFG_SCALE=7.0

# Google APIs (Get from Google Cloud Console)
GOOGLE_CUSTOM_SEARCH_API_KEY=your_google_search_api_key
GOOGLE_CUSTOM_SEARCH_ENGINE_ID=your_search_engine_id
GOOGLE_TRENDS_API_KEY=your_google_trends_api_key
GOOGLE_BOOKS_API_KEY=your_google_books_api_key
GOOGLE_NEWS_RSS_ENABLED=true

# Redis Configuration (Get from Railway Redis)
REDIS_URL=redis://username:password@host:port/database_number
CELERY_BROKER_URL=redis://username:password@host:port/database_number

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=117158686154364
CLOUDINARY_API_SECRET=QkWKsPdbREy6Ox86kpncl6q4KbI

# Security Configuration
JWT_SECRET_KEY=a5308400690e449e632a50f4004ffeacc662cb24b9cdf7708811e7da069cb247
JWT_ACCESS_TOKEN_EXPIRES=3600
CORS_ORIGINS=https://content-gray-nu.vercel.app,https://www.content-gray-nu.vercel.app
ALLOWED_HOSTS=content-gray-nu.vercel.app,www.content-gray-nu.vercel.app
CSRF_TRUSTED_ORIGINS=https://content-gray-nu.vercel.app

# Rate Limiting Configuration
RATE_LIMIT_CONTENT_GENERATION=10
RATE_LIMIT_GOOGLE_SEARCH=100
RATE_LIMIT_IMAGE_GENERATION=20
RATE_LIMIT_WINDOW=3600

# Performance Configuration
CACHE_CONFIG_GOOGLE_SEARCH=3600
CACHE_CONFIG_CONTENT_GENERATION=300
CACHE_CONFIG_IMAGE_GENERATION=600
CACHE_CONFIG_ANALYTICS=86400

# Monitoring Configuration
PROMETHEUS_ENABLED=true
METRICS_ENDPOINT=/metrics
LOG_LEVEL=INFO

# File Upload Configuration
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
```

### **Frontend Environment Variables (Vercel)**

Go to your Vercel dashboard and add these environment variables:

```bash
# Backend Configuration
BACKEND_URL=https://content-contentmaker.up.railway.app

# Environment
NODE_ENV=production

# Frontend Configuration
NEXT_PUBLIC_APP_NAME=Content Creator Pro
NEXT_PUBLIC_APP_URL=https://content-gray-nu.vercel.app

# AI Feature Flags
NEXT_PUBLIC_DEEPSEEK_ENABLED=true
NEXT_PUBLIC_STABLE_DIFFUSION_ENABLED=true
NEXT_PUBLIC_GOOGLE_SEARCH_ENABLED=true

# Google APIs Configuration (Same as backend)
NEXT_PUBLIC_GOOGLE_CUSTOM_SEARCH_API_KEY=your_google_search_api_key
NEXT_PUBLIC_GOOGLE_CUSTOM_SEARCH_ENGINE_ID=your_search_engine_id

# Feature Flags
NEXT_PUBLIC_IMAGE_GENERATION_ENABLED=true
NEXT_PUBLIC_GOOGLE_TRENDS_ENABLED=true
NEXT_PUBLIC_GOOGLE_NEWS_ENABLED=true
NEXT_PUBLIC_GOOGLE_BOOKS_ENABLED=true

# UI Configuration
NEXT_PUBLIC_MAX_TOPICS_PER_REQUEST=5
NEXT_PUBLIC_MAX_IMAGE_VARIATIONS=4
NEXT_PUBLIC_CONTENT_GENERATION_TIMEOUT=30000
NEXT_PUBLIC_IMAGE_GENERATION_TIMEOUT=60000

# Analytics Configuration
NEXT_PUBLIC_ANALYTICS_ENABLED=true
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=your_google_analytics_id
```

---

## 📋 **Setup Instructions**

### **1. Railway Backend Setup**

1. **Go to Railway Dashboard**: https://railway.app/
2. **Select your project**: `content-contentmaker`
3. **Add Environment Variables**:
   - Click on your backend service
   - Go to "Variables" tab
   - Add each environment variable from the list above

4. **Add PostgreSQL Database**:
   - Click "New Service" → "Database" → "PostgreSQL"
   - Copy the `DATABASE_URL` from the database service

5. **Add Redis Service**:
   - Click "New Service" → "Database" → "Redis"
   - Copy the `REDIS_URL` from the Redis service

### **2. Vercel Frontend Setup**

1. **Go to Vercel Dashboard**: https://vercel.com/
2. **Select your project**: `content-gray-nu`
3. **Add Environment Variables**:
   - Go to "Settings" → "Environment Variables"
   - Add each environment variable from the list above

### **3. API Keys Setup**

#### **Stability AI (Already Configured)**
✅ API Key: `sk-4LYzKcgv6IQ5qVtXBNTZD6j8oeo3NVToOWAar2ykfD8Ux5IW`

#### **Google Custom Search API (Required for Topic Generation)**
1. Go to: https://console.cloud.google.com/
2. Enable Custom Search API
3. Create API key
4. Go to: https://programmablesearchengine.google.com/
5. Create search engine and get Engine ID
6. Add to both Railway and Vercel:
   ```bash
   GOOGLE_CUSTOM_SEARCH_API_KEY=your-api-key
   GOOGLE_CUSTOM_SEARCH_ENGINE_ID=your-engine-id
   ```

---

## 🧪 **Testing Your Setup**

### **Test Backend API**
```bash
curl https://content-contentmaker.up.railway.app/api/health
```

### **Test Frontend**
Visit: https://content-gray-nu.vercel.app/

### **Test AI Content Generation**
1. Go to: https://content-gray-nu.vercel.app/generator
2. Try the 6-step AI content generation workflow
3. Test topic generation with Google Search
4. Test image generation with Stable Diffusion

---

## 🔍 **Troubleshooting**

### **Common Issues**

1. **CORS Errors**: Make sure `CORS_ORIGINS` includes your Vercel domain
2. **API Key Errors**: Verify all API keys are correctly set
3. **Database Connection**: Check `DATABASE_URL` in Railway
4. **Redis Connection**: Check `REDIS_URL` in Railway

### **Check Logs**
- **Railway**: Go to your service → "Deployments" → Click on deployment → "Logs"
- **Vercel**: Go to your project → "Deployments" → Click on deployment → "Functions" → "View Function Logs"

---

## 📊 **Monitoring**

### **Backend Health Check**
- URL: https://content-contentmaker.up.railway.app/api/health
- Expected: `{"status": "healthy", "timestamp": "..."}`

### **Frontend Status**
- URL: https://content-gray-nu.vercel.app/
- Expected: Content Creator Pro homepage loads

---

*Last Updated: $(date)*
*Deployment URLs: Frontend - https://content-gray-nu.vercel.app/, Backend - https://content-contentmaker.up.railway.app* 