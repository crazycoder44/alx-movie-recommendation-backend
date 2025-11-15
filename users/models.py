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
