// Test script to check podcast API response
const API_BASE_URL = 'https://content-contentmaker.up.railway.app';

async function testPodcastAPI() {
  console.log('🧪 Testing Podcast API...');
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/podcasts/generate-link`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        direction: 'business_finance',
        categories: {
          topics: ['entrepreneurship', 'investment']
        },
        country: 'US'
      })
    });
    
    console.log('📡 Response status:', response.status);
    
    const data = await response.json();
    console.log('📦 Full response:', data);
    
    if (data.success && data.data && data.data.podcasts) {
      console.log('✅ Podcasts found:', data.data.podcasts.length);
      data.data.podcasts.forEach((podcast, index) => {
        console.log(`🎧 Podcast ${index + 1}:`);
        console.log(`   Title: ${podcast.title}`);
        console.log(`   Host: ${podcast.host}`);
        console.log(`   URL: ${podcast.url}`);
        console.log(`   Description: ${podcast.description?.substring(0, 100)}...`);
        console.log('---');
      });
    } else {
      console.log('❌ No podcasts in response');
    }
    
  } catch (error) {
    console.error('❌ API Error:', error);
  }
}

// Run the test
testPodcastAPI(); 