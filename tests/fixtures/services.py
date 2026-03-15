import pytest
from api.v1.data import get_data_service

class MockDataService:
    def post_data(self, data):
        return [
            {
                "base_url": "TEST_BASE_URL",
                "params": None,
                "data": None,
                "url_ext": None,
                "status_code": None
            }
        ]

    def get_sources(self):
        return [
            {
                "base_url": "TEST_BASE_URL",
                "url_ext": None
            }
        ]

@pytest.fixture
def mock_data_service():
    return MockDataService()

@pytest.fixture
def override_data_service(app, mock_data_service):
    app.dependency_overrides[get_data_service] = lambda: mock_data_service
    yield
    app.dependency_overrides.clear()