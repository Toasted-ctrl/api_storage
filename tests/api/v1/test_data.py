class TestEndPointData:

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