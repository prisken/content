# 🔗 Frontend-Backend Integration Guide

## 📋 **Overview**

This guide covers the complete integration between your Railway backend and Vercel frontend for Content Creator Pro.

## 🎯 **Current Status**

### ✅ **Backend (Railway)**
- **URL**: `https://content-contentmaker.up.railway.app`
- **Status**: ✅ Running with Gunicorn
- **Database**: ✅ PostgreSQL connected
- **API Endpoints**: ✅ Available

### ⚠️ **Frontend (Vercel)**
- **Status**: ⚠️ Configuration ready, needs deployment
- **Structure**: ⚠️ Next.js config exists, needs app code

---

## 🔧 **Backend Configuration**

### **1. CORS Configuration (Already Updated)**

Your backend is configured to accept requests from:
- `http://localhost:3000` (local development)
- `https://*.vercel.app` (Vercel deployments)
- `https://*.railway.app` (Railway previews)

### **2. Environment Variables (Add to Railway)**

| Variable | Value | Description |
|----------|-------|-------------|
| `SECRET_KEY` | `1e5ff73c70e9d4cccecc9a1a438ceac6c997cd0f05d04906dc6fbd07f1ff441c` | Flask secret |
| `FLASK_ENV` | `production` | Environment |
| `FLASK_APP` | `run.py` | App entry point |
| `CLOUDINARY_CLOUD_NAME` | `debyzbnjb` | Cloudinary config |
| `CLOUDINARY_API_KEY` | `117158686154364` | Cloudinary key |
| `CLOUDINARY_API_SECRET` | `QkWKsPdbREy6Ox86kpncl6q4KbI` | Cloudinary secret |
| `DEEPSEEK_API_KEY` | `sk-9d217f003dd24fd1bc1ce4e5440b11e9` | AI API key |
| `ALLOWED_ORIGINS` | `https://your-frontend-domain.vercel.app` | CORS origins |

---

## 🚀 **Frontend Configuration**

### **1. Environment Variables (Add to Vercel)**

| Variable | Value | Description |
|----------|-------|-------------|
| `BACKEND_URL` | `https://content-contentmaker.up.railway.app` | Backend API URL |
| `NEXT_PUBLIC_APP_NAME` | `Content Creator Pro` | App name |
| `NEXT_PUBLIC_VERSION` | `1.0.0` | App version |

### **2. Next.js Configuration (Already Updated)**

```javascript
// next.config.js
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['res.cloudinary.com', 'via.placeholder.com'],
  },
  env: {
    BACKEND_URL: process.env.BACKEND_URL || 'https://content-contentmaker.up.railway.app',
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.BACKEND_URL}/api/:path*`,
      },
    ];
  },
}
```

### **3. API Client Setup**

Create `frontend/lib/api.js`:

```javascript
const API_BASE_URL = process.env.BACKEND_URL || 'https://content-contentmaker.up.railway.app';

export const apiClient = {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    if (options.body) {
      config.body = JSON.stringify(options.body);
    }

    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  },

  // Content Generation
  async generateContent(data) {
    return this.request('/api/generate', {
      method: 'POST',
      body: data,
    });
  },

  // Image Generation
  async generateImage(data) {
    return this.request('/api/images/generate', {
      method: 'POST',
      body: data,
    });
  },

  // Health Check
  async healthCheck() {
    return this.request('/health');
  },

  // Get Content Directions
  async getDirections() {
    return this.request('/api/directions');
  },
};
```

---

## 🧪 **Testing Integration**

### **1. Backend Health Check**

```bash
curl https://content-contentmaker.up.railway.app/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-12-19T22:30:44Z",
  "version": "1.0.0"
}
```

### **2. Content Generation Test**

```bash
curl -X POST https://content-contentmaker.up.railway.app/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "direction": "business_finance",
    "platform": "linkedin",
    "source": "personal_experience",
    "topic": "AI in Business",
    "tone": "professional",
    "language": "en"
  }'
```

### **3. Frontend API Test**

```javascript
// Test in browser console
const response = await fetch('https://content-contentmaker.up.railway.app/health');
const data = await response.json();
console.log(data);
```

---

## 🚀 **Deployment Steps**

### **1. Backend (Railway) - ✅ Complete**

1. ✅ **Code deployed** to Railway
2. ✅ **Gunicorn running** on port 8080
3. ⚠️ **Add environment variables** (see above)
4. ⚠️ **Apply 10 changes** in Railway dashboard

### **2. Frontend (Vercel) - ⚠️ Needs Setup**

1. ⚠️ **Create Next.js app structure** (pages, components, etc.)
2. ⚠️ **Deploy to Vercel**
3. ⚠️ **Add environment variables** in Vercel
4. ⚠️ **Test integration**

---

## 📁 **Frontend Structure Needed**

```
frontend/
├── pages/
│   ├── _app.js
│   ├── index.js
│   ├── dashboard.js
│   ├── generator.js
│   └── api/
├── components/
│   ├── Layout.js
│   ├── Header.js
│   ├── ContentGenerator.js
│   └── ImageGenerator.js
├── lib/
│   └── api.js
├── styles/
│   └── globals.css
└── public/
```

---

## 🔧 **CORS Troubleshooting**

### **If you get CORS errors:**

1. **Check Railway environment variables:**
   ```bash
   # Add to Railway
   ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
   ```

2. **Test CORS headers:**
   ```bash
   curl -H "Origin: https://your-frontend-domain.vercel.app" \
        -H "Access-Control-Request-Method: POST" \
        -H "Access-Control-Request-Headers: Content-Type" \
        -X OPTIONS \
        https://content-contentmaker.up.railway.app/api/generate
   ```

3. **Check browser console** for CORS errors

---

## 📊 **API Endpoints Reference**

### **Health & Status**
- `GET /health` - Health check
- `GET /api/status` - API status

### **Content Generation**
- `POST /api/generate` - Generate content
- `GET /api/directions` - Get content directions
- `GET /api/platforms` - Get platforms

### **Image Generation**
- `POST /api/images/generate` - Generate images
- `GET /api/images/styles` - Get image styles

### **Authentication**
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/logout` - User logout

---

## 🎯 **Next Steps**

### **Immediate Actions:**

1. **✅ Add environment variables** to Railway
2. **✅ Apply 10 changes** in Railway
3. **⚠️ Create Next.js frontend** structure
4. **⚠️ Deploy frontend** to Vercel
5. **⚠️ Test integration** between services

### **Testing Checklist:**

- [ ] Backend health check works
- [ ] Content generation API works
- [ ] Image generation API works
- [ ] Frontend can connect to backend
- [ ] CORS is properly configured
- [ ] Environment variables are set

---

## 🆘 **Troubleshooting**

### **Common Issues:**

1. **CORS Errors**: Check `ALLOWED_ORIGINS` in Railway
2. **API Timeouts**: Check Railway logs
3. **Database Errors**: Check PostgreSQL connection
4. **Environment Variables**: Verify all keys are set

### **Debug Commands:**

```bash
# Test backend
curl https://content-contentmaker.up.railway.app/health

# Test API
curl -X POST https://content-contentmaker.up.railway.app/api/generate \
  -H "Content-Type: application/json" \
  -d '{"direction": "business_finance", "platform": "linkedin"}'

# Check Railway logs
# Go to Railway dashboard → Logs tab
```

---

**Last Updated**: December 19, 2024  
**Status**: Backend ✅ Ready, Frontend ⚠️ Needs Setup 