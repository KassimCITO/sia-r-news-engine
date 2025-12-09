import logging
import time
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class TwitterSource:
    @staticmethod
    def fetch(limit: int = 10, keywords: list = None) -> List[Dict[str, Any]]:
        try:
            from config import TWITTER_API_ENABLED, TWITTER_BEARER_TOKEN
            
            if not TWITTER_API_ENABLED or not TWITTER_BEARER_TOKEN:
                logger.warning("Twitter API not enabled or configured")
                return []
            
            import tweepy
            
            # Initialize API with Bearer Token (v1.1 API for trends)
            auth = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
            # Actually we need OAuth2BearerHandler for v1.1 API access with bearer token
            # But tweepy.Client is v2. For trends we need v1.1.
            # However, Tweepy's Client doesn't have get_place_trends.
            # We need tweepy.API. 
            
            auth = tweepy.OAuth2BearerHandler(TWITTER_BEARER_TOKEN)
            api = tweepy.API(auth)
            
            # Get trending topics for Mexico (geo_id 23424957)
            trends_result = api.get_place_trends(id=23424957)
            
            trends = []
            if trends_result:
                # API returns list containing one object with 'trends' key
                for idx, trend in enumerate(trends_result[0]['trends'][:limit]):
                    trends.append({
                        "id": f"tw_{idx}",
                        "title": trend['name'],
                        "source": "Twitter/X",
                        "category": "Social Media",
                        "score": 100 - (idx * 5),
                        "summary": f"Trending on Twitter/X ({trend.get('tweet_volume') or 'organic'} tweets)",
                        "timestamp": datetime.utcnow().isoformat() + 'Z',
                        "url": trend['url']
                    })
            
            logger.info(f"Fetched {len(trends)} trends from Twitter")
            return trends
            
        except Exception as e:
            logger.error(f"Twitter API error: {e}")
            return []
