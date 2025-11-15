# Contributing to Movie Recommendation Backend

Thank you for your interest in contributing to the Movie Recommendation Backend project! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Commit Guidelines](#commit-guidelines)
6. [Pull Request Process](#pull-request-process)
7. [Testing](#testing)
8. [Documentation](#documentation)

## Code of Conduct

This project follows the ALX Backend Development program standards. Be respectful, professional, and collaborative in all interactions.

## Getting Started

### Prerequisites

Before you begin, ensure you have:

- Python 3.9 or higher
- Git installed and configured
- A GitHub account
- Basic knowledge of Django and REST APIs

### Setup

1. **Fork the repository**
   - Navigate to the [repository](https://github.com/crazycoder44/alx-movie-recommendation-backend)
   - Click the "Fork" button in the top right

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/alx-movie-recommendation-backend.git
   cd alx-movie-recommendation-backend
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/crazycoder44/alx-movie-recommendation-backend.git
   ```

4. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Install development dependencies
   pip install pytest pytest-django black flake8 coverage
   ```

5. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Verify setup**
   ```bash
   python manage.py check
   python manage.py runserver
   ```

## Development Workflow

### Branching Strategy

We use a feature branch workflow:

- `master` - Main branch, always deployable
- `feature/feature-name` - New features
- `fix/bug-name` - Bug fixes
- `docs/documentation-name` - Documentation updates
- `refactor/refactor-name` - Code refactoring

### Creating a Feature Branch

```bash
# Update your master branch
git checkout master
git pull upstream master

# Create a new feature branch
git checkout -b feature/your-feature-name
```

### Working on Your Feature

1. **Make your changes**
   - Write clean, readable code
   - Follow the coding standards (see below)
   - Add tests for new features
   - Update documentation as needed

2. **Test your changes**
   ```bash
   # Run all tests
   pytest
   
   # Run specific test file
   pytest tests/test_movies.py
   
   # Run with coverage
   coverage run -m pytest
   coverage report
   ```

3. **Format your code**
   ```bash
   # Format with Black
   black .
   
   # Check linting
   flake8
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Keep your branch updated**
   ```bash
   git fetch upstream
   git rebase upstream/master
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

## Coding Standards

### Python Style

We follow PEP 8 with some modifications:

- **Line length**: Maximum 100 characters
- **Imports**: Group in order (standard library, third-party, local)
- **Docstrings**: Use Google style docstrings
- **Type hints**: Use where appropriate

**Example:**

```python
from typing import Optional, List

from django.db import models
from rest_framework import serializers


class Movie(models.Model):
    """
    Movie model representing a film from TMDb.
    
    Attributes:
        tmdb_id: Unique identifier from TMDb
        title: Movie title
        overview: Plot synopsis
    """
    
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    overview = models.TextField()
    
    def __str__(self) -> str:
        """Return string representation of the movie."""
        return self.title
    
    @classmethod
    def get_by_tmdb_id(cls, tmdb_id: int) -> Optional['Movie']:
        """
        Retrieve a movie by its TMDb ID.
        
        Args:
            tmdb_id: The TMDb movie ID
            
        Returns:
            Movie instance or None if not found
        """
        try:
            return cls.objects.get(tmdb_id=tmdb_id)
        except cls.DoesNotExist:
            return None
```

### Django Best Practices

- **Models**: Keep business logic in models, not views
- **Views**: Use ViewSets for REST APIs
- **Serializers**: Validate data thoroughly
- **Queries**: Use `select_related()` and `prefetch_related()` to optimize
- **Security**: Never commit sensitive data (API keys, passwords)

### File Organization

```
app_name/
├── __init__.py
├── models.py          # Database models
├── serializers.py     # DRF serializers
├── views.py           # API views
├── urls.py            # URL routing
├── admin.py           # Admin configuration
├── services/          # Business logic
│   └── service_name.py
├── tests/             # Unit tests
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   └── test_serializers.py
└── migrations/        # Database migrations
```

## Commit Guidelines

### Commit Message Format

We follow Conventional Commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```bash
# Feature
git commit -m "feat: add movie search functionality"

# Bug fix
git commit -m "fix: resolve authentication token expiry issue"

# Documentation
git commit -m "docs: update API endpoint documentation"

# Performance
git commit -m "perf: optimize database queries for trending movies"
```

### Commit Best Practices

- **Atomic commits**: One logical change per commit
- **Clear messages**: Describe what and why, not how
- **Present tense**: "add feature" not "added feature"
- **Imperative mood**: "fix bug" not "fixes bug"
- **Reference issues**: Include issue numbers when applicable

## Pull Request Process

### Before Submitting

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/master
   ```

2. **Run all tests**
   ```bash
   pytest
   ```

3. **Check code quality**
   ```bash
   black .
   flake8
   ```

4. **Update documentation**
   - Update README if needed
   - Add docstrings to new functions/classes
   - Update API_GUIDE.md for new endpoints

### Submitting a Pull Request

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill out the PR template

### Pull Request Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## How Has This Been Tested?
Describe the tests you ran to verify your changes.

## Checklist
- [ ] My code follows the project's coding standards
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Related Issues
Closes #issue_number
```

### Review Process

1. **Automated Checks**: Wait for CI/CD to pass
2. **Code Review**: Maintainers will review your code
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, your PR will be merged

## Testing

### Writing Tests

Place tests in the `tests/` directory within each app:

```python
# movies/tests/test_views.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class MovieViewTests(TestCase):
    """Test cases for movie views."""
    
    def setUp(self):
        """Set up test client and test data."""
        self.client = APIClient()
    
    def test_get_trending_movies(self):
        """Test retrieving trending movies."""
        response = self.client.get('/api/movies/trending/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_search_movies(self):
        """Test movie search functionality."""
        response = self.client.get('/api/movies/search/', {'query': 'inception'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific app tests
pytest movies/tests/

# Run specific test file
pytest movies/tests/test_views.py

# Run specific test
pytest movies/tests/test_views.py::MovieViewTests::test_get_trending_movies

# Run with coverage
coverage run -m pytest
coverage report
coverage html  # Generates HTML report in htmlcov/
```

### Test Coverage

We aim for at least 80% test coverage. Check coverage with:

```bash
coverage run -m pytest
coverage report

# View coverage for specific file
coverage report movies/views.py
```

## Documentation

### Code Documentation

- **Docstrings**: Add to all classes, methods, and functions
- **Inline comments**: Explain complex logic
- **Type hints**: Use for function parameters and return types

### Project Documentation

Update the following when making changes:

- **README.md**: Overview, setup, quick start
- **SETUP.md**: Detailed installation and configuration
- **API_GUIDE.md**: API endpoint documentation
- **IMPLEMENTATION_PLAN.md**: Development roadmap

### API Documentation

The project uses Swagger/OpenAPI for API docs. Update docstrings in views:

```python
class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for movie operations.
    
    list:
    Return a list of all movies.
    
    retrieve:
    Return details of a specific movie.
    
    create:
    Create a new movie entry.
    """
    pass
```

## Questions?

If you have questions:

1. Check existing documentation
2. Search existing issues on GitHub
3. Ask in discussions
4. Contact the maintainers

---

**Thank you for contributing to the Movie Recommendation Backend!** 🎬

Your contributions help make this project better for everyone.
