# 🚀 Content Creator Pro - Deployment Guide

This guide will help you deploy Content Creator Pro to Vercel (frontend) and Railway (backend).

## 📋 Prerequisites

- [Node.js](https://nodejs.org/) (v16 or higher)
- [Python](https://python.org/) (v3.8 or higher)
- [Git](https://git-scm.com/)
- [Vercel CLI](https://vercel.com/cli) (`npm i -g vercel`)
- [Railway CLI](https://railway.app/cli) (`npm i -g @railway/cli`)

## 🏗️ Architecture

- **Frontend**: Next.js application deployed on Vercel
- **Backend**: Flask API deployed on Railway
- **Database**: PostgreSQL (provided by Railway)

## 🚀 Quick Deployment

### Option 1: Automated Deployment (Recommended)

1. **Clone and setup**:
   ```bash
   git clone <your-repo-url>
   cd content-creation
   chmod +x deploy.sh
   ```

2. **Run deployment script**:
   ```bash
   ./deploy.sh
   ```

3. **Follow the prompts** to deploy backend, frontend, or both.

### Option 2: Manual Deployment

## 🔧 Backend Deployment (Railway)

### Step 1: Prepare Backend

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create environment file**:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

### Step 2: Deploy to Railway

1. **Login to Railway**:
   ```bash
   railway login
   ```

2. **Initialize Railway project**:
   ```bash
   railway init
   ```

3. **Deploy**:
   ```bash
   railway up
   ```

4. **Set environment variables** in Railway dashboard:
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-secret-key`
   - `DATABASE_URL=postgresql://...` (auto-generated by Railway)
   - `CORS_ORIGINS=https://your-vercel-app.vercel.app`

5. **Get your Railway URL** from the dashboard (e.g., `https://your-app.railway.app`)

## 🎨 Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Update environment variables**:
   ```bash
   cp env.production.example .env.production
   # Edit .env.production with your Railway backend URL
   ```

### Step 2: Deploy to Vercel

1. **Login to Vercel**:
   ```bash
   vercel login
   ```

2. **Deploy**:
   ```bash
   vercel --prod
   ```

3. **Set environment variables** in Vercel dashboard:
   - `BACKEND_URL=https://your-railway-app.railway.app`

## 🔗 Connect Frontend and Backend

1. **Update frontend environment**:
   - Go to Vercel dashboard → Your project → Settings → Environment Variables
   - Add `BACKEND_URL` with your Railway URL

2. **Update backend CORS**:
   - Go to Railway dashboard → Your project → Variables
   - Add `CORS_ORIGINS` with your Vercel URL

## 🗄️ Database Setup

Railway automatically provides a PostgreSQL database. The application will create tables on first run.

### Manual Database Initialization (if needed):

```bash
# Connect to Railway shell
railway shell

# Initialize database
flask init-db
```

## 🔐 Environment Variables

### Backend (Railway)

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `production` |
| `SECRET_KEY` | Flask secret key | `your-secret-key` |
| `DATABASE_URL` | PostgreSQL connection | `postgresql://...` |
| `CORS_ORIGINS` | Allowed origins | `https://your-app.vercel.app` |
| `JWT_SECRET_KEY` | JWT signing key | `your-jwt-secret` |

### Frontend (Vercel)

| Variable | Description | Example |
|----------|-------------|---------|
| `BACKEND_URL` | Railway backend URL | `https://your-app.railway.app` |
| `NEXT_PUBLIC_APP_NAME` | App name | `Content Creator Pro` |

## 🧪 Testing Deployment

1. **Test backend health**:
   ```bash
   curl https://your-railway-app.railway.app/health
   ```

2. **Test frontend**:
   - Visit your Vercel URL
   - Try logging in with demo credentials:
     - Email: `admin@contentcreator.com`
     - Password: `admin123`

## 🔄 Continuous Deployment

### GitHub Integration

1. **Connect GitHub to Vercel**:
   - Go to Vercel dashboard → Import Project → GitHub
   - Select your repository
   - Configure build settings

2. **Connect GitHub to Railway**:
   - Go to Railway dashboard → New Project → Deploy from GitHub repo
   - Select your repository
   - Configure deployment settings

### Automatic Deployments

- **Vercel**: Automatically deploys on push to `main` branch
- **Railway**: Automatically deploys on push to `main` branch

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**:
   - Ensure `CORS_ORIGINS` includes your Vercel URL
   - Check that the URL format is correct

2. **Database Connection**:
   - Verify `DATABASE_URL` is set correctly
   - Check Railway database status

3. **Build Failures**:
   - Check build logs in Vercel/Railway dashboard
   - Verify all dependencies are in `requirements.txt`/`package.json`

### Debug Commands

```bash
# Check Railway logs
railway logs

# Check Vercel logs
vercel logs

# Test backend locally
python run.py

# Test frontend locally
cd frontend && npm run dev
```

## 📊 Monitoring

### Railway Monitoring
- **Logs**: Available in Railway dashboard
- **Metrics**: CPU, memory, and network usage
- **Health Checks**: Automatic health check endpoint

### Vercel Monitoring
- **Analytics**: Built-in analytics dashboard
- **Performance**: Core Web Vitals monitoring
- **Functions**: Serverless function logs

## 🔒 Security

### Production Security Checklist

- [ ] Use strong secret keys
- [ ] Enable HTTPS (automatic on Vercel/Railway)
- [ ] Set up proper CORS origins
- [ ] Use environment variables for sensitive data
- [ ] Enable rate limiting (if needed)
- [ ] Set up monitoring and alerts

## 📈 Scaling

### Railway Scaling
- **Auto-scaling**: Automatically scales based on traffic
- **Custom scaling**: Set minimum/maximum instances
- **Database scaling**: Upgrade PostgreSQL plan as needed

### Vercel Scaling
- **Edge Network**: Global CDN automatically
- **Serverless**: Scales to zero when not in use
- **Functions**: Automatic scaling for API routes

## 🆘 Support

- **Railway**: [docs.railway.app](https://docs.railway.app)
- **Vercel**: [vercel.com/docs](https://vercel.com/docs)
- **Project Issues**: Create an issue in the GitHub repository

---

**Happy Deploying! 🚀** 