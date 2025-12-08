"""
Multi-source Trends Service
Fetches trending topics from multiple real sources:
- Google Trends
- Twitter/X API
- News API
- RSS Feeds
- SerpAPI
"""

import logging
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any
import requests
import feedparser

logger = logging.getLogger(__name__)


class MultiTrendsService:
    """Aggregate trends from multiple real sources"""

    # Default cache to store results
    _cache = {}
    _cache_ttl = 3600  # 1 hour

    @staticmethod
    def _is_cached_valid(source: str, ttl: int = None) -> bool:
        """Check if cache for a source is still valid"""
        if ttl is None:
            ttl = MultiTrendsService._cache_ttl
        
        cached = MultiTrendsService._cache.get(source, {})
        if not cached or "timestamp" not in cached:
            return False
        
        age = time.time() - cached["timestamp"]
        return age < ttl

    @staticmethod
    def fetch_google_trends(limit: int = 10, geo: str = "global", retries: int = 3) -> List[Dict[str, Any]]:
        """
        Fetch trends from Google Trends via pytrends
        
        Args:
            limit: Number of trends to fetch
            geo: Geographic code (e.g., 'US', 'MX', 'global')
            retries: Number of retry attempts
            
        Returns:
            List of trend dicts
        """
        if MultiTrendsService._is_cached_valid("google_trends"):
            logger.info("Returning cached Google Trends")
            return MultiTrendsService._cache["google_trends"]["data"][:limit]
        
        try:
            from pytrends.request import TrendReq
            
            pytrends = TrendReq(hl='es-MX', tz=360)
            
            for attempt in range(retries):
                try:
                    # Get trending searches
                    trending = pytrends.trending_searches(pn='MEXICO' if geo in ['MX', 'mexico'] else 'GLOBAL')
                    
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
                    
                    # Cache result
                    MultiTrendsService._cache["google_trends"] = {
                        "data": trends,
                        "timestamp": time.time()
                    }
                    
                    logger.info(f"Fetched {len(trends)} trends from Google Trends")
                    return trends
                    
                except Exception as e:
                    if attempt < retries - 1:
                        wait_time = 2 ** attempt  # Exponential backoff
                        logger.warning(f"Google Trends attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Google Trends failed after {retries} attempts: {e}")
                        raise
                        
        except Exception as e:
            logger.error(f"Google Trends error: {e}")
            return []

    @staticmethod
    def fetch_twitter_trends(limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch trending topics from Twitter/X API v2
        
        Requires:
        - TWITTER_BEARER_TOKEN environment variable
        
        Args:
            limit: Number of trends to fetch
            
        Returns:
            List of trend dicts
        """
        try:
            from config import TWITTER_API_ENABLED, TWITTER_BEARER_TOKEN
            
            if not TWITTER_API_ENABLED or not TWITTER_BEARER_TOKEN:
                logger.warning("Twitter API not enabled or configured")
                return []
            
            if MultiTrendsService._is_cached_valid("twitter"):
                logger.info("Returning cached Twitter trends")
                return MultiTrendsService._cache["twitter"]["data"][:limit]
            
            import tweepy
            
            # Initialize client with Bearer Token (v2 API)
            client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
            
            # Get trending topics for Mexico (geo_id 23424957)
            # Worldwide is 1
            response = client.get_trending_by_place(
                id=23424957,  # Mexico ID
                max_results=limit
            )
            
            trends = []
            if response.data:
                for idx, trend in enumerate(response.data):
                    trends.append({
                        "id": f"tw_{idx}",
                        "title": trend.name,
                        "source": "Twitter/X",
                        "category": "Social Media",
                        "score": 100 - (idx * 5),
                        "summary": f"Trending on Twitter/X (#{trend.promoted_content or 'organic'})",
                        "timestamp": datetime.utcnow().isoformat() + 'Z',
                        "url": f"https://twitter.com/search?q={trend.name.replace(' ', '%20')}"
                    })
            
            # Cache result
            MultiTrendsService._cache["twitter"] = {
                "data": trends,
                "timestamp": time.time()
            }
            
            logger.info(f"Fetched {len(trends)} trends from Twitter")
            return trends
            
        except Exception as e:
            logger.error(f"Twitter API error: {e}")
            return []

    @staticmethod
    def fetch_news_api_trends(limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch trending news topics from NewsAPI
        
        Requires:
        - NEWS_API_KEY environment variable
        Uses requests library to call REST API directly (no newsapi package needed)
        
        Args:
            limit: Number of trends to fetch
            
        Returns:
            List of trend dicts
        """
        try:
            from config import NEWS_API_ENABLED, NEWS_API_KEY, NEWS_API_COUNTRY, NEWS_API_CATEGORY
            
            if not NEWS_API_ENABLED or not NEWS_API_KEY:
                logger.warning("News API not enabled or configured")
                return []
            
            if MultiTrendsService._is_cached_valid("newsapi"):
                logger.info("Returning cached News API trends")
                return MultiTrendsService._cache["newsapi"]["data"][:limit]
            
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                "apiKey": NEWS_API_KEY,
                "country": NEWS_API_COUNTRY,
                "category": NEWS_API_CATEGORY,
                "pageSize": limit
            }
            
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
            
            # Cache result
            MultiTrendsService._cache["newsapi"] = {
                "data": trends,
                "timestamp": time.time()
            }
            
            logger.info(f"Fetched {len(trends)} trends from News API")
            return trends
            
        except Exception as e:
            logger.error(f"News API error: {e}")
            return []

    @staticmethod
    def fetch_rss_feeds_trends(limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch trending topics from configured RSS feeds
        
        No API key required, uses RSS_FEED_URLS from config
        
        Args:
            limit: Number of trends to fetch
            
        Returns:
            List of trend dicts
        """
        try:
            from config import RSS_FEEDS_ENABLED, RSS_FEED_URLS
            
            if not RSS_FEEDS_ENABLED or not RSS_FEED_URLS:
                logger.warning("RSS Feeds not enabled or configured")
                return []
            
            if MultiTrendsService._is_cached_valid("rss_feeds"):
                logger.info("Returning cached RSS Feeds trends")
                return MultiTrendsService._cache["rss_feeds"]["data"][:limit]
            
            trends = []
            
            for feed_url in RSS_FEED_URLS:
                if len(trends) >= limit:
                    break
                
                try:
                    feed = feedparser.parse(feed_url)
                    
                    for idx, entry in enumerate(feed.entries[:5]):  # Max 5 per feed
                        if len(trends) >= limit:
                            break
                        
                        trends.append({
                            "id": f"rss_{len(trends)}",
                            "title": entry.get("title", ""),
                            "source": feed.feed.get("title", "RSS Feed"),
                            "category": "RSS",
                            "score": 90 - (len(trends) * 3),
                            "summary": entry.get("summary", "")[:200],
                            "timestamp": entry.get("published", datetime.utcnow().isoformat() + 'Z'),
                            "url": entry.get("link", "")
                        })
                        
                except Exception as feed_err:
                    logger.warning(f"Error parsing RSS feed {feed_url}: {feed_err}")
                    continue
            
            # Cache result
            MultiTrendsService._cache["rss_feeds"] = {
                "data": trends,
                "timestamp": time.time()
            }
            
            logger.info(f"Fetched {len(trends)} trends from RSS Feeds")
            return trends
            
        except Exception as e:
            logger.error(f"RSS Feeds error: {e}")
            return []

    @staticmethod
    def fetch_serpapi_trends(limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch trending topics from SerpAPI
        
        Requires:
        - SERPAPI_API_KEY environment variable
        
        Args:
            limit: Number of trends to fetch
            
        Returns:
            List of trend dicts
        """
        try:
            from config import SERPAPI_ENABLED, SERPAPI_API_KEY
            
            if not SERPAPI_ENABLED or not SERPAPI_API_KEY:
                logger.warning("SerpAPI not enabled or configured")
                return []
            
            if MultiTrendsService._is_cached_valid("serpapi"):
                logger.info("Returning cached SerpAPI trends")
                return MultiTrendsService._cache["serpapi"]["data"][:limit]
            
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
            
            # Cache result
            MultiTrendsService._cache["serpapi"] = {
                "data": trends,
                "timestamp": time.time()
            }
            
            logger.info(f"Fetched {len(trends)} trends from SerpAPI")
            return trends
            
        except Exception as e:
            logger.error(f"SerpAPI error: {e}")
            return []

    @staticmethod
    def fetch_all_trends(limit: int = 20, sources: List[str] = None, force: bool = False) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch trends from all enabled sources and combine them
        
        Args:
            limit: Maximum number of results per source
            sources: List of sources to fetch from. If None, fetches from all enabled
            force: Force refresh even if cached
            
        Returns:
            Dict with source names as keys and trend lists as values
        """
        all_sources = ["google_trends", "twitter", "newsapi", "rss_feeds", "serpapi"]
        
        if sources is None:
            sources = all_sources
        
        # Clear cache if force refresh requested
        if force:
            MultiTrendsService._cache.clear()
        
        results = {}
        
        if "google_trends" in sources:
            results["google_trends"] = MultiTrendsService.fetch_google_trends(limit)
        
        if "twitter" in sources:
            results["twitter"] = MultiTrendsService.fetch_twitter_trends(limit)
        
        if "newsapi" in sources:
            results["newsapi"] = MultiTrendsService.fetch_news_api_trends(limit)
        
        if "rss_feeds" in sources:
            results["rss_feeds"] = MultiTrendsService.fetch_rss_feeds_trends(limit)
        
        if "serpapi" in sources:
            results["serpapi"] = MultiTrendsService.fetch_serpapi_trends(limit)
        
        return results

    @staticmethod
    def flatten_trends(all_trends: Dict[str, List[Dict[str, Any]]], limit: int = 20) -> List[Dict[str, Any]]:
        """
        Flatten and sort all trends from multiple sources by score
        
        Args:
            all_trends: Dict from fetch_all_trends()
            limit: Maximum number of results to return
            
        Returns:
            Sorted list of unique trends
        """
        flattened = []
        seen_titles = set()
        
        # Combine all trends
        for source, trends in all_trends.items():
            for trend in trends:
                title_lower = trend.get("title", "").lower()
                if title_lower not in seen_titles:
                    flattened.append(trend)
                    seen_titles.add(title_lower)
        
        # Sort by score descending
        flattened.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        return flattened[:limit]
