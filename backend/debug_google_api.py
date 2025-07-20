#!/usr/bin/env python3
"""
Debug script to test Google Custom Search API with different parameters
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_google_api_with_different_params():
    """Test Google API with various parameter combinations"""
    
    api_key = os.getenv('GOOGLE_CUSTOM_SEARCH_API_KEY')
    search_engine_id = os.getenv('GOOGLE_CUSTOM_SEARCH_ENGINE_ID')
    
    if not api_key or not search_engine_id:
        print("❌ API credentials not configured")
        return
    
    print("🔍 Testing Google Custom Search API with different parameters")
    print("=" * 60)
    
    # Test different search queries
    test_queries = [
        "business finance",
        "business finance site:youtube.com",
        "entrepreneurship",
        "entrepreneurship site:youtube.com",
        "technology AI",
        "technology AI site:youtube.com"
    ]
    
    base_url = "https://www.googleapis.com/customsearch/v1"
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🧪 Test {i}: '{query}'")
        print("-" * 40)
        
        # Test without searchType parameter
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
                    title = item.get('title', 'No title')[:50]
                    link = item.get('link', 'No link')
                    print(f"  {j}. {title}...")
                    print(f"     {link}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        print()

def test_search_engine_configuration():
    """Test if search engine is configured properly"""
    
    api_key = os.getenv('GOOGLE_CUSTOM_SEARCH_API_KEY')
    search_engine_id = os.getenv('GOOGLE_CUSTOM_SEARCH_ENGINE_ID')
    
    print("\n🔧 Testing Search Engine Configuration")
    print("=" * 60)
    
    # Test basic search without site restriction
    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': 'business finance',
        'num': 1
    }
    
    try:
        response = requests.get("https://www.googleapis.com/customsearch/v1", params=params, timeout=10)
        print(f"Basic search status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Basic search works - search engine is configured")
            
            # Check if search engine supports site restriction
            params['q'] = 'business finance site:youtube.com'
            response2 = requests.get("https://www.googleapis.com/customsearch/v1", params=params, timeout=10)
            print(f"Site-restricted search status: {response2.status_code}")
            
            if response2.status_code == 200:
                print("✅ Site restriction works")
            else:
                print("❌ Site restriction doesn't work - check search engine settings")
                print(f"Error: {response2.text[:200]}...")
        else:
            print("❌ Basic search failed - check API key and search engine ID")
            print(f"Error: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    print("🚀 Google Custom Search API Debug Tool")
    print("=" * 60)
    
    test_google_api_with_different_params()
    test_search_engine_configuration()
    
    print("\n" + "=" * 60)
    print("📋 Next Steps:")
    print("1. If basic search works but site restriction doesn't:")
    print("   - Go to https://cse.google.com/cse/")
    print("   - Edit your search engine")
    print("   - Add 'youtube.com/*' to sites to search")
    print("   - Enable 'Search the entire web'")
    print("2. If all searches fail:")
    print("   - Check your API key and search engine ID")
    print("   - Verify Custom Search API is enabled")
    print("   - Check API quotas in Google Cloud Console") 