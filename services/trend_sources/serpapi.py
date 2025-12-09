import logging
import time
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class SerpApiSource:
    @staticmethod
    def fetch(limit: int = 10, keywords: list = None) -> List[Dict[str, Any]]:
        try:
            from config import SERPAPI_ENABLED, SERPAPI_API_KEY
            
            if not SERPAPI_ENABLED or not SERPAPI_API_KEY:
                logger.warning("SerpAPI not enabled or configured")
                return []
            
            from google_search_results import GoogleSearchResults
            
            params = {
                "api_key": SERPAPI_API_KEY,
                "engine": "google_trends",
                "data_type": "realtime_trends",
                "data_geo": "MEXICO"
            }
            
            client = GoogleSearchResults(params)
            results = client.get_dict()
            
            trends = []
            
            if "realtime_trends" in results:
                for idx, trend_data in enumerate(results["realtime_trends"][:limit]):
                    trends.append({
                        "id": f"serp_{idx}",
                        "title": trend_data.get("title", ""),
                        "source": "SerpAPI",
                        "category": "Search",
                        "score": 100 - (idx * 5),
                        "summary": trend_data.get("description", ""),
                        "timestamp": datetime.utcnow().isoformat() + 'Z',
                        "url": trend_data.get("url", "")
                    })
            
            logger.info(f"Fetched {len(trends)} trends from SerpAPI")
            return trends
            
        except Exception as e:
            logger.error(f"SerpAPI error: {e}")
            return []
