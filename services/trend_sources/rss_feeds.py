import logging
import time
import feedparser
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class RssFeedSource:
    @staticmethod
    def fetch(limit: int = 10, keywords: list = None) -> List[Dict[str, Any]]:
        try:
            from config import RSS_FEEDS_ENABLED, RSS_FEED_URLS
            
            if not RSS_FEEDS_ENABLED or not RSS_FEED_URLS:
                logger.warning("RSS Feeds not enabled or configured")
                return []
            
            trends = []
            
            # Helper to check keywords
            def matches_keywords(text):
                if not keywords: return True
                text = text.lower()
                return any(k.lower() in text for k in keywords)
            
            for feed_url in RSS_FEED_URLS:
                if len(trends) >= limit:
                    break
                
                try:
                    feed = feedparser.parse(feed_url)
                    
                    for idx, entry in enumerate(feed.entries[:10]):  # Check more to filter
                        if len(trends) >= limit:
                            break
                        
                        title = entry.get("title", "")
                        summary = entry.get("summary", "")[:200]
                        
                        if not matches_keywords(title + " " + summary):
                            continue
                        
                        trends.append({
                            "id": f"rss_{len(trends)}",
                            "title": title,
                            "source": feed.feed.get("title", "RSS Feed"),
                            "category": "RSS",
                            "score": 90 - (len(trends) * 3),
                            "summary": summary,
                            "timestamp": entry.get("published", datetime.utcnow().isoformat() + 'Z'),
                            "url": entry.get("link", "")
                        })
                        
                except Exception as feed_err:
                    logger.warning(f"Error parsing RSS feed {feed_url}: {feed_err}")
                    continue
            
            logger.info(f"Fetched {len(trends)} trends from RSS Feeds")
            return trends
            
        except Exception as e:
            logger.error(f"RSS Feeds error: {e}")
            return []
