"""
TMDb API Service Module

This module provides services for interacting with The Movie Database (TMDb) API.
It handles fetching trending movies, recommendations, movie details, and search functionality.
"""

import requests
from django.conf import settings
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class TMDbService:
    """Service class for interacting with TMDb API"""
    
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.base_url = settings.TMDB_BASE_URL
        self.image_base_url = "https://image.tmdb.org/t/p/"
        
        if not self.api_key:
            logger.warning("TMDb API key is not configured")
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make a request to TMDb API with error handling
        
        Args:
            endpoint: API endpoint (e.g., '/movie/popular')
            params: Query parameters
            
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
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
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
        Get trending movies
        
        Args:
            time_window: 'day' or 'week'
            page: Page number for pagination
            
        Returns:
            Dictionary containing trending movies data
        """
        endpoint = f"/trending/movie/{time_window}"
        params = {'page': page}
        return self._make_request(endpoint, params)
    
    def get_popular_movies(self, page: int = 1) -> Optional[Dict]:
        """
        Get popular movies
        
        Args:
            page: Page number for pagination
            
        Returns:
            Dictionary containing popular movies data
        """
        endpoint = "/movie/popular"
        params = {'page': page}
        return self._make_request(endpoint, params)
    
    def get_top_rated_movies(self, page: int = 1) -> Optional[Dict]:
        """
        Get top rated movies
        
        Args:
            page: Page number for pagination
            
        Returns:
            Dictionary containing top rated movies data
        """
        endpoint = "/movie/top_rated"
        params = {'page': page}
        return self._make_request(endpoint, params)
    
    def get_movie_details(self, movie_id: int) -> Optional[Dict]:
        """
        Get detailed information about a specific movie
        
        Args:
            movie_id: TMDb movie ID
            
        Returns:
            Dictionary containing movie details
        """
        endpoint = f"/movie/{movie_id}"
        params = {
            'append_to_response': 'videos,credits,similar,recommendations'
        }
        return self._make_request(endpoint, params)
    
    def get_movie_recommendations(self, movie_id: int, page: int = 1) -> Optional[Dict]:
        """
        Get movie recommendations based on a specific movie
        
        Args:
            movie_id: TMDb movie ID
            page: Page number for pagination
            
        Returns:
            Dictionary containing recommended movies
        """
        endpoint = f"/movie/{movie_id}/recommendations"
        params = {'page': page}
        return self._make_request(endpoint, params)
    
    def get_similar_movies(self, movie_id: int, page: int = 1) -> Optional[Dict]:
        """
        Get similar movies based on a specific movie
        
        Args:
            movie_id: TMDb movie ID
            page: Page number for pagination
            
        Returns:
            Dictionary containing similar movies
        """
        endpoint = f"/movie/{movie_id}/similar"
        params = {'page': page}
        return self._make_request(endpoint, params)
    
    def search_movies(self, query: str, page: int = 1) -> Optional[Dict]:
        """
        Search for movies by title
        
        Args:
            query: Search query string
            page: Page number for pagination
            
        Returns:
            Dictionary containing search results
        """
        endpoint = "/search/movie"
        params = {
            'query': query,
            'page': page
        }
        return self._make_request(endpoint, params)
    
    def discover_movies(self, **kwargs) -> Optional[Dict]:
        """
        Discover movies with various filters
        
        Args:
            **kwargs: Filter parameters (genre, year, sort_by, etc.)
            
        Returns:
            Dictionary containing discovered movies
        """
        endpoint = "/discover/movie"
        params = kwargs
        params['page'] = kwargs.get('page', 1)
        return self._make_request(endpoint, params)
    
    def get_movie_genres(self) -> Optional[Dict]:
        """
        Get list of official movie genres
        
        Returns:
            Dictionary containing genre list
        """
        endpoint = "/genre/movie/list"
        return self._make_request(endpoint)
    
    def get_now_playing(self, page: int = 1) -> Optional[Dict]:
        """
        Get movies currently in theaters
        
        Args:
            page: Page number for pagination
            
        Returns:
            Dictionary containing now playing movies
        """
        endpoint = "/movie/now_playing"
        params = {'page': page}
        return self._make_request(endpoint, params)
    
    def get_upcoming_movies(self, page: int = 1) -> Optional[Dict]:
        """
        Get upcoming movies
        
        Args:
            page: Page number for pagination
            
        Returns:
            Dictionary containing upcoming movies
        """
        endpoint = "/movie/upcoming"
        params = {'page': page}
        return self._make_request(endpoint, params)
    
    def get_image_url(self, image_path: Optional[str], size: str = 'original') -> Optional[str]:
        """
        Get full URL for an image
        
        Args:
            image_path: Image path from TMDb
            size: Image size (w500, w780, original, etc.)
            
        Returns:
            Full image URL or None
        """
        if not image_path:
            return None
        return f"{self.image_base_url}{size}{image_path}"


# Create a singleton instance
tmdb_service = TMDbService()
