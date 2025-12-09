import logging
import time
from typing import List, Dict, Any
from services.trend_sources.google_trends import GoogleTrendsSource
from services.trend_sources.twitter_x import TwitterSource
from services.trend_sources.news_api import NewsApiSource
from services.trend_sources.rss_feeds import RssFeedSource
from services.trend_sources.serpapi import SerpApiSource

logger = logging.getLogger(__name__)

class TrendHarvester:
    """Aggregate trends from multiple real sources"""

    # Default cache to store results
    _cache = {}
    _cache_ttl = 10800  # 3 hours (was 1 hour)

    @staticmethod
    def _is_cached_valid(source: str, ttl: int = None) -> bool:
        """Check if cache for a source is still valid"""
        if ttl is None:
            ttl = TrendHarvester._cache_ttl
        
        cached = TrendHarvester._cache.get(source, {})
        if not cached or "timestamp" not in cached:
            return False
        
        age = time.time() - cached["timestamp"]
        return age < ttl

    @staticmethod
    def _filter_trends_by_keywords(trends: List[Dict[str, Any]], keywords: List[str]) -> List[Dict[str, Any]]:
        """Filter trends based on keywords"""
        if not keywords:
            return trends
            
        keyword_set = {k.lower() for k in keywords}
        filtered = []
        
        for trend in trends:
            title = trend.get('title', '').lower()
            summary = trend.get('summary', '').lower()
            
            if any(keyword in title or keyword in summary for keyword in keyword_set):
                filtered.append(trend)
        return filtered

    @staticmethod
    def fetch_all_trends(limit: int = 20, sources: List[str] = None, 
                        force: bool = False, keywords: str = '') -> Dict[str, List[Dict[str, Any]]]:
        """Fetch trends from all enabled sources and combine them"""
        
        all_sources_map = {
            "google_trends": GoogleTrendsSource,
            "twitter": TwitterSource,
            "newsapi": NewsApiSource,
            "rss_feeds": RssFeedSource,
            "serpapi": SerpApiSource
        }
        
        keyword_list = [k.strip() for k in keywords.split(',')] if keywords else []
        if sources is None:
            sources = list(all_sources_map.keys())
        
        if force:
            TrendHarvester._cache.clear()
        
        results = {}
        
        for source_name in sources:
            if source_name not in all_sources_map:
                continue
                
            # Check cache unless forced
            if not force and TrendHarvester._is_cached_valid(source_name):
                 results[source_name] = TrendHarvester._cache[source_name]["data"][:limit]
                 continue
            
            try:
                # Fetch new data
                source_class = all_sources_map[source_name]
                # Fetch more to allow for filtering
                trends = source_class.fetch(limit=limit + len(keyword_list) * 2, keywords=keyword_list)
                
                if keyword_list:
                    trends = TrendHarvester._filter_trends_by_keywords(trends, keyword_list)
                
                # Update cache
                TrendHarvester._cache[source_name] = {
                    "data": trends,
                    "timestamp": time.time()
                }
                
                results[source_name] = trends[:limit]
            except Exception as e:
                logger.error(f"Error fetching trends from {source_name}: {e}")
                # Continue to next source instead of failing completely
        
        return results

    @staticmethod
    def fetch_trends_realtime(limit: int = 20) -> List[Dict[str, Any]]:
        """API specific method to get flattened trends quickly"""
        trends_dict = TrendHarvester.fetch_all_trends(limit=limit)
        return TrendHarvester.flatten_trends(trends_dict, limit)

    @staticmethod
    def flatten_trends(all_trends: Dict[str, List[Dict[str, Any]]], limit: int = 20) -> List[Dict[str, Any]]:
        """Flatten and sort all trends from multiple sources by score"""
        flattened = []
        seen_titles = set()
        
        for source, trends in all_trends.items():
            for trend in trends:
                title_lower = trend.get("title", "").lower()
                if title_lower not in seen_titles:
                    flattened.append(trend)
                    seen_titles.add(title_lower)
        
        # Sort by score descending
        flattened.sort(key=lambda x: x.get("score", 0), reverse=True)
        return flattened[:limit]
