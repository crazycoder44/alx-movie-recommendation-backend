"""
Cache utility functions for movies app
"""

from django.core.cache import cache
from django.conf import settings
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """Manager class for handling cache operations"""
    
    @staticmethod
    def generate_cache_key(prefix, **kwargs):
        """
        Generate a unique cache key based on prefix and kwargs
        
        Args:
            prefix: String prefix for the cache key
            **kwargs: Additional parameters to include in the key
        
        Returns:
            String cache key
        """
        # Sort kwargs to ensure consistent key generation
        sorted_kwargs = sorted(kwargs.items())
        key_data = f"{prefix}:{json.dumps(sorted_kwargs)}"
        
        # Generate hash for long keys
        if len(key_data) > 200:
            key_hash = hashlib.md5(key_data.encode()).hexdigest()
            return f"{prefix}:{key_hash}"
        
        return key_data.replace(' ', '_')
    
    @staticmethod
    def get_cached_data(cache_key):
        """
        Get data from cache
        
        Args:
            cache_key: Cache key to retrieve
        
        Returns:
            Cached data or None if not found
        """
        try:
            data = cache.get(cache_key)
            if data is not None:
                logger.info(f"Cache HIT for key: {cache_key}")
            else:
                logger.info(f"Cache MISS for key: {cache_key}")
            return data
        except Exception as e:
            logger.error(f"Error getting cache for key {cache_key}: {str(e)}")
            return None
    
    @staticmethod
    def set_cached_data(cache_key, data, timeout=None):
        """
        Set data in cache
        
        Args:
            cache_key: Cache key to set
            data: Data to cache
            timeout: Cache timeout in seconds (None for default)
        
        Returns:
            Boolean indicating success
        """
        try:
            cache.set(cache_key, data, timeout)
            logger.info(f"Cache SET for key: {cache_key} (timeout: {timeout}s)")
            return True
        except Exception as e:
            logger.error(f"Error setting cache for key {cache_key}: {str(e)}")
            return False
    
    @staticmethod
    def delete_cached_data(cache_key):
        """
        Delete data from cache
        
        Args:
            cache_key: Cache key to delete
        
        Returns:
            Boolean indicating success
        """
        try:
            cache.delete(cache_key)
            logger.info(f"Cache DELETE for key: {cache_key}")
            return True
        except Exception as e:
            logger.error(f"Error deleting cache for key {cache_key}: {str(e)}")
            return False
    
    @staticmethod
    def clear_pattern(pattern):
        """
        Clear all cache keys matching a pattern
        
        Args:
            pattern: Pattern to match (e.g., 'trending:*')
        
        Returns:
            Integer count of deleted keys
        """
        try:
            keys = cache.keys(f"*{pattern}*")
            if keys:
                cache.delete_many(keys)
                logger.info(f"Cache CLEAR pattern: {pattern} ({len(keys)} keys)")
                return len(keys)
            return 0
        except Exception as e:
            logger.error(f"Error clearing cache pattern {pattern}: {str(e)}")
            return 0


def get_cache_timeout(cache_type):
    """
    Get cache timeout for a specific cache type
    
    Args:
        cache_type: Type of cache ('trending', 'popular', etc.)
    
    Returns:
        Integer timeout in seconds
    """
    return settings.CACHE_TTL.get(cache_type, 3600)  # Default 1 hour


def cache_tmdb_response(cache_type, **params):
    """
    Decorator to cache TMDb API responses
    
    Usage:
        @cache_tmdb_response('trending', time_window='day', page=1)
        def fetch_trending_movies(**kwargs):
            # API call here
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = CacheManager.generate_cache_key(cache_type, **params, **kwargs)
            
            # Try to get from cache
            cached_data = CacheManager.get_cached_data(cache_key)
            if cached_data is not None:
                return cached_data
            
            # Fetch fresh data
            data = func(*args, **kwargs)
            
            # Cache the result
            if data is not None:
                timeout = get_cache_timeout(cache_type)
                CacheManager.set_cached_data(cache_key, data, timeout)
            
            return data
        
        return wrapper
    return decorator


# Cache instance for easy access
cache_manager = CacheManager()
