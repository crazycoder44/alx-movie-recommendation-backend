"""
URL configuration for users app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserViewSet, FavoriteMovieViewSet, WatchlistViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'favorites', FavoriteMovieViewSet, basename='favorite')
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')

app_name = 'users'

urlpatterns = [
    path('', include(router.urls)),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
