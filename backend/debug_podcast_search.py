#!/usr/bin/env python3
"""
Debug script specifically for podcast search
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_podcast_search():
    """Test podcast search specifically"""
    
    api_key = os.getenv('GOOGLE_CUSTOM_SEARCH_API_KEY')
    search_engine_id = os.getenv('GOOGLE_CUSTOM_SEARCH_ENGINE_ID')
    
    print("🎤 Testing Podcast Search Specifically")
    print("=" * 50)
    
    if not api_key or not search_engine_id:
        print("❌ API credentials not configured")
        return
    
    # Test different podcast search queries
    test_queries = [
        "business finance site:podcasts.apple.com",
        "entrepreneurship site:podcasts.apple.com",
        "technology AI site:podcasts.apple.com",
        "podcast business finance",
        "podcast entrepreneurship"
    ]
    
    base_url = "https://www.googleapis.com/customsearch/v1"
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🧪 Test {i}: '{query}'")
        print("-" * 40)
        
        params = {
            'key': api_key,
            'cx': search_engine_id,
            'q': query,
            'num': 3
        }
        
        try:
            response = requests.get(base_url, params=params, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                print(f"✅ Success! Found {len(items)} results")
                
                for j, item in enumerate(items, 1):
                    title = item.get('title', 'No title')
                    link = item.get('link', 'No link')
                    snippet = item.get('snippet', 'No description')
                    print(f"  {j}. {title}")
                    print(f"     URL: {link}")
                    print(f"     Description: {snippet[:100]}...")
                    print()
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text[:300]}...")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        print()

def test_google_search_service_podcast():
    """Test the actual GoogleSearchService podcast method"""
    
    print("\n🔧 Testing GoogleSearchService.search_podcasts()")
    print("=" * 50)
    
    try:
        from services.google_search_service import GoogleSearchService
        
        google_service = GoogleSearchService()
        
        # Test with different directions and categories
        test_cases = [
            ("business_finance", ["entrepreneurship", "investment"]),
            ("technology", ["AI", "programming"]),
            ("health_wellness", ["fitness", "nutrition"])
        ]
        
        for direction, categories in test_cases:
            print(f"\n🎯 Testing: {direction} with categories: {categories}")
            print("-" * 40)
            
            try:
                podcasts = google_service.search_podcasts(direction, categories, "US")
                print(f"✅ Found {len(podcasts)} podcasts")
                
                for i, podcast in enumerate(podcasts, 1):
                    print(f"  {i}. {podcast.get('title', 'No title')}")
                    print(f"     URL: {podcast.get('url', 'No URL')}")
                    print(f"     Host: {podcast.get('host', 'No host')}")
                    print()
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except ImportError as e:
        print(f"❌ Import error: {e}")

if __name__ == "__main__":
    print("🚀 Podcast Search Debug Tool")
    print("=" * 50)
    
    test_podcast_search()
    test_google_search_service_podcast()
    
    print("\n" + "=" * 50)
    print("📋 Analysis:")
    print("1. If direct API calls work but service doesn't:")
    print("   - Check the search_podcasts method implementation")
    print("   - Verify error handling and fallback logic")
    print("2. If API calls fail:")
    print("   - Check search engine configuration")
    print("   - Verify site restrictions work for podcasts.apple.com") 