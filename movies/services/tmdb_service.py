"""
TMDb API Service Module

This module provides services for interacting with The Movie Database (TMDb) API.
It handles fetching trending movies, recommendations, movie details, and search functionality.
Includes caching support for improved performance.
"""

import requests
from django.conf import settings
from django.core.cache import cache
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class TMDbService:
    """Service class for interacting with TMDb API with caching support"""
    
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.base_url = settings.TMDB_BASE_URL
        self.image_base_url = "https://image.tmdb.org/t/p/"
        self.cache_ttl = settings.CACHE_TTL
        
        if not self.api_key:
            logger.warning("TMDb API key is not configured")
    
    def _generate_cache_key(self, endpoint: str, params: Optional[Dict] = None) -> str:
        """Generate a unique cache key for the request"""
        param_str = "_".join([f"{k}={v}" for k, v in sorted((params or {}).items()) if k != 'api_key'])
        return f"tmdb:{endpoint.replace('/', '_')}:{param_str}"
    
    def _get_cached_data(self, cache_key: str) -> Optional[Dict]:
        """Get data from cache"""
        try:
            data = cache.get(cache_key)
            if data:
                logger.info(f"Cache HIT: {cache_key}")
            else:
                logger.info(f"Cache MISS: {cache_key}")
            return data
        except Exception as e:
            logger.error(f"Cache get error: {str(e)}")
            return None
    
    def _set_cached_data(self, cache_key: str, data: Dict, timeout: int):
        """Set data in cache"""
        try:
            cache.set(cache_key, data, timeout)
            logger.info(f"Cache SET: {cache_key} (TTL: {timeout}s)")
        except Exception as e:
            logger.error(f"Cache set error: {str(e)}")
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None,
                     cache_timeout: Optional[int] = None, use_cache: bool = True) -> Optional[Dict]:
        """
        Make a request to TMDb API with error handling and caching
        
        Args:
            endpoint: API endpoint (e.g., '/movie/popular')
            params: Query parameters
            cache_timeout: Cache timeout in seconds (None for no caching)
            use_cache: Whether to use cache
            
        Returns:
            Response data as dictionary or None if error
        """
        if not self.api_key:
            logger.error("TMDb API key is not configured")
            return None
        
        # Add API key to params
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        
        # Check cache if enabled
        if use_cache and cache_timeout:
            cache_key = self._generate_cache_key(endpoint, params)
            cached_data = self._get_cached_data(cache_key)
            if cached_data is not None:
                return cached_data
        
        # Make API request
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Cache the result if enabled
            if use_cache and cache_timeout and data:
                cache_key = self._generate_cache_key(endpoint, params)
                self._set_cached_data(cache_key, data, cache_timeout)
            
            return data
        except requests.exceptions.Timeout:
            logger.error(f"Timeout error for endpoint: {endpoint}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error for endpoint {endpoint}: {str(e)}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for endpoint {endpoint}: {str(e)}")
            return None
        except ValueError as e:
            logger.error(f"JSON decode error for endpoint {endpoint}: {str(e)}")
            return None
    
    def get_trending_movies(self, time_window: str = 'day', page: int = 1) -> Optional[Dict]:
        """
        Get trending movies (with caching)
        
        Args:
            time_window: 'day' or 'week'
            page: Page number for pagination
            
        Returns:
            Dictionary containing trending movies data
        """
        endpoint = f"/trending/movie/{time_window}"
        params = {'page': page}
        return self._make_request(endpoint, params, cache_timeout=self.cache_ttl['trending'])
    
    def get_popular_movies(self, page: int = 1) -> Optional[Dict]:
        """
        Get popular movies (with caching)
        
        Args:
            page: Page number for pagination
            
        Returns:
            Dictionary containing popular movies data
        """
        endpoint = "/movie/popular"
        params = {'page': page}
        return self._make_request(endpoint, params, cache_timeout=self.cache_ttl['popular'])
    
    def get_top_rated_movies(self, page: int = 1) -> Optional[Dict]:
        """
        Get top rated movies (with caching)
        
        Args:
            page: Page number for pagination
            
        Returns:
            Dictionary containing top rated movies data
        """
        endpoint = "/movie/top_rated"
        params = {'page': page}
        return self._make_request(endpoint, params, cache_timeout=self.cache_ttl['top_rated'])
    
    def get_movie_details(self, movie_id: int) -> Optional[Dict]:
        """
        Get detailed information about a specific movie (with caching)
        
        Args:
            movie_id: TMDb movie ID
            
        Returns:
            Dictionary containing movie details
        """
        endpoint = f"/movie/{movie_id}"
        params = {'append_to_response': 'credits,videos,images,keywords'}
        return self._make_request(endpoint, params, cache_timeout=self.cache_ttl['movie_details'])
    
    def get_movie_recommendations(self, movie_id: int, page: int = 1) -> Optional[Dict]:
        """
        Get movie recommendations based on a specific movie (with caching)
        
        Args:
            movie_id: TMDb movie ID
            page: Page number for pagination
            
        Returns:
            Dictionary containing recommended movies
        """
        endpoint = f"/movie/{movie_id}/recommendations"
        params = {'page': page}
        return self._make_request(endpoint, params, cache_timeout=self.cache_ttl['recommendations'])
    
    def get_similar_movies(self, movie_id: int, page: int = 1) -> Optional[Dict]:
        """
        Get similar movies based on a specific movie (with caching)
        
        Args:
            movie_id: TMDb movie ID
            page: Page number for pagination
            
        Returns:
            Dictionary containing similar movies
        """
        endpoint = f"/movie/{movie_id}/similar"
        params = {'page': page}
        return self._make_request(endpoint, params, cache_timeout=self.cache_ttl['similar'])
    
    def search_movies(self, query: str, page: int = 1) -> Optional[Dict]:
        """
        Search for movies by query (with caching)
        
        Args:
            query: Search query string
            page: Page number for pagination
            
        Returns:
            Dictionary containing search results
        """
        endpoint = "/search/movie"
        params = {'query': query, 'page': page}
        return self._make_request(endpoint, params, cache_timeout=self.cache_ttl['search'])
    
    def get_movie_genres(self) -> Optional[Dict]:
        """
        Get list of official movie genres (with long-term caching)
        
        Returns:
            Dictionary containing genre list
        """
        endpoint = "/genre/movie/list"
        return self._make_request(endpoint, cache_timeout=self.cache_ttl['genres'])
    
    def get_poster_url(self, poster_path: str, size: str = 'w500') -> Optional[str]:
        """
        Get full URL for movie poster
        
        Args:
            poster_path: Poster path from TMDb
            size: Image size ('w92', 'w154', 'w185', 'w342', 'w500', 'w780', 'original')
            
        Returns:
            Full URL string or None
        """
        if not poster_path:
            return None
        return f"{self.image_base_url}{size}{poster_path}"
    
    def get_backdrop_url(self, backdrop_path: str, size: str = 'original') -> Optional[str]:
        """
        Get full URL for movie backdrop
        
        Args:
            backdrop_path: Backdrop path from TMDb
            size: Image size ('w300', 'w780', 'w1280', 'original')
            
        Returns:
            Full URL string or None
        """
        if not backdrop_path:
            return None
        return f"{self.image_base_url}{size}{backdrop_path}"


# Create a singleton instance
tmdb_service = TMDbService()
