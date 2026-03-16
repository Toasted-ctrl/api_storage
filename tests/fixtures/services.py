import pytest
from api.v1.data import get_data_service
from api.v1.user import get_user_service

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

class MockUserService:
    def get_users(self):
        return [
            {"email": "TEST_MAIL_123",
             "user_id": 1}
        ]
    
    def post_user(self, data):
        return (
            {
                "first_name": "TEST_FIRST_NAME",
                "last_name": "TEST_LAST_NAME",
                "email": "TEST_MAIL",
                "is_admin": True,
                "can_write": True,
                "can_read": True,
                "user_id": 2,
                "is_active": True
            },
            "TEST_KEY_123"
        )
    
    def get_user(self, id):
        return {
            "first_name": "TEST_FIRST_NAME",
            "last_name": "TEST_LAST_NAME",
            "email": "TEST_MAIL",
            "is_admin": True,
            "can_write": True,
            "can_read": True,
            "user_id": 2,
            "is_active": True
        }
    
    def update_user(self, data, user_id):
        return {
            "is_admin": True,
            "is_active": True,
            "can_read": True,
            "can_write": True,
            "email": "TEST_MAIL",
            "first_name": "UPDATED_NAME",
            "last_name": "TEST_LAST_NAME",
            "user_id": 4
        }

@pytest.fixture
def mock_user_service():
    return MockUserService()

@pytest.fixture
def override_user_service(app, mock_user_service):
    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    yield
    app.dependency_overrides.clear()