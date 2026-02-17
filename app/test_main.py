from app.main import app, dependency_auth, dependency_auth_admin
from datetime import datetime
from fastapi import HTTPException
from fastapi.testclient import TestClient

client = TestClient(app=app)

def override_api_key_invalid():
    raise HTTPException(403)

def override_api_key_valid():
    return {"api_key": "test-key-123", "user_id": 123}

def override_api_key_server_error():
    raise HTTPException(500)

class TestRoot:

    def test_success(self):
        response = client.get(url='/')
        assert response.status_code == 200
        assert response.json() == {"message": "Hello There",
                                   "version": app.version,
                                   "contact": app.contact}

class TestPostSingle:

    def test_success(self):
        app.dependency_overrides[dependency_auth] = override_api_key_valid
        response = client.post(url='/single',
                               headers={"API-KEY": "test-api-key-123"},
                               json={
                                   "table": "test_table",
                                   "url": "test_url",
                                   "data": {
                                       "data_entry_1": "data_1_OK"}})
        
        assert response.status_code == 200
        assert response.json() == {"api_key": "test-key-123",
                                   "message": "Success",
                                   "table": "test_table",
                                   "url": "test_url",
                                   "data": {
                                       "data_entry_1": "data_1_OK"}}
        
        app.dependency_overrides.clear()

    def test_api_key_invalid(self):
        app.dependency_overrides[dependency_auth] = override_api_key_invalid
        response = client.post(url='/single',
                               headers={"API-KEY": "test-api-key-123"})
        
        assert response.status_code == 403
        assert response.json() == {"detail": "Forbidden"}
        app.dependency_overrides.clear()

    def test_api_key_server_error(self):
        app.dependency_overrides[dependency_auth] = override_api_key_server_error
        response = client.post(url='/single',
                               headers={"API_KEY": "test-key-123"},
                               json={
                                   "table": "test-table-123",
                                   "url": "test-url-123",
                                   "data":{
                                       "test-data-1": "test-data-1-OK"}})
        
        assert response.status_code == 500
        assert response.json() == {"detail": "Internal Server Error"}
        app.dependency_overrides.clear()

    def test_api_key_missing(self):
        response = client.post(url='/single',
                               headers={},
                               json={
                                   "table": "test-table-123",
                                   "url": "test-url-123",
                                   "data": {
                                       "test-data-1": "test-data-1-OK"}})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_payload_missing(self):
        app.dependency_overrides[dependency_auth] = override_api_key_valid
        response = client.post(url='/single',
                               headers={"API-KEY": "test-api-key-123"})
        
        assert response.status_code == 422
        app.dependency_overrides.clear()

    def test_payload_incomplete(self):
        app.dependency_overrides[dependency_auth] = override_api_key_valid
        response = client.post(url='/single',
                               headers={"API_KEY": "test-key-123"},
                               data={
                                   "table": "test-table-123"})
    
        assert response.status_code == 422
        app.dependency_overrides.clear()

class TestAddUser():

    def test_success(self):
        app.dependency_overrides[dependency_auth_admin] = override_api_key_valid
        current_date = datetime.now()
        response = client.post(url='/add_user',
                               headers={"API_KEY": "test-api-key-123"},
                               json={
                                   "user_first_name": "test-user-first-name",
                                   "user_last_name": "test-user-last-name",
                                   "access_type": "test-access-type",
                                   "expiry_date": str(current_date)})
        
        assert response.status_code == 200
        assert response.json() == {"api_key": "test-key-123",
                                   "message": "Success",
                                   "new_user_api_key": "test-new-user-api-key-123",
                                   "expiry_date": str(current_date).replace(' ', 'T')}
        
        app.dependency_overrides.clear()

    def test_api_key_invalid(self):
        app.dependency_overrides[dependency_auth_admin] = override_api_key_invalid
        response = client.post(url='/add_user',
                               headers={"API-KEY": "test-api-key-123"},
                               json={
                                   "user_first_name": "test-user-first-name",
                                   "user_last_name": "test-user-last-name",
                                   "access_type": "test-access-type"})
        
        assert response.status_code == 403
        assert response.json() == {"detail": "Forbidden"}
        app.dependency_overrides.clear()

    def test_api_key_server_error(self):
        app.dependency_overrides[dependency_auth_admin] = override_api_key_server_error
        response = client.post(url='/add_user',
                               headers={"API-KEY": "test-api-key-123"},
                               json={
                                   "user_first_name": "test-user-first-name",
                                   "user_last_name": "test-user-last-name",
                                   "access_type": "test-access-type"})
        
        assert response.status_code == 500
        assert response.json() == {"detail": "Internal Server Error"}
        app.dependency_overrides.clear()

    def test_api_key_missing(self):
        response = client.post(url='/add_user',
                               headers={},
                               json={
                                   "user_first_name": "test-user-first-name-123",
                                   "user_last_name": "test-user-last-name-123",
                                   "access_type": "test-access-type-123"})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_payload_missing(self):
        app.dependency_overrides[dependency_auth_admin] = override_api_key_valid
        response = client.post(url='/add_user',
                               headers={"API_KEY": "test-api-key-123"})
        
        assert response.status_code == 422
        app.dependency_overrides.clear()

    def test_payload_incomplete(self):
        app.dependency_overrides[dependency_auth_admin] = override_api_key_valid
        response = client.post(url='/add_user',
                               headers={"API_KEY": "test-api-key-123"},
                               json={"user_first_name": "test-user-first-name-123"})
        
        assert response.status_code == 422
        app.dependency_overrides.clear()