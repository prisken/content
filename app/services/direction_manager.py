from app.models.content_direction import ContentDirection, RegionalData
from app import db
import json

class DirectionManager:
    """Manages content direction/niche configurations and regional adaptations"""
    
    def __init__(self):
        self.content_directions = {
            "business_finance": {
                "name": "Business & Finance",
                "subcategories": ["entrepreneurship", "investing", "corporate", "market_analysis"],
                "language_style": "professional, authoritative",
                "sources": ["bloomberg", "cnbc", "wsj", "forbes"],
                "hashtags": ["business", "finance", "entrepreneurship", "investing"],
                "regional_adaptation": "local_markets, regional_business_trends"
            },
            "technology": {
                "name": "Technology",
                "subcategories": ["tech_news", "software", "ai", "digital_transformation"],
                "language_style": "innovative, technical",
                "sources": ["techcrunch", "the_verge", "wired", "ars_technica"],
                "hashtags": ["tech", "innovation", "ai", "digital"],
                "regional_adaptation": "local_tech_scene, regional_innovation"
            },
            "health_wellness": {
                "name": "Health & Wellness",
                "subcategories": ["fitness", "nutrition", "mental_health", "lifestyle"],
                "language_style": "supportive, informative",
                "sources": ["health_news", "nutrition_sources", "fitness_experts"],
                "hashtags": ["health", "wellness", "fitness", "nutrition"],
                "regional_adaptation": "local_health_trends, regional_wellness"
            },
            "education": {
                "name": "Education",
                "subcategories": ["learning", "skills_development", "academic_insights", "online_courses"],
                "language_style": "informative, educational",
                "sources": ["education_news", "academic_journals", "learning_platforms"],
                "hashtags": ["education", "learning", "skills", "academic"],
                "regional_adaptation": "local_education_trends, regional_learning"
            },
            "entertainment": {
                "name": "Entertainment",
                "subcategories": ["movies", "music", "gaming", "pop_culture"],
                "language_style": "engaging, trend_aware",
                "sources": ["entertainment_news", "music_platforms", "gaming_sites"],
                "hashtags": ["entertainment", "movies", "music", "gaming"],
                "regional_adaptation": "local_entertainment, regional_pop_culture"
            },
            "travel_tourism": {
                "name": "Travel & Tourism",
                "subcategories": ["destinations", "travel_tips", "cultural_experiences", "hospitality"],
                "language_style": "inspirational, destination_focused",
                "sources": ["travel_guides", "tourism_news", "destination_sites"],
                "hashtags": ["travel", "tourism", "destinations", "adventure"],
                "regional_adaptation": "local_travel_trends, regional_destinations"
            },
            "food_cooking": {
                "name": "Food & Cooking",
                "subcategories": ["recipes", "culinary_trends", "restaurant_reviews", "food_industry"],
                "language_style": "appetizing, recipe_friendly",
                "sources": ["food_news", "recipe_sites", "culinary_platforms"],
                "hashtags": ["food", "cooking", "recipes", "culinary"],
                "regional_adaptation": "local_food_trends, regional_cuisine"
            },
            "fashion_beauty": {
                "name": "Fashion & Beauty",
                "subcategories": ["style_trends", "beauty_tips", "fashion_industry", "personal_style"],
                "language_style": "trend_aware, style_focused",
                "sources": ["fashion_news", "beauty_platforms", "style_sites"],
                "hashtags": ["fashion", "beauty", "style", "trends"],
                "regional_adaptation": "local_fashion_trends, regional_style"
            },
            "sports_fitness": {
                "name": "Sports & Fitness",
                "subcategories": ["athletics", "training", "sports_news", "fitness_trends"],
                "language_style": "dynamic, action_oriented",
                "sources": ["sports_news", "fitness_platforms", "training_sites"],
                "hashtags": ["sports", "fitness", "training", "athletics"],
                "regional_adaptation": "local_sports_trends, regional_fitness"
            },
            "science_research": {
                "name": "Science & Research",
                "subcategories": ["scientific_discoveries", "research_insights", "innovation"],
                "language_style": "accurate, research_based",
                "sources": ["science_journals", "research_papers", "scientific_news"],
                "hashtags": ["science", "research", "innovation", "discovery"],
                "regional_adaptation": "local_research_trends, regional_innovation"
            },
            "politics_current_events": {
                "name": "Politics & Current Events",
                "subcategories": ["political_analysis", "world_news", "policy_insights"],
                "language_style": "balanced, fact_based",
                "sources": ["political_news", "policy_analysis", "world_news"],
                "hashtags": ["politics", "news", "current_events", "policy"],
                "regional_adaptation": "local_political_trends, regional_news"
            },
            "environment_sustainability": {
                "name": "Environment & Sustainability",
                "subcategories": ["climate_change", "green_living", "environmental_news"],
                "language_style": "eco_conscious, sustainability_focused",
                "sources": ["environmental_news", "sustainability_sites", "climate_research"],
                "hashtags": ["environment", "sustainability", "climate", "green"],
                "regional_adaptation": "local_environmental_trends, regional_sustainability"
            },
            "personal_development": {
                "name": "Personal Development",
                "subcategories": ["self_improvement", "motivation", "productivity", "life_coaching"],
                "language_style": "motivational, growth_oriented",
                "sources": ["self_help_books", "motivation_platforms", "productivity_sites"],
                "hashtags": ["personal_development", "motivation", "growth", "productivity"],
                "regional_adaptation": "local_development_trends, regional_motivation"
            },
            "parenting_family": {
                "name": "Parenting & Family",
                "subcategories": ["child_rearing", "family_life", "education", "parenting_tips"],
                "language_style": "supportive, family_focused",
                "sources": ["parenting_news", "family_platforms", "education_sites"],
                "hashtags": ["parenting", "family", "children", "education"],
                "regional_adaptation": "local_parenting_trends, regional_family"
            },
            "art_creativity": {
                "name": "Art & Creativity",
                "subcategories": ["design", "creativity", "artistic_expression", "creative_industries"],
                "language_style": "creative, aesthetic_focused",
                "sources": ["art_news", "design_platforms", "creative_sites"],
                "hashtags": ["art", "creativity", "design", "creative"],
                "regional_adaptation": "local_art_trends, regional_creativity"
            },
            "real_estate": {
                "name": "Real Estate",
                "subcategories": ["property_market", "investment", "home_improvement", "market_trends"],
                "language_style": "market_aware, property_focused",
                "sources": ["real_estate_news", "property_platforms", "market_analysis"],
                "hashtags": ["real_estate", "property", "investment", "housing"],
                "regional_adaptation": "local_market_trends, regional_property"
            },
            "automotive": {
                "name": "Automotive",
                "subcategories": ["cars", "industry_news", "maintenance_tips", "automotive_technology"],
                "language_style": "technical, feature_focused",
                "sources": ["automotive_news", "car_reviews", "tech_platforms"],
                "hashtags": ["automotive", "cars", "technology", "maintenance"],
                "regional_adaptation": "local_automotive_trends, regional_technology"
            },
            "pet_care": {
                "name": "Pet Care",
                "subcategories": ["animal_welfare", "pet_training", "veterinary_insights", "pet_industry"],
                "language_style": "caring, informative",
                "sources": ["pet_news", "veterinary_sites", "training_platforms"],
                "hashtags": ["pet_care", "animals", "training", "veterinary"],
                "regional_adaptation": "local_pet_trends, regional_animal_care"
            }
        }
    
    def get_direction_config(self, direction_key, region='global'):
        """Get direction configuration with regional adaptation"""
        if direction_key not in self.content_directions:
            return None
        
        direction_config = self.content_directions[direction_key].copy()
        
        # Add regional adaptation
        direction_config['region'] = region
        direction_config['regional_context'] = self.get_regional_context(region)
        
        return direction_config
    
    def get_direction_context(self, direction_key, region='global'):
        """Get direction context for content generation"""
        config = self.get_direction_config(direction_key, region)
        if not config:
            return {}
        
        return {
            'direction_name': config['name'],
            'language_style': config['language_style'],
            'hashtags': config['hashtags'],
            'regional_context': config.get('regional_context', {}),
            'subcategories': config['subcategories']
        }
    
    def get_regional_context(self, region):
        """Get regional context and cultural preferences"""
        # In real app, fetch from RegionalData model
        # For now, return basic regional context
        regional_contexts = {
            'global': {
                'cultural_sensitivity': 'general',
                'local_events': [],
                'regional_trends': [],
                'business_practices': 'international'
            },
            'north_america': {
                'cultural_sensitivity': 'western',
                'local_events': ['holidays', 'business_events'],
                'regional_trends': ['tech_innovation', 'business_growth'],
                'business_practices': 'american'
            },
            'europe': {
                'cultural_sensitivity': 'european',
                'local_events': ['cultural_festivals', 'business_conferences'],
                'regional_trends': ['sustainability', 'innovation'],
                'business_practices': 'european'
            },
            'asia_pacific': {
                'cultural_sensitivity': 'asian',
                'local_events': ['traditional_celebrations', 'business_meetings'],
                'regional_trends': ['digital_transformation', 'economic_growth'],
                'business_practices': 'asian'
            }
        }
        
        return regional_contexts.get(region, regional_contexts['global'])
    
    def validate_direction_appropriateness(self, content, direction_key, region='global'):
        """Validate if content is appropriate for selected direction and region"""
        config = self.get_direction_config(direction_key, region)
        if not config:
            return False, "Invalid direction"
        
        # Basic validation (in real app, use AI for more sophisticated checking)
        validation_result = {
            'is_appropriate': True,
            'suggestions': [],
            'warnings': []
        }
        
        # Check if content contains direction-specific keywords
        direction_keywords = self.get_direction_keywords(direction_key)
        content_lower = content.lower()
        
        keyword_matches = [keyword for keyword in direction_keywords if keyword.lower() in content_lower]
        
        if len(keyword_matches) < 1:
            validation_result['suggestions'].append(f"Consider including {direction_key} related terms")
        
        # Check cultural sensitivity
        regional_context = self.get_regional_context(region)
        if regional_context['cultural_sensitivity'] != 'general':
            validation_result['warnings'].append(f"Ensure content is culturally appropriate for {region}")
        
        return validation_result
    
    def get_direction_keywords(self, direction_key):
        """Get keywords relevant to the direction"""
        direction_keywords = {
            'business_finance': ['business', 'finance', 'investment', 'market', 'entrepreneur', 'startup', 'revenue', 'profit'],
            'technology': ['technology', 'innovation', 'digital', 'software', 'ai', 'tech', 'startup', 'development'],
            'health_wellness': ['health', 'wellness', 'fitness', 'nutrition', 'mental', 'lifestyle', 'wellbeing'],
            'education': ['education', 'learning', 'skills', 'knowledge', 'training', 'development', 'academic'],
            'entertainment': ['entertainment', 'movie', 'music', 'gaming', 'celebrity', 'show', 'performance'],
            'travel_tourism': ['travel', 'tourism', 'destination', 'vacation', 'adventure', 'explore', 'journey'],
            'food_cooking': ['food', 'cooking', 'recipe', 'culinary', 'kitchen', 'chef', 'cuisine', 'dining'],
            'fashion_beauty': ['fashion', 'beauty', 'style', 'trend', 'design', 'aesthetic', 'look', 'outfit'],
            'sports_fitness': ['sports', 'fitness', 'athletic', 'training', 'workout', 'performance', 'competition'],
            'science_research': ['science', 'research', 'discovery', 'innovation', 'study', 'analysis', 'experiment'],
            'politics_current_events': ['politics', 'news', 'current', 'policy', 'government', 'election', 'democracy'],
            'environment_sustainability': ['environment', 'sustainability', 'climate', 'green', 'eco', 'conservation'],
            'personal_development': ['personal', 'development', 'growth', 'motivation', 'improvement', 'success'],
            'parenting_family': ['parenting', 'family', 'children', 'child', 'parent', 'family_life', 'raising'],
            'art_creativity': ['art', 'creativity', 'creative', 'design', 'artistic', 'inspiration', 'expression'],
            'real_estate': ['real_estate', 'property', 'housing', 'market', 'investment', 'home', 'buying'],
            'automotive': ['automotive', 'car', 'vehicle', 'transportation', 'driving', 'maintenance', 'technology'],
            'pet_care': ['pet', 'animal', 'care', 'training', 'veterinary', 'companion', 'pet_health']
        }
        
        return direction_keywords.get(direction_key, [])
    
    def get_all_directions(self):
        """Get all available content directions"""
        return [
            {
                'key': key,
                'name': config['name'],
                'subcategories': config['subcategories'],
                'hashtags': config['hashtags']
            }
            for key, config in self.content_directions.items()
        ] 