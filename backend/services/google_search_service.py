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
            ]
        }
        
        return podcast_topics.get(direction, podcast_topics['technology'])
    
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
            ]
        }
        
        return book_topics.get(direction, book_topics['technology']) 