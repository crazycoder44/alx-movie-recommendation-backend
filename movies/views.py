"""
Views for movies app
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.paginator import Paginator

from .models import Movie, Genre
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    GenreSerializer,
    TMDbMovieSerializer
)
from .services import tmdb_service
import logging

logger = logging.getLogger(__name__)


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for movie operations
    
    Provides endpoints for listing and retrieving movies from database
    """
    queryset = Movie.objects.all()
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieListSerializer
    
    @action(detail=False, methods=['get'], url_path='trending')
    def trending(self, request):
        """
        Get trending movies from TMDb API
        
        Query Parameters:
        - time_window: 'day' or 'week' (default: 'day')
        - page: page number (default: 1)
        """
        time_window = request.query_params.get('time_window', 'day')
        page = request.query_params.get('page', 1)
        
        try:
            page = int(page)
        except ValueError:
            page = 1
        
        # Validate time_window
        if time_window not in ['day', 'week']:
            time_window = 'day'
        
        # Fetch from TMDb
        data = tmdb_service.get_trending_movies(time_window=time_window, page=page)
        
        if data is None:
            return Response(
                {'error': 'Failed to fetch trending movies'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Serialize the results
        results = data.get('results', [])
        serializer = TMDbMovieSerializer(results, many=True)
        
        return Response({
            'page': data.get('page', page),
            'total_pages': data.get('total_pages', 1),
            'total_results': data.get('total_results', 0),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='popular')
    def popular(self, request):
        """
        Get popular movies from TMDb API
        
        Query Parameters:
        - page: page number (default: 1)
        """
        page = request.query_params.get('page', 1)
        
        try:
            page = int(page)
        except ValueError:
            page = 1
        
        # Fetch from TMDb
        data = tmdb_service.get_popular_movies(page=page)
        
        if data is None:
            return Response(
                {'error': 'Failed to fetch popular movies'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Serialize the results
        results = data.get('results', [])
        serializer = TMDbMovieSerializer(results, many=True)
        
        return Response({
            'page': data.get('page', page),
            'total_pages': data.get('total_pages', 1),
            'total_results': data.get('total_results', 0),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='top-rated')
    def top_rated(self, request):
        """
        Get top rated movies from TMDb API
        
        Query Parameters:
        - page: page number (default: 1)
        """
        page = request.query_params.get('page', 1)
        
        try:
            page = int(page)
        except ValueError:
            page = 1
        
        # Fetch from TMDb
        data = tmdb_service.get_top_rated_movies(page=page)
        
        if data is None:
            return Response(
                {'error': 'Failed to fetch top rated movies'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Serialize the results
        results = data.get('results', [])
        serializer = TMDbMovieSerializer(results, many=True)
        
        return Response({
            'page': data.get('page', page),
            'total_pages': data.get('total_pages', 1),
            'total_results': data.get('total_results', 0),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        """
        Search movies from TMDb API
        
        Query Parameters:
        - query: search query (required)
        - page: page number (default: 1)
        """
        query = request.query_params.get('query', '').strip()
        page = request.query_params.get('page', 1)
        
        if not query:
            return Response(
                {'error': 'Query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            page = int(page)
        except ValueError:
            page = 1
        
        # Fetch from TMDb
        data = tmdb_service.search_movies(query=query, page=page)
        
        if data is None:
            return Response(
                {'error': 'Failed to search movies'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Serialize the results
        results = data.get('results', [])
        serializer = TMDbMovieSerializer(results, many=True)
        
        return Response({
            'page': data.get('page', page),
            'total_pages': data.get('total_pages', 1),
            'total_results': data.get('total_results', 0),
            'results': serializer.data
        })
    
    @action(detail=True, methods=['get'], url_path='recommendations')
    def recommendations(self, request, pk=None):
        """
        Get movie recommendations from TMDb API
        
        Query Parameters:
        - page: page number (default: 1)
        """
        page = request.query_params.get('page', 1)
        
        try:
            page = int(page)
            movie_id = int(pk)
        except ValueError:
            return Response(
                {'error': 'Invalid movie ID or page number'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Fetch from TMDb
        data = tmdb_service.get_movie_recommendations(movie_id=movie_id, page=page)
        
        if data is None:
            return Response(
                {'error': 'Failed to fetch movie recommendations'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Serialize the results
        results = data.get('results', [])
        serializer = TMDbMovieSerializer(results, many=True)
        
        return Response({
            'page': data.get('page', page),
            'total_pages': data.get('total_pages', 1),
            'total_results': data.get('total_results', 0),
            'results': serializer.data
        })
    
    @action(detail=True, methods=['get'], url_path='similar')
    def similar(self, request, pk=None):
        """
        Get similar movies from TMDb API
        
        Query Parameters:
        - page: page number (default: 1)
        """
        page = request.query_params.get('page', 1)
        
        try:
            page = int(page)
            movie_id = int(pk)
        except ValueError:
            return Response(
                {'error': 'Invalid movie ID or page number'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Fetch from TMDb
        data = tmdb_service.get_similar_movies(movie_id=movie_id, page=page)
        
        if data is None:
            return Response(
                {'error': 'Failed to fetch similar movies'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Serialize the results
        results = data.get('results', [])
        serializer = TMDbMovieSerializer(results, many=True)
        
        return Response({
            'page': data.get('page', page),
            'total_pages': data.get('total_pages', 1),
            'total_results': data.get('total_results', 0),
            'results': serializer.data
        })
    
    @action(detail=True, methods=['get'], url_path='details')
    def tmdb_details(self, request, pk=None):
        """
        Get detailed movie information from TMDb API
        """
        try:
            movie_id = int(pk)
        except ValueError:
            return Response(
                {'error': 'Invalid movie ID'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Fetch from TMDb
        data = tmdb_service.get_movie_details(movie_id=movie_id)
        
        if data is None:
            return Response(
                {'error': 'Failed to fetch movie details'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        return Response(data)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for genre operations
    
    Provides endpoints for listing genres
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'], url_path='fetch-from-tmdb')
    def fetch_from_tmdb(self, request):
        """
        Fetch and store genres from TMDb API
        """
        data = tmdb_service.get_movie_genres()
        
        if data is None:
            return Response(
                {'error': 'Failed to fetch genres from TMDb'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        genres_data = data.get('genres', [])
        created_count = 0
        updated_count = 0
        
        for genre_data in genres_data:
            genre, created = Genre.objects.update_or_create(
                tmdb_id=genre_data['id'],
                defaults={'name': genre_data['name']}
            )
            if created:
                created_count += 1
            else:
                updated_count += 1
        
        return Response({
            'message': 'Genres synchronized successfully',
            'created': created_count,
            'updated': updated_count,
            'total': len(genres_data)
        })
