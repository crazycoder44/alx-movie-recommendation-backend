# Movie Recommendation Backend

A robust Django-based backend for a movie recommendation application with user authentication, TMDb API integration, Redis caching, and comprehensive Swagger documentation.

## 🎯 Features

- 🎬 **Movie Data from TMDb API** - Access to trending, popular, and top-rated movies
- 🔐 **JWT-based Authentication** - Secure user registration and login
- ⚡ **Redis Caching** - Optimized performance with intelligent caching
- 📚 **Comprehensive Swagger API Documentation** - Interactive API docs at `/api/docs/`
- ❤️ **User Favorites & Watchlist** - Save and manage favorite movies
- 🔍 **Movie Search & Recommendations** - Find movies and get personalized recommendations
- 🔒 **Secure and Scalable Architecture** - Built with best practices

## 🛠 Tech Stack

- **Backend Framework**: Django 4.2.7
- **API Framework**: Django REST Framework 3.14.0
- **Database**: PostgreSQL / SQLite (configurable)
- **Caching**: Redis 5.0.1
- **Authentication**: JWT (djangorestframework-simplejwt)
- **API Documentation**: drf-yasg (Swagger/OpenAPI)
- **External API**: TMDb (The Movie Database)

## 📋 Project Status

✅ **Production Ready** - All core features implemented and tested

### Completed Features:
- ✅ Django project setup with PostgreSQL support
- ✅ TMDb API integration with error handling
- ✅ Movie models and API endpoints
- ✅ JWT user authentication
- ✅ User favorites and watchlist functionality
- ✅ Redis caching for performance optimization
- ✅ Swagger API documentation

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL (optional - SQLite works for development)
- Redis (optional - caching can be disabled)
- TMDb API Key (get it from [themoviedb.org](https://www.themoviedb.org/settings/api))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/crazycoder44/alx-movie-recommendation-backend.git
   cd alx-movie-recommendation-backend
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file**
   ```bash
   cp .env.example .env
   ```
   
   Update the `.env` file with your configuration:
   ```env
   SECRET_KEY=your-secret-key-here-change-in-production
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   # Database (optional - uses SQLite by default)
   USE_POSTGRESQL=False
   DATABASE_NAME=movie_recommendation_db
   DATABASE_USER=postgres
   DATABASE_PASSWORD=your-password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432

   # TMDb API (required)
   TMDB_API_KEY=your-tmdb-api-key-here
   TMDB_BASE_URL=https://api.themoviedb.org/3

   # Redis (optional - uses in-memory cache if not configured)
   REDIS_URL=redis://localhost:6379/0

   # JWT Settings
   JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
   JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - API Base URL: `http://localhost:8000/api/`
   - Swagger Documentation: `http://localhost:8000/api/docs/`
   - ReDoc Documentation: `http://localhost:8000/api/redoc/`
   - Admin Panel: `http://localhost:8000/admin/`

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/users/register/` | Register new user | No |
| POST | `/api/users/login/` | Login user | No |
| POST | `/api/token/refresh/` | Refresh JWT token | No |
| GET | `/api/users/profile/` | Get user profile | Yes |
| PUT/PATCH | `/api/users/profile/update/` | Update user profile | Yes |
| POST | `/api/users/change-password/` | Change password | Yes |
| POST | `/api/users/logout/` | Logout user | Yes |

### Movies

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/movies/` | List all movies | No |
| GET | `/api/movies/{id}/` | Get movie details | No |
| GET | `/api/movies/trending/` | Get trending movies | No |
| GET | `/api/movies/popular/` | Get popular movies | No |
| GET | `/api/movies/top-rated/` | Get top rated movies | No |
| GET | `/api/movies/search/` | Search movies | No |
| GET | `/api/movies/{id}/recommendations/` | Get movie recommendations | No |
| GET | `/api/movies/{id}/similar/` | Get similar movies | No |
| GET | `/api/movies/{id}/details/` | Get detailed movie info from TMDb | No |

### Genres

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/genres/` | List all genres | No |
| GET | `/api/genres/{id}/` | Get genre details | No |
| GET | `/api/genres/fetch-from-tmdb/` | Sync genres from TMDb | No |

### User Favorites

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/favorites/` | Get user's favorites | Yes |
| POST | `/api/favorites/` | Add movie to favorites | Yes |
| DELETE | `/api/favorites/{id}/` | Remove from favorites | Yes |
| GET | `/api/favorites/check/{tmdb_id}/` | Check if movie is favorited | Yes |

### Watchlist

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/watchlist/` | Get user's watchlist | Yes |
| POST | `/api/watchlist/` | Add movie to watchlist | Yes |
| DELETE | `/api/watchlist/{id}/` | Remove from watchlist | Yes |
| GET | `/api/watchlist/check/{tmdb_id}/` | Check if movie is in watchlist | Yes |

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints:

1. **Register or Login** to get tokens:
   ```json
   POST /api/users/login/
   {
     "username": "your_username",
     "password": "your_password"
   }
   ```

2. **Response** includes access and refresh tokens:
   ```json
   {
     "user": {...},
     "tokens": {
       "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
       "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
     }
   }
   ```

3. **Use the access token** in the Authorization header:
   ```
   Authorization: Bearer <access_token>
   ```

4. **Refresh the token** when it expires:
   ```json
   POST /api/token/refresh/
   {
     "refresh": "your_refresh_token"
   }
   ```

## ⚡ Caching

The application uses Redis for caching to improve performance:

- **Trending Movies**: Cached for 12 hours
- **Popular Movies**: Cached for 24 hours
- **Top Rated Movies**: Cached for 24 hours
- **Movie Details**: Cached for 7 days
- **Genres**: Cached for 30 days
- **Recommendations**: Cached for 6 hours
- **Search Results**: Cached for 1 hour

## 🎯 Example Usage

### Register a new user
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!"
  }'
```

### Get trending movies
```bash
curl -X GET http://localhost:8000/api/movies/trending/?time_window=day&page=1
```

### Add movie to favorites (requires authentication)
```bash
curl -X POST http://localhost:8000/api/favorites/ \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "tmdb_id": 550,
    "title": "Fight Club",
    "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
    "release_date": "1999-10-15",
    "vote_average": 8.4
  }'
```

## 🏗 Project Structure

```
alx-movie-recommendation-app-backend/
├── movie_recommendation_backend/  # Django project settings
│   ├── settings.py               # Configuration
│   ├── urls.py                   # URL routing
│   └── wsgi.py                   # WSGI config
├── movies/                       # Movies app
│   ├── models.py                 # Movie and Genre models
│   ├── views.py                  # API views
│   ├── serializers.py            # Data serializers
│   ├── urls.py                   # Movie routes
│   ├── admin.py                  # Admin configuration
│   ├── cache.py                  # Cache utilities
│   └── services/                 # Business logic
│       └── tmdb_service.py       # TMDb API service
├── users/                        # Users app
│   ├── models.py                 # User, Favorite, Watchlist models
│   ├── views.py                  # User API views
│   ├── serializers.py            # User serializers
│   ├── urls.py                   # User routes
│   └── admin.py                  # User admin
├── requirements.txt              # Python dependencies
├── manage.py                     # Django management script
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
└── IMPLEMENTATION_PLAN.md        # Development roadmap
```

## 🧪 Development

### Running Tests
```bash
pytest
```

### Code Quality
```bash
# Run linting
flake8

# Format code
black .
```

### Generate Coverage Report
```bash
coverage run -m pytest
coverage report
coverage html
```

## 🤝 Git Workflow

This project follows conventional commits:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `perf:` - Performance improvements
- `chore:` - Maintenance tasks

## 📝 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Django secret key | Generated | Yes |
| `DEBUG` | Debug mode | True | No |
| `ALLOWED_HOSTS` | Allowed hosts | localhost,127.0.0.1 | Yes |
| `USE_POSTGRESQL` | Use PostgreSQL | False | No |
| `DATABASE_NAME` | Database name | movie_recommendation_db | No |
| `DATABASE_USER` | Database user | postgres | No |
| `DATABASE_PASSWORD` | Database password | - | No |
| `DATABASE_HOST` | Database host | localhost | No |
| `DATABASE_PORT` | Database port | 5432 | No |
| `TMDB_API_KEY` | TMDb API key | - | Yes |
| `TMDB_BASE_URL` | TMDb base URL | https://api.themoviedb.org/3 | No |
| `REDIS_URL` | Redis connection URL | redis://localhost:6379/0 | No |
| `JWT_ACCESS_TOKEN_LIFETIME_MINUTES` | Access token lifetime | 60 | No |
| `JWT_REFRESH_TOKEN_LIFETIME_DAYS` | Refresh token lifetime | 7 | No |

## 🐛 Troubleshooting

### Issue: TMDb API not working
- **Solution**: Verify your `TMDB_API_KEY` is correct in `.env` file

### Issue: Redis connection error
- **Solution**: Install and start Redis, or set `REDIS_URL` in `.env`

### Issue: Database connection error
- **Solution**: Check PostgreSQL is running or set `USE_POSTGRESQL=False` to use SQLite

### Issue: Migration errors
- **Solution**: Delete `db.sqlite3` and run `python manage.py migrate` again

## 📄 License

This project is part of the ALX Backend Development program.

## 👥 Contributors

- ALX Students

## 📧 Contact

For questions or support, please contact the development team.

---

**Made with ❤️ by ALX Students**
