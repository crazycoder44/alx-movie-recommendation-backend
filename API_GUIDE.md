# API Guide

Comprehensive guide to using the Movie Recommendation Backend API.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Authentication](#authentication)
3. [Movies API](#movies-api)
4. [Genres API](#genres-api)
5. [User Management](#user-management)
6. [Favorites & Watchlist](#favorites--watchlist)
7. [Error Handling](#error-handling)
8. [Rate Limiting](#rate-limiting)
9. [Pagination](#pagination)
10. [Examples](#examples)

---

## Getting Started

### Base URL

```
http://localhost:8000/api/
```

### API Documentation

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/

### Response Format

All API responses follow this structure:

**Success Response:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/movies/?page=2",
  "previous": null,
  "results": [...]
}
```

**Error Response:**
```json
{
  "detail": "Error message here"
}
```

Or for field-specific errors:
```json
{
  "field_name": ["Error message for this field"],
  "another_field": ["Another error message"]
}
```

---

## Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### 1. Register a New User

**Endpoint:** `POST /api/users/register/`

**Request:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:** `201 Created`
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "User registered successfully"
}
```

### 2. Login

**Endpoint:** `POST /api/users/login/`

**Request:**
```json
{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### 3. Refresh Token

**Endpoint:** `POST /api/token/refresh/`

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 4. Using Tokens

Include the access token in the Authorization header for protected endpoints:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Example with cURL:**
```bash
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Example with JavaScript:**
```javascript
fetch('http://localhost:8000/api/users/profile/', {
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  }
})
```

---

## Movies API

### 1. Get Trending Movies

**Endpoint:** `GET /api/movies/trending/`

**Query Parameters:**
- `time_window` (optional): `day` or `week` (default: `day`)
- `page` (optional): Page number (default: `1`)

**Request:**
```bash
GET /api/movies/trending/?time_window=week&page=1
```

**Response:** `200 OK`
```json
{
  "count": 20,
  "next": "http://localhost:8000/api/movies/trending/?page=2",
  "previous": null,
  "results": [
    {
      "id": 550,
      "title": "Fight Club",
      "overview": "A ticking-time-bomb insomniac...",
      "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
      "backdrop_path": "/fCayJrkfRaCRCTh8GqN30f8oyQF.jpg",
      "release_date": "1999-10-15",
      "vote_average": 8.4,
      "vote_count": 26280,
      "popularity": 61.416,
      "adult": false,
      "original_language": "en",
      "genre_ids": [18, 53, 35]
    }
  ],
  "page": 1,
  "total_pages": 500,
  "total_results": 10000
}
```

### 2. Get Popular Movies

**Endpoint:** `GET /api/movies/popular/`

**Query Parameters:**
- `page` (optional): Page number (default: `1`)

**Request:**
```bash
GET /api/movies/popular/?page=1
```

**Response:** Same structure as trending movies.

### 3. Get Top Rated Movies

**Endpoint:** `GET /api/movies/top-rated/`

**Query Parameters:**
- `page` (optional): Page number (default: `1`)

**Request:**
```bash
GET /api/movies/top-rated/?page=1
```

**Response:** Same structure as trending movies.

### 4. Search Movies

**Endpoint:** `GET /api/movies/search/`

**Query Parameters:**
- `query` (required): Search query
- `page` (optional): Page number (default: `1`)

**Request:**
```bash
GET /api/movies/search/?query=inception&page=1
```

**Response:** Same structure as trending movies.

### 5. Get Movie Details

**Endpoint:** `GET /api/movies/{movie_id}/`

**Request:**
```bash
GET /api/movies/550/
```

**Response:** `200 OK`
```json
{
  "id": 550,
  "title": "Fight Club",
  "overview": "A ticking-time-bomb insomniac and a slippery soap salesman...",
  "tagline": "Mischief. Mayhem. Soap.",
  "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
  "backdrop_path": "/fCayJrkfRaCRCTh8GqN30f8oyQF.jpg",
  "release_date": "1999-10-15",
  "runtime": 139,
  "vote_average": 8.4,
  "vote_count": 26280,
  "popularity": 61.416,
  "budget": 63000000,
  "revenue": 100853753,
  "status": "Released",
  "adult": false,
  "original_language": "en",
  "original_title": "Fight Club",
  "homepage": "http://www.foxmovies.com/movies/fight-club",
  "imdb_id": "tt0137523",
  "genres": [
    {
      "id": 18,
      "name": "Drama"
    },
    {
      "id": 53,
      "name": "Thriller"
    }
  ],
  "production_companies": [
    {
      "id": 508,
      "name": "Regency Enterprises",
      "logo_path": "/7PzJdsLGlR7oW4J0J5Xcd0pHGRg.png",
      "origin_country": "US"
    }
  ],
  "production_countries": [
    {
      "iso_3166_1": "US",
      "name": "United States of America"
    }
  ],
  "spoken_languages": [
    {
      "english_name": "English",
      "iso_639_1": "en",
      "name": "English"
    }
  ]
}
```

### 6. Get Movie Recommendations

**Endpoint:** `GET /api/movies/{movie_id}/recommendations/`

**Query Parameters:**
- `page` (optional): Page number (default: `1`)

**Request:**
```bash
GET /api/movies/550/recommendations/?page=1
```

**Response:** List of recommended movies based on the given movie.

### 7. Get Similar Movies

**Endpoint:** `GET /api/movies/{movie_id}/similar/`

**Query Parameters:**
- `page` (optional): Page number (default: `1`)

**Request:**
```bash
GET /api/movies/550/similar/?page=1
```

**Response:** List of similar movies.

---

## Genres API

### 1. Get All Genres

**Endpoint:** `GET /api/genres/`

**Request:**
```bash
GET /api/genres/
```

**Response:** `200 OK`
```json
{
  "count": 19,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 28,
      "name": "Action",
      "tmdb_id": 28
    },
    {
      "id": 12,
      "name": "Adventure",
      "tmdb_id": 12
    },
    {
      "id": 16,
      "name": "Animation",
      "tmdb_id": 16
    }
  ]
}
```

### 2. Sync Genres from TMDb

**Endpoint:** `GET /api/genres/fetch-from-tmdb/`

**Request:**
```bash
GET /api/genres/fetch-from-tmdb/
```

**Response:** `200 OK`
```json
{
  "message": "Genres synced successfully",
  "count": 19
}
```

---

## User Management

### 1. Get User Profile

**Endpoint:** `GET /api/users/profile/`

**Authentication:** Required

**Request:**
```bash
GET /api/users/profile/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Movie enthusiast",
  "profile_image": null,
  "date_joined": "2024-01-15T10:30:00Z"
}
```

### 2. Update User Profile

**Endpoint:** `PUT /api/users/profile/update/` or `PATCH /api/users/profile/update/`

**Authentication:** Required

**Request:**
```json
{
  "first_name": "Jonathan",
  "last_name": "Doe",
  "bio": "Passionate about cinema and storytelling",
  "email": "jonathan@example.com"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "jonathan@example.com",
  "first_name": "Jonathan",
  "last_name": "Doe",
  "bio": "Passionate about cinema and storytelling",
  "profile_image": null
}
```

### 3. Change Password

**Endpoint:** `POST /api/users/change-password/`

**Authentication:** Required

**Request:**
```json
{
  "old_password": "OldPass123!",
  "new_password": "NewSecurePass456!",
  "new_password2": "NewSecurePass456!"
}
```

**Response:** `200 OK`
```json
{
  "message": "Password changed successfully"
}
```

### 4. Logout

**Endpoint:** `POST /api/users/logout/`

**Authentication:** Required

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "message": "Successfully logged out"
}
```

---

## Favorites & Watchlist

### Favorites

#### 1. Get User's Favorites

**Endpoint:** `GET /api/favorites/`

**Authentication:** Required

**Request:**
```bash
GET /api/favorites/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response:** `200 OK`
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "tmdb_id": 550,
      "title": "Fight Club",
      "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
      "release_date": "1999-10-15",
      "vote_average": 8.4,
      "added_at": "2024-01-20T14:30:00Z"
    }
  ]
}
```

#### 2. Add to Favorites

**Endpoint:** `POST /api/favorites/`

**Authentication:** Required

**Request:**
```json
{
  "tmdb_id": 550,
  "title": "Fight Club",
  "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
  "release_date": "1999-10-15",
  "vote_average": 8.4
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "user": 1,
  "tmdb_id": 550,
  "title": "Fight Club",
  "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
  "release_date": "1999-10-15",
  "vote_average": 8.4,
  "added_at": "2024-01-20T14:30:00Z"
}
```

#### 3. Remove from Favorites

**Endpoint:** `DELETE /api/favorites/{id}/`

**Authentication:** Required

**Request:**
```bash
DELETE /api/favorites/1/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response:** `204 No Content`

#### 4. Check if Movie is Favorited

**Endpoint:** `GET /api/favorites/check/{tmdb_id}/`

**Authentication:** Required

**Request:**
```bash
GET /api/favorites/check/550/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response:** `200 OK`
```json
{
  "is_favorite": true,
  "favorite_id": 1
}
```

Or:
```json
{
  "is_favorite": false,
  "favorite_id": null
}
```

### Watchlist

#### 1. Get User's Watchlist

**Endpoint:** `GET /api/watchlist/`

**Authentication:** Required

**Request:**
```bash
GET /api/watchlist/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response:** Same structure as favorites.

#### 2. Add to Watchlist

**Endpoint:** `POST /api/watchlist/`

**Authentication:** Required

**Request:**
```json
{
  "tmdb_id": 550,
  "title": "Fight Club",
  "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
  "release_date": "1999-10-15",
  "vote_average": 8.4
}
```

**Response:** `201 Created`

#### 3. Remove from Watchlist

**Endpoint:** `DELETE /api/watchlist/{id}/`

**Authentication:** Required

**Response:** `204 No Content`

#### 4. Check if Movie is in Watchlist

**Endpoint:** `GET /api/watchlist/check/{tmdb_id}/`

**Authentication:** Required

**Response:** Same structure as favorites check.

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Request successful, no content to return |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Authentication required or failed |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

### Error Response Examples

**400 Bad Request:**
```json
{
  "username": ["This field is required."],
  "password": ["This password is too short. It must contain at least 8 characters."]
}
```

**401 Unauthorized:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

Or:
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

**404 Not Found:**
```json
{
  "detail": "Not found."
}
```

---

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Anonymous users**: 100 requests per hour
- **Authenticated users**: 1000 requests per hour

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640000000
```

**Rate Limit Exceeded Response:**
```json
{
  "detail": "Request was throttled. Expected available in 3600 seconds."
}
```

---

## Pagination

List endpoints return paginated results:

**Response Structure:**
```json
{
  "count": 10000,
  "next": "http://localhost:8000/api/movies/trending/?page=3",
  "previous": "http://localhost:8000/api/movies/trending/?page=1",
  "results": [...]
}
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

**Example:**
```bash
GET /api/movies/trending/?page=2&page_size=50
```

---

## Examples

### Complete Authentication Flow (JavaScript)

```javascript
class MovieAPI {
  constructor(baseURL = 'http://localhost:8000/api') {
    this.baseURL = baseURL;
    this.accessToken = null;
    this.refreshToken = null;
  }

  async register(userData) {
    const response = await fetch(`${this.baseURL}/users/register/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    
    const data = await response.json();
    if (response.ok) {
      this.accessToken = data.tokens.access;
      this.refreshToken = data.tokens.refresh;
    }
    return data;
  }

  async login(username, password) {
    const response = await fetch(`${this.baseURL}/users/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    
    const data = await response.json();
    if (response.ok) {
      this.accessToken = data.tokens.access;
      this.refreshToken = data.tokens.refresh;
    }
    return data;
  }

  async refreshAccessToken() {
    const response = await fetch(`${this.baseURL}/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: this.refreshToken })
    });
    
    const data = await response.json();
    if (response.ok) {
      this.accessToken = data.access;
    }
    return data;
  }

  async getTrendingMovies(timeWindow = 'day', page = 1) {
    const response = await fetch(
      `${this.baseURL}/movies/trending/?time_window=${timeWindow}&page=${page}`
    );
    return await response.json();
  }

  async addToFavorites(movieData) {
    const response = await fetch(`${this.baseURL}/favorites/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.accessToken}`
      },
      body: JSON.stringify(movieData)
    });
    return await response.json();
  }
}

// Usage
const api = new MovieAPI();

// Login
await api.login('johndoe', 'SecurePass123!');

// Get trending movies
const movies = await api.getTrendingMovies('week', 1);

// Add to favorites
await api.addToFavorites({
  tmdb_id: 550,
  title: "Fight Club",
  poster_path: "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
  release_date: "1999-10-15",
  vote_average: 8.4
});
```

### Python Example

```python
import requests

class MovieAPI:
    def __init__(self, base_url='http://localhost:8000/api'):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None
    
    def login(self, username, password):
        response = requests.post(
            f'{self.base_url}/users/login/',
            json={'username': username, 'password': password}
        )
        
        if response.ok:
            data = response.json()
            self.access_token = data['tokens']['access']
            self.refresh_token = data['tokens']['refresh']
            return data
        return response.json()
    
    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def get_trending_movies(self, time_window='day', page=1):
        response = requests.get(
            f'{self.base_url}/movies/trending/',
            params={'time_window': time_window, 'page': page}
        )
        return response.json()
    
    def add_to_favorites(self, movie_data):
        response = requests.post(
            f'{self.base_url}/favorites/',
            headers=self.get_headers(),
            json=movie_data
        )
        return response.json()

# Usage
api = MovieAPI()
api.login('johndoe', 'SecurePass123!')

# Get trending movies
movies = api.get_trending_movies('week', 1)

# Add to favorites
api.add_to_favorites({
    'tmdb_id': 550,
    'title': 'Fight Club',
    'poster_path': '/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg',
    'release_date': '1999-10-15',
    'vote_average': 8.4
})
```

### cURL Examples

**Register:**
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

**Login:**
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
```

**Get Trending Movies:**
```bash
curl -X GET "http://localhost:8000/api/movies/trending/?time_window=week&page=1"
```

**Add to Favorites:**
```bash
curl -X POST http://localhost:8000/api/favorites/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tmdb_id": 550,
    "title": "Fight Club",
    "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
    "release_date": "1999-10-15",
    "vote_average": 8.4
  }'
```

---

## Best Practices

1. **Store tokens securely** - Never expose tokens in client-side code
2. **Refresh tokens proactively** - Don't wait for 401 errors
3. **Handle errors gracefully** - Always check response status
4. **Use pagination** - Don't fetch all results at once
5. **Cache responses** - Reduce API calls where appropriate
6. **Respect rate limits** - Implement exponential backoff

---

## Support

For more information:
- **Swagger Docs**: http://localhost:8000/api/docs/
- **Setup Guide**: [SETUP.md](SETUP.md)
- **Main Documentation**: [README.md](README.md)

---

**Questions?** Open an issue on GitHub or contact the development team.
