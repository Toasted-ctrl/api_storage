import pytest

class TestPostData:

    def test_post_data_success(self, client, override_user, admin_user, override_data_service):

        override_user(admin_user)

        payload = {
            "entries": [
                {
                    "base_url": "TEST_BASE_URL"
                }
            ]
        }

        response = client.post("/api/v1/data", json=payload)
        assert response.status_code == 200
        assert response.json() == {
            "detail": "Success",
            "ingested": [
                {
                    "base_url": "TEST_BASE_URL",
                    "data": None,
                    "params": None,
                    "status_code": None,
                    "url_ext": None
                }
            ]
        }

    def test_payload_incomplete(self, client, override_user, admin_user):

        override_user(admin_user)

        payload = {
            "entries": [
                {"url_ext": "TEST_EXT"}
            ]
        }

        response = client.post("/api/v1/data", json=payload)
        assert response.status_code == 422

    def test_payload_missing(self, client, override_user, admin_user):

        override_user(admin_user)

        response = client.post("/api/v1/data")
        assert response.status_code == 422

    def test_user_permissions_incorrect(self, client, override_user, read_only_user):

        override_user(read_only_user)

        response = client.post("/api/v1/data")
        assert response.status_code == 403
        assert response.json() == {
            "detail": "Write permission required"
        }

    def test_api_key_missing(self, client):

        response = client.post("/api/v1/data")
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
        response = client.post("/api/v1/data")
        assert response.status_code == expected[0]
        assert response.json() == expected[1]

class TestGetDataSources:

    

    remaining_permission_errors_data = [
        ((403, "Invalid API key"), (403, {"detail": "Invalid API key"})),
        ((403, "User not found"), (403, {"detail": "User not found"})),
        ((403, "User inactive"), (403, {"detail": "User inactive"}))
    ]

    @pytest.mark.parametrize("data, expected", remaining_permission_errors_data)
    def test_remaining_permission_errors(self, client, override_auth_error, data, expected):

        override_auth_error(data[0], data[1])
        response = client.get("/api/v1/data/sources")
        assert response.status_code == expected[0]
        assert response.json() == expected[1]