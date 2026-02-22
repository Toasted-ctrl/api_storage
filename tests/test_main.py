from app.main import app
from fastapi.testclient import TestClient
from datetime import datetime

client = TestClient(app=app)

class TestRoot:

    def test_success(self):
        response = client.get(url='/')
        assert response.status_code == 200
        assert response.json() == {"message": "Hello There",
                                   "version": app.version,
                                   "contact": app.contact}
        
class TestHealth:

    def test_success(self):
        response = client.get(url='/health')
        assert response.status_code == 200
        assert response.json() == {"status": "OK"}

class TestPostSingle:

    def test_success(self, client_with_fake_db):
        response = client_with_fake_db.post(url='/single',
                                            headers={"api-key": "TEST-KEY-123"},
                                            json={"table": "TEST-TABLE-123",
                                                  "url": "TEST-URL-123",
                                                  "data": {
                                                      "data-item-1": "DATA-ITEM-1-OK"}})
        
        assert response.status_code == 200
        assert response.json() == {"message": "Success",
                                   "table": "TEST-TABLE-123",
                                   "url": "TEST-URL-123",
                                   "data": {
                                       "data-item-1": "DATA-ITEM-1-OK"}}

    def test_api_key_invalid(self, client_with_fake_db):
        response = client_with_fake_db.post(url='/single',
                                            headers={"api-key": "TEST-KEY-XYZ"},
                                            json={"table": "TEST-TABLE-123",
                                                  "url": "TEST-URL-123",
                                                  "data": {
                                                      "data-item-1": "DATA-ITEM-1-OK"}})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid API key"}

    def test_api_key_server_error(self):
        pass
        # TODO: Replace with real test, for now pass.

    def test_api_key_missing(self, client_with_fake_db):
        response = client_with_fake_db.post(url='/single',
                                            headers={},
                                            json={"table": "TEST-TABLE-123",
                                                  "url": "TEST-URL-123",
                                                  "data": {
                                                      "data-item-1": "DATA-ITEM-1-OK"}})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_payload_missing(self, client_with_fake_db):
        response = client_with_fake_db.post(url='/single',
                                            headers={'api-key': "TEST-KEY-123"})
        
        assert response.status_code == 422

    def test_payload_incomplete(self, client_with_fake_db):
        response = client_with_fake_db.post(url='/single',
                                            headers={"api-key": "TEST-KEY-123"},
                                            json={"table": "TEST-TABLE-123",
                                                  "url": "TEST-URL-123"})
        
        assert response.status_code == 422

    def test_invalid_access_rights(self, client_with_fake_db):
        response = client_with_fake_db.post(url='/single',
                                            headers={"api-key": "TEST-KEY-789"},
                                            json={"table": "TEST-TABLE-123",
                                                  "url": "TEST-URL-123",
                                                  "data": {
                                                      "data-item-1": "DATA-ITEM-1-OK"}})
        
        assert response.status_code == 403
        assert response.json() == {"detail": "Forbidden"}

class TestPostAddUser():

    def test_success(self, client_with_fake_db):
        test_date = str(datetime.now())
        response = client_with_fake_db.post(url='/add_user',
                                            headers={"api-key": "TEST-KEY-123"},
                                            json={"first_name": "FIRST-NAME-456",
                                                  "last_name": "LAST-NAME-456",
                                                  "is_admin": False,
                                                  "can_read": True,
                                                  "can_write": False,
                                                  "expiry_date": test_date})
        
        assert response.status_code == 200
        assert response.json() == {"message": "Success",
                                   "new_user_api_key": "TEST-KEY-NEW-USER-123",
                                   "api_key": "TEST-KEY-123",
                                   "expiry_date": test_date.replace(' ', 'T')}

    def test_api_key_invalid(self, client_with_fake_db):
        response = client_with_fake_db.post(url='/add_user',
                                            headers={"api-key": "TEST-KEY-XYZ"},
                                            json={"first_name": "FIRST-NAME-456",
                                                  "last_name": "LAST-NAME-456",
                                                  "is_admin": False,
                                                  "can_read": True,
                                                  "can_write": False})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid API key"}

    def test_api_key_server_error(self):
        pass
        # TODO: Replace with real test, for now pass.

    def test_api_key_missing(self, client_with_fake_db):
        response = client_with_fake_db.post(url='/add_user',
                                            headers={},
                                            json={"first_name": "FIRST-NAME-456",
                                                  "last_name": "LAST-NAME-456",
                                                  "access_type": "Read-only"})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_payload_missing(self, client_with_fake_db):
        response = client_with_fake_db.post(url='/add_user',
                                            headers={"api-key": "TEST-KEY-123"})
        
        assert response.status_code == 422

    def test_payload_incomplete(self, client_with_fake_db):
        response = client_with_fake_db.post(url='/add_user',
                                            headers={"api-key": "TEST-KEY-123"},
                                            json={"last_name": "LAST-NAME-456",
                                                  "access_type": "Read-only"})
        
        assert response.status_code == 422

    def test_invalid_access_rights(self, client_with_fake_db):
        response = client_with_fake_db.post(url='/add_user',
                                            headers={"api-key": "TEST-KEY-789"},
                                            json={"first_name": "FIRST-NAME-456",
                                                  "last_name": "LAST-NAME-456",
                                                  "is_admin": False,
                                                  "can_read": True,
                                                  "can_write": False})
        
        assert response.status_code == 403
        assert response.json() == {"detail": "Forbidden"}