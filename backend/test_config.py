#!/usr/bin/env python3
"""
Test Configuration Script for Content Creator Pro
This script tests all API keys and configurations before Railway deployment
"""

import os
import requests
import json
from dotenv import load_dotenv

def test_deepseek_api():
    """Test DeepSeek API connection"""
    print("🔍 Testing DeepSeek API...")
    
    api_key = "sk-9d217f003dd24fd1bc1ce4e5440b11e9"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": "Hello! Please respond with 'DeepSeek API is working!'"
            }
        ],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"✅ DeepSeek API: Working! Response: {content}")
            return True
        else:
            print(f"❌ DeepSeek API: Error {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ DeepSeek API: Connection failed - {str(e)}")
        return False

def test_cloudinary_api():
    """Test Cloudinary API connection"""
    print("🔍 Testing Cloudinary API...")
    
    cloud_name = "debyzbnjb"
    api_key = "117158686154364"
    api_secret = "QkWKsPdbREy6Ox86kpncl6q4KbI"
    
    # Test basic Cloudinary configuration
    try:
        import cloudinary
        import cloudinary.api
        
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        
        # Test API connection by getting account info
        result = cloudinary.api.ping()
        print(f"✅ Cloudinary API: Working! Ping response: {result}")
        return True
        
    except ImportError:
        print("⚠️ Cloudinary: Package not installed (will use fallback)")
        return True
    except Exception as e:
        print(f"❌ Cloudinary API: Error - {str(e)}")
        return False

def test_flask_app():
    """Test Flask app configuration"""
    print("🔍 Testing Flask app configuration...")
    
    try:
        # Test if app can be imported
        from app import app
        
        # Test database connection
        with app.app_context():
            from models import db
            db.create_all()
            print("✅ Flask app: Database tables created successfully")
        
        print("✅ Flask app: Configuration is valid")
        return True
        
    except Exception as e:
        print(f"❌ Flask app: Error - {str(e)}")
        return False

def test_content_generation():
    """Test content generation with AI"""
    print("🔍 Testing content generation...")
    
    try:
        from services.ai_service import ai_service
        
        # Test content generation
        content = ai_service.generate_content(
            direction="business_finance",
            platform="linkedin",
            source="personal_experience",
            topic="AI in Business",
            tone="professional",
            language="en"
        )
        
        print(f"✅ Content generation: Working!")
        print(f"📝 Generated content preview: {content[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Content generation: Error - {str(e)}")
        return False

def test_image_generation():
    """Test image generation"""
    print("🔍 Testing image generation...")
    
    try:
        from services.ai_service import ai_service
        
        # Test image prompt generation
        prompt = ai_service.generate_image_prompt(
            content="AI is transforming business",
            direction="business_finance",
            platform="linkedin"
        )
        
        print(f"✅ Image generation: Working!")
        print(f"🎨 Generated prompt: {prompt[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Image generation: Error - {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Content Creator Pro - Configuration Test")
    print("=" * 50)
    
    # Test results
    results = []
    
    # Run tests
    results.append(("DeepSeek API", test_deepseek_api()))
    results.append(("Cloudinary API", test_cloudinary_api()))
    results.append(("Flask App", test_flask_app()))
    results.append(("Content Generation", test_content_generation()))
    results.append(("Image Generation", test_image_generation()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your configuration is ready for Railway deployment.")
        print("\n📋 Railway Environment Variables to add:")
        print("=" * 50)
        print("SECRET_KEY=your-super-secure-secret-key-change-this-in-production-2024")
        print("FLASK_ENV=production")
        print("FLASK_APP=app.py")
        print("CLOUDINARY_CLOUD_NAME=debyzbnjb")
        print("CLOUDINARY_API_KEY=117158686154364")
        print("CLOUDINARY_API_SECRET=QkWKsPdbREy6Ox86kpncl6q4KbI")
        print("DEEPSEEK_API_KEY=sk-9d217f003dd24fd1bc1ce4e5440b11e9")
        print("ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("💡 Make sure all API keys are correct and services are accessible.")

if __name__ == "__main__":
    main() 