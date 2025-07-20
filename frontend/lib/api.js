const API_BASE_URL = process.env.BACKEND_URL || 'https://content-contentmaker.up.railway.app';

export const apiClient = {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    // Get user from localStorage for admin requests
    let userEmail = null;
    try {
      const savedUser = localStorage.getItem('user');
      if (savedUser) {
        const user = JSON.parse(savedUser);
        userEmail = user.email;
      }
    } catch (error) {
      console.error('Error parsing user data:', error);
    }
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Add user email header for admin requests
    if (userEmail && endpoint.includes('/admin/')) {
      config.headers['X-User-Email'] = userEmail;
    }

    if (options.body) {
      config.body = JSON.stringify(options.body);
    }

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `API Error: ${response.status}`);
      }

      return response.json();
    } catch (error) {
      console.error('API Request Error:', error);
      throw error;
    }
  },

  // Health Check
  async healthCheck() {
    return this.request('/health');
  },

  // AI Content Generation
  async generateContent(data) {
    // Transform frontend data format to backend format
    const backendData = {
      direction: data.direction,
      platform: data.platform,
      postType: data.postType,
      source: data.source,
      sourceDetails: data.sourceDetails,
      selectedTopic: data.selectedTopic,
      tone: data.tone,
      language: data.language || 'en',
      imageStyle: data.imageStyle,
      generate_images: data.generate_images !== false // Default to true
    };
    
    return this.request('/api/generate', {
      method: 'POST',
      body: backendData,
    });
  },

  // Topic Generation with Google Search
  async generateTopics(data) {
    return this.request('/api/topics/generate', {
      method: 'POST',
      body: data,
    });
  },

  // Video Link Generation
  async generateVideoLink(data) {
    return this.request('/api/videos/generate-link', {
      method: 'POST',
      body: data,
    });
  },

  // Podcast Link Generation
  async generatePodcastLink(data) {
    return this.request('/api/podcasts/generate-link', {
      method: 'POST',
      body: data,
    });
  },

  // Google Search Integration
  async googleSearch(query, country = 'US') {
    return this.request('/api/google/search', {
      method: 'POST',
      body: { query, country },
    });
  },

  async googleNews(country = 'US', category = 'all') {
    return this.request('/api/google/news', {
      method: 'POST',
      body: { country, category },
    });
  },

  async googleTrends(query, country = 'US') {
    return this.request('/api/google/trends', {
      method: 'POST',
      body: { query, country },
    });
  },

  async googleBooks(query, country = 'US') {
    return this.request('/api/google/books', {
      method: 'POST',
      body: { query, country },
    });
  },

  // Image Generation
  async generateImage(data) {
    return this.request('/api/generate-image', {
      method: 'POST',
      body: data,
    });
  },

  // Get Image Specifications
  async getImageSpecs(platform) {
    return this.request(`/api/image-specs/${platform}`);
  },

  // Get Content Directions
  async getDirections() {
    return this.request('/api/directions');
  },

  // Get Platforms
  async getPlatforms() {
    return this.request('/api/platforms');
  },

  // Get Image Styles
  async getImageStyles() {
    return this.request('/api/images/styles');
  },

  // Get Sources
  async getSources() {
    return this.request('/api/sources');
  },

  // Get Tones
  async getTones() {
    return this.request('/api/tones');
  },

  // Authentication
  async login(credentials) {
    return this.request('/api/auth/login', {
      method: 'POST',
      body: credentials,
    });
  },

  async register(userData) {
    return this.request('/api/auth/register', {
      method: 'POST',
      body: userData,
    });
  },

  async logout() {
    return this.request('/api/auth/logout', {
      method: 'POST',
    });
  },

  // Admin user management
  async getUsers(params = {}) {
    const queryParams = new URLSearchParams(params)
    return this.request(`/api/admin/users?${queryParams}`);
  },

  async getUser(userId) {
    return this.request(`/api/admin/users/${userId}`);
  },

  async updateUser(userId, data) {
    return this.request(`/api/admin/users/${userId}`, {
      method: 'PUT',
      body: data,
    });
  },

  async deleteUser(userId) {
    return this.request(`/api/admin/users/${userId}`, {
      method: 'DELETE',
    });
  },

  async toggleUserStatus(userId) {
    return this.request(`/api/admin/users/${userId}/toggle-status`, {
      method: 'POST',
    });
  },

  async resetUserPassword(userId, newPassword) {
    return this.request(`/api/admin/users/${userId}/reset-password`, {
      method: 'POST',
      body: { new_password: newPassword },
    });
  },
};

// Content directions data - Updated to match design document exactly
export const contentDirections = [
  { key: 'business_finance', name: 'Business & Finance', icon: '💼' },
  { key: 'technology', name: 'Technology', icon: '💻' },
  { key: 'health_wellness', name: 'Health & Wellness', icon: '🏥' },
  { key: 'education', name: 'Education', icon: '📚' },
  { key: 'entertainment', name: 'Entertainment', icon: '🎬' },
  { key: 'travel', name: 'Travel & Tourism', icon: '✈️' },
  { key: 'food_cooking', name: 'Food & Cooking', icon: '🍳' },
  { key: 'fashion_beauty', name: 'Fashion & Beauty', icon: '👗' },
  { key: 'sports', name: 'Sports & Fitness', icon: '⚽' },
  { key: 'science_research', name: 'Science & Research', icon: '🔬' },
  { key: 'politics_society', name: 'Politics & Current Events', icon: '📰' },
  { key: 'environment_sustainability', name: 'Environment & Sustainability', icon: '🌱' },
  { key: 'lifestyle', name: 'Personal Development', icon: '🧠' },
  { key: 'parenting', name: 'Parenting & Family', icon: '👨‍👩‍👧‍👦' },
  { key: 'art_creativity', name: 'Art & Creativity', icon: '🎨' },
  { key: 'real_estate', name: 'Real Estate', icon: '🏠' },
  { key: 'automotive', name: 'Automotive', icon: '🚗' },
  { key: 'pets_animals', name: 'Pet Care', icon: '🐕' },
];

// Platforms data (legacy - now using enhancedPlatforms in generator.js)
export const platforms = [
  { key: 'linkedin', name: 'LinkedIn', icon: '💼' },
  { key: 'facebook', name: 'Facebook', icon: '📘' },
  { key: 'instagram', name: 'Instagram', icon: '📷' },
  { key: 'twitter', name: 'Twitter', icon: '🐦' },
  { key: 'youtube_shorts', name: 'YouTube Shorts', icon: '📺' },
  { key: 'blog_article', name: 'Blog Article', icon: '📝' },
];

// Sources data (legacy - now using enhancedSources in generator.js)
export const sources = [
  { key: 'personal_experience', name: 'Personal Experience' },
  { key: 'industry_trends', name: 'Industry Trends' },
  { key: 'customer_feedback', name: 'Customer Feedback' },
  { key: 'market_research', name: 'Market Research' },
  { key: 'competitor_analysis', name: 'Competitor Analysis' },
  { key: 'expert_interviews', name: 'Expert Interviews' },
  { key: 'case_studies', name: 'Case Studies' },
  { key: 'data_analytics', name: 'Data Analytics' },
  { key: 'trending_topics', name: 'Trending Topics' },
  { key: 'seasonal_events', name: 'Seasonal Events' },
];

// Tones data - Updated to match design document exactly (6 tones) with emojis
export const tones = [
  { key: 'professional', name: 'Professional', icon: '💼' },
  { key: 'casual', name: 'Casual', icon: '😊' },
  { key: 'inspirational', name: 'Inspirational', icon: '✨' },
  { key: 'educational', name: 'Educational', icon: '📚' },
  { key: 'entertaining', name: 'Entertaining', icon: '🎉' },
  { key: 'serious', name: 'Serious', icon: '🎯' },
];

// Image styles data
export const imageStyles = [
  { key: 'professional', name: 'Professional' },
  { key: 'creative', name: 'Creative' },
  { key: 'minimalist', name: 'Minimalist' },
  { key: 'vibrant', name: 'Vibrant' },
  { key: 'modern', name: 'Modern' },
  { key: 'natural', name: 'Natural' },
]; 