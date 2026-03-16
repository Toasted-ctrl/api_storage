import pytest

class TestGetUsers:

    def test_success(self, client, override_user, admin_user, override_user_service):
        override_user(admin_user)
        response = client.get("/api/v1/users")
        assert response.status_code == 200
        assert response.json() == {
            "detail": "Success",
            "users": [
                {
                    "email": "TEST_MAIL_123",
                    "user_id": 1
                }
            ]
        }

    def test_incorrect_permissions(self, client, override_user, no_access_user):
        override_user(no_access_user)
        response = client.get("/api/v1/users")
        assert response.status_code == 403
        assert response.json() == {
            "detail": "Admin permission required"
        }

    def test_missing_api_key(self, client):
        response = client.get("/api/v1/users")
        assert response.status_code == 401
        assert response.json() == {
            "detail": "Missing API key"
        }

    remaining_permission_errors_data = [
        ((403, "Invalid API key"), (403, {"detail": "Invalid API key"})),
        ((403, "User not found"), (403, {"detail": "User not found"})),
        ((403, "User inactive"), (403, {"detail": "User inactive"}))
    ]

    @pytest.mark.parametrize("data, expected", remaining_permission_errors_data)
    def test_remaining_permission_errors(self, client, override_auth_error, data, expected):
        override_auth_error(data[0], data[1])
        response = client.get("/api/v1/users")
        assert response.status_code == expected[0]
        assert response.json() == expected[1]

class TestPostUser:

    def test_success(self, client, override_user, admin_user, override_user_service):
        override_user(admin_user)
        payload = {
            "first_name": "TEST_FIRST_NAME",
            "last_name": "TEST_LAST_NAME",
            "email": "TEST_MAIL",
            "is_admin": True,
            "can_read": True,
            "can_write": True
        }
        response = client.post("/api/v1/users",
                               json=payload)
        assert response.status_code == 200
        assert response.json() == {
            "detail": "Success",
            "new_user": {
                "api_key": "TEST_KEY_123",
                "user": {
                    "can_read": True,
                    "is_admin": True,
                    "can_write": True,
                    "id": 2,
                    "email": "TEST_MAIL",
                    "first_name": "TEST_FIRST_NAME",
                    "last_name": "TEST_LAST_NAME",
                    "is_active": True
                }
            }
        }

    def test_payload_incomplete(self, client, override_user, admin_user):
        override_user(admin_user)
        payload = {
            "first_name": "TEST_FIRST_NAME"
        }
        response = client.post("api/v1/users",
                               json=payload)
        assert response.status_code == 422

    def test_payload_missing(self, client, override_user, admin_user):
        override_user(admin_user)
        response = client.post("/api/v1/users")
        assert response.status_code == 422

    def test_invalid_permissions(self, client, override_user, no_access_user):
        override_user(no_access_user)
        response = client.post("/api/v1/users")
        assert response.status_code == 403
        assert response.json() == {
            "detail": "Admin permission required"
        }

    def test_missing_api_key(self, client):
        response = client.post("/api/v1/users")
        assert response.status_code == 401
        assert response.json() == {
            "detail": "Missing API key"
        }

    remaining_permission_errors_data = [
        ((403, "Invalid API key"), (403, {"detail": "Invalid API key"})),
        ((403, "User not found"), (403, {"detail": "User not found"})),
        ((403, "User inactive"), (403, {"detail": "User inactive"}))
    ]

    @pytest.mark.parametrize("data, expected", remaining_permission_errors_data)
    def test_remaining_permission_errors(self, client, override_auth_error, data, expected):
        override_auth_error(data[0], data[1])
        response = client.post("/api/v1/users")
        assert response.status_code == expected[0]
        assert response.json() == expected[1]