# 🧪 Local Testing Guide

## 📋 **Overview**

This guide will help you test your Content Creator Pro application locally while waiting for Vercel deployment.

## 🚀 **Quick Start**

### **1. Test Backend Only**
```bash
# Terminal 1: Start backend
source venv/bin/activate
python test_local_backend.py
```

### **2. Test Frontend Only**
```bash
# Terminal 2: Start frontend
cd frontend
npm run dev
```

### **3. Test Both Together**
```bash
# Terminal 1: Backend
source venv/bin/activate
python test_local_backend.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

---

## 🔧 **Backend Testing**

### **Start Local Backend:**
```bash
# Activate virtual environment
source venv/bin/activate

# Run local backend
python test_local_backend.py
```

### **Backend URLs:**
- **Main App**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **API Status**: http://localhost:5000/api/status
- **Content Generation**: http://localhost:5000/api/generate

### **Test Backend API:**
```bash
# Health check
curl http://localhost:5000/health

# Content generation
curl -X POST http://localhost:5000/api/generate \
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

---

## 🎨 **Frontend Testing**

### **Start Local Frontend:**
```bash
cd frontend
npm run dev
```

### **Frontend URLs:**
- **Main App**: http://localhost:3000
- **Generator**: http://localhost:3000/generator
- **Dashboard**: http://localhost:3000/dashboard
- **Library**: http://localhost:3000/library

### **Frontend Features to Test:**
1. **Landing Page**: Hero section, features, navigation
2. **Content Generator**: 5-step wizard, form validation
3. **Dashboard**: Statistics, recent content, analytics
4. **Library**: Search, filtering, content management

---

## 🔗 **Full Stack Testing**

### **1. Start Both Services:**
```bash
# Terminal 1: Backend
source venv/bin/activate
python test_local_backend.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

### **2. Test Integration:**
1. **Open**: http://localhost:3000
2. **Navigate to**: Generator page
3. **Fill out**: Content generation form
4. **Test**: Content generation with AI
5. **Verify**: Content appears with hashtags

### **3. Test All Features:**
- ✅ **Content Generation**: Create AI-powered content
- ✅ **Platform Selection**: Choose from 6 platforms
- ✅ **Direction Selection**: Choose from 18 directions
- ✅ **Search & Filter**: Test library functionality
- ✅ **Responsive Design**: Test on different screen sizes

---

## 🧪 **API Testing**

### **Test Content Generation:**
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "direction": "technology",
    "platform": "twitter",
    "source": "industry_trends",
    "topic": "AI and Machine Learning",
    "tone": "professional",
    "language": "en"
  }'
```

### **Test Image Generation:**
```bash
curl -X POST http://localhost:5000/api/images/generate \
  -H "Content-Type: application/json" \
  -d '{
    "content": "AI is transforming business",
    "image_style": "modern",
    "platform": "linkedin",
    "direction": "business_finance"
  }'
```

### **Test Health Check:**
```bash
curl http://localhost:5000/health
```

---

## 🔍 **Troubleshooting**

### **Backend Issues:**
1. **Port already in use**: Change port in `test_local_backend.py`
2. **Import errors**: Make sure virtual environment is activated
3. **Database errors**: Check SQLite file permissions

### **Frontend Issues:**
1. **Port 3000 in use**: Next.js will automatically use next available port
2. **API connection errors**: Check backend is running on port 5000
3. **Build errors**: Run `npm install` again

### **Integration Issues:**
1. **CORS errors**: Backend is configured for localhost:3000
2. **API timeouts**: Check both services are running
3. **Environment variables**: All set in `test_local_backend.py`

---

## 📊 **Testing Checklist**

### **Backend Testing:**
- [ ] Health check endpoint works
- [ ] Content generation API works
- [ ] Image generation API works
- [ ] Database connection works
- [ ] Environment variables loaded

### **Frontend Testing:**
- [ ] Landing page loads
- [ ] Navigation works
- [ ] Generator form works
- [ ] Dashboard displays
- [ ] Library search works
- [ ] Responsive design works

### **Integration Testing:**
- [ ] Frontend can connect to backend
- [ ] Content generation works end-to-end
- [ ] Error handling works
- [ ] Loading states work
- [ ] Toast notifications work

---

## 🎯 **Expected Results**

### **Backend Health Check:**
```json
{
  "status": "healthy",
  "timestamp": "2024-12-19T22:30:44Z",
  "version": "1.0.0"
}
```

### **Content Generation:**
```json
{
  "content": "AI is revolutionizing how businesses operate...",
  "hashtags": ["AI", "Business", "Innovation", "Technology"],
  "platform": "linkedin",
  "direction": "business_finance"
}
```

---

## 🚀 **Next Steps**

After local testing:
1. **✅ Verify everything works locally**
2. **⏰ Wait for Vercel deployment (7 hours)**
3. **🔗 Deploy frontend to Vercel**
4. **🌐 Test production deployment**
5. **📱 Share your application!**

---

**Happy Testing! 🎉** 