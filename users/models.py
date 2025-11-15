from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model extending AbstractUser
    """
    email = models.EmailField(unique=True, help_text="User email address")
    bio = models.TextField(blank=True, help_text="User biography")
    profile_image = models.URLField(blank=True, help_text="Profile image URL")
    date_of_birth = models.DateField(null=True, blank=True, help_text="Date of birth")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}".strip() or self.username


class FavoriteMovie(models.Model):
    """
    Model for storing user's favorite movies
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_movies',
        help_text="User who favorited the movie"
    )
    tmdb_id = models.IntegerField(help_text="TMDb movie ID")
    title = models.CharField(max_length=255, help_text="Movie title")
    poster_path = models.CharField(max_length=255, blank=True, help_text="Poster image path")
    release_date = models.DateField(null=True, blank=True, help_text="Release date")
    vote_average = models.FloatField(default=0.0, help_text="Average vote rating")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Favorite Movie'
        verbose_name_plural = 'Favorite Movies'
        unique_together = ['user', 'tmdb_id']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'tmdb_id']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    @property
    def poster_url(self):
        """Get full poster URL"""
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return None


class Watchlist(models.Model):
    """
    Model for storing user's watchlist
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='watchlist',
        help_text="User who added to watchlist"
    )
    tmdb_id = models.IntegerField(help_text="TMDb movie ID")
    title = models.CharField(max_length=255, help_text="Movie title")
    poster_path = models.CharField(max_length=255, blank=True, help_text="Poster image path")
    release_date = models.DateField(null=True, blank=True, help_text="Release date")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Watchlist'
        verbose_name_plural = 'Watchlist'
        unique_together = ['user', 'tmdb_id']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'tmdb_id']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    @property
    def poster_url(self):
        """Get full poster URL"""
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return None
