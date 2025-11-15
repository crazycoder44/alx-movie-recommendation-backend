from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import FavoriteMovie, Watchlist

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model"""
    list_display = [
        'id', 'username', 'email', 'first_name', 'last_name',
        'is_staff', 'is_active', 'date_joined'
    ]
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('bio', 'profile_image', 'date_of_birth', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'date_joined', 'last_login']


@admin.register(FavoriteMovie)
class FavoriteMovieAdmin(admin.ModelAdmin):
    """Admin interface for FavoriteMovie model"""
    list_display = ['id', 'user', 'title', 'tmdb_id', 'vote_average', 'created_at']
    list_filter = ['created_at', 'vote_average']
    search_fields = ['user__username', 'title', 'tmdb_id']
    readonly_fields = ['created_at', 'poster_url']
    ordering = ['-created_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Movie Info', {
            'fields': ('tmdb_id', 'title', 'release_date', 'vote_average')
        }),
        ('Media', {
            'fields': ('poster_path', 'poster_url')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    """Admin interface for Watchlist model"""
    list_display = ['id', 'user', 'title', 'tmdb_id', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'title', 'tmdb_id']
    readonly_fields = ['created_at', 'poster_url']
    ordering = ['-created_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Movie Info', {
            'fields': ('tmdb_id', 'title', 'release_date')
        }),
        ('Media', {
            'fields': ('poster_path', 'poster_url')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
