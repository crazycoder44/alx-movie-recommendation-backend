from django.contrib import admin
from .models import Movie, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Admin interface for Genre model"""
    list_display = ['id', 'name', 'tmdb_id']
    search_fields = ['name']
    list_filter = ['name']
    ordering = ['name']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Admin interface for Movie model"""
    list_display = [
        'id', 'title', 'release_date', 'vote_average',
        'popularity', 'tmdb_id'
    ]
    list_filter = ['release_date', 'adult', 'original_language']
    search_fields = ['title', 'original_title', 'overview']
    readonly_fields = ['created_at', 'updated_at', 'poster_url', 'backdrop_url']
    filter_horizontal = ['genres']
    ordering = ['-popularity', '-vote_average']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('tmdb_id', 'title', 'original_title', 'overview', 'tagline')
        }),
        ('Release & Runtime', {
            'fields': ('release_date', 'runtime')
        }),
        ('Ratings & Popularity', {
            'fields': ('vote_average', 'vote_count', 'popularity')
        }),
        ('Media', {
            'fields': ('poster_path', 'poster_url', 'backdrop_path', 'backdrop_url')
        }),
        ('Additional Info', {
            'fields': ('original_language', 'adult', 'video', 'genres')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
