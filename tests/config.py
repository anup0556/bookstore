"""Test configuration settings."""

from typing import Dict

# Test database settings
TEST_DATABASE_URL = "sqlite:///./test_db.db"

# API settings
API_V1_PREFIX = ""
PROJECT_NAME = "Bookstore API"
API_HOST = "http://localhost"
API_PORT = 8000
BASE_URL = f"{API_HOST}:{API_PORT}"

# JWT settings
JWT_SECRET_KEY = "test_secret_key_123"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Test user credentials
TEST_USER = {"email": "test@example.com", "password": "test_password123"}

# Test book data
TEST_BOOK = {
    "name": "Test Book",
    "author": "Test Author",
    "published_year": 2024,
    "book_summary": "A test book summary",
}

# API endpoints
ENDPOINTS: Dict[str, str] = {
    "health": "/health",
    "signup": "/signup",
    "login": "/login",
    "books": "/books/",
    "book_by_id": "/books/{book_id}",
}
