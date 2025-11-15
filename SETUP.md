# Setup Guide

This guide provides detailed instructions for setting up the Movie Recommendation Backend in different environments.

## Table of Contents

1. [Development Setup](#development-setup)
2. [Production Setup](#production-setup)
3. [Database Configuration](#database-configuration)
4. [Redis Configuration](#redis-configuration)
5. [Environment Variables](#environment-variables)
6. [Troubleshooting](#troubleshooting)

## Development Setup

### Step 1: Prerequisites

Ensure you have the following installed:

- **Python 3.9+**
  ```bash
  # Check Python version
  python --version
  ```

- **Git**
  ```bash
  # Check Git version
  git --version
  ```

- **pip** (usually comes with Python)
  ```bash
  # Check pip version
  pip --version
  ```

### Step 2: Clone the Repository

```bash
git clone https://github.com/crazycoder44/alx-movie-recommendation-backend.git
cd alx-movie-recommendation-backend
```

### Step 3: Create Virtual Environment

**Windows:**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**Linux/macOS:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**Verify activation:**
```bash
# You should see (venv) in your terminal prompt
which python  # Linux/macOS
where python  # Windows
```

### Step 4: Install Dependencies

```bash
# Upgrade pip (recommended)
python -m pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

### Step 5: Environment Configuration

#### Option A: Simple Setup (SQLite + No Redis)

Create a `.env` file:
```env
# Django
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite - no setup needed)
USE_POSTGRESQL=False

# TMDb API (REQUIRED - get from https://www.themoviedb.org/settings/api)
TMDB_API_KEY=your_tmdb_api_key_here
TMDB_BASE_URL=https://api.themoviedb.org/3

# JWT
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

#### Option B: Full Setup (PostgreSQL + Redis)

See [Database Configuration](#database-configuration) and [Redis Configuration](#redis-configuration) sections below.

### Step 6: Get TMDb API Key

1. Go to [The Movie Database](https://www.themoviedb.org/)
2. Create a free account (if you don't have one)
3. Go to Settings → API
4. Request an API key (choose "Developer" option)
5. Copy your API key and add it to `.env`:
   ```env
   TMDB_API_KEY=your_api_key_here
   ```

### Step 7: Run Migrations

```bash
# Apply database migrations
python manage.py migrate
```

### Step 8: Create Superuser (Optional)

```bash
# Create admin account
python manage.py createsuperuser

# Follow the prompts:
# - Username: admin
# - Email: admin@example.com
# - Password: (enter a secure password)
```

### Step 9: Run Development Server

```bash
# Start the server
python manage.py runserver

# Server will start at http://localhost:8000
```

### Step 10: Verify Installation

Open your browser and check:

- **API Root**: http://localhost:8000/api/
- **Swagger Docs**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/ (login with superuser credentials)

---

## Production Setup

### Step 1: Server Requirements

- Ubuntu 20.04+ / CentOS 8+ / similar Linux distribution
- Python 3.9+
- PostgreSQL 12+
- Redis 5+
- Nginx (for reverse proxy)
- Gunicorn (WSGI server)

### Step 2: Install System Dependencies

**Ubuntu/Debian:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install Redis
sudo apt install redis-server -y

# Install Nginx
sudo apt install nginx -y
```

### Step 3: Database Setup

See [Database Configuration](#database-configuration) section.

### Step 4: Application Setup

```bash
# Create application directory
sudo mkdir -p /var/www/movie-recommendation
cd /var/www/movie-recommendation

# Clone repository
sudo git clone https://github.com/crazycoder44/alx-movie-recommendation-backend.git .

# Create virtual environment
sudo python3 -m venv venv

# Activate and install dependencies
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn  # Production WSGI server
```

### Step 5: Environment Configuration

```bash
# Create production .env file
sudo nano .env
```

Add production settings:
```env
SECRET_KEY=use-a-very-secure-random-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

USE_POSTGRESQL=True
DATABASE_NAME=movie_recommendation_db
DATABASE_USER=movie_user
DATABASE_PASSWORD=secure_password_here
DATABASE_HOST=localhost
DATABASE_PORT=5432

TMDB_API_KEY=your_production_tmdb_api_key
TMDB_BASE_URL=https://api.themoviedb.org/3

REDIS_URL=redis://localhost:6379/0

JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

### Step 6: Collect Static Files

```bash
# Configure static files location
python manage.py collectstatic --noinput
```

### Step 7: Run Migrations

```bash
python manage.py migrate
```

### Step 8: Create Systemd Service

Create a systemd service file:
```bash
sudo nano /etc/systemd/system/movie-recommendation.service
```

Add the following:
```ini
[Unit]
Description=Movie Recommendation Backend
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/movie-recommendation
Environment="PATH=/var/www/movie-recommendation/venv/bin"
ExecStart=/var/www/movie-recommendation/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/movie-recommendation/gunicorn.sock \
    movie_recommendation_backend.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable movie-recommendation
sudo systemctl start movie-recommendation
sudo systemctl status movie-recommendation
```

### Step 9: Configure Nginx

Create Nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/movie-recommendation
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location /static/ {
        alias /var/www/movie-recommendation/staticfiles/;
    }

    location /media/ {
        alias /var/www/movie-recommendation/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/movie-recommendation/gunicorn.sock;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/movie-recommendation /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 10: SSL Certificate (Optional but Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

---

## Database Configuration

### SQLite (Development)

**No setup required!** SQLite is perfect for development:

```env
USE_POSTGRESQL=False
```

Django will automatically create `db.sqlite3` in your project directory.

### PostgreSQL (Production)

#### Installation

**Ubuntu/Debian:**
```bash
sudo apt install postgresql postgresql-contrib -y
```

**macOS (with Homebrew):**
```bash
brew install postgresql
brew services start postgresql
```

**Windows:**
Download and install from [postgresql.org](https://www.postgresql.org/download/windows/)

#### Configuration

1. **Access PostgreSQL:**
   ```bash
   sudo -u postgres psql
   ```

2. **Create database and user:**
   ```sql
   CREATE DATABASE movie_recommendation_db;
   CREATE USER movie_user WITH PASSWORD 'secure_password';
   ALTER ROLE movie_user SET client_encoding TO 'utf8';
   ALTER ROLE movie_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE movie_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE movie_recommendation_db TO movie_user;
   \q
   ```

3. **Update .env file:**
   ```env
   USE_POSTGRESQL=True
   DATABASE_NAME=movie_recommendation_db
   DATABASE_USER=movie_user
   DATABASE_PASSWORD=secure_password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   ```

4. **Test connection:**
   ```bash
   python manage.py check --database default
   ```

---

## Redis Configuration

### Why Redis?

Redis is used for caching API responses to improve performance and reduce external API calls.

### Installation

**Ubuntu/Debian:**
```bash
sudo apt install redis-server -y
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

**macOS (with Homebrew):**
```bash
brew install redis
brew services start redis
```

**Windows:**
Download from [redis.io](https://redis.io/download) or use Docker:
```bash
docker run -d -p 6379:6379 redis
```

### Configuration

1. **Test Redis connection:**
   ```bash
   redis-cli ping
   # Should return: PONG
   ```

2. **Update .env file:**
   ```env
   REDIS_URL=redis://localhost:6379/0
   ```

3. **Configure Redis (optional):**
   ```bash
   sudo nano /etc/redis/redis.conf
   ```
   
   Recommended settings:
   ```conf
   maxmemory 256mb
   maxmemory-policy allkeys-lru
   ```

4. **Restart Redis:**
   ```bash
   sudo systemctl restart redis-server
   ```

### Without Redis

If you don't want to use Redis, the app will fall back to Django's local memory cache:

```env
# Don't set REDIS_URL or comment it out
# REDIS_URL=redis://localhost:6379/0
```

---

## Environment Variables

### Complete Reference

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `SECRET_KEY` | string | Yes | - | Django secret key for cryptographic signing |
| `DEBUG` | boolean | No | True | Enable Django debug mode |
| `ALLOWED_HOSTS` | string | Yes | localhost,127.0.0.1 | Comma-separated list of allowed hosts |
| `USE_POSTGRESQL` | boolean | No | False | Use PostgreSQL instead of SQLite |
| `DATABASE_NAME` | string | No | movie_recommendation_db | Database name |
| `DATABASE_USER` | string | No | postgres | Database user |
| `DATABASE_PASSWORD` | string | No | - | Database password |
| `DATABASE_HOST` | string | No | localhost | Database host |
| `DATABASE_PORT` | integer | No | 5432 | Database port |
| `TMDB_API_KEY` | string | Yes | - | TMDb API key from themoviedb.org |
| `TMDB_BASE_URL` | string | No | https://api.themoviedb.org/3 | TMDb API base URL |
| `REDIS_URL` | string | No | - | Redis connection URL |
| `JWT_ACCESS_TOKEN_LIFETIME_MINUTES` | integer | No | 60 | JWT access token lifetime in minutes |
| `JWT_REFRESH_TOKEN_LIFETIME_DAYS` | integer | No | 7 | JWT refresh token lifetime in days |

### Generating a Secret Key

```python
# Python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Or use this one-liner:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'xxx'"

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. "django.db.utils.OperationalError: unable to open database file"

**Solution:**
```bash
# Check file permissions
chmod 664 db.sqlite3  # Linux/macOS

# Or delete and recreate database
rm db.sqlite3
python manage.py migrate
```

#### 3. "connection to server at 'localhost' failed"

**Solution:**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql

# Or switch to SQLite for development
USE_POSTGRESQL=False
```

#### 4. "Error connecting to Redis"

**Solution:**
```bash
# Check if Redis is running
redis-cli ping

# Start Redis
sudo systemctl start redis-server

# Or disable Redis by removing REDIS_URL from .env
```

#### 5. "TMDb API returns 401 Unauthorized"

**Solution:**
- Verify your API key in `.env` file
- Check if API key is active at https://www.themoviedb.org/settings/api
- Ensure no extra spaces in the API key

#### 6. "Port 8000 is already in use"

**Solution:**
```bash
# Find process using port 8000
# Linux/macOS:
lsof -i :8000
kill -9 <PID>

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use a different port
python manage.py runserver 8001
```

### Getting Help

If you encounter issues not covered here:

1. Check the logs:
   ```bash
   # Django development server logs
   python manage.py runserver

   # Production logs
   sudo journalctl -u movie-recommendation -f
   ```

2. Enable debug mode temporarily (development only):
   ```env
   DEBUG=True
   ```

3. Check Django system:
   ```bash
   python manage.py check
   ```

4. Validate database connections:
   ```bash
   python manage.py dbshell
   ```

---

## Next Steps

After successful setup:

1. Read the [README.md](README.md) for API usage
2. Check out [API_GUIDE.md](API_GUIDE.md) for detailed endpoint documentation
3. Explore the Swagger docs at http://localhost:8000/api/docs/
4. Review [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) to understand the project architecture

---

**Need help?** Contact the development team or open an issue on GitHub.
