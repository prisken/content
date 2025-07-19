const API_BASE_URL = process.env.BACKEND_URL || 'http://localhost:8000';

export const apiClient = {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

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

  // Content Generation
  async generateContent(data) {
    // Transform frontend data format to backend format
    const backendData = {
      content_direction: data.direction,
      content_type: data.platform,
      source_type: data.source,
      specific_content: data.topic,
      tone: data.tone,
      region: data.region || 'global',
      language: data.language || 'en',
      user_id: data.user_id || null
    };
    
    return this.request('/api/generate', {
      method: 'POST',
      body: backendData,
    });
  },

  // Image Generation
  async generateImage(data) {
    return this.request('/api/images/generate', {
      method: 'POST',
      body: data,
    });
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

// Content directions data
export const contentDirections = [
  { key: 'business_finance', name: 'Business & Finance', icon: '💼' },
  { key: 'technology', name: 'Technology', icon: '💻' },
  { key: 'health_wellness', name: 'Health & Wellness', icon: '🏥' },
  { key: 'education', name: 'Education', icon: '📚' },
  { key: 'entertainment', name: 'Entertainment', icon: '🎬' },
  { key: 'travel_tourism', name: 'Travel & Tourism', icon: '✈️' },
  { key: 'food_cooking', name: 'Food & Cooking', icon: '🍳' },
  { key: 'fashion_beauty', name: 'Fashion & Beauty', icon: '👗' },
  { key: 'sports_fitness', name: 'Sports & Fitness', icon: '⚽' },
  { key: 'science_research', name: 'Science & Research', icon: '🔬' },
  { key: 'politics_current_events', name: 'Politics & Current Events', icon: '📰' },
  { key: 'environment_sustainability', name: 'Environment & Sustainability', icon: '🌱' },
  { key: 'personal_development', name: 'Personal Development', icon: '🧠' },
  { key: 'parenting_family', name: 'Parenting & Family', icon: '👨‍👩‍👧‍👦' },
  { key: 'art_creativity', name: 'Art & Creativity', icon: '🎨' },
  { key: 'real_estate', name: 'Real Estate', icon: '🏠' },
  { key: 'automotive', name: 'Automotive', icon: '🚗' },
  { key: 'pet_care', name: 'Pet Care', icon: '🐕' },
];

// Platforms data
export const platforms = [
  { key: 'linkedin', name: 'LinkedIn', icon: '💼' },
  { key: 'facebook', name: 'Facebook', icon: '📘' },
  { key: 'instagram', name: 'Instagram', icon: '📷' },
  { key: 'twitter', name: 'Twitter', icon: '🐦' },
  { key: 'youtube_shorts', name: 'YouTube Shorts', icon: '📺' },
  { key: 'blog_article', name: 'Blog Article', icon: '📝' },
];

// Sources data
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

// Tones data
export const tones = [
  { key: 'professional', name: 'Professional' },
  { key: 'casual', name: 'Casual' },
  { key: 'inspirational', name: 'Inspirational' },
  { key: 'educational', name: 'Educational' },
  { key: 'entertaining', name: 'Entertaining' },
];

// Image styles data
export const imageStyles = [
  { key: 'modern', name: 'Modern' },
  { key: 'vintage', name: 'Vintage' },
  { key: 'minimalist', name: 'Minimalist' },
  { key: 'colorful', name: 'Colorful' },
  { key: 'professional', name: 'Professional' },
  { key: 'creative', name: 'Creative' },
]; 