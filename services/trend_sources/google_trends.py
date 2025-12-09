import logging
import time
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class GoogleTrendsSource:
    @staticmethod
    def fetch(limit: int = 10, geo: str = "global", retries: int = 3, keywords: list = None) -> List[Dict[str, Any]]:
        try:
            from pytrends.request import TrendReq
            
            pytrends = TrendReq(hl='es-MX', tz=360)
            
            for attempt in range(retries):
                try:
                    # Get trending searches
                    trending = pytrends.trending_searches(pn='mexico' if geo in ['MX', 'mexico'] else 'united_states')
                    
                    trends = []
                    for idx, title in enumerate(trending.values.flatten()[:limit]):
                        trends.append({
                            "id": f"gt_{idx}",
                            "title": str(title),
                            "source": "Google Trends",
                            "category": "General",
                            "score": 100 - (idx * 5),  # Decreasing score
                            "summary": f"Trending on Google Trends",
                            "timestamp": datetime.utcnow().isoformat() + 'Z'
                        })
                    
                    logger.info(f"Fetched {len(trends)} trends from Google Trends")
                    return trends
                    
                except Exception as e:
                    if attempt < retries - 1:
                        wait_time = 2 ** attempt
                        logger.warning(f"Google Trends attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Google Trends failed after {retries} attempts: {e}")
            return []
                        
        except Exception as e:
            logger.error(f"Google Trends error: {e}")
            return []
