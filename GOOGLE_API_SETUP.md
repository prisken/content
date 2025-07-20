# 🔍 Google Custom Search API Setup Guide

This guide will help you configure the Google Custom Search API to get real search results for videos and podcasts.

## 📋 Prerequisites

- Google account
- Access to Google Cloud Console
- Access to Google Custom Search Engine

## 🚀 Step-by-Step Setup

### Step 1: Create Google Cloud Project

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create New Project:**
   - Click the project dropdown at the top
   - Click "New Project"
   - Name: `Content Creator Pro`
   - Click "Create"

3. **Select the Project:**
   - Make sure your new project is selected

### Step 2: Enable Custom Search API

1. **Go to API Library:**
   - Navigate to "APIs & Services" > "Library"

2. **Search for Custom Search API:**
   - Search for "Custom Search API"
   - Click on "Custom Search API"

3. **Enable the API:**
   - Click "Enable"

### Step 3: Create API Key

1. **Go to Credentials:**
   - Navigate to "APIs & Services" > "Credentials"

2. **Create API Key:**
   - Click "Create Credentials" > "API Key"
   - Copy the generated API key (you'll need this)

3. **Restrict the API Key (Optional but Recommended):**
   - Click on the API key you just created
   - Under "Application restrictions" select "HTTP referrers"
   - Add your domain: `*.railway.app/*`
   - Under "API restrictions" select "Restrict key"
   - Select "Custom Search API"
   - Click "Save"

### Step 4: Create Custom Search Engine

1. **Go to Custom Search Engine:**
   - Visit: https://cse.google.com/cse/
   - Sign in with your Google account

2. **Create New Search Engine:**
   - Click "Add" to create a new search engine

3. **Configure Search Engine:**
   - **Sites to search:** Enter `youtube.com/*`
   - **Name:** `Content Creator Pro Search`
   - Click "Create"

4. **Get Search Engine ID:**
   - Go to "Setup" > "Basic"
   - Copy the "Search engine ID" (cx) - you'll need this

5. **Configure Search Settings:**
   - **Search the entire web:** Turn ON
   - **Sites to search:** Add these sites:
     - `youtube.com/*`
     - `podcasts.apple.com/*`
     - `spotify.com/*`
   - Click "Save"

### Step 5: Configure Environment Variables

1. **Edit your `.env` file:**
   ```bash
   # In backend/.env, update these lines:
   GOOGLE_CUSTOM_SEARCH_API_KEY=YOUR_ACTUAL_API_KEY_HERE
   GOOGLE_CUSTOM_SEARCH_ENGINE_ID=YOUR_ACTUAL_SEARCH_ENGINE_ID_HERE
   ```

2. **Replace the placeholders:**
   - `YOUR_ACTUAL_API_KEY_HERE` → Your Google API key
   - `YOUR_ACTUAL_SEARCH_ENGINE_ID_HERE` → Your Search Engine ID (cx)

### Step 6: Test Configuration

1. **Run the test script:**
   ```bash
   cd backend
   python3 test_google_api.py
   ```

2. **Expected output:**
   ```
   ✅ API Key: Configured
   ✅ Search Engine ID: Configured
   ✅ API call successful!
   📊 Found 3 results
   ```

## 🔧 Troubleshooting

### Common Issues

**1. "API key not valid" error:**
- Make sure you copied the API key correctly
- Check that the Custom Search API is enabled
- Verify the API key restrictions

**2. "Search engine not found" error:**
- Make sure you copied the Search Engine ID correctly
- Check that the search engine is configured properly

**3. "No results found" error:**
- Make sure "Search the entire web" is enabled
- Check that the sites are added to the search engine
- Try a different search query

### API Quotas

- **Free tier:** 100 searches per day
- **Paid tier:** $5 per 1000 searches
- Monitor usage in Google Cloud Console

## 🎯 What You'll Get

Once configured, your app will:

✅ **Real YouTube Videos:** Actual videos from YouTube search
✅ **Real Podcasts:** Actual podcasts from Apple Podcasts
✅ **Real URLs:** Clickable links to actual content
✅ **Real Metadata:** Titles, descriptions, thumbnails
✅ **Dynamic Results:** Different results on each refresh

## 🚀 Next Steps

1. Configure your API keys
2. Test with the provided script
3. Deploy your backend to Railway
4. Test the video and podcast generation in your app

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your API configuration
3. Test with the provided script
4. Check Google Cloud Console for errors

---

**Happy searching! 🎉** 