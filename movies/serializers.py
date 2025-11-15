"""
Serializers for movies app
"""

from rest_framework import serializers
from .models import Movie, Genre


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre model"""
    
    class Meta:
        model = Genre
        fields = ['id', 'tmdb_id', 'name']
        read_only_fields = ['id']


class MovieListSerializer(serializers.ModelSerializer):
    """Serializer for movie list views (lightweight)"""
    genres = GenreSerializer(many=True, read_only=True)
    poster_url = serializers.ReadOnlyField()
    rating_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'tmdb_id', 'title', 'overview', 'release_date',
            'vote_average', 'vote_count', 'popularity', 'poster_path',
            'poster_url', 'backdrop_path', 'genres', 'rating_percentage'
        ]
        read_only_fields = ['id']


class MovieDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed movie view"""
    genres = GenreSerializer(many=True, read_only=True)
    poster_url = serializers.ReadOnlyField()
    backdrop_url = serializers.ReadOnlyField()
    rating_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'tmdb_id', 'title', 'original_title', 'overview',
            'tagline', 'release_date', 'runtime', 'vote_average',
            'vote_count', 'popularity', 'poster_path', 'poster_url',
            'backdrop_path', 'backdrop_url', 'original_language',
            'adult', 'video', 'genres', 'rating_percentage',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TMDbMovieSerializer(serializers.Serializer):
    """Serializer for TMDb API response data"""
    id = serializers.IntegerField(source='tmdb_id')
    title = serializers.CharField()
    overview = serializers.CharField(allow_blank=True)
    release_date = serializers.DateField(required=False, allow_null=True)
    vote_average = serializers.FloatField()
    vote_count = serializers.IntegerField()
    popularity = serializers.FloatField()
    poster_path = serializers.CharField(allow_null=True, allow_blank=True)
    backdrop_path = serializers.CharField(allow_null=True, allow_blank=True)
    original_language = serializers.CharField()
    adult = serializers.BooleanField()
    genre_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    
    def to_representation(self, instance):
        """Add full image URLs to response"""
        data = super().to_representation(instance)
        
        # Add full poster URL
        if data.get('poster_path'):
            data['poster_url'] = f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
        else:
            data['poster_url'] = None
        
        # Add full backdrop URL
        if data.get('backdrop_path'):
            data['backdrop_url'] = f"https://image.tmdb.org/t/p/original{data['backdrop_path']}"
        else:
            data['backdrop_url'] = None
        
        # Add rating percentage
        data['rating_percentage'] = int(data.get('vote_average', 0) * 10)
        
        return data
