#!/usr/bin/env python3
"""
Test script to verify Google Custom Search API configuration
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_google_search_api():
    """Test Google Custom Search API configuration"""
    
    # Get API credentials from environment
    api_key = os.getenv('GOOGLE_CUSTOM_SEARCH_API_KEY')
    search_engine_id = os.getenv('GOOGLE_CUSTOM_SEARCH_ENGINE_ID')
    
    print("🔍 Testing Google Custom Search API Configuration")
    print("=" * 50)
    
    # Check if credentials are set
    if not api_key or api_key == 'your_google_search_api_key':
        print("❌ GOOGLE_CUSTOM_SEARCH_API_KEY not configured")
        print("   Please set your Google API key in the .env file")
        return False
    
    if not search_engine_id or search_engine_id == 'your_search_engine_id':
        print("❌ GOOGLE_CUSTOM_SEARCH_ENGINE_ID not configured")
        print("   Please set your Search Engine ID in the .env file")
        return False
    
    print("✅ API Key: Configured")
    print("✅ Search Engine ID: Configured")
    
    # Test the API
    try:
        # Test search for YouTube videos
        search_query = "business finance entrepreneurship site:youtube.com"
        url = "https://www.googleapis.com/customsearch/v1"
        
        params = {
            'key': api_key,
            'cx': search_engine_id,
            'q': search_query,
            'num': 3
        }
        
        print(f"\n🔍 Testing search: '{search_query}'")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            
            print("✅ API call successful!")
            print(f"📊 Found {len(items)} results")
            
            for i, item in enumerate(items, 1):
                title = item.get('title', 'No title')
                link = item.get('link', 'No link')
                print(f"  {i}. {title[:60]}...")
                print(f"     {link}")
            
            return True
            
        else:
            print(f"❌ API call failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {str(e)}")
        return False

def test_podcast_search():
    """Test podcast search functionality"""
    
    api_key = os.getenv('GOOGLE_CUSTOM_SEARCH_API_KEY')
    search_engine_id = os.getenv('GOOGLE_CUSTOM_SEARCH_ENGINE_ID')
    
    if not api_key or not search_engine_id:
        return False
    
    try:
        search_query = "business finance podcast"
        url = "https://www.googleapis.com/customsearch/v1"
        
        params = {
            'key': api_key,
            'cx': search_engine_id,
            'q': search_query,
            'sitesearch': 'podcasts.apple.com',
            'num': 3
        }
        
        print(f"\n🎤 Testing podcast search: '{search_query}'")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            
            print("✅ Podcast search successful!")
            print(f"📊 Found {len(items)} podcast results")
            
            for i, item in enumerate(items, 1):
                title = item.get('title', 'No title')
                link = item.get('link', 'No link')
                print(f"  {i}. {title[:60]}...")
                print(f"     {link}")
            
            return True
        else:
            print(f"❌ Podcast search failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing podcast search: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Google Custom Search API Test")
    print("=" * 50)
    
    # Test basic configuration
    config_ok = test_google_search_api()
    
    if config_ok:
        # Test podcast search
        test_podcast_search()
        
        print("\n" + "=" * 50)
        print("✅ Google API configuration is working!")
        print("🎉 You can now use real search results in your app")
    else:
        print("\n" + "=" * 50)
        print("❌ Please fix the configuration issues above")
        print("📖 Follow the setup guide to configure your API keys") 