"""Test authentication endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    """Test health check endpoint."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "up"}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_data",
    [
        {"email": "test1@example.com", "password": "password123"},
        {"email": "test2@example.com", "password": "strongPass123!"},
        {"email": "admin@example.com", "password": "adminPass456!"},
        {"email": "user.name@example.com", "password": "userPass789!"},
    ],
)
async def test_signup_success(async_client: AsyncClient, user_data):
    """Test successful user signup with different user data."""
    response = await async_client.post("/signup", json=user_data)
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "User created successfully"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "duplicate_email",
    [
        "duplicate1@example.com",
        "duplicate2@example.com",
        "test.user@example.com",
    ],
)
async def test_signup_duplicate_email(async_client: AsyncClient, duplicate_email):
    """Test signup with duplicate email."""
    user_data = {"email": duplicate_email, "password": "testpass123"}

    # First signup
    await async_client.post("/signup", json=user_data)

    # Try to signup again with same email
    response = await async_client.post("/signup", json=user_data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_data",
    [
        {"email": "login1@example.com", "password": "password123"},
        {"email": "login2@example.com", "password": "strongPass456!"},
        {"email": "login.test@example.com", "password": "testPass789!"},
    ],
)
async def test_login_success(async_client: AsyncClient, user_data):
    """Test successful login with different credentials."""
    # Create user first
    await async_client.post("/signup", json=user_data)

    # Try to login
    response = await async_client.post("/login", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "invalid_credentials",
    [
        {"email": "test@example.com", "password": "wrongpass"},
        {"email": "user@example.com", "password": "incorrect123"},
        {"email": "admin@example.com", "password": "invalid456"},
    ],
)
async def test_login_invalid_credentials(
    async_client: AsyncClient, invalid_credentials
):
    """Test login with invalid credentials."""
    # Create user first with correct password
    valid_credentials = invalid_credentials.copy()
    valid_credentials["password"] = "correctpass123"
    await async_client.post("/signup", json=valid_credentials)

    # Try to login with wrong password
    response = await async_client.post("/login", json=invalid_credentials)
    assert response.status_code == 400
    assert "Incorrect email or password" in response.json()["detail"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "nonexistent_user",
    [
        {"email": "nonexistent1@example.com", "password": "pass123"},
        {"email": "nonexistent2@example.com", "password": "pass456"},
        {"email": "ghost.user@example.com", "password": "pass789"},
    ],
)
async def test_login_nonexistent_user(async_client: AsyncClient, nonexistent_user):
    """Test login with nonexistent user."""
    response = await async_client.post("/login", json=nonexistent_user)
    assert response.status_code == 400
    assert "Incorrect email or password" in response.json()["detail"]
