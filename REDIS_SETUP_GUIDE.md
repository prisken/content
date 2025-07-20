# Redis Setup Guide for Content Creator Pro

## 🎯 **Overview**

Redis is used for:
- **Background task queue** (Celery broker)
- **Caching** (API responses, search results)
- **Session storage** (user sessions)
- **Rate limiting** (API request throttling)

---

## 🚀 **Option 1: Railway Redis (Production - Recommended)**

### **Step-by-Step Setup**

#### **Step 1: Access Railway Dashboard**
1. Go to: https://railway.app/
2. Sign in to your account
3. Select your project: `content-contentmaker`

#### **Step 2: Add Redis Service**
1. In your Railway project dashboard, click **"New Service"**
2. Select **"Database"** from the options
3. Choose **"Redis"** from the database types
4. Click **"Deploy"** to create the Redis service

#### **Step 3: Get Redis Connection String**
1. Once Redis is deployed, click on the **Redis service** in your project
2. Go to the **"Connect"** tab
3. Click on **"Redis"** connection type
4. Copy the connection string (format: `redis://username:password@host:port/database_number`)

#### **Step 4: Add Redis URL to Environment Variables**
1. Go back to your **backend service** in Railway
2. Click on the **"Variables"** tab
3. Add these environment variables:
   ```bash
   REDIS_URL=redis://username:password@host:port/database_number
   CELERY_BROKER_URL=redis://username:password@host:port/database_number
   ```
   (Replace with the actual connection string you copied)

#### **Step 5: Verify Setup**
1. Check Railway logs for any connection errors
2. Test the connection by accessing your backend API
3. Monitor Redis usage in Railway dashboard

---

## 💻 **Option 2: Local Redis Setup (Development)**

### **Step-by-Step Setup**

#### **Step 1: Install Redis on macOS**
```bash
# Install Redis using Homebrew
brew install redis
```

#### **Step 2: Start Redis Server**
```bash
# Start Redis as a background service
brew services start redis

# Or start manually (for testing)
redis-server
```

#### **Step 3: Test Redis Connection**
```bash
# Test Redis CLI
redis-cli ping
# Expected output: PONG

# Test with Python
python3 -c "import redis; r = redis.Redis(host='localhost', port=6379, db=0); print('Redis connection successful:', r.ping())"
```

#### **Step 4: Install Redis Python Package**
```bash
# Install Redis Python client
pip3 install redis
```

#### **Step 5: Set Environment Variables**
```bash
# Add to your .env file
echo "REDIS_URL=redis://localhost:6379/0" >> .env
echo "CELERY_BROKER_URL=redis://localhost:6379/0" >> .env
```

#### **Step 6: Verify Local Setup**
```bash
# Test Redis connection
redis-cli ping

# Test Python connection
python3 -c "import redis; r = redis.Redis(host='localhost', port=6379, db=0); print('Redis connection successful:', r.ping())"

# Check Redis info
redis-cli info
```

---

## 🔧 **Redis Configuration**

### **Environment Variables**
```bash
# Redis Connection
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0

# Redis Configuration (Optional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=  # Leave empty for local development
```

### **Redis Configuration File**
Location: `/opt/homebrew/etc/redis.conf` (macOS with Homebrew)

Key settings:
```conf
# Network
bind 127.0.0.1
port 6379

# Memory
maxmemory 256mb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000

# Security (for production)
# requirepass your_password
```

---

## 🧪 **Testing Redis Setup**

### **Basic Connection Test**
```bash
# Test Redis server
redis-cli ping

# Test Python connection
python3 -c "
import redis
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    print('✅ Redis connection successful:', r.ping())
    print('✅ Redis version:', r.info()['redis_version'])
except Exception as e:
    print('❌ Redis connection failed:', e)
"
```

### **Celery Test**
```bash
# Test Celery with Redis
python3 -c "
from celery import Celery
try:
    app = Celery('test', broker='redis://localhost:6379/0')
    print('✅ Celery with Redis setup successful')
except Exception as e:
    print('❌ Celery with Redis setup failed:', e)
"
```

### **Performance Test**
```bash
# Test Redis performance
redis-benchmark -h localhost -p 6379 -n 1000 -c 10
```

---

## 🔍 **Troubleshooting**

### **Common Issues**

#### **1. Redis Connection Refused**
```bash
# Check if Redis is running
brew services list | grep redis

# Start Redis if not running
brew services start redis

# Check Redis logs
tail -f /opt/homebrew/var/log/redis.log
```

#### **2. Permission Denied**
```bash
# Check Redis permissions
ls -la /opt/homebrew/var/run/redis.pid

# Fix permissions if needed
sudo chown -R $(whoami) /opt/homebrew/var/run/redis.pid
```

#### **3. Port Already in Use**
```bash
# Check what's using port 6379
lsof -i :6379

# Kill process if needed
sudo kill -9 <PID>
```

#### **4. Python Redis Module Not Found**
```bash
# Install Redis Python package
pip3 install redis

# Or install in virtual environment
pip install redis
```

### **Redis Commands for Debugging**
```bash
# Connect to Redis CLI
redis-cli

# Check Redis info
INFO

# Check memory usage
INFO memory

# List all keys
KEYS *

# Monitor Redis commands
MONITOR

# Check Redis logs
redis-cli --latency
```

---

## 📊 **Monitoring Redis**

### **Redis CLI Monitoring**
```bash
# Real-time monitoring
redis-cli monitor

# Check memory usage
redis-cli info memory

# Check connected clients
redis-cli client list

# Check slow queries
redis-cli slowlog get 10
```

### **Redis GUI Tools**
- **RedisInsight**: https://redis.com/redis-enterprise/redis-insight/
- **Redis Desktop Manager**: https://rdm.dev/
- **Another Redis Desktop Manager**: https://github.com/qishibo/AnotherRedisDesktopManager

---

## 🔒 **Security Considerations**

### **Local Development**
- Redis runs on localhost only
- No password required
- Suitable for development only

### **Production (Railway)**
- Redis runs in secure cloud environment
- Connection string includes authentication
- Automatic backups and monitoring
- SSL/TLS encryption

---

## 📈 **Performance Optimization**

### **Redis Configuration**
```conf
# Memory optimization
maxmemory 512mb
maxmemory-policy allkeys-lru

# Persistence optimization
save 900 1
save 300 10
save 60 10000

# Network optimization
tcp-keepalive 300
```

### **Application Level**
```python
# Connection pooling
import redis
from redis import ConnectionPool

pool = ConnectionPool(host='localhost', port=6379, db=0, max_connections=20)
r = redis.Redis(connection_pool=pool)

# Pipeline for multiple operations
pipe = r.pipeline()
pipe.set('key1', 'value1')
pipe.set('key2', 'value2')
pipe.execute()
```

---

## ✅ **Setup Verification Checklist**

### **Local Development**
- [ ] Redis installed via Homebrew
- [ ] Redis service started (`brew services start redis`)
- [ ] Redis CLI test successful (`redis-cli ping`)
- [ ] Python Redis package installed (`pip3 install redis`)
- [ ] Python connection test successful
- [ ] Environment variables set in `.env`
- [ ] Celery broker configuration working

### **Production (Railway)**
- [ ] Redis service added to Railway project
- [ ] Connection string copied from Railway
- [ ] Environment variables added to backend service
- [ ] Backend deployment successful
- [ ] Redis connection verified in logs
- [ ] Background tasks working properly

---

## 🚀 **Next Steps**

After Redis setup is complete:

1. **Test your backend API** with Redis caching
2. **Verify background tasks** are working
3. **Monitor Redis performance** in production
4. **Set up Redis monitoring** and alerts
5. **Configure Redis backups** (Railway handles this automatically)

---

*Last Updated: $(date)*
*Redis Version: 8.0.3*
*Setup Status: ✅ Local development complete* 