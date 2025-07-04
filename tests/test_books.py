"""Test book management endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "book_data",
    [
        {
            "name": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "published_year": 1925,
            "book_summary": "A story of decadence and excess.",
        },
        {
            "name": "1984",
            "author": "George Orwell",
            "published_year": 1949,
            "book_summary": "A dystopian social science fiction.",
        },
        {
            "name": "Pride and Prejudice",
            "author": "Jane Austen",
            "published_year": 1813,
            "book_summary": "A romantic novel of manners.",
        },
        {
            "name": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "published_year": 1960,
            "book_summary": "A story of racial injustice and loss of innocence.",
        },
    ],
)
async def test_create_book(authenticated_client: AsyncClient, book_data):
    """Test creating a new book with different data."""
    response = await authenticated_client.post("/books/", json=book_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == book_data["name"]
    assert data["author"] == book_data["author"]
    assert data["published_year"] == book_data["published_year"]
    assert data["book_summary"] == book_data["book_summary"]
    assert "id" in data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "book_data",
    [
        {
            "name": "Book One",
            "author": "Author One",
            "published_year": 2020,
            "book_summary": "Summary one",
        },
        {
            "name": "Book Two",
            "author": "Author Two",
            "published_year": 2021,
            "book_summary": "Summary two",
        },
    ],
)
async def test_get_book(authenticated_client: AsyncClient, book_data):
    """Test getting a book by ID."""
    # First create a book
    create_response = await authenticated_client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]

    # Get the book
    response = await authenticated_client.get(f"/books/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book_id
    assert data["name"] == book_data["name"]
    assert data["author"] == book_data["author"]


@pytest.mark.asyncio
@pytest.mark.parametrize("nonexistent_id", [999, 888, 777])
async def test_get_nonexistent_book(authenticated_client: AsyncClient, nonexistent_id):
    """Test getting a nonexistent book."""
    response = await authenticated_client.get(f"/books/{nonexistent_id}")
    assert response.status_code == 404
    assert "Book not found" in response.json()["detail"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "initial_data,update_data",
    [
        (
            {
                "name": "Initial Name 1",
                "author": "Initial Author 1",
                "published_year": 2020,
                "book_summary": "Initial Summary 1",
            },
            {
                "name": "Updated Name 1",
                "author": "Updated Author 1",
                "published_year": 2021,
                "book_summary": "Updated Summary 1",
            },
        ),
        (
            {
                "name": "Initial Name 2",
                "author": "Initial Author 2",
                "published_year": 2019,
                "book_summary": "Initial Summary 2",
            },
            {
                "name": "Updated Name 2",
                "author": "Initial Author 2",
                "published_year": 2019,
                "book_summary": "Updated Summary 2",
            },
        ),
        (
            {
                "name": "Initial Name 3",
                "author": "Initial Author 3",
                "published_year": 2018,
                "book_summary": "Initial Summary 3",
            },
            {
                "name": "Initial Name 3",
                "author": "Updated Author 3",
                "published_year": 2018,
                "book_summary": "Updated Summary 3",
            },
        ),
    ],
)
async def test_update_book(
    authenticated_client: AsyncClient, initial_data, update_data
):
    """Test updating a book with different data combinations."""
    # First create a book
    create_response = await authenticated_client.post("/books/", json=initial_data)
    book_id = create_response.json()["id"]

    # Update the book
    response = await authenticated_client.put(f"/books/{book_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book_id
    assert data["name"] == update_data["name"]
    assert data["author"] == update_data["author"]
    assert data["published_year"] == update_data["published_year"]
    assert data["book_summary"] == update_data["book_summary"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "nonexistent_id,update_data",
    [
        (
            999,
            {
                "name": "New Name 1",
                "author": "New Author 1",
                "published_year": 2022,
                "book_summary": "New Summary 1",
            },
        ),
        (
            888,
            {
                "name": "New Name 2",
                "author": "New Author 2",
                "published_year": 2023,
                "book_summary": "New Summary 2",
            },
        ),
    ],
)
async def test_update_nonexistent_book(
    authenticated_client: AsyncClient, nonexistent_id, update_data
):
    """Test updating a nonexistent book."""
    response = await authenticated_client.put(
        f"/books/{nonexistent_id}", json=update_data
    )
    assert response.status_code == 404
    assert "Book not found" in response.json()["detail"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "book_data",
    [
        {
            "name": "Delete Book 1",
            "author": "Author 1",
            "published_year": 2020,
            "book_summary": "Summary 1",
        },
        {
            "name": "Delete Book 2",
            "author": "Author 2",
            "published_year": 2021,
            "book_summary": "Summary 2",
        },
    ],
)
async def test_delete_book(authenticated_client: AsyncClient, book_data):
    """Test deleting a book."""
    # First create a book
    create_response = await authenticated_client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]

    # Delete the book
    response = await authenticated_client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"

    # Verify book is deleted
    get_response = await authenticated_client.get(f"/books/{book_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize("nonexistent_id", [999, 888, 777])
async def test_delete_nonexistent_book(
    authenticated_client: AsyncClient, nonexistent_id
):
    """Test deleting a nonexistent book."""
    response = await authenticated_client.delete(f"/books/{nonexistent_id}")
    assert response.status_code == 404
    assert "Book not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_all_books(authenticated_client: AsyncClient):
    """Test getting all books."""
    # Create multiple books
    books = [
        {
            "name": "Book One",
            "author": "Author One",
            "published_year": 2020,
            "book_summary": "Summary One",
        },
        {
            "name": "Book Two",
            "author": "Author Two",
            "published_year": 2021,
            "book_summary": "Summary Two",
        },
        {
            "name": "Book Three",
            "author": "Author Three",
            "published_year": 2022,
            "book_summary": "Summary Three",
        },
    ]

    for book in books:
        await authenticated_client.post("/books/", json=book)

    # Get all books
    response = await authenticated_client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= len(books)

    # Verify the books are in the response
    book_names = [book["name"] for book in data]
    for book in books:
        assert book["name"] in book_names


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoint,method,expected_status",
    [
        ("/books/", "GET", 403),
        ("/books/", "POST", 403),
        ("/books/1", "GET", 403),
        ("/books/1", "PUT", 403),
        ("/books/1", "DELETE", 403),
    ],
)
async def test_unauthorized_access(
    async_client: AsyncClient, endpoint, method, expected_status
):
    """Test accessing protected endpoints without authentication."""
    book_data = {
        "name": "Test Book",
        "author": "Test Author",
        "published_year": 2024,
        "book_summary": "Test Summary",
    }

    if method == "GET":
        response = await async_client.get(endpoint)
    elif method == "POST":
        response = await async_client.post(endpoint, json=book_data)
    elif method == "PUT":
        response = await async_client.put(endpoint, json=book_data)
    else:  # DELETE
        response = await async_client.delete(endpoint)

    assert response.status_code == expected_status
