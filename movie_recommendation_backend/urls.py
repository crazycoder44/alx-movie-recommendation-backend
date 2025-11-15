"""
URL configuration for movie_recommendation_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/OpenAPI schema configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Movie Recommendation API",
        default_version='v1',
        description="""
        # Movie Recommendation Backend API
        
        A comprehensive REST API for movie recommendations, user management, and favorites.
        
        ## Features
        - 🎬 Movie data from TMDb API
        - 🔐 JWT-based authentication  
        - ⚡ Redis caching for optimal performance
        - ❤️ User favorites and watchlist
        - 🔍 Movie search and recommendations
        
        ## Authentication
        Most endpoints require authentication. To authenticate:
        1. Register or login to get JWT tokens
        2. Include the access token in the Authorization header: `Bearer <token>`
        3. Refresh the token when it expires using the refresh endpoint
        
        ## Rate Limiting
        API calls may be rate-limited to prevent abuse.
        
        ## Support
        For issues or questions, please contact the development team.
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@movieapp.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('movies.urls')),
    path('api/', include('users.urls')),
    
    # Swagger/OpenAPI documentation
    re_path(r'^api/docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
