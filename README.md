# Movie Recommendation Backend

A robust Django-based backend for a movie recommendation application with user authentication, TMDb API integration, Redis caching, and comprehensive Swagger documentation.

## Features

- 🎬 Movie data from TMDb API
- 🔐 JWT-based authentication
- ⚡ Redis caching for optimal performance
- 📚 Comprehensive Swagger API documentation
- ❤️ User favorites and preferences
- 🔒 Secure and scalable architecture

## Tech Stack

- **Backend Framework**: Django 4.2.7
- **API Framework**: Django REST Framework
- **Database**: PostgreSQL
- **Caching**: Redis
- **Authentication**: JWT (Simple JWT)
- **API Documentation**: drf-yasg (Swagger)
- **External API**: TMDb (The Movie Database)

## Project Status

🚧 **Under Development** - Following phase-by-phase implementation

See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for detailed development roadmap.

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL
- Redis
- TMDb API Key (get it from [themoviedb.org](https://www.themoviedb.org/settings/api))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd alx-movie-recommendation-app-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create .env file**
   ```bash
   cp .env.example .env
   ```
   
   Update the `.env` file with your configuration:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   DATABASE_NAME=movie_db
   DATABASE_USER=postgres
   DATABASE_PASSWORD=your-password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   TMDB_API_KEY=your-tmdb-api-key
   REDIS_URL=redis://localhost:6379
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## API Documentation

Once the server is running, access the interactive API documentation at:
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`

## API Endpoints

### Authentication
- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - Login user
- `POST /api/users/token/refresh/` - Refresh JWT token
- `GET /api/users/profile/` - Get user profile

### Movies
- `GET /api/movies/trending/` - Get trending movies
- `GET /api/movies/recommended/` - Get recommended movies
- `GET /api/movies/{id}/` - Get movie details
- `GET /api/movies/search/` - Search movies

### User Favorites
- `GET /api/users/favorites/` - Get user's favorite movies
- `POST /api/users/favorites/` - Add movie to favorites
- `DELETE /api/users/favorites/{id}/` - Remove movie from favorites

## Development

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

## Git Workflow

This project follows conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `perf:` - Performance improvements
- `chore:` - Maintenance tasks

## Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Ensure all tests pass
5. Submit a pull request

## License

This project is part of the ALX Backend Development program.

## Contact

For questions or support, please contact the development team.

---

**Made with ❤️ by ALX Students**
