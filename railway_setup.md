# 🚀 Railway Environment Variables Setup Guide

## 📋 **Step-by-Step Instructions**

### **Step 1: Access Railway Dashboard**
1. Go to [railway.app](https://railway.app)
2. Sign in to your account
3. Click on your "content" service (Flask backend)

### **Step 2: Navigate to Variables**
1. Click the **"Variables"** tab (next to "Deployments", "Metrics", "Settings")
2. You'll see a list of existing variables

### **Step 3: Add Each Variable**

Click **"New Variable"** for each of these:

#### **🔑 Flask Configuration**
```
Variable Name: SECRET_KEY
Value: your-super-secure-secret-key-change-this-in-production-2024
```

```
Variable Name: FLASK_ENV
Value: production
```

```
Variable Name: FLASK_APP
Value: app.py
```

#### **☁️ Cloudinary Configuration**
```
Variable Name: CLOUDINARY_CLOUD_NAME
Value: debyzbnjb
```

```
Variable Name: CLOUDINARY_API_KEY
Value: 117158686154364
```

```
Variable Name: CLOUDINARY_API_SECRET
Value: QkWKsPdbREy6Ox86kpncl6q4KbI
```

#### **🤖 DeepSeek AI Configuration**
```
Variable Name: DEEPSEEK_API_KEY
Value: sk-9d217f003dd24fd1bc1ce4e5440b11e9
```

#### **🌐 CORS Configuration**
```
Variable Name: ALLOWED_ORIGINS
Value: https://your-frontend-domain.vercel.app
```
*(Update this later when you deploy to Vercel)*

### **Step 4: Verify Variables**
After adding all variables, you should see:
- ✅ SECRET_KEY
- ✅ FLASK_ENV
- ✅ FLASK_APP
- ✅ CLOUDINARY_CLOUD_NAME
- ✅ CLOUDINARY_API_KEY
- ✅ CLOUDINARY_API_SECRET
- ✅ DEEPSEEK_API_KEY
- ✅ ALLOWED_ORIGINS
- ✅ DATABASE_URL (automatically set by Railway)

### **Step 5: Deploy**
1. Go back to **"Settings"** tab
2. Click **"Deploy + Enter"**
3. Monitor the deployment logs

## 🧪 **Test Your Configuration**

Run this test script locally first:

```bash
cd backend
python3 test_config.py
```

## 📊 **Expected Results**

After deployment, test these endpoints:

### **Health Check**
```bash
curl https://your-railway-app.railway.app/health
```

### **Content Generation**
```bash
curl -X POST https://your-railway-app.railway.app/api/generate \
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

### **Image Generation**
```bash
curl -X POST https://your-railway-app.railway.app/api/images/generate \
  -H "Content-Type: application/json" \
  -d '{
    "content": "AI is transforming business",
    "image_style": "modern",
    "platform": "linkedin",
    "direction": "business_finance"
  }'
```

## 🔧 **Troubleshooting**

### **If Variables Don't Appear**
- Make sure you're in the "Variables" tab
- Click "New Variable" for each one
- Check that you're editing the "content" service

### **If Deployment Fails**
- Check deployment logs for specific errors
- Verify all variable names are exactly as shown
- Make sure there are no extra spaces

### **If API Calls Fail**
- Verify API keys are correct
- Check CORS configuration
- Test health endpoint first

## 📞 **Need Help?**

If you encounter issues:
1. Check the deployment logs in Railway
2. Run the test script locally: `python3 test_config.py`
3. Verify all variables are set correctly
4. Test each API endpoint individually

## 🎯 **Success Indicators**

Your deployment is successful when:
- ✅ Railway shows "Deploy successful"
- ✅ Health endpoint returns: `{"status": "healthy"}`
- ✅ Content generation returns AI-generated content
- ✅ Image generation returns image URLs
- ✅ No errors in Railway logs 