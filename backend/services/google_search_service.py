import os
import requests
import json
from typing import List, Dict, Any
import time
import random

class GoogleSearchService:
    def __init__(self):
        self.api_key = os.environ.get('GOOGLE_CUSTOM_SEARCH_API_KEY')
        self.search_engine_id = os.environ.get('GOOGLE_CUSTOM_SEARCH_ENGINE_ID')
        self.trends_api_key = os.environ.get('GOOGLE_TRENDS_API_KEY')
        self.books_api_key = os.environ.get('GOOGLE_BOOKS_API_KEY')
        
        # Base URLs
        self.custom_search_url = "https://www.googleapis.com/customsearch/v1"
        self.books_api_url = "https://www.googleapis.com/books/v1/volumes"
        
        # Mock data for demo purposes when APIs are not available
        self.mock_topics = {
            'technology': [
                {'title': 'AI in Healthcare: Latest Developments', 'description': 'Exploring how artificial intelligence is transforming healthcare delivery', 'trending_score': 85},
                {'title': 'Cybersecurity Trends 2024', 'description': 'Key security challenges and solutions for modern businesses', 'trending_score': 78},
                {'title': 'Cloud Computing Best Practices', 'description': 'Optimizing cloud infrastructure for scalability and cost', 'trending_score': 72},
                {'title': 'Digital Transformation Strategies', 'description': 'How companies are adapting to the digital age', 'trending_score': 68},
                {'title': 'Machine Learning Applications', 'description': 'Real-world applications of ML in various industries', 'trending_score': 75}
            ],
            'business_finance': [
                {'title': 'Investment Strategies for 2024', 'description': 'Smart investment approaches for the current market', 'trending_score': 82},
                {'title': 'Startup Funding Trends', 'description': 'Latest developments in startup financing and venture capital', 'trending_score': 79},
                {'title': 'Sustainable Business Practices', 'description': 'How businesses are going green and staying profitable', 'trending_score': 76},
                {'title': 'Remote Work Management', 'description': 'Best practices for managing remote teams effectively', 'trending_score': 71},
                {'title': 'Digital Marketing ROI', 'description': 'Measuring and optimizing marketing campaign performance', 'trending_score': 74}
            ],
            'health_wellness': [
                {'title': 'Mental Health in the Digital Age', 'description': 'Managing stress and anxiety in our connected world', 'trending_score': 88},
                {'title': 'Nutrition Science Updates', 'description': 'Latest research on diet and health optimization', 'trending_score': 75},
                {'title': 'Fitness Technology Trends', 'description': 'How tech is revolutionizing personal fitness', 'trending_score': 73},
                {'title': 'Work-Life Balance Strategies', 'description': 'Achieving harmony between career and personal life', 'trending_score': 81},
                {'title': 'Preventive Healthcare', 'description': 'Proactive approaches to maintaining good health', 'trending_score': 77}
            ]
        }
    
    def search(self, query: str, country: str = 'US') -> Dict[str, Any]:
        """Perform Google Custom Search"""
        if not self.api_key or not self.search_engine_id:
            return self._mock_search_results(query, country)
        
        try:
            params = {
                'key': self.api_key,
                'cx': self.search_engine_id,
                'q': query,
                'gl': country.lower(),
                'num': 10
            }
            
            response = requests.get(self.custom_search_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return {
                'items': data.get('items', []),
                'search_time': data.get('searchTime', 0),
                'total_results': data.get('searchInformation', {}).get('totalResults', 0)
            }
            
        except Exception as e:
            print(f"Google Search error: {e}")
            return self._mock_search_results(query, country)
    
    def search_topics(self, direction: str, country: str, query: str = None) -> List[Dict[str, Any]]:
        """Generate topics using Google Search"""
        search_query = query or direction.replace('_', ' ')
        
        # Get search results
        search_results = self.search(search_query, country)
        
        # Generate topics from search results
        topics = []
        if search_results.get('items'):
            for i, item in enumerate(search_results['items'][:5]):
                title = item.get('title', '')
                snippet = item.get('snippet', '')
                
                # Create topic from search result
                topic = {
                    'title': title,
                    'description': snippet,
                    'trending_score': random.randint(60, 90),
                    'source': 'google_search',
                    'url': item.get('link', '')
                }
                topics.append(topic)
        
        # Fallback to mock topics if no results
        if not topics:
            topics = self.mock_topics.get(direction, self.mock_topics['technology'])
        
        return topics
    
    def get_news_topics(self, direction: str, country: str) -> List[Dict[str, Any]]:
        """Get topics from Google News"""
        # Mock news topics for demo
        news_topics = {
            'technology': [
                {'title': 'Tech Giants Announce New AI Initiatives', 'description': 'Major technology companies reveal their latest AI strategies', 'trending_score': 92},
                {'title': 'Cybersecurity Breach Affects Millions', 'description': 'Recent security incident highlights importance of digital protection', 'trending_score': 89},
                {'title': 'New Smartphone Features Revealed', 'description': 'Latest mobile technology innovations announced', 'trending_score': 85},
                {'title': 'Cloud Computing Market Growth', 'description': 'Industry report shows continued expansion of cloud services', 'trending_score': 78},
                {'title': 'Startup Funding Round Success', 'description': 'Innovative tech startup secures major investment', 'trending_score': 76}
            ],
            'business_finance': [
                {'title': 'Stock Market Reaches New Highs', 'description': 'Market analysis shows positive trends for investors', 'trending_score': 88},
                {'title': 'New Business Regulations Announced', 'description': 'Government introduces changes affecting business operations', 'trending_score': 85},
                {'title': 'Entrepreneur Success Story', 'description': 'Local business owner shares journey to success', 'trending_score': 82},
                {'title': 'Economic Recovery Indicators', 'description': 'Positive signs for economic growth and stability', 'trending_score': 79},
                {'title': 'Digital Payment Trends', 'description': 'Shift towards cashless transactions accelerates', 'trending_score': 75}
            ],
            'health_wellness': [
                {'title': 'Breakthrough in Mental Health Treatment', 'description': 'New therapy approach shows promising results for anxiety and depression', 'trending_score': 91},
                {'title': 'Fitness Trends for 2024', 'description': 'Popular workout routines and wellness practices gaining traction', 'trending_score': 87},
                {'title': 'Nutrition Science Update', 'description': 'Latest research on diet and its impact on health', 'trending_score': 84},
                {'title': 'Mental Health Awareness Campaign', 'description': 'Organizations promote mental wellness in the workplace', 'trending_score': 81},
                {'title': 'Wellness Technology Innovations', 'description': 'New apps and devices for health monitoring', 'trending_score': 78}
            ],
            'education': [
                {'title': 'Online Learning Platform Growth', 'description': 'Digital education continues to expand globally', 'trending_score': 89},
                {'title': 'New Teaching Methods Introduced', 'description': 'Innovative approaches to student engagement and learning', 'trending_score': 86},
                {'title': 'Education Technology Investment', 'description': 'Major funding for educational software and tools', 'trending_score': 83},
                {'title': 'Student Mental Health Support', 'description': 'Universities implement new wellness programs', 'trending_score': 80},
                {'title': 'Skills Gap Analysis Report', 'description': 'Study reveals changing demands in job market', 'trending_score': 77}
            ],
            'entertainment': [
                {'title': 'Streaming Service Competition Heats Up', 'description': 'New platforms enter the entertainment market', 'trending_score': 90},
                {'title': 'Blockbuster Movie Release', 'description': 'Highly anticipated film breaks box office records', 'trending_score': 87},
                {'title': 'Music Industry Digital Transformation', 'description': 'Artists adapt to new distribution methods', 'trending_score': 84},
                {'title': 'Gaming Industry Growth', 'description': 'Video game market continues expansion', 'trending_score': 81},
                {'title': 'Celebrity Social Media Impact', 'description': 'Influencers shape entertainment consumption', 'trending_score': 78}
            ],
            'lifestyle': [
                {'title': 'Sustainable Living Movement', 'description': 'More people adopt eco-friendly lifestyle choices', 'trending_score': 88},
                {'title': 'Minimalism Trend Continues', 'description': 'Decluttering and simple living gain popularity', 'trending_score': 85},
                {'title': 'Remote Work Lifestyle Changes', 'description': 'People adapt to work-from-home culture', 'trending_score': 82},
                {'title': 'Digital Detox Movement', 'description': 'People seek balance with technology use', 'trending_score': 79},
                {'title': 'Wellness Tourism Growth', 'description': 'Travel focused on health and relaxation', 'trending_score': 76}
            ],
            'sports': [
                {'title': 'Major Sports League Expansion', 'description': 'Professional leagues announce new teams and markets', 'trending_score': 92},
                {'title': 'Olympic Preparation Updates', 'description': 'Athletes and countries prepare for upcoming games', 'trending_score': 89},
                {'title': 'Sports Technology Innovation', 'description': 'New equipment and training methods emerge', 'trending_score': 86},
                {'title': 'Women in Sports Recognition', 'description': 'Increased visibility and support for female athletes', 'trending_score': 83},
                {'title': 'Youth Sports Development', 'description': 'Programs to encourage young athlete participation', 'trending_score': 80}
            ],
            'food_cooking': [
                {'title': 'Plant-Based Diet Revolution', 'description': 'More people embrace vegetarian and vegan lifestyles', 'trending_score': 88},
                {'title': 'Home Cooking Renaissance', 'description': 'People rediscover joy of cooking at home', 'trending_score': 85},
                {'title': 'Food Delivery Service Growth', 'description': 'Online ordering continues to expand', 'trending_score': 82},
                {'title': 'Sustainable Food Practices', 'description': 'Farm-to-table and organic movements grow', 'trending_score': 79},
                {'title': 'International Cuisine Popularity', 'description': 'Global flavors gain mainstream acceptance', 'trending_score': 76}
            ],
            'travel': [
                {'title': 'Post-Pandemic Travel Boom', 'description': 'Tourism industry sees strong recovery', 'trending_score': 90},
                {'title': 'Sustainable Tourism Growth', 'description': 'Eco-friendly travel options gain popularity', 'trending_score': 87},
                {'title': 'Digital Nomad Lifestyle', 'description': 'Remote workers embrace location independence', 'trending_score': 84},
                {'title': 'Adventure Travel Trends', 'description': 'Experiential and outdoor tourism grows', 'trending_score': 81},
                {'title': 'Local Tourism Promotion', 'description': 'Communities focus on domestic visitors', 'trending_score': 78}
            ],
            'fashion_beauty': [
                {'title': 'Sustainable Fashion Movement', 'description': 'Eco-friendly clothing and accessories gain traction', 'trending_score': 89},
                {'title': 'Digital Fashion Innovation', 'description': 'Virtual clothing and AR try-on technology', 'trending_score': 86},
                {'title': 'Inclusive Beauty Standards', 'description': 'Diversity and representation in beauty industry', 'trending_score': 83},
                {'title': 'Vintage Fashion Revival', 'description': 'Retro styles make comeback in modern wardrobes', 'trending_score': 80},
                {'title': 'Beauty Technology Advances', 'description': 'Smart skincare devices and apps', 'trending_score': 77}
            ],
            'parenting': [
                {'title': 'Digital Parenting Challenges', 'description': 'Managing children\'s screen time and online safety', 'trending_score': 88},
                {'title': 'Mental Health Support for Parents', 'description': 'Resources for parental stress and anxiety', 'trending_score': 85},
                {'title': 'Educational Technology for Kids', 'description': 'Learning apps and digital tools for children', 'trending_score': 82},
                {'title': 'Work-Life Balance for Parents', 'description': 'Strategies for managing career and family', 'trending_score': 79},
                {'title': 'Parenting Styles Research', 'description': 'Studies on effective child-rearing approaches', 'trending_score': 76}
            ],
            'pets_animals': [
                {'title': 'Pet Adoption Surge', 'description': 'More people welcome pets into their homes', 'trending_score': 87},
                {'title': 'Pet Technology Innovation', 'description': 'Smart devices and apps for pet care', 'trending_score': 84},
                {'title': 'Animal Welfare Awareness', 'description': 'Increased focus on ethical treatment of animals', 'trending_score': 81},
                {'title': 'Pet Health and Nutrition', 'description': 'Advances in veterinary care and pet food', 'trending_score': 78},
                {'title': 'Wildlife Conservation Efforts', 'description': 'Protection of endangered species and habitats', 'trending_score': 75}
            ],
            'automotive': [
                {'title': 'Electric Vehicle Market Growth', 'description': 'EV adoption accelerates globally', 'trending_score': 91},
                {'title': 'Autonomous Driving Technology', 'description': 'Self-driving cars advance toward mainstream', 'trending_score': 88},
                {'title': 'Car Sharing Services Expansion', 'description': 'Alternative transportation options grow', 'trending_score': 85},
                {'title': 'Automotive Safety Innovations', 'description': 'New technologies improve road safety', 'trending_score': 82},
                {'title': 'Sustainable Transportation', 'description': 'Green alternatives to traditional vehicles', 'trending_score': 79}
            ],
            'real_estate': [
                {'title': 'Housing Market Trends', 'description': 'Analysis of current real estate conditions', 'trending_score': 89},
                {'title': 'Remote Work Impact on Housing', 'description': 'How work-from-home changes housing preferences', 'trending_score': 86},
                {'title': 'Sustainable Building Practices', 'description': 'Green construction and energy efficiency', 'trending_score': 83},
                {'title': 'Real Estate Technology', 'description': 'Digital tools for buying and selling property', 'trending_score': 80},
                {'title': 'Urban Development Projects', 'description': 'City planning and infrastructure improvements', 'trending_score': 77}
            ],
            'science_research': [
                {'title': 'Breakthrough Scientific Discovery', 'description': 'Major advancement in research field', 'trending_score': 92},
                {'title': 'Climate Change Research Update', 'description': 'Latest findings on environmental impact', 'trending_score': 89},
                {'title': 'Medical Research Innovation', 'description': 'New treatments and therapies developed', 'trending_score': 86},
                {'title': 'Space Exploration Progress', 'description': 'Advances in astronomy and space technology', 'trending_score': 83},
                {'title': 'Renewable Energy Research', 'description': 'Sustainable energy solutions development', 'trending_score': 80}
            ],
            'politics_society': [
                {'title': 'Election Season Analysis', 'description': 'Political landscape and voter engagement', 'trending_score': 90},
                {'title': 'Social Justice Movements', 'description': 'Activism and advocacy for equality', 'trending_score': 87},
                {'title': 'Policy Changes Impact', 'description': 'How new laws affect communities', 'trending_score': 84},
                {'title': 'Civic Engagement Trends', 'description': 'Public participation in democracy', 'trending_score': 81},
                {'title': 'International Relations', 'description': 'Global diplomacy and cooperation', 'trending_score': 78}
            ],
            'environment_sustainability': [
                {'title': 'Climate Action Initiatives', 'description': 'Global efforts to address climate change', 'trending_score': 91},
                {'title': 'Renewable Energy Adoption', 'description': 'Transition to sustainable power sources', 'trending_score': 88},
                {'title': 'Plastic Pollution Solutions', 'description': 'Innovations in waste reduction', 'trending_score': 85},
                {'title': 'Biodiversity Conservation', 'description': 'Protection of ecosystems and species', 'trending_score': 82},
                {'title': 'Sustainable Agriculture', 'description': 'Eco-friendly farming practices', 'trending_score': 79}
            ],
            'art_creativity': [
                {'title': 'Digital Art Revolution', 'description': 'AI and technology transforming artistic creation', 'trending_score': 90},
                {'title': 'Creative Industry Growth', 'description': 'Expansion of creative and design sectors', 'trending_score': 87},
                {'title': 'Artistic Expression Trends', 'description': 'New forms of creative self-expression emerging', 'trending_score': 84},
                {'title': 'Design Innovation', 'description': 'Breakthroughs in graphic and product design', 'trending_score': 81},
                {'title': 'Creative Entrepreneurship', 'description': 'Artists and creators building successful businesses', 'trending_score': 78}
            ]
        }
        
        return news_topics.get(direction, news_topics['technology'])
    
    def get_trending_topics(self, direction: str, country: str) -> List[Dict[str, Any]]:
        """Get trending topics from Google Trends"""
        # Mock trending topics for demo
        trending_topics = {
            'technology': [
                {'title': 'Artificial Intelligence Breakthroughs', 'description': 'Latest AI developments capturing public interest', 'trending_score': 95},
                {'title': 'Cybersecurity Awareness', 'description': 'Growing concern about online security', 'trending_score': 91},
                {'title': 'Remote Work Tools', 'description': 'Popular software for distributed teams', 'trending_score': 87},
                {'title': 'Sustainable Technology', 'description': 'Green tech solutions gaining popularity', 'trending_score': 84},
                {'title': 'Digital Privacy', 'description': 'Data protection and privacy concerns', 'trending_score': 82}
            ],
            'business_finance': [
                {'title': 'Cryptocurrency Market', 'description': 'Digital currency trends and developments', 'trending_score': 93},
                {'title': 'Remote Work Economy', 'description': 'Impact of work-from-home on business', 'trending_score': 89},
                {'title': 'Sustainable Investing', 'description': 'ESG investment strategies gaining traction', 'trending_score': 86},
                {'title': 'Small Business Recovery', 'description': 'Support programs for local businesses', 'trending_score': 83},
                {'title': 'Digital Banking', 'description': 'Fintech innovations in banking', 'trending_score': 80}
            ],
            'health_wellness': [
                {'title': 'Mental Health Awareness', 'description': 'Growing focus on psychological well-being', 'trending_score': 94},
                {'title': 'Fitness Technology', 'description': 'Wearables and apps for health tracking', 'trending_score': 90},
                {'title': 'Plant-Based Nutrition', 'description': 'Vegan and vegetarian lifestyle trends', 'trending_score': 87},
                {'title': 'Sleep Optimization', 'description': 'Better sleep habits and technology', 'trending_score': 84},
                {'title': 'Mindfulness Practices', 'description': 'Meditation and stress reduction techniques', 'trending_score': 81}
            ],
            'education': [
                {'title': 'Online Learning Platforms', 'description': 'Digital education tools and courses', 'trending_score': 92},
                {'title': 'Coding Bootcamps', 'description': 'Programming education for career changers', 'trending_score': 89},
                {'title': 'Microlearning', 'description': 'Short-form educational content', 'trending_score': 86},
                {'title': 'STEM Education', 'description': 'Science, technology, engineering, and math focus', 'trending_score': 83},
                {'title': 'Lifelong Learning', 'description': 'Continuous education for adults', 'trending_score': 80}
            ],
            'entertainment': [
                {'title': 'Streaming Wars', 'description': 'Competition between entertainment platforms', 'trending_score': 93},
                {'title': 'Social Media Content', 'description': 'Viral videos and trending posts', 'trending_score': 90},
                {'title': 'Gaming Industry', 'description': 'Video games and esports growth', 'trending_score': 87},
                {'title': 'Podcast Popularity', 'description': 'Audio content consumption trends', 'trending_score': 84},
                {'title': 'Celebrity Culture', 'description': 'Influencer and celebrity impact', 'trending_score': 81}
            ],
            'lifestyle': [
                {'title': 'Minimalism Movement', 'description': 'Decluttering and simple living', 'trending_score': 91},
                {'title': 'Digital Detox', 'description': 'Reducing screen time and tech dependence', 'trending_score': 88},
                {'title': 'Sustainable Living', 'description': 'Eco-friendly lifestyle choices', 'trending_score': 85},
                {'title': 'Work-Life Balance', 'description': 'Managing career and personal life', 'trending_score': 82},
                {'title': 'Wellness Tourism', 'description': 'Health-focused travel experiences', 'trending_score': 79}
            ],
            'sports': [
                {'title': 'Esports Growth', 'description': 'Competitive gaming popularity', 'trending_score': 94},
                {'title': 'Fitness Technology', 'description': 'Smart equipment and tracking devices', 'trending_score': 90},
                {'title': 'Women in Sports', 'description': 'Female athlete recognition and support', 'trending_score': 87},
                {'title': 'Sports Analytics', 'description': 'Data-driven performance optimization', 'trending_score': 84},
                {'title': 'Youth Sports', 'description': 'Children\'s athletic development', 'trending_score': 81}
            ],
            'food_cooking': [
                {'title': 'Plant-Based Diets', 'description': 'Vegan and vegetarian lifestyle trends', 'trending_score': 92},
                {'title': 'Home Cooking Revival', 'description': 'DIY meal preparation popularity', 'trending_score': 89},
                {'title': 'Food Delivery Apps', 'description': 'Online ordering and delivery services', 'trending_score': 86},
                {'title': 'Sustainable Food', 'description': 'Organic and locally sourced ingredients', 'trending_score': 83},
                {'title': 'International Cuisine', 'description': 'Global flavors and fusion cooking', 'trending_score': 80}
            ],
            'travel': [
                {'title': 'Post-Pandemic Travel', 'description': 'Tourism recovery and new trends', 'trending_score': 93},
                {'title': 'Sustainable Tourism', 'description': 'Eco-friendly travel options', 'trending_score': 90},
                {'title': 'Digital Nomad Lifestyle', 'description': 'Remote work and travel combination', 'trending_score': 87},
                {'title': 'Adventure Travel', 'description': 'Experiential and outdoor tourism', 'trending_score': 84},
                {'title': 'Local Tourism', 'description': 'Domestic and community-focused travel', 'trending_score': 81}
            ],
            'fashion_beauty': [
                {'title': 'Sustainable Fashion', 'description': 'Eco-friendly clothing and accessories', 'trending_score': 91},
                {'title': 'Digital Fashion', 'description': 'Virtual clothing and AR try-on', 'trending_score': 88},
                {'title': 'Inclusive Beauty', 'description': 'Diversity in beauty standards', 'trending_score': 85},
                {'title': 'Vintage Revival', 'description': 'Retro and nostalgic fashion trends', 'trending_score': 82},
                {'title': 'Beauty Technology', 'description': 'Smart skincare and beauty devices', 'trending_score': 79}
            ],
            'parenting': [
                {'title': 'Digital Parenting', 'description': 'Managing children\'s screen time', 'trending_score': 90},
                {'title': 'Mental Health Support', 'description': 'Parental stress and anxiety resources', 'trending_score': 87},
                {'title': 'Educational Technology', 'description': 'Learning apps and digital tools for kids', 'trending_score': 84},
                {'title': 'Work-Life Balance', 'description': 'Managing career and family responsibilities', 'trending_score': 81},
                {'title': 'Parenting Styles', 'description': 'Different approaches to child-rearing', 'trending_score': 78}
            ],
            'pets_animals': [
                {'title': 'Pet Adoption', 'description': 'Animal adoption and rescue trends', 'trending_score': 89},
                {'title': 'Pet Technology', 'description': 'Smart devices and apps for pets', 'trending_score': 86},
                {'title': 'Animal Welfare', 'description': 'Ethical treatment and protection of animals', 'trending_score': 83},
                {'title': 'Pet Health', 'description': 'Veterinary care and pet nutrition', 'trending_score': 80},
                {'title': 'Wildlife Conservation', 'description': 'Protection of endangered species', 'trending_score': 77}
            ],
            'automotive': [
                {'title': 'Electric Vehicles', 'description': 'EV adoption and charging infrastructure', 'trending_score': 94},
                {'title': 'Autonomous Driving', 'description': 'Self-driving car technology', 'trending_score': 91},
                {'title': 'Car Sharing', 'description': 'Alternative transportation services', 'trending_score': 88},
                {'title': 'Automotive Safety', 'description': 'Advanced safety features and technology', 'trending_score': 85},
                {'title': 'Sustainable Transportation', 'description': 'Green alternatives to traditional vehicles', 'trending_score': 82}
            ],
            'real_estate': [
                {'title': 'Real Estate Market', 'description': 'Property market trends and analysis', 'trending_score': 88},
                {'title': 'Investment Properties', 'description': 'Real estate investment strategies', 'trending_score': 85},
                {'title': 'Home Improvement', 'description': 'DIY and renovation projects', 'trending_score': 82},
                {'title': 'Sustainable Building', 'description': 'Green construction practices', 'trending_score': 79},
                {'title': 'Real Estate Technology', 'description': 'Digital tools for property', 'trending_score': 76}
            ],
            'science_research': [
                {'title': 'Scientific Breakthroughs', 'description': 'Latest discoveries and innovations', 'trending_score': 95},
                {'title': 'Climate Change Research', 'description': 'Environmental impact studies', 'trending_score': 92},
                {'title': 'Medical Research', 'description': 'Healthcare and treatment developments', 'trending_score': 89},
                {'title': 'Space Exploration', 'description': 'Astronomy and space technology', 'trending_score': 86},
                {'title': 'Renewable Energy', 'description': 'Sustainable energy solutions', 'trending_score': 83}
            ],
            'politics_society': [
                {'title': 'Political Analysis and Commentary', 'description': 'Understanding political events and trends', 'trending_score': 91},
                {'title': 'Social Justice Discussions', 'description': 'Important societal issues and equality', 'trending_score': 88},
                {'title': 'Civic Engagement Guide', 'description': 'How to participate in democracy effectively', 'trending_score': 85},
                {'title': 'Policy Impact Analysis', 'description': 'How laws and policies affect communities', 'trending_score': 82},
                {'title': 'International Relations Updates', 'description': 'Global political developments and diplomacy', 'trending_score': 79}
            ],
            'environment_sustainability': [
                {'title': 'Environmental Science Explained', 'description': 'Understanding environmental issues', 'trending_score': 91},
                {'title': 'Sustainable Living Practices', 'description': 'Eco-friendly lifestyle tips', 'trending_score': 88},
                {'title': 'Climate Change Updates', 'description': 'Latest climate science and news', 'trending_score': 85},
                {'title': 'Conservation Efforts', 'description': 'Protecting the environment', 'trending_score': 82},
                {'title': 'Green Technology Innovations', 'description': 'Sustainable technology solutions', 'trending_score': 79}
            ],
            'art_creativity': [
                {'title': 'Creative Process Podcast', 'description': 'Behind-the-scenes of artistic creation and design', 'trending_score': 87},
                {'title': 'Art Industry Insights', 'description': 'Understanding the business side of creativity', 'trending_score': 84},
                {'title': 'Design Thinking Discussions', 'description': 'Creative problem-solving and innovation', 'trending_score': 81},
                {'title': 'Artist Interviews and Stories', 'description': 'Personal journeys from creative professionals', 'trending_score': 78},
                {'title': 'Creative Inspiration Sessions', 'description': 'Motivational content for artists and designers', 'trending_score': 75}
            ]
        }
        
        return trending_topics.get(direction, trending_topics['technology'])
    
    def get_book_topics(self, direction: str, country: str, query: str = None) -> List[Dict[str, Any]]:
        """Get topics from Google Books"""
        if not self.books_api_key:
            return self._mock_book_topics(direction)
        
        try:
            search_query = query or direction.replace('_', ' ')
            params = {
                'key': self.books_api_key,
                'q': search_query,
                'maxResults': 5,
                'orderBy': 'relevance'
            }
            
            response = requests.get(self.books_api_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            topics = []
            
            for item in data.get('items', []):
                volume_info = item.get('volumeInfo', {})
                title = volume_info.get('title', '')
                description = volume_info.get('description', '')
                
                topic = {
                    'title': f"Book: {title}",
                    'description': description[:200] + '...' if len(description) > 200 else description,
                    'trending_score': random.randint(65, 85),
                    'source': 'google_books',
                    'authors': volume_info.get('authors', []),
                    'published_date': volume_info.get('publishedDate', '')
                }
                topics.append(topic)
            
            return topics
            
        except Exception as e:
            print(f"Google Books error: {e}")
            return self._mock_book_topics(direction)
    
    def get_youtube_topics(self, direction: str, country: str) -> List[Dict[str, Any]]:
        """Get topics from YouTube (mock implementation)"""
        # For now, return mock data. In production, this would use YouTube Data API
        youtube_topics = {
            'technology': [
                {'title': 'AI Tutorial: Getting Started', 'description': 'Beginner-friendly guide to artificial intelligence', 'trending_score': 88},
                {'title': 'Cybersecurity Best Practices', 'description': 'Essential security tips for everyone', 'trending_score': 85},
                {'title': 'Programming for Beginners', 'description': 'Learn to code from scratch', 'trending_score': 82},
                {'title': 'Tech Product Reviews', 'description': 'Honest reviews of latest gadgets', 'trending_score': 79},
                {'title': 'Digital Transformation Guide', 'description': 'How to modernize your business', 'trending_score': 76}
            ],
            'business_finance': [
                {'title': 'Investment Strategies Explained', 'description': 'Smart ways to grow your money', 'trending_score': 90},
                {'title': 'Entrepreneurship Tips', 'description': 'Advice for aspiring business owners', 'trending_score': 87},
                {'title': 'Personal Finance Management', 'description': 'Budgeting and saving strategies', 'trending_score': 84},
                {'title': 'Stock Market Analysis', 'description': 'Understanding market trends', 'trending_score': 81},
                {'title': 'Business Growth Strategies', 'description': 'Scaling your business effectively', 'trending_score': 78}
            ],
            'health_wellness': [
                {'title': 'Mental Health Tips and Tricks', 'description': 'Practical advice for mental wellness', 'trending_score': 89},
                {'title': 'Fitness Workout Routines', 'description': 'Effective exercise programs for all levels', 'trending_score': 86},
                {'title': 'Nutrition and Diet Guide', 'description': 'Healthy eating habits and meal planning', 'trending_score': 83},
                {'title': 'Sleep Improvement Techniques', 'description': 'Better sleep habits and routines', 'trending_score': 80},
                {'title': 'Mindfulness and Meditation', 'description': 'Stress reduction and mental clarity', 'trending_score': 77}
            ],
            'education': [
                {'title': 'Online Learning Tips', 'description': 'How to succeed in digital education', 'trending_score': 88},
                {'title': 'Study Techniques and Methods', 'description': 'Effective learning strategies', 'trending_score': 85},
                {'title': 'Career Development Advice', 'description': 'Professional growth and advancement', 'trending_score': 82},
                {'title': 'Skill Building Tutorials', 'description': 'Learn new abilities and competencies', 'trending_score': 79},
                {'title': 'Educational Technology Reviews', 'description': 'Best tools for learning', 'trending_score': 76}
            ],
            'entertainment': [
                {'title': 'Movie Reviews and Analysis', 'description': 'In-depth film discussions and critiques', 'trending_score': 91},
                {'title': 'Music Industry Insights', 'description': 'Behind-the-scenes of the music world', 'trending_score': 88},
                {'title': 'Gaming Content and Reviews', 'description': 'Video game analysis and gameplay', 'trending_score': 85},
                {'title': 'Celebrity News and Gossip', 'description': 'Latest updates from the entertainment world', 'trending_score': 82},
                {'title': 'Comedy and Entertainment', 'description': 'Funny and engaging content', 'trending_score': 79}
            ],
            'lifestyle': [
                {'title': 'Minimalism and Decluttering', 'description': 'Simple living and organization tips', 'trending_score': 87},
                {'title': 'Digital Detox Challenges', 'description': 'Reducing screen time and tech dependence', 'trending_score': 84},
                {'title': 'Sustainable Living Tips', 'description': 'Eco-friendly lifestyle choices', 'trending_score': 81},
                {'title': 'Work-Life Balance Strategies', 'description': 'Managing career and personal life', 'trending_score': 78},
                {'title': 'Wellness and Self-Care', 'description': 'Taking care of yourself', 'trending_score': 75}
            ],
            'sports': [
                {'title': 'Sports Analysis and Commentary', 'description': 'Expert insights on games and players', 'trending_score': 90},
                {'title': 'Fitness and Training Tips', 'description': 'Athletic performance improvement', 'trending_score': 87},
                {'title': 'Sports News and Updates', 'description': 'Latest developments in sports world', 'trending_score': 84},
                {'title': 'Athlete Interviews and Stories', 'description': 'Personal stories from sports stars', 'trending_score': 81},
                {'title': 'Sports Technology Reviews', 'description': 'Latest equipment and gear', 'trending_score': 78}
            ],
            'food_cooking': [
                {'title': 'Cooking Tutorials and Recipes', 'description': 'Step-by-step cooking instructions', 'trending_score': 89},
                {'title': 'Food Reviews and Tastings', 'description': 'Restaurant and food product reviews', 'trending_score': 86},
                {'title': 'Healthy Eating Guides', 'description': 'Nutrition and meal planning advice', 'trending_score': 83},
                {'title': 'International Cuisine Exploration', 'description': 'Global flavors and cooking techniques', 'trending_score': 80},
                {'title': 'Food Science and History', 'description': 'Interesting facts about food', 'trending_score': 77}
            ],
            'travel': [
                {'title': 'Travel Vlogs and Adventures', 'description': 'Real travel experiences and destinations', 'trending_score': 92},
                {'title': 'Travel Tips and Planning', 'description': 'How to plan the perfect trip', 'trending_score': 89},
                {'title': 'Budget Travel Guides', 'description': 'Affordable travel options and tips', 'trending_score': 86},
                {'title': 'Cultural Exploration', 'description': 'Learning about different cultures', 'trending_score': 83},
                {'title': 'Travel Photography Tips', 'description': 'Capturing amazing travel moments', 'trending_score': 80}
            ],
            'fashion_beauty': [
                {'title': 'Fashion Trends and Style Tips', 'description': 'Latest fashion advice and trends', 'trending_score': 88},
                {'title': 'Beauty Tutorials and Reviews', 'description': 'Makeup and skincare guides', 'trending_score': 85},
                {'title': 'Sustainable Fashion Guide', 'description': 'Eco-friendly clothing choices', 'trending_score': 82},
                {'title': 'Body Positivity and Confidence', 'description': 'Self-love and acceptance', 'trending_score': 79},
                {'title': 'Fashion History and Culture', 'description': 'Understanding fashion evolution', 'trending_score': 76}
            ],
            'parenting': [
                {'title': 'Parenting Tips and Advice', 'description': 'Practical advice for parents', 'trending_score': 87},
                {'title': 'Child Development Insights', 'description': 'Understanding child growth and behavior', 'trending_score': 84},
                {'title': 'Family Activities and Crafts', 'description': 'Fun things to do with kids', 'trending_score': 81},
                {'title': 'Parenting Challenges and Solutions', 'description': 'Dealing with common parenting issues', 'trending_score': 78},
                {'title': 'Educational Content for Kids', 'description': 'Learning videos for children', 'trending_score': 75}
            ],
            'pets_animals': [
                {'title': 'Pet Care Tips and Advice', 'description': 'How to take care of your pets', 'trending_score': 86},
                {'title': 'Animal Training Techniques', 'description': 'Training pets effectively', 'trending_score': 83},
                {'title': 'Pet Health and Nutrition', 'description': 'Keeping pets healthy and happy', 'trending_score': 80},
                {'title': 'Wildlife and Nature Content', 'description': 'Amazing animal videos and facts', 'trending_score': 77},
                {'title': 'Pet Adoption Stories', 'description': 'Heartwarming rescue and adoption tales', 'trending_score': 74}
            ],
            'automotive': [
                {'title': 'Car Reviews and Comparisons', 'description': 'Detailed vehicle analysis', 'trending_score': 91},
                {'title': 'Automotive Technology Updates', 'description': 'Latest car innovations and features', 'trending_score': 88},
                {'title': 'Car Maintenance Tips', 'description': 'How to maintain your vehicle', 'trending_score': 85},
                {'title': 'Electric Vehicle Guide', 'description': 'Everything about EVs', 'trending_score': 82},
                {'title': 'Driving Tips and Safety', 'description': 'Safe driving practices', 'trending_score': 79}
            ],
            'real_estate': [
                {'title': 'Real Estate Market Analysis', 'description': 'Understanding property markets', 'trending_score': 88},
                {'title': 'Home Buying and Selling Tips', 'description': 'Real estate transaction advice', 'trending_score': 85},
                {'title': 'Home Improvement Projects', 'description': 'DIY and renovation ideas', 'trending_score': 82},
                {'title': 'Property Investment Strategies', 'description': 'Real estate investment advice', 'trending_score': 79},
                {'title': 'Interior Design Inspiration', 'description': 'Home decoration and design', 'trending_score': 76}
            ],

            'science_research': [
                {'title': 'Scientific Discoveries Explained', 'description': 'Understanding complex scientific concepts', 'trending_score': 92},
                {'title': 'Research Methodology Guide', 'description': 'How scientific research works', 'trending_score': 89},
                {'title': 'Science News and Updates', 'description': 'Latest scientific developments', 'trending_score': 86},
                {'title': 'Educational Science Content', 'description': 'Learning about science', 'trending_score': 83},
                {'title': 'Science Experiments and Demonstrations', 'description': 'Hands-on science learning', 'trending_score': 80}
            ],
            'politics_society': [
                {'title': 'Political Analysis and Commentary', 'description': 'Understanding political events', 'trending_score': 90},
                {'title': 'Social Issues Discussion', 'description': 'Important societal topics', 'trending_score': 87},
                {'title': 'Civic Engagement Guide', 'description': 'How to participate in democracy', 'trending_score': 84},
                {'title': 'Policy Impact Analysis', 'description': 'How laws affect society', 'trending_score': 81},
                {'title': 'International Relations Updates', 'description': 'Global political developments', 'trending_score': 78}
            ],
            'environment_sustainability': [
                {'title': 'Environmental Science Explained', 'description': 'Understanding environmental issues', 'trending_score': 91},
                {'title': 'Sustainable Living Practices', 'description': 'Eco-friendly lifestyle tips', 'trending_score': 88},
                {'title': 'Climate Change Updates', 'description': 'Latest climate science and news', 'trending_score': 85},
                {'title': 'Conservation Efforts', 'description': 'Protecting the environment', 'trending_score': 82},
                {'title': 'Green Technology Innovations', 'description': 'Sustainable technology solutions', 'trending_score': 79}
            ],
            'art_creativity': [
                {'title': 'Digital Art Tutorials', 'description': 'Learn digital painting and design', 'trending_score': 89},
                {'title': 'Creative Process Videos', 'description': 'Behind-the-scenes of artistic creation', 'trending_score': 86},
                {'title': 'Design Tips and Tricks', 'description': 'Graphic design and visual arts advice', 'trending_score': 83},
                {'title': 'Art History and Culture', 'description': 'Understanding art movements and styles', 'trending_score': 80},
                {'title': 'Creative Inspiration Content', 'description': 'Motivational content for artists', 'trending_score': 77}
            ]
        }
        
        return youtube_topics.get(direction, youtube_topics['technology'])
    
    def get_podcast_topics(self, direction: str, country: str) -> List[Dict[str, Any]]:
        """Get topics from Podcasts (mock implementation)"""
        podcast_topics = {
            'technology': [
                {'title': 'AI and the Future of Work', 'description': 'How artificial intelligence is changing employment', 'trending_score': 86},
                {'title': 'Cybersecurity Threats', 'description': 'Current security challenges and solutions', 'trending_score': 83},
                {'title': 'Tech Startup Stories', 'description': 'Behind-the-scenes of successful startups', 'trending_score': 80},
                {'title': 'Digital Privacy Matters', 'description': 'Protecting your online presence', 'trending_score': 77},
                {'title': 'Innovation in Tech', 'description': 'Latest breakthroughs and inventions', 'trending_score': 74}
            ],
            'business_finance': [
                {'title': 'Market Analysis Weekly', 'description': 'Weekly financial market insights', 'trending_score': 89},
                {'title': 'Entrepreneur Success Stories', 'description': 'Real stories from business leaders', 'trending_score': 86},
                {'title': 'Investment Strategies', 'description': 'Expert advice on building wealth', 'trending_score': 83},
                {'title': 'Business Growth Tactics', 'description': 'Practical strategies for scaling', 'trending_score': 80},
                {'title': 'Economic Trends', 'description': 'Understanding the current economy', 'trending_score': 77}
            ],
            'health_wellness': [
                {'title': 'Mental Health Conversations', 'description': 'Open discussions about psychological well-being', 'trending_score': 88},
                {'title': 'Fitness and Nutrition Science', 'description': 'Evidence-based health and wellness advice', 'trending_score': 85},
                {'title': 'Mindfulness and Meditation', 'description': 'Stress reduction and mental clarity techniques', 'trending_score': 82},
                {'title': 'Sleep Science and Optimization', 'description': 'Understanding and improving sleep quality', 'trending_score': 79},
                {'title': 'Holistic Health Approaches', 'description': 'Integrative wellness and natural healing', 'trending_score': 76}
            ],
            'education': [
                {'title': 'Learning Science and Methods', 'description': 'Evidence-based approaches to education', 'trending_score': 87},
                {'title': 'Career Development Insights', 'description': 'Professional growth and advancement strategies', 'trending_score': 84},
                {'title': 'Educational Technology Trends', 'description': 'How technology is transforming learning', 'trending_score': 81},
                {'title': 'Student Success Stories', 'description': 'Inspiring educational journeys and achievements', 'trending_score': 78},
                {'title': 'Lifelong Learning Strategies', 'description': 'Continuous education for adults', 'trending_score': 75}
            ],
            'entertainment': [
                {'title': 'Behind the Scenes Stories', 'description': 'Insider perspectives from entertainment industry', 'trending_score': 90},
                {'title': 'Movie and TV Analysis', 'description': 'Deep dives into film and television content', 'trending_score': 87},
                {'title': 'Music Industry Insights', 'description': 'Behind-the-scenes of the music world', 'trending_score': 84},
                {'title': 'Gaming Culture and Trends', 'description': 'Video game industry and community discussions', 'trending_score': 81},
                {'title': 'Celebrity Interviews and Stories', 'description': 'Personal stories from entertainment figures', 'trending_score': 78}
            ],
            'lifestyle': [
                {'title': 'Minimalism and Simple Living', 'description': 'Decluttering and intentional lifestyle choices', 'trending_score': 86},
                {'title': 'Digital Wellness and Balance', 'description': 'Managing technology use and screen time', 'trending_score': 83},
                {'title': 'Sustainable Living Practices', 'description': 'Eco-friendly lifestyle choices and tips', 'trending_score': 80},
                {'title': 'Work-Life Integration', 'description': 'Balancing career and personal life', 'trending_score': 77},
                {'title': 'Personal Development Journey', 'description': 'Self-improvement and growth strategies', 'trending_score': 74}
            ],
            'sports': [
                {'title': 'Sports Analysis and Commentary', 'description': 'Expert insights on games and athletes', 'trending_score': 89},
                {'title': 'Athlete Stories and Interviews', 'description': 'Personal journeys from sports stars', 'trending_score': 86},
                {'title': 'Sports Psychology and Performance', 'description': 'Mental aspects of athletic achievement', 'trending_score': 83},
                {'title': 'Sports History and Culture', 'description': 'Historical perspectives on sports', 'trending_score': 80},
                {'title': 'Youth Sports Development', 'description': 'Supporting young athletes and programs', 'trending_score': 77}
            ],
            'food_cooking': [
                {'title': 'Culinary Stories and Traditions', 'description': 'Food culture and cooking heritage', 'trending_score': 87},
                {'title': 'Chef Interviews and Techniques', 'description': 'Professional cooking insights and tips', 'trending_score': 84},
                {'title': 'Food Science and Nutrition', 'description': 'Understanding the science behind food', 'trending_score': 81},
                {'title': 'Restaurant Industry Insights', 'description': 'Behind-the-scenes of the food business', 'trending_score': 78},
                {'title': 'Sustainable Food Practices', 'description': 'Eco-friendly cooking and eating', 'trending_score': 75}
            ],
            'travel': [
                {'title': 'Travel Stories and Adventures', 'description': 'Personal travel experiences and tales', 'trending_score': 90},
                {'title': 'Cultural Immersion Stories', 'description': 'Deep cultural experiences and learning', 'trending_score': 87},
                {'title': 'Budget Travel Strategies', 'description': 'Affordable travel tips and planning', 'trending_score': 84},
                {'title': 'Sustainable Tourism Practices', 'description': 'Responsible and eco-friendly travel', 'trending_score': 81},
                {'title': 'Digital Nomad Lifestyle', 'description': 'Working remotely while traveling', 'trending_score': 78}
            ],
            'fashion_beauty': [
                {'title': 'Fashion Industry Insights', 'description': 'Behind-the-scenes of the fashion world', 'trending_score': 88},
                {'title': 'Sustainable Fashion Movement', 'description': 'Eco-friendly fashion choices and trends', 'trending_score': 85},
                {'title': 'Beauty Science and Trends', 'description': 'Understanding beauty products and practices', 'trending_score': 82},
                {'title': 'Body Positivity and Confidence', 'description': 'Self-love and acceptance discussions', 'trending_score': 79},
                {'title': 'Fashion History and Culture', 'description': 'Evolution of fashion and style', 'trending_score': 76}
            ],
            'parenting': [
                {'title': 'Parenting Challenges and Solutions', 'description': 'Practical advice for modern parents', 'trending_score': 87},
                {'title': 'Child Development Science', 'description': 'Understanding how children grow and learn', 'trending_score': 84},
                {'title': 'Digital Parenting Strategies', 'description': 'Managing children\'s technology use', 'trending_score': 81},
                {'title': 'Parent Mental Health Support', 'description': 'Wellness resources for parents', 'trending_score': 78},
                {'title': 'Family Relationship Building', 'description': 'Strengthening family bonds and communication', 'trending_score': 75}
            ],
            'pets_animals': [
                {'title': 'Pet Care and Training Tips', 'description': 'Expert advice on pet ownership', 'trending_score': 86},
                {'title': 'Animal Welfare and Rescue', 'description': 'Protecting and helping animals in need', 'trending_score': 83},
                {'title': 'Veterinary Science Insights', 'description': 'Understanding pet health and medicine', 'trending_score': 80},
                {'title': 'Wildlife Conservation Stories', 'description': 'Protecting endangered species and habitats', 'trending_score': 77},
                {'title': 'Pet Adoption Success Stories', 'description': 'Heartwarming rescue and adoption tales', 'trending_score': 74}
            ],
            'automotive': [
                {'title': 'Car Industry Analysis', 'description': 'Understanding automotive trends and technology', 'trending_score': 89},
                {'title': 'Electric Vehicle Revolution', 'description': 'The future of transportation and EVs', 'trending_score': 86},
                {'title': 'Car Maintenance and Care', 'description': 'Keeping vehicles in top condition', 'trending_score': 83},
                {'title': 'Automotive Safety Technology', 'description': 'Latest safety features and innovations', 'trending_score': 80},
                {'title': 'Classic Car Stories', 'description': 'Vintage vehicles and automotive history', 'trending_score': 77}
            ],
            'real_estate': [
                {'title': 'Real Estate Market Analysis', 'description': 'Understanding property trends and markets', 'trending_score': 88},
                {'title': 'Investment Property Strategies', 'description': 'Real estate investment advice and tips', 'trending_score': 85},
                {'title': 'Home Improvement Projects', 'description': 'DIY and renovation ideas and tips', 'trending_score': 82},
                {'title': 'Sustainable Building Practices', 'description': 'Green construction and energy efficiency', 'trending_score': 79},
                {'title': 'Real Estate Technology Trends', 'description': 'Digital tools and innovations in real estate', 'trending_score': 76}
            ],

            'science_research': [
                {'title': 'Scientific Discoveries Explained', 'description': 'Understanding complex scientific concepts', 'trending_score': 92},
                {'title': 'Research Methodology Insights', 'description': 'How scientific research works', 'trending_score': 89},
                {'title': 'Climate Science Updates', 'description': 'Latest findings on environmental impact', 'trending_score': 86},
                {'title': 'Medical Research Breakthroughs', 'description': 'Healthcare and treatment developments', 'trending_score': 83},
                {'title': 'Space Exploration Updates', 'description': 'Latest developments in astronomy and space', 'trending_score': 80}
            ],
            'politics_society': [
                {'title': 'Political Analysis and Commentary', 'description': 'Understanding political events and trends', 'trending_score': 91},
                {'title': 'Social Justice Discussions', 'description': 'Important societal issues and equality', 'trending_score': 88},
                {'title': 'Civic Engagement Guide', 'description': 'How to participate in democracy effectively', 'trending_score': 85},
                {'title': 'Policy Impact Analysis', 'description': 'How laws and policies affect communities', 'trending_score': 82},
                {'title': 'International Relations Updates', 'description': 'Global political developments and diplomacy', 'trending_score': 79}
            ],
            'environment_sustainability': [
                {'title': 'Environmental Science Explained', 'description': 'Understanding environmental issues', 'trending_score': 91},
                {'title': 'Sustainable Living Practices', 'description': 'Eco-friendly lifestyle tips', 'trending_score': 88},
                {'title': 'Climate Change Updates', 'description': 'Latest climate science and news', 'trending_score': 85},
                {'title': 'Conservation Efforts', 'description': 'Protecting the environment', 'trending_score': 82},
                {'title': 'Green Technology Innovations', 'description': 'Sustainable technology solutions', 'trending_score': 79}
            ],
            'art_creativity': [
                {'title': 'Creative Process Podcast', 'description': 'Behind-the-scenes of artistic creation and design', 'trending_score': 87},
                {'title': 'Art Industry Insights', 'description': 'Understanding the business side of creativity', 'trending_score': 84},
                {'title': 'Design Thinking Discussions', 'description': 'Creative problem-solving and innovation', 'trending_score': 81},
                {'title': 'Artist Interviews and Stories', 'description': 'Personal journeys from creative professionals', 'trending_score': 78},
                {'title': 'Creative Inspiration Sessions', 'description': 'Motivational content for artists and designers', 'trending_score': 75}
            ]
        }
        
        return podcast_topics.get(direction, podcast_topics['technology'])
    
    def search_youtube_videos(self, direction: str, categories: List[str], country: str = 'US') -> List[Dict[str, Any]]:
        """Search for real YouTube videos using Google Custom Search or web scraping"""
        if not self.api_key or not self.search_engine_id:
            # Try web scraping as fallback
            return self._scrape_youtube_videos(direction, categories)
        
        try:
            # Create search query based on direction and categories
            search_terms = [direction.replace('_', ' ')]
            if categories:
                search_terms.extend(categories[:2])  # Use top 2 categories to avoid long queries
            
            # Add location-specific terms based on country
            location_terms = self._get_location_terms(country)
            if location_terms:
                import random
                location_term = random.choice(location_terms)
                search_terms.append(location_term)
            
            # Create a cleaner search query
            base_query = ' '.join(search_terms)
            search_query = f'{base_query} site:youtube.com'
            
            # Add randomization for variety
            import random
            start_index = random.randint(1, 10)  # Start from random position for variety
            
            params = {
                'key': self.api_key,
                'cx': self.search_engine_id,
                'q': search_query,
                'gl': country.lower(),
                'lr': f'lang_{self._get_language_code(country)}',  # Language preference
                'start': start_index,  # Random start position for variety
                'num': 3  # Get 3 results
            }
            
            response = requests.get(self.custom_search_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            videos = []
            
            if 'items' in data:
                for item in data['items']:
                    # Extract video ID from URL
                    video_url = item.get('link', '')
                    video_id = self._extract_youtube_id(video_url)
                    
                    if video_id:
                        # Get additional video details (thumbnail, duration, etc.)
                        video_details = self._get_youtube_video_details(video_id)
                        
                        video = {
                            'title': item.get('title', ''),
                            'url': video_url,
                            'thumbnail': video_details.get('thumbnail', 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=300&h=200&fit=crop'),
                            'duration': video_details.get('duration', 'Unknown'),
                            'views': video_details.get('views', 'Unknown'),
                            'channel': video_details.get('channel', 'Unknown'),
                            'description': item.get('snippet', '')
                        }
                        videos.append(video)
            
            # Fallback to mock data if no results
            if not videos:
                videos = self._mock_youtube_videos(direction, categories)
            
            return videos
            
        except Exception as e:
            print(f"YouTube search error: {e}")
            print(f"Search query: {search_query}")
            print(f"API URL: {self.custom_search_url}")
            print(f"Parameters: {params}")
            return self._mock_youtube_videos(direction, categories)
    
    def search_podcasts(self, direction: str, categories: List[str], country: str = 'US') -> List[Dict[str, Any]]:
        """Search for real podcasts using Google Custom Search or web scraping"""
        print(f"🔍 DEBUG: Starting podcast search for direction={direction}, categories={categories}, country={country}")
        print(f"🔍 DEBUG: API Key configured: {bool(self.api_key)}")
        print(f"🔍 DEBUG: Search Engine ID configured: {bool(self.search_engine_id)}")
        
        if not self.api_key or not self.search_engine_id:
            print("⚠️ DEBUG: No API credentials, trying web scraping fallback")
            # Try web scraping as fallback
            return self._scrape_podcasts(direction, categories)
        
        try:
            # Create multiple search queries for better results
            search_queries = self._generate_search_queries(direction, categories, country, 'podcast')
            
            all_podcasts = []
            seen_urls = set()  # Track seen URLs to avoid duplicates
            
            for i, search_query in enumerate(search_queries[:2]):  # Try first 2 queries
                print(f"🔍 DEBUG: Search query {i+1}: '{search_query}'")
                
                # Add randomization for variety
                import random
                start_index = random.randint(1, 5)  # Smaller range for better results
                
                params = {
                    'key': self.api_key,
                    'cx': self.search_engine_id,
                    'q': search_query,
                    'gl': country.lower(),
                    'lr': f'lang_{self._get_language_code(country)}',  # Language preference
                    'start': start_index,  # Random start position for variety
                    'num': 5  # Get more results to filter from
                }
            
                response = requests.get(self.custom_search_url, params=params)
                print(f"🔍 DEBUG: API Response Status: {response.status_code}")
                
                if response.status_code != 200:
                    print(f"❌ DEBUG: API Error Response: {response.text[:500]}")
                    continue  # Try next query instead of failing
                
                data = response.json()
                print(f"🔍 DEBUG: API Response has {len(data.get('items', []))} items")
                
                if 'items' in data:
                    print(f"🔍 DEBUG: Processing {len(data['items'])} search results")
                    for item in data['items']:
                        podcast_url = item.get('link', '')
                        title = item.get('title', '')
                        snippet = item.get('snippet', '')
                        
                        # Skip if we've seen this URL before
                        if podcast_url in seen_urls:
                            continue
                        seen_urls.add(podcast_url)
                        
                        print(f"🔍 DEBUG: Processing: Title='{title[:50]}...'")
                        print(f"🔍 DEBUG: URL='{podcast_url}'")
                        
                        # Extract podcast details from URL or search result
                        podcast_details = self._extract_podcast_details(item)
                        
                        podcast = {
                            'title': item.get('title', ''),
                            'url': podcast_url,
                            'cover': podcast_details.get('cover', 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=300&h=300&fit=crop'),
                            'duration': podcast_details.get('duration', 'Unknown'),
                            'episodes': podcast_details.get('episodes', 'Unknown'),
                            'host': podcast_details.get('host', 'Unknown'),
                            'description': item.get('snippet', '')
                        }
                        all_podcasts.append(podcast)
                        print(f"✅ DEBUG: Added podcast: {podcast['title'][:50]}... (Host: {podcast['host']})")
                        
                        # Stop if we have enough unique results
                        if len(all_podcasts) >= 3:
                            break
                
                # Stop if we have enough results
                if len(all_podcasts) >= 3:
                    break
            
            # Return the best results
            podcasts = all_podcasts[:3]
            
            # Fallback to mock data if no results
            if not podcasts:
                print("⚠️ DEBUG: No podcasts found, falling back to mock data")
                podcasts = self._mock_podcasts(direction, categories)
            else:
                print(f"✅ DEBUG: Successfully found {len(podcasts)} unique podcasts")
            
            print(f"🔍 DEBUG: Final podcast count: {len(podcasts)}")
            return podcasts
            
        except Exception as e:
            print(f"❌ DEBUG: Podcast search error: {e}")
            print(f"🔍 DEBUG: Search query: {search_query}")
            print(f"🔍 DEBUG: API URL: {self.custom_search_url}")
            print(f"🔍 DEBUG: Parameters: {params}")
            print("⚠️ DEBUG: Falling back to mock data due to error")
            return self._mock_podcasts(direction, categories)
    
    def _extract_youtube_id(self, url: str) -> str:
        """Extract YouTube video ID from URL"""
        import re
        
        # YouTube URL patterns
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def _get_youtube_video_details(self, video_id: str) -> Dict[str, Any]:
        """Get additional YouTube video details (mock implementation)"""
        # In production, this would use YouTube Data API
        # For now, return mock data
        return {
            'thumbnail': f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg',
            'duration': '12:34',
            'views': '1.2M',
            'channel': 'Popular Channel'
        }
    
    def _get_location_terms(self, country: str) -> List[str]:
        """Get location-specific search terms based on country"""
        location_terms = {
            'US': ['United States', 'American', 'US', 'USA'],
            'CA': ['Canada', 'Canadian', 'Toronto', 'Vancouver'],
            'GB': ['UK', 'British', 'England', 'London'],
            'AU': ['Australia', 'Australian', 'Sydney', 'Melbourne'],
            'DE': ['Germany', 'German', 'Berlin', 'Munich'],
            'FR': ['France', 'French', 'Paris', 'Lyon'],
            'JP': ['Japan', 'Japanese', 'Tokyo', 'Osaka'],
            'KR': ['Korea', 'Korean', 'Seoul', 'Busan'],
            'CN': ['China', 'Chinese', 'Beijing', 'Shanghai'],
            'IN': ['India', 'Indian', 'Mumbai', 'Delhi'],
            'BR': ['Brazil', 'Brazilian', 'São Paulo', 'Rio'],
            'MX': ['Mexico', 'Mexican', 'Mexico City', 'Guadalajara'],
            'ES': ['Spain', 'Spanish', 'Madrid', 'Barcelona'],
            'IT': ['Italy', 'Italian', 'Rome', 'Milan'],
            'NL': ['Netherlands', 'Dutch', 'Amsterdam', 'Rotterdam'],
        }
        return location_terms.get(country.upper(), [])
    
    def _get_language_code(self, country: str) -> str:
        """Get language code for country"""
        language_codes = {
            'US': 'en', 'CA': 'en', 'GB': 'en', 'AU': 'en',
            'DE': 'de', 'FR': 'fr', 'JP': 'ja', 'KR': 'ko',
            'CN': 'zh', 'IN': 'en', 'BR': 'pt', 'MX': 'es',
            'ES': 'es', 'IT': 'it', 'NL': 'nl'
        }
        return language_codes.get(country.upper(), 'en')
    
    def _generate_search_queries(self, direction: str, categories: List[str], country: str, content_type: str = 'podcast') -> List[str]:
        """Generate multiple search queries for better results"""
        import random
        
        # Base direction terms
        direction_terms = {
            'business_finance': ['business', 'finance', 'entrepreneurship', 'money', 'investment'],
            'technology': ['technology', 'tech', 'AI', 'programming', 'software'],
            'health_wellness': ['health', 'wellness', 'fitness', 'nutrition', 'mental health'],
            'food_cooking': ['food', 'cooking', 'recipes', 'kitchen', 'culinary'],
            'education': ['education', 'learning', 'teaching', 'academic', 'study'],
            'entertainment': ['entertainment', 'movies', 'music', 'celebrity', 'pop culture'],
            'travel': ['travel', 'tourism', 'vacation', 'adventure', 'exploration'],
            'sports': ['sports', 'fitness', 'athletics', 'training', 'competition'],
            'lifestyle': ['lifestyle', 'personal development', 'self improvement', 'motivation'],
            'science_research': ['science', 'research', 'discovery', 'innovation', 'technology']
        }
        
        # Get direction-specific terms
        direction_keywords = direction_terms.get(direction, [direction.replace('_', ' ')])
        
        # Get location terms
        location_terms = self._get_location_terms(country)
        
        # Generate multiple search queries
        queries = []
        
        # Query 1: Direction + Category + Location
        if categories:
            category_terms = categories[:2]  # Use top 2 categories
            base_terms = direction_keywords[:2] + category_terms
            if location_terms:
                base_terms.append(random.choice(location_terms))
            query = ' '.join(base_terms)
            if content_type == 'podcast':
                queries.append(f'{query} site:podcasts.apple.com')
            else:
                queries.append(f'{query} site:youtube.com')
        
        # Query 2: Direction + Location + "best"
        if location_terms:
            location_term = random.choice(location_terms)
            query = f"{random.choice(direction_keywords)} {location_term} best"
            if content_type == 'podcast':
                queries.append(f'{query} site:podcasts.apple.com')
            else:
                queries.append(f'{query} site:youtube.com')
        
        # Query 3: Category-focused
        if categories:
            category = random.choice(categories)
            query = f"{category} {random.choice(direction_keywords)}"
            if content_type == 'podcast':
                queries.append(f'{query} site:podcasts.apple.com')
            else:
                queries.append(f'{query} site:youtube.com')
        
        # Query 4: Popular/popular
        query = f"{random.choice(direction_keywords)} popular"
        if content_type == 'podcast':
            queries.append(f'{query} site:podcasts.apple.com')
        else:
            queries.append(f'{query} site:youtube.com')
        
        return queries
    
    def _generate_no_preview_image(self, title: str) -> str:
        """Generate a "No Preview Available" image with podcast title"""
        # Use a better placeholder service that handles text well
        # Gray background (#6B7280) with white text
        import urllib.parse
        
        # Create a clean "No Preview Available" image
        text = urllib.parse.quote("No Preview Available")
        return f"https://via.placeholder.com/300x300/6B7280/FFFFFF?text={text}"
    
    def _extract_podcast_details(self, search_item: Dict[str, Any]) -> Dict[str, Any]:
        """Extract podcast details from search result"""
        import re
        
        title = search_item.get('title', '')
        snippet = search_item.get('snippet', '')
        url = search_item.get('link', '')
        
        # Try to extract host from title or snippet
        host = 'Unknown Host'
        
        # Common patterns for host extraction
        host_patterns = [
            r'with\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',  # "with John Smith"
            r'by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',    # "by John Smith"
            r'hosted\s+by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',  # "hosted by John Smith"
            r'featuring\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',    # "featuring John Smith"
            r'presented\s+by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',  # "presented by John Smith"
            r'from\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',  # "from John Smith"
        ]
        
        # Search in title first, then snippet
        for pattern in host_patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                host = match.group(1)
                break
            match = re.search(pattern, snippet, re.IGNORECASE)
            if match:
                host = match.group(1)
                break
        
        # If no host found, try to extract from podcast name
        if host == 'Unknown Host':
            # Look for podcast names that might be the host
            podcast_name_patterns = [
                r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+Show',  # "John Smith Show"
                r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+Podcast',  # "John Smith Podcast"
                r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+Experience',  # "John Smith Experience"
                r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+Insights',  # "John Smith Insights"
            ]
            
            for pattern in podcast_name_patterns:
                match = re.search(pattern, title)
                if match:
                    host = match.group(1)
                    break
        
        # If no host found, try to extract from URL or use a default
        if host == 'Unknown Host':
            # Extract from Apple Podcasts URL if possible
            if 'podcasts.apple.com' in url:
                # Try to get host from the podcast name in URL
                url_parts = url.split('/')
                if len(url_parts) > 2:
                    # Find the podcast name part (before the ID)
                    for i, part in enumerate(url_parts):
                        if part == 'podcast' and i + 1 < len(url_parts):
                            podcast_name = url_parts[i + 1]
                            # Clean up the podcast name
                            host = podcast_name.replace('-', ' ').replace('_', ' ').title()
                            
                            # Skip if it's just an ID or generic name
                            if host.isdigit() or host.lower() in ['podcast', 'podcasts', 'apple', 'id']:
                                host = 'Podcast Host'
                            elif len(host) > 30:  # If too long, use a shorter version
                                host = host[:30] + '...'
                            break
        
        # Generate realistic duration and episodes
        import random
        durations = ['30-45 min', '45-60 min', '60-90 min', '20-30 min']
        episode_counts = ['50+', '100+', '200+', '300+', '500+']
        
        # Generate different cover images based on podcast content
        cover_images = [
            'https://images.unsplash.com/photo-1552664730-d307ca884978?w=300&h=300&fit=crop',  # Business
            'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=300&h=300&fit=crop',  # Technology
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=300&fit=crop',  # Health
            'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=300&h=300&fit=crop',  # Food
            'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=300&h=300&fit=crop',  # Education
            'https://images.unsplash.com/photo-1547658719-da2b51169166?w=300&h=300&fit=crop',  # Creative
            'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=300&h=300&fit=crop',  # Finance
            'https://images.unsplash.com/photo-1556761175-b413da4baf72?w=300&h=300&fit=crop',  # Entrepreneurship
        ]
        
        # Select cover based on podcast title/content
        cover = random.choice(cover_images)
        
        # Try to match cover to content
        title_lower = title.lower()
        if any(word in title_lower for word in ['business', 'finance', 'money', 'entrepreneur']):
            cover = 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=300&h=300&fit=crop'
        elif any(word in title_lower for word in ['tech', 'ai', 'programming', 'coding']):
            cover = 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=300&h=300&fit=crop'
        elif any(word in title_lower for word in ['health', 'fitness', 'wellness', 'nutrition']):
            cover = 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=300&fit=crop'
        elif any(word in title_lower for word in ['food', 'cooking', 'recipe', 'kitchen']):
            cover = 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=300&h=300&fit=crop'
        elif any(word in title_lower for word in ['education', 'learning', 'school', 'study']):
            cover = 'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=300&h=300&fit=crop'
        
        # Check if we should use "No Preview Available" image
        # Use it for podcasts that don't have clear content matching
        if not any(word in title_lower for word in ['business', 'finance', 'money', 'entrepreneur', 'tech', 'ai', 'programming', 'coding', 'health', 'fitness', 'wellness', 'nutrition', 'food', 'cooking', 'recipe', 'kitchen', 'education', 'learning', 'school', 'study']):
            # Use a "No Preview Available" image
            cover = self._generate_no_preview_image(title)
        
        return {
            'cover': cover,
            'duration': random.choice(durations),
            'episodes': random.choice(episode_counts),
            'host': host
        }
    
    def _mock_youtube_videos(self, direction: str, categories: List[str]) -> List[Dict[str, Any]]:
        """Mock YouTube videos with rich metadata"""
        mock_videos = {
            'business_finance': [
                {
                    'title': 'How to Build a Successful Business from Scratch',
                    'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                    'thumbnail': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=300&h=200&fit=crop',
                    'duration': '12:34',
                    'views': '2.1M',
                    'channel': 'Business Insights'
                },
                {
                    'title': 'Financial Freedom: 10 Steps to Wealth',
                    'url': 'https://www.youtube.com/watch?v=9bZkp7q19f0',
                    'thumbnail': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=300&h=200&fit=crop',
                    'duration': '18:45',
                    'views': '1.8M',
                    'channel': 'Finance Mastery'
                },
                {
                    'title': 'Entrepreneurship Secrets Revealed',
                    'url': 'https://www.youtube.com/watch?v=kJQP7kiw5Fk',
                    'thumbnail': 'https://images.unsplash.com/photo-1556761175-b413da4baf72?w=300&h=200&fit=crop',
                    'duration': '15:22',
                    'views': '3.2M',
                    'channel': 'Startup Success'
                }
            ],
            'technology': [
                {
                    'title': 'AI Revolution: What\'s Next in Tech',
                    'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                    'thumbnail': 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=300&h=200&fit=crop',
                    'duration': '14:18',
                    'views': '1.5M',
                    'channel': 'Tech Trends'
                },
                {
                    'title': 'Coding for Beginners: Start Your Journey',
                    'url': 'https://www.youtube.com/watch?v=9bZkp7q19f0',
                    'thumbnail': 'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=300&h=200&fit=crop',
                    'duration': '22:33',
                    'views': '2.8M',
                    'channel': 'Code Academy'
                },
                {
                    'title': 'Future of Web Development',
                    'url': 'https://www.youtube.com/watch?v=kJQP7kiw5Fk',
                    'thumbnail': 'https://images.unsplash.com/photo-1547658719-da2b51169166?w=300&h=200&fit=crop',
                    'duration': '16:47',
                    'views': '1.9M',
                    'channel': 'Web Dev Pro'
                }
            ],
            'health_wellness': [
                {
                    'title': 'Complete Morning Routine for Success',
                    'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                    'thumbnail': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=200&fit=crop',
                    'duration': '11:25',
                    'views': '4.1M',
                    'channel': 'Wellness Daily'
                },
                {
                    'title': 'Nutrition Myths Debunked',
                    'url': 'https://www.youtube.com/watch?v=9bZkp7q19f0',
                    'thumbnail': 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=300&h=200&fit=crop',
                    'duration': '19:12',
                    'views': '2.3M',
                    'channel': 'Health Facts'
                },
                {
                    'title': 'Meditation for Beginners',
                    'url': 'https://www.youtube.com/watch?v=kJQP7kiw5Fk',
                    'thumbnail': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=200&fit=crop',
                    'duration': '13:56',
                    'views': '3.7M',
                    'channel': 'Mindful Living'
                }
            ]
        }
        
        return mock_videos.get(direction, mock_videos['business_finance'])
    
    def _mock_podcasts(self, direction: str, categories: List[str]) -> List[Dict[str, Any]]:
        """Mock podcasts with rich metadata"""
        mock_podcasts = {
            'business_finance': [
                {
                    'title': 'The Tim Ferriss Show',
                    'url': 'https://podcasts.apple.com/us/podcast/the-tim-ferriss-show/id863897795',
                    'cover': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=300&h=300&fit=crop',
                    'duration': '1-2 hours',
                    'episodes': '700+',
                    'host': 'Tim Ferriss',
                    'description': 'Interviews with world-class performers'
                },
                {
                    'title': 'How I Built This',
                    'url': 'https://podcasts.apple.com/us/podcast/how-i-built-this/id1150510297',
                    'cover': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=300&h=300&fit=crop',
                    'duration': '45-60 min',
                    'episodes': '400+',
                    'host': 'Guy Raz',
                    'description': 'Stories behind successful companies'
                },
                {
                    'title': 'Masters of Scale',
                    'url': 'https://podcasts.apple.com/us/podcast/masters-of-scale/id1227971746',
                    'cover': 'https://images.unsplash.com/photo-1556761175-b413da4baf72?w=300&h=300&fit=crop',
                    'duration': '30-45 min',
                    'episodes': '200+',
                    'host': 'Reid Hoffman',
                    'description': 'How companies grow from zero to a gazillion'
                }
            ],
            'technology': [
                {
                    'title': 'Lex Fridman Podcast',
                    'url': 'https://podcasts.apple.com/us/podcast/lex-fridman-podcast/id1434243584',
                    'cover': 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=300&h=300&fit=crop',
                    'duration': '2-3 hours',
                    'episodes': '400+',
                    'host': 'Lex Fridman',
                    'description': 'Conversations about AI, science, and technology'
                },
                {
                    'title': 'The Vergecast',
                    'url': 'https://podcasts.apple.com/us/podcast/the-vergecast/id430333725',
                    'cover': 'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=300&h=300&fit=crop',
                    'duration': '1-2 hours',
                    'episodes': '600+',
                    'host': 'The Verge Team',
                    'description': 'Tech news and analysis'
                },
                {
                    'title': 'Recode Decode',
                    'url': 'https://podcasts.apple.com/us/podcast/recode-decode/id1011668648',
                    'cover': 'https://images.unsplash.com/photo-1547658719-da2b51169166?w=300&h=300&fit=crop',
                    'duration': '45-60 min',
                    'episodes': '500+',
                    'host': 'Kara Swisher',
                    'description': 'Tech industry insights and interviews'
                }
            ],
            'health_wellness': [
                {
                    'title': 'The Joe Rogan Experience',
                    'url': 'https://podcasts.apple.com/us/podcast/the-joe-rogan-experience/id360084272',
                    'cover': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=300&fit=crop',
                    'duration': '2-3 hours',
                    'episodes': '2000+',
                    'host': 'Joe Rogan',
                    'description': 'Long-form conversations with interesting people'
                },
                {
                    'title': 'On Purpose with Jay Shetty',
                    'url': 'https://podcasts.apple.com/us/podcast/on-purpose-with-jay-shetty/id1437448722',
                    'cover': 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=300&h=300&fit=crop',
                    'duration': '30-45 min',
                    'episodes': '300+',
                    'host': 'Jay Shetty',
                    'description': 'Wisdom for modern life'
                },
                {
                    'title': 'The Wellness Mama Podcast',
                    'url': 'https://podcasts.apple.com/us/podcast/the-wellness-mama-podcast/id1070840096',
                    'cover': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=300&fit=crop',
                    'duration': '20-30 min',
                    'episodes': '400+',
                    'host': 'Katie Wells',
                    'description': 'Natural health and wellness tips'
                }
            ]
        }
        
        return mock_podcasts.get(direction, mock_podcasts['business_finance'])
    
    def _scrape_youtube_videos(self, direction: str, categories: List[str]) -> List[Dict[str, Any]]:
        """Scrape real YouTube videos using search queries"""
        try:
            import requests
            from bs4 import BeautifulSoup
            import re
            import random
            
            # Create search query
            search_terms = [direction.replace('_', ' ')]
            if categories:
                search_terms.extend(categories[:2])
            search_query = ' '.join(search_terms)
            
            # Use YouTube search URL
            search_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract video data from YouTube page
            videos = []
            video_scripts = soup.find_all('script')
            
            for script in video_scripts:
                if 'var ytInitialData = ' in str(script):
                    script_text = str(script)
                    # Extract video data from YouTube's JavaScript
                    video_matches = re.findall(r'"videoId":"([^"]+)"', script_text)
                    title_matches = re.findall(r'"title":{"runs":\[{"text":"([^"]+)"', script_text)
                    channel_matches = re.findall(r'"channelName":"([^"]+)"', script_text)
                    
                    for i, video_id in enumerate(video_matches[:3]):
                        if i < len(title_matches) and i < len(channel_matches):
                            video = {
                                'title': title_matches[i][:100] + '...' if len(title_matches[i]) > 100 else title_matches[i],
                                'url': f'https://www.youtube.com/watch?v={video_id}',
                                'thumbnail': f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg',
                                'duration': f'{random.randint(5, 25)}:{random.randint(10, 59):02d}',
                                'views': f'{random.randint(100, 999)}K',
                                'channel': channel_matches[i][:50] + '...' if len(channel_matches[i]) > 50 else channel_matches[i],
                                'description': f'Real YouTube video about {search_query}'
                            }
                            videos.append(video)
                    break
            
            # If scraping failed, return mock data
            if not videos:
                return self._mock_youtube_videos(direction, categories)
            
            return videos
            
        except Exception as e:
            print(f"YouTube scraping error: {e}")
            return self._mock_youtube_videos(direction, categories)
    
    def _scrape_podcasts(self, direction: str, categories: List[str]) -> List[Dict[str, Any]]:
        """Scrape real podcasts using search queries"""
        try:
            import requests
            from bs4 import BeautifulSoup
            import re
            import random
            
            # Create search query
            search_terms = [direction.replace('_', ' ')]
            if categories:
                search_terms.extend(categories[:2])
            search_query = ' '.join(search_terms)
            
            # Use Apple Podcasts search URL
            search_url = f"https://podcasts.apple.com/search?term={search_query.replace(' ', '+')}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract podcast data from Apple Podcasts page
            podcasts = []
            podcast_links = soup.find_all('a', href=re.compile(r'/podcast/'))
            
            for i, link in enumerate(podcast_links[:3]):
                try:
                    title_elem = link.find('h3') or link.find('h2') or link.find('h1')
                    title = title_elem.get_text().strip() if title_elem else f'Podcast about {search_query}'
                    
                    # Clean up title
                    title = title[:100] + '...' if len(title) > 100 else title
                    
                    podcast = {
                        'title': title,
                        'url': f"https://podcasts.apple.com{link.get('href')}",
                        'cover': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=300&h=300&fit=crop',
                        'duration': f'{random.randint(30, 90)}-{random.randint(60, 120)} min',
                        'episodes': f'{random.randint(50, 500)}+',
                        'host': f'Host {i+1}',
                        'description': f'Real podcast about {search_query}'
                    }
                    podcasts.append(podcast)
                except Exception as e:
                    print(f"Error parsing podcast {i}: {e}")
                    continue
            
            # If scraping failed, return mock data
            if not podcasts:
                return self._mock_podcasts(direction, categories)
            
            return podcasts
            
        except Exception as e:
            print(f"Podcast scraping error: {e}")
            return self._mock_podcasts(direction, categories)
    
    def get_ai_discovery_topics(self, direction: str, country: str) -> List[Dict[str, Any]]:
        """Get AI-powered discovery topics combining multiple sources"""
        # Combine topics from multiple sources
        search_topics = self.search_topics(direction, country)
        news_topics = self.get_news_topics(direction, country)
        trending_topics = self.get_trending_topics(direction, country)
        
        # Merge and rank topics
        all_topics = search_topics + news_topics + trending_topics
        
        # Remove duplicates and sort by trending score
        unique_topics = []
        seen_titles = set()
        
        for topic in all_topics:
            if topic['title'] not in seen_titles:
                unique_topics.append(topic)
                seen_titles.add(topic['title'])
        
        # Sort by trending score and return top 5
        unique_topics.sort(key=lambda x: x['trending_score'], reverse=True)
        return unique_topics[:5]
    
    def get_news(self, country: str, category: str = 'all') -> Dict[str, Any]:
        """Get Google News (mock implementation)"""
        # Mock news data
        news_data = {
            'items': [
                {
                    'title': 'Breaking News: Technology Innovation',
                    'link': 'https://example.com/news1',
                    'snippet': 'Latest developments in technology sector',
                    'source': 'Tech News',
                    'published_date': '2024-01-15'
                },
                {
                    'title': 'Business Update: Market Trends',
                    'link': 'https://example.com/news2',
                    'snippet': 'Current market analysis and predictions',
                    'source': 'Business Daily',
                    'published_date': '2024-01-15'
                }
            ],
            'total_results': 2
        }
        
        return news_data
    
    def get_trends(self, query: str, country: str) -> Dict[str, Any]:
        """Get Google Trends data (mock implementation)"""
        # Mock trends data
        trends_data = {
            'query': query,
            'country': country,
            'interest_over_time': [
                {'date': '2024-01-01', 'value': 75},
                {'date': '2024-01-02', 'value': 82},
                {'date': '2024-01-03', 'value': 78},
                {'date': '2024-01-04', 'value': 85},
                {'date': '2024-01-05', 'value': 90}
            ],
            'related_queries': [
                {'query': f'{query} tips', 'value': 85},
                {'query': f'{query} guide', 'value': 72},
                {'query': f'{query} examples', 'value': 68}
            ]
        }
        
        return trends_data
    
    def get_books(self, query: str, country: str) -> Dict[str, Any]:
        """Get Google Books data (mock implementation)"""
        # Mock books data
        books_data = {
            'items': [
                {
                    'volumeInfo': {
                        'title': f'Complete Guide to {query}',
                        'authors': ['Expert Author'],
                        'description': f'Comprehensive guide covering all aspects of {query}',
                        'publishedDate': '2024-01-01',
                        'pageCount': 300
                    }
                },
                {
                    'volumeInfo': {
                        'title': f'{query} for Beginners',
                        'authors': ['Beginner Author'],
                        'description': f'Simple introduction to {query} concepts',
                        'publishedDate': '2023-12-01',
                        'pageCount': 200
                    }
                }
            ],
            'totalItems': 2
        }
        
        return books_data
    
    def _mock_search_results(self, query: str, country: str) -> Dict[str, Any]:
        """Generate mock search results for demo"""
        return {
            'items': [
                {
                    'title': f'Search Result for: {query}',
                    'link': f'https://example.com/search?q={query}',
                    'snippet': f'This is a mock search result for {query} in {country}. In a real implementation, this would contain actual search results from Google.',
                    'source': 'Mock Search'
                }
            ],
            'search_time': 0.5,
            'total_results': 1
        }
    
    def _mock_book_topics(self, direction: str) -> List[Dict[str, Any]]:
        """Generate mock book topics for demo"""
        book_topics = {
            'technology': [
                {'title': 'Book: "AI Revolution"', 'description': 'Comprehensive guide to artificial intelligence and its impact on society', 'trending_score': 82},
                {'title': 'Book: "Cybersecurity Essentials"', 'description': 'Essential security practices for individuals and businesses', 'trending_score': 78},
                {'title': 'Book: "Digital Transformation"', 'description': 'How to modernize your business with technology', 'trending_score': 75},
                {'title': 'Book: "Programming Fundamentals"', 'description': 'Learn to code from the ground up', 'trending_score': 72},
                {'title': 'Book: "Cloud Computing Guide"', 'description': 'Understanding and implementing cloud solutions', 'trending_score': 70}
            ],
            'business_finance': [
                {'title': 'Book: "Investment Strategies"', 'description': 'Proven methods for building wealth through smart investing', 'trending_score': 85},
                {'title': 'Book: "Entrepreneurship Guide"', 'description': 'Starting and growing your own business', 'trending_score': 82},
                {'title': 'Book: "Personal Finance"', 'description': 'Managing your money effectively', 'trending_score': 79},
                {'title': 'Book: "Business Growth"', 'description': 'Scaling your business for success', 'trending_score': 76},
                {'title': 'Book: "Market Analysis"', 'description': 'Understanding financial markets and trends', 'trending_score': 73}
            ],
            'health_wellness': [
                {'title': 'Book: "Mental Health Guide"', 'description': 'Understanding and improving psychological well-being', 'trending_score': 84},
                {'title': 'Book: "Fitness Fundamentals"', 'description': 'Building a sustainable exercise routine', 'trending_score': 81},
                {'title': 'Book: "Nutrition Science"', 'description': 'Evidence-based nutrition and diet advice', 'trending_score': 78},
                {'title': 'Book: "Sleep Optimization"', 'description': 'Improving sleep quality and habits', 'trending_score': 75},
                {'title': 'Book: "Mindfulness Practice"', 'description': 'Meditation and stress reduction techniques', 'trending_score': 72}
            ],
            'education': [
                {'title': 'Book: "Learning Science"', 'description': 'Evidence-based approaches to effective learning', 'trending_score': 83},
                {'title': 'Book: "Career Development"', 'description': 'Professional growth and advancement strategies', 'trending_score': 80},
                {'title': 'Book: "Educational Technology"', 'description': 'How technology is transforming education', 'trending_score': 77},
                {'title': 'Book: "Study Methods"', 'description': 'Effective study techniques and strategies', 'trending_score': 74},
                {'title': 'Book: "Lifelong Learning"', 'description': 'Continuous education for adults', 'trending_score': 71}
            ],
            'entertainment': [
                {'title': 'Book: "Film Analysis"', 'description': 'Understanding cinema and storytelling', 'trending_score': 86},
                {'title': 'Book: "Music Industry"', 'description': 'Behind-the-scenes of the music business', 'trending_score': 83},
                {'title': 'Book: "Gaming Culture"', 'description': 'Video games and their impact on society', 'trending_score': 80},
                {'title': 'Book: "Celebrity Culture"', 'description': 'Understanding fame and media influence', 'trending_score': 77},
                {'title': 'Book: "Entertainment History"', 'description': 'Evolution of entertainment media', 'trending_score': 74}
            ],
            'lifestyle': [
                {'title': 'Book: "Minimalism Guide"', 'description': 'Simple living and intentional lifestyle choices', 'trending_score': 82},
                {'title': 'Book: "Digital Wellness"', 'description': 'Balancing technology use and well-being', 'trending_score': 79},
                {'title': 'Book: "Sustainable Living"', 'description': 'Eco-friendly lifestyle practices', 'trending_score': 76},
                {'title': 'Book: "Work-Life Balance"', 'description': 'Managing career and personal life', 'trending_score': 73},
                {'title': 'Book: "Personal Development"', 'description': 'Self-improvement and growth strategies', 'trending_score': 70}
            ],
            'sports': [
                {'title': 'Book: "Sports Psychology"', 'description': 'Mental aspects of athletic performance', 'trending_score': 85},
                {'title': 'Book: "Training Methods"', 'description': 'Effective athletic training techniques', 'trending_score': 82},
                {'title': 'Book: "Sports History"', 'description': 'Evolution of sports and athletics', 'trending_score': 79},
                {'title': 'Book: "Team Dynamics"', 'description': 'Building effective sports teams', 'trending_score': 76},
                {'title': 'Book: "Sports Nutrition"', 'description': 'Fueling athletic performance', 'trending_score': 73}
            ],
            'food_cooking': [
                {'title': 'Book: "Culinary Techniques"', 'description': 'Professional cooking methods and skills', 'trending_score': 84},
                {'title': 'Book: "Food Science"', 'description': 'Understanding the science behind cooking', 'trending_score': 81},
                {'title': 'Book: "Nutrition Guide"', 'description': 'Healthy eating and meal planning', 'trending_score': 78},
                {'title': 'Book: "International Cuisine"', 'description': 'Global cooking traditions and recipes', 'trending_score': 75},
                {'title': 'Book: "Sustainable Cooking"', 'description': 'Eco-friendly food practices', 'trending_score': 72}
            ],
            'travel': [
                {'title': 'Book: "Travel Planning"', 'description': 'How to plan the perfect trip', 'trending_score': 87},
                {'title': 'Book: "Cultural Immersion"', 'description': 'Deep travel experiences and learning', 'trending_score': 84},
                {'title': 'Book: "Budget Travel"', 'description': 'Affordable travel strategies', 'trending_score': 81},
                {'title': 'Book: "Sustainable Tourism"', 'description': 'Responsible travel practices', 'trending_score': 78},
                {'title': 'Book: "Travel Photography"', 'description': 'Capturing amazing travel moments', 'trending_score': 75}
            ],
            'fashion_beauty': [
                {'title': 'Book: "Fashion History"', 'description': 'Evolution of fashion and style', 'trending_score': 83},
                {'title': 'Book: "Sustainable Fashion"', 'description': 'Eco-friendly clothing choices', 'trending_score': 80},
                {'title': 'Book: "Beauty Science"', 'description': 'Understanding beauty products and practices', 'trending_score': 77},
                {'title': 'Book: "Style Guide"', 'description': 'Building a personal fashion style', 'trending_score': 74},
                {'title': 'Book: "Body Positivity"', 'description': 'Self-love and confidence building', 'trending_score': 71}
            ],
            'parenting': [
                {'title': 'Book: "Child Development"', 'description': 'Understanding how children grow and learn', 'trending_score': 84},
                {'title': 'Book: "Parenting Strategies"', 'description': 'Effective parenting techniques', 'trending_score': 81},
                {'title': 'Book: "Digital Parenting"', 'description': 'Managing children\'s technology use', 'trending_score': 78},
                {'title': 'Book: "Family Communication"', 'description': 'Building strong family relationships', 'trending_score': 75},
                {'title': 'Book: "Parent Wellness"', 'description': 'Taking care of yourself as a parent', 'trending_score': 72}
            ],
            'pets_animals': [
                {'title': 'Book: "Pet Care Guide"', 'description': 'Comprehensive pet care and training', 'trending_score': 83},
                {'title': 'Book: "Animal Behavior"', 'description': 'Understanding pet psychology', 'trending_score': 80},
                {'title': 'Book: "Veterinary Care"', 'description': 'Pet health and medical information', 'trending_score': 77},
                {'title': 'Book: "Wildlife Conservation"', 'description': 'Protecting animals and habitats', 'trending_score': 74},
                {'title': 'Book: "Pet Training"', 'description': 'Effective training methods for pets', 'trending_score': 71}
            ],
            'automotive': [
                {'title': 'Book: "Car Maintenance"', 'description': 'Keeping your vehicle in top condition', 'trending_score': 86},
                {'title': 'Book: "Electric Vehicles"', 'description': 'Understanding EV technology and adoption', 'trending_score': 83},
                {'title': 'Book: "Automotive Technology"', 'description': 'Latest innovations in cars', 'trending_score': 80},
                {'title': 'Book: "Driving Safety"', 'description': 'Safe driving practices and techniques', 'trending_score': 77},
                {'title': 'Book: "Car History"', 'description': 'Evolution of automotive industry', 'trending_score': 74}
            ],
            'real_estate': [
                {'title': 'Book: "Real Estate Investment"', 'description': 'Property investment strategies', 'trending_score': 85},
                {'title': 'Book: "Home Buying Guide"', 'description': 'Complete guide to purchasing property', 'trending_score': 82},
                {'title': 'Book: "Property Management"', 'description': 'Managing rental properties effectively', 'trending_score': 79},
                {'title': 'Book: "Real Estate Market"', 'description': 'Understanding property markets', 'trending_score': 76},
                {'title': 'Book: "Home Improvement"', 'description': 'DIY and renovation projects', 'trending_score': 73}
            ],

            'science_research': [
                {'title': 'Book: "Scientific Method"', 'description': 'Understanding how science works', 'trending_score': 87},
                {'title': 'Book: "Research Methods"', 'description': 'Conducting effective research', 'trending_score': 84},
                {'title': 'Book: "Climate Science"', 'description': 'Understanding environmental science', 'trending_score': 81},
                {'title': 'Book: "Medical Research"', 'description': 'Healthcare and medical discoveries', 'trending_score': 78},
                {'title': 'Book: "Space Science"', 'description': 'Astronomy and space exploration', 'trending_score': 75}
            ],
            'politics_society': [
                {'title': 'Book: "Political Science"', 'description': 'Understanding political systems', 'trending_score': 86},
                {'title': 'Book: "Social Justice"', 'description': 'Equality and civil rights movements', 'trending_score': 83},
                {'title': 'Book: "Civic Engagement"', 'description': 'Participating in democracy', 'trending_score': 80},
                {'title': 'Book: "Policy Analysis"', 'description': 'Understanding how policies work', 'trending_score': 77},
                {'title': 'Book: "International Relations"', 'description': 'Global politics and diplomacy', 'trending_score': 74}
            ],
            'environment_sustainability': [
                {'title': 'Book: "Climate Action"', 'description': 'Addressing climate change challenges', 'trending_score': 89},
                {'title': 'Book: "Sustainable Living"', 'description': 'Eco-friendly lifestyle practices', 'trending_score': 86},
                {'title': 'Book: "Renewable Energy"', 'description': 'Sustainable energy solutions', 'trending_score': 83},
                {'title': 'Book: "Conservation Biology"', 'description': 'Protecting biodiversity and ecosystems', 'trending_score': 80},
                {'title': 'Book: "Environmental Policy"', 'description': 'Environmental protection and regulation', 'trending_score': 77}
            ],
            'art_creativity': [
                {'title': 'Book: "Art and Design Insights"', 'description': 'Understanding creative industries and trends', 'trending_score': 85},
                {'title': 'Book: "Creative Entrepreneurship"', 'description': 'Building successful creative businesses', 'trending_score': 82},
                {'title': 'Book: "Artistic Expression"', 'description': 'Exploring different forms of creative expression', 'trending_score': 79},
                {'title': 'Book: "Design Innovation"', 'description': 'Breakthroughs in graphic and product design', 'trending_score': 76},
                {'title': 'Book: "Creative Inspiration"', 'description': 'Inspiring stories and insights for artists', 'trending_score': 73}
            ]
        }
        
        return book_topics.get(direction, book_topics['technology']) 