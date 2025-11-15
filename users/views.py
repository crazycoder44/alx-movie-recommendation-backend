"""
Views for users app
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    FavoriteMovieSerializer,
    AddFavoriteMovieSerializer,
    WatchlistSerializer,
    AddWatchlistSerializer
)
from .models import FavoriteMovie, Watchlist

User = get_user_model()


class UserViewSet(viewsets.GenericViewSet):
    """
    ViewSet for user operations
    
    Provides endpoints for user registration, login, profile management
    """
    queryset = User.objects.all()
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['register', 'login']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'register':
            return UserRegistrationSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        elif self.action == 'update_profile':
            return UserUpdateSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return UserProfileSerializer
    
    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        """
        Register a new user
        
        Request Body:
        - username: string (required)
        - email: string (required)
        - password: string (required)
        - password2: string (required)
        - first_name: string (optional)
        - last_name: string (optional)
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """
        Login user and return JWT tokens
        
        Request Body:
        - username: string (required)
        - password: string (required)
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({
                'error': 'User account is disabled'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'Login successful'
        })
    
    @action(detail=False, methods=['get'], url_path='profile')
    def profile(self, request):
        """
        Get current user's profile
        """
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'], url_path='profile/update')
    def update_profile(self, request):
        """
        Update current user's profile
        
        Request Body:
        - first_name: string (optional)
        - last_name: string (optional)
        - bio: string (optional)
        - profile_image: string (optional)
        - date_of_birth: date (optional)
        """
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'user': UserProfileSerializer(request.user).data,
            'message': 'Profile updated successfully'
        })
    
    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        """
        Change user password
        
        Request Body:
        - old_password: string (required)
        - new_password: string (required)
        - new_password2: string (required)
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        # Check old password
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'error': 'Old password is incorrect'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Password changed successfully'
        })
    
    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        """
        Logout user (client should discard tokens)
        """
        return Response({
            'message': 'Logout successful. Please discard your tokens.'
        })


class FavoriteMovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user's favorite movies
    """
    serializer_class = FavoriteMovieSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return favorites for the current user"""
        return FavoriteMovie.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'create':
            return AddFavoriteMovieSerializer
        return FavoriteMovieSerializer
    
    def create(self, request, *args, **kwargs):
        """Add a movie to user's favorites"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if movie already in favorites
        tmdb_id = serializer.validated_data['tmdb_id']
        existing = FavoriteMovie.objects.filter(
            user=request.user,
            tmdb_id=tmdb_id
        ).first()
        
        if existing:
            return Response({
                'message': 'Movie already in favorites',
                'favorite': FavoriteMovieSerializer(existing).data
            }, status=status.HTTP_200_OK)
        
        # Create favorite
        favorite = serializer.save(user=request.user)
        
        return Response({
            'message': 'Movie added to favorites',
            'favorite': FavoriteMovieSerializer(favorite).data
        }, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        """Remove a movie from user's favorites"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Movie removed from favorites'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='check/(?P<tmdb_id>[0-9]+)')
    def check_favorite(self, request, tmdb_id=None):
        """Check if a movie is in user's favorites"""
        is_favorite = FavoriteMovie.objects.filter(
            user=request.user,
            tmdb_id=tmdb_id
        ).exists()
        
        return Response({
            'is_favorite': is_favorite,
            'tmdb_id': tmdb_id
        })


class WatchlistViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user's watchlist
    """
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return watchlist for the current user"""
        return Watchlist.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'create':
            return AddWatchlistSerializer
        return WatchlistSerializer
    
    def create(self, request, *args, **kwargs):
        """Add a movie to user's watchlist"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if movie already in watchlist
        tmdb_id = serializer.validated_data['tmdb_id']
        existing = Watchlist.objects.filter(
            user=request.user,
            tmdb_id=tmdb_id
        ).first()
        
        if existing:
            return Response({
                'message': 'Movie already in watchlist',
                'watchlist': WatchlistSerializer(existing).data
            }, status=status.HTTP_200_OK)
        
        # Create watchlist item
        watchlist = serializer.save(user=request.user)
        
        return Response({
            'message': 'Movie added to watchlist',
            'watchlist': WatchlistSerializer(watchlist).data
        }, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        """Remove a movie from user's watchlist"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Movie removed from watchlist'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='check/(?P<tmdb_id>[0-9]+)')
    def check_watchlist(self, request, tmdb_id=None):
        """Check if a movie is in user's watchlist"""
        is_in_watchlist = Watchlist.objects.filter(
            user=request.user,
            tmdb_id=tmdb_id
        ).exists()
        
        return Response({
            'is_in_watchlist': is_in_watchlist,
            'tmdb_id': tmdb_id
        })
