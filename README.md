# Bookstore API Test Suite

This repository contains a comprehensive test suite for the Bookstore API, implementing both unit tests and integration tests using pytest.

## Project Structure

```
bookstore/
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures and configuration
│   ├── config.py            # Test settings and constants
│   ├── test_auth.py         # Authentication tests
│   ├── test_books.py        # Book management tests
│   └── requirements-test.txt # Test dependencies
├── bookstore/               # Main application code
├── pytest.ini              # Pytest configuration
└── .github/
    └── workflows/
        └── test.yml        # GitHub Actions CI configuration
```

## Testing Strategy

### Unit Tests
- Tests for core business logic and utility functions
- Database operations are mocked to isolate functionality
- Authentication and authorization flows are tested independently
- Edge cases and error conditions are covered

### Integration Tests
- End-to-end testing of API endpoints
- Real database interactions using a test database
- Authentication flow testing
- CRUD operations for book management
- Error handling and edge cases

### Test Coverage
- Minimum 80% code coverage requirement
- Coverage reports generated in HTML format
- Codecov integration for tracking coverage trends

## Running Tests Locally

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r bookstore/requirements.txt
   pip install -r tests/requirements-test.txt
   ```

3. Run tests:
   ```bash
   pytest
   ```

   Additional options:
   - `pytest -v`: Verbose output
   - `pytest -k "test_name"`: Run specific tests
   - `pytest --cov`: Generate coverage report

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration:

- Automated testing on Python 3.9, 3.10, and 3.11
- Code coverage reporting
- Integration with Codecov
- Runs on every push and pull request

## Test Configuration

Tests can be configured using environment variables or by modifying `tests/config.py`:

- `TEST_DATABASE_URL`: Test database connection string
- `API_HOST` and `API_PORT`: API endpoint configuration
- `JWT_SECRET_KEY`: JWT token signing key
- Test user credentials and sample data

## Challenges and Solutions

1. **Database Isolation**
   - Challenge: Ensuring tests don't interfere with each other
   - Solution: Each test uses a fresh database instance with automatic cleanup

2. **Asynchronous Testing**
   - Challenge: Testing async endpoints effectively
   - Solution: Using pytest-asyncio and async fixtures

3. **Authentication Testing**
   - Challenge: Managing JWT tokens in tests
   - Solution: Dedicated authenticated client fixture

4. **Test Data Management**
   - Challenge: Maintaining consistent test data
   - Solution: Centralized test data configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 