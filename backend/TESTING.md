# Testing Guide - SmartTourism Backend

## Overview
Comprehensive testing setup for SmartTourism API with pytest, covering unit tests, integration tests, and WebSocket functionality.

## Test Structure

```
backend/tests/
├── conftest.py                 # Global fixtures and configuration
├── unit/
│   ├── test_orion_service.py  # Orion CB integration tests
│   ├── test_auth.py           # JWT authentication tests
│   └── test_websocket.py      # WebSocket manager tests
├── integration/
│   └── test_api.py            # API endpoint tests
└── fixtures/                   # Test data and mocks
```

## Quick Start

### Install Test Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest
```

### Run Specific Test Categories

**Unit tests only:**
```bash
pytest -m unit
```

**Integration tests only:**
```bash
pytest -m integration
```

**Specific test file:**
```bash
pytest tests/unit/test_auth.py -v
```

**With coverage report:**
```bash
pytest --cov=app --cov-report=html
```

## Test Categories

### Unit Tests (70% coverage target)

#### Orion CB Integration (`test_orion_service.py`)
- Entity creation with proper NGSI-LD formatting
- Entity retrieval and querying
- Entity updates and deletions
- Retry logic with exponential backoff
- Error handling (404, timeouts, etc.)
- **Tests**: 8

#### Authentication (`test_auth.py`)
- JWT token creation and expiration
- Token verification and validation
- User extraction from tokens
- Password hashing verification
- Login flow
- Invalid credential handling
- **Tests**: 10

#### WebSocket (`test_websocket.py`)
- Connection management
- Channel subscriptions
- Broadcasting to user/channel
- Multiple connections per user
- Disconnection handling
- Keep-alive mechanism
- **Tests**: 10

### Integration Tests (60% coverage target)

#### API Endpoints (`test_api.py`)
- **POIs Endpoints**: List, get, create, update, delete, occupancy
- **Tourists Endpoints**: Profile, history, recommendations
- **Events Endpoints**: List, get, create, update, occupancy
- **Auth Endpoints**: Signup, login, refresh, health check
- **Error Handling**: 404, validation errors, 401/403
- **Tests**: 25+

## Fixtures

### Database Fixtures
- `test_db`: In-memory SQLite database with auto-migration

### HTTP Client Fixtures
- `async_client`: AsyncClient for testing FastAPI endpoints

### Mock Data Fixtures
- `mock_orion_response`: Typical Orion CB entity response
- `mock_jwt_token`: Valid JWT token for tests
- `mock_admin_token`: Admin JWT token
- `sample_poi_data`: Sample POI for testing
- `sample_user_data`: Sample user for testing
- `sample_event_data`: Sample event for testing

## Running Tests with Coverage

Generate HTML coverage report:
```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

## Continuous Integration

Tests are configured to run automatically on:
- Push to main branch
- Pull requests
- Development branches

### GitHub Actions (Future Setup)
```yaml
- name: Run tests
  run: pytest --cov=app --cov-fail-under=70
```

## Test Markers

### Available Markers
- `@pytest.mark.asyncio` - Async test
- `@pytest.mark.unit` - Unit test
- `@pytest.mark.integration` - Integration test
- `@pytest.mark.slow` - Slow test (optional)

### Using Markers
```bash
# Run only async tests
pytest -m asyncio

# Run only unit tests
pytest -m unit

# Run all except slow tests
pytest -m "not slow"
```

## Best Practices

### Writing Tests
1. Use descriptive test names: `test_create_entity_with_valid_data`
2. Test both success and failure paths
3. Use fixtures for setup/teardown
4. Mock external dependencies (HTTP, DB)
5. Test edge cases (empty, null, invalid)

### Test Structure (AAA Pattern)
```python
@pytest.mark.asyncio
async def test_operation():
    # Arrange - Set up test data
    input_data = {"key": "value"}
    
    # Act - Execute the operation
    result = await function(input_data)
    
    # Assert - Verify results
    assert result is not None
```

### Mocking Best Practices
```python
from unittest.mock import AsyncMock, patch

@patch("app.services.orion_service.OrionClient")
async def test_with_mock(mock_client):
    mock_instance = AsyncMock()
    mock_client.return_value = mock_instance
    
    # Test code
```

## Coverage Targets

| Component | Target |
|-----------|--------|
| Services | 85% |
| Routes | 80% |
| Middleware | 75% |
| Models | 70% |
| Overall | 70% |

## Debugging Tests

### Verbose Output
```bash
pytest -vv
```

### Show Print Statements
```bash
pytest -s
```

### Drop into Debugger
```python
def test_something():
    import pdb; pdb.set_trace()
    # Code here
```

### Run Specific Test with Debug
```bash
pytest tests/unit/test_auth.py::TestTokenManager::test_create_access_token_success -vv -s
```

## Known Issues & Workarounds

### Async Test Issues
- Ensure `pytest-asyncio` is installed
- Use `@pytest.mark.asyncio` decorator
- Run with `asyncio_mode = auto` in pytest.ini

### Database Issues
- In-memory SQLite used for tests (not production DB)
- Migrations run automatically
- Test isolation: Each test gets fresh DB

## Future Improvements

- [ ] Add property-based testing (hypothesis)
- [ ] Add performance benchmarks
- [ ] Add mutation testing (mutmut)
- [ ] Add security scanning (bandit)
- [ ] Add E2E tests with Selenium/Playwright
- [ ] Integrate with CI/CD pipeline

## References

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)
- [FastAPI testing](https://fastapi.tiangolo.com/advanced/testing-intro/)
- [pytest fixtures](https://docs.pytest.org/en/6.2.x/fixture.html)
