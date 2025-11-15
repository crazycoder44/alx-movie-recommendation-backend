from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    """Model for movie genres"""
    tmdb_id = models.IntegerField(unique=True, help_text="TMDb genre ID")
    name = models.CharField(max_length=100, help_text="Genre name")
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
    
    def __str__(self):
        return self.name


class Movie(models.Model):
    """Model for storing movie data from TMDb"""
    # TMDb specific fields
    tmdb_id = models.IntegerField(unique=True, db_index=True, help_text="TMDb movie ID")
    
    # Basic information
    title = models.CharField(max_length=255, help_text="Movie title")
    original_title = models.CharField(max_length=255, blank=True, help_text="Original title")
    overview = models.TextField(blank=True, help_text="Movie overview/description")
    tagline = models.CharField(max_length=255, blank=True, help_text="Movie tagline")
    
    # Release and runtime
    release_date = models.DateField(null=True, blank=True, help_text="Release date")
    runtime = models.IntegerField(null=True, blank=True, help_text="Runtime in minutes")
    
    # Ratings and popularity
    vote_average = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        help_text="Average vote rating"
    )
    vote_count = models.IntegerField(default=0, help_text="Number of votes")
    popularity = models.FloatField(default=0.0, help_text="Popularity score")
    
    # Images
    poster_path = models.CharField(max_length=255, blank=True, help_text="Poster image path")
    backdrop_path = models.CharField(max_length=255, blank=True, help_text="Backdrop image path")
    
    # Additional information
    original_language = models.CharField(max_length=10, blank=True, help_text="Original language code")
    adult = models.BooleanField(default=False, help_text="Adult content flag")
    video = models.BooleanField(default=False, help_text="Has video flag")
    
    # Relationships
    genres = models.ManyToManyField(Genre, related_name='movies', blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-popularity', '-vote_average']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        indexes = [
            models.Index(fields=['tmdb_id']),
            models.Index(fields=['-popularity']),
            models.Index(fields=['-vote_average']),
            models.Index(fields=['release_date']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.release_date.year if self.release_date else 'N/A'})"
    
    @property
    def poster_url(self):
        """Get full poster URL"""
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return None
    
    @property
    def backdrop_url(self):
        """Get full backdrop URL"""
        if self.backdrop_path:
            return f"https://image.tmdb.org/t/p/original{self.backdrop_path}"
        return None
    
    @property
    def rating_percentage(self):
        """Get rating as percentage"""
        return int(self.vote_average * 10)
