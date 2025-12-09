import logging
import time
import requests
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class NewsApiSource:
    @staticmethod
    def fetch(limit: int = 10, keywords: list = None) -> List[Dict[str, Any]]:
        try:
            from config import NEWS_API_ENABLED, NEWS_API_KEY, NEWS_API_COUNTRY, NEWS_API_CATEGORY
            
            if not NEWS_API_ENABLED or not NEWS_API_KEY:
                logger.warning("News API not enabled or configured")
                return []
            
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                "apiKey": NEWS_API_KEY,
                "pageSize": limit
            }

            # Use keywords if provided, otherwise default to country/category
            if keywords and len(keywords) > 0:
                params["q"] = " OR ".join(keywords)
            else:
                params["country"] = NEWS_API_COUNTRY
                params["category"] = NEWS_API_CATEGORY
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            trends = []
            
            if data.get("status") == "ok":
                for idx, article in enumerate(data.get("articles", [])[:limit]):
                    trends.append({
                        "id": f"news_{idx}",
                        "title": article.get("title", ""),
                        "source": article.get("source", {}).get("name", "News"),
                        "category": "News",
                        "score": 100 - (idx * 5),
                        "summary": article.get("description", ""),
                        "timestamp": article.get("publishedAt", datetime.utcnow().isoformat() + 'Z'),
                        "url": article.get("url", ""),
                        "image": article.get("urlToImage", "")
                    })
            
            logger.info(f"Fetched {len(trends)} trends from News API")
            return trends
            
        except Exception as e:
            logger.error(f"News API error: {e}")
            return []
