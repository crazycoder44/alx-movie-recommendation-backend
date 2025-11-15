"""
URL configuration for movies app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, GenreViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'genres', GenreViewSet, basename='genre')

app_name = 'movies'

urlpatterns = [
    path('', include(router.urls)),
]
