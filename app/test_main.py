from app.main import app, dependecy_auth
from fastapi import HTTPException
from fastapi.testclient import TestClient

client = TestClient(app=app)

class TestReadRoot:

    def test_success(self):
        response = client.get(url='/')
        
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

class TestPostSingleEntry:

    def test_success(self, monkeypatch):

        # Overriding auth.verify_api_key to test successful db call
        def override_verify_api_key(*args, **kwargs):
            return 'test_user_123'
        
        monkeypatch.setattr("app.main.auth.verify_api_key", override_verify_api_key)

        response = client.post(url='/post_single',
                               headers={"API_KEY": "122"},
                               json={"table": "test_table",
                                     "url": "test_url",
                                     "data": {
                                         "test_data_1": "test_data_1_OK",
                                         "test_data_2": "test_data_2_OK"}})
        
        assert response.status_code == 200
        assert response.json() == {"message": "Data added successfully",
                                   "user_id": "test_user_123",
                                   "data": {
                                       "test_data_1": "test_data_1_OK",
                                       "test_data_2": "test_data_2_OK"}}
        
    def test_auth_db_error(self, monkeypatch):

        # Overriding auth.verify_api_key to throw an error on db connection
        def raise_postgres_server_error(*args, **kwargs):
            raise HTTPException(status_code=500)
        
        monkeypatch.setattr("app.main.auth.verify_api_key", raise_postgres_server_error)

        response = client.post(url='/post_single',
                               headers={"API_KEY": "122"},
                               json={"table": "test_table",
                                     "url": "test_url",
                                     "data": {
                                         "test_data_1": "test_data_1_OK",
                                         "test_data_2": "test_data_2_OK"}})
        
        assert response.status_code == 500
        assert response.json() == {"detail": "Internal Server Error"}

    def test_invalid_api_key(self, monkeypatch):

        # Overriding auth.verify_api_key to throw an invalid api key error
        def raise_invalid_api_key(*args, **kwargs):
            raise HTTPException(status_code=401)
        
        monkeypatch.setattr("app.main.auth.verify_api_key", raise_invalid_api_key)

        response = client.post(url='/post_single',
                               headers={"API_KEY": "invalid_api_key"},
                               json={"table": "test_table",
                                     "url": "test_url",
                                     "data": {
                                         "test_data_1": "test_data_1_OK",
                                         "test_data_2": "test_data_2_OK"}})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}

    def test_missing_api_key(self):
        response = client.post(url='/post_single')
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_missing_data(self):
        response = client.post(url='/post_single',
                               headers ={"API_KEY": "123"})
        
        assert response.status_code == 422

def override_api_key_invalid():
    raise HTTPException(403)

def override_api_key_valid():
    return {"api_key": "test-key-123", "database": "test-db-123", "access_type": "Write"}

class TestPostSingle2:

    def test_api_key_invalid(self):
        app.dependency_overrides[dependecy_auth] = override_api_key_invalid
        response = client.post(url='/single_2',
                               headers={"API-KEY": "test-api-key-123"})
        
        assert response.status_code == 403
        app.dependency_overrides.clear()

    def test_success(self):
        app.dependency_overrides[dependecy_auth] = override_api_key_valid
        response = client.post(url='/single_2',
                               headers={"API-KEY": "test-api-key-123"})
        
        assert response.status_code == 200
        app.dependency_overrides.clear()