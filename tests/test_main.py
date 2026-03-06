from app.main import app
from app.database import Ingest, Users, ApiKeys
from fastapi.testclient import TestClient
from datetime import datetime

client = TestClient(app=app)

class TestHashedApiKey:

    def test_hashed_key(self, fake_db):
        check_api_key_hash_user_1 = fake_db.query(ApiKeys).filter(ApiKeys.user_id == 1).first()
        assert check_api_key_hash_user_1.hashed_api_key == "3360cf424220348735283eac04c5c60af56bf993bfee236b7aa6739674923da3"
        check_api_key_hash_user_2 = fake_db.query(ApiKeys).filter(ApiKeys.user_id == 2).first()
        assert check_api_key_hash_user_2.hashed_api_key == "e3c4258019236928ff5e79fdaaa033d6e4a9b881b6eb080d8aba7768e434f752"

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

class TestPostSingleEntry:

    def test_success(self, client_with_fake_db, fake_db):

        response = client_with_fake_db.post(url="/data/add_single",
                                            headers={"api-key": "TEST-KEY-123"},
                                            json={"url_primary": "TEST-URL-123",
                                                  "url_extension": "TEST-EXTENSION-123",
                                                  "status_code": 200,
                                                  "params": {
                                                      "param_item_1": "PARAM-ITEM-1-OK"},
                                                  "data": {
                                                      "data_item_1": "DATA-ITEM-1-OK"}})
        
        assert response.status_code == 200
        assert response.json() == {"message": "Success",
                                   "url_primary": "TEST-URL-123",
                                   "url_extension": "TEST-EXTENSION-123",
                                   "params": {
                                       "param_item_1": "PARAM-ITEM-1-OK"},
                                   "data": {
                                       "data_item_1": "DATA-ITEM-1-OK"}}
        
        # Verifying that the entry actually got added to the database

        check_tb_ingest = fake_db.query(Ingest).filter(Ingest.item_id == 4).first()
        assert check_tb_ingest.url_primary == "TEST-URL-123"
        assert check_tb_ingest.url_extension == "TEST-EXTENSION-123"
        assert check_tb_ingest.params == {"param_item_1": "PARAM-ITEM-1-OK"}
        assert check_tb_ingest.data == {"data_item_1": "DATA-ITEM-1-OK"}
        assert isinstance(check_tb_ingest.date_created, datetime)

    def test_api_key_invalid(self, client_with_fake_db):
        response = client_with_fake_db.post(url="/data/add_single",
                                            headers={"api-key": "TEST-KEY-XYZ"},
                                            json={"table": "TEST-TABLE-123",
                                                  "url_primary": "TEST-URL-123",
                                                  "url_extension": "TEST-EXTENSION-123",
                                                  "status_code": 200,
                                                  "data": {
                                                      "data-item-1": "DATA-ITEM-1-OK"}})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid API key"}

    def test_api_key_server_error(self):
        pass

        # TODO: Replace with real test, for now pass.

    def test_api_key_missing(self, client_with_fake_db):
        response = client_with_fake_db.post(url="/data/add_single",
                                            headers={},
                                            json={"table": "TEST-TABLE-123",
                                                  "url": "TEST-URL-123",
                                                  "data": {
                                                      "data-item-1": "DATA-ITEM-1-OK"}})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_payload_missing(self, client_with_fake_db):
        response = client_with_fake_db.post(url="/data/add_single",
                                            headers={'api-key': "TEST-KEY-123"})
        
        assert response.status_code == 422

    def test_payload_incomplete(self, client_with_fake_db):
        response = client_with_fake_db.post(url="/data/add_single",
                                            headers={"api-key": "TEST-KEY-123"},
                                            json={"table": "TEST-TABLE-123",
                                                  "url": "TEST-URL-123"})
        
        assert response.status_code == 422

    def test_invalid_access_rights(self, client_with_fake_db):
        response = client_with_fake_db.post(url="/data/add_single",
                                            headers={"api-key": "TEST-KEY-789"},
                                            json={"table": "TEST-TABLE-123",
                                                  "url_primary": "TEST-URL-123",
                                                  "url_extension": "TEST-EXTENSION-123",
                                                  "status_code": 200,
                                                  "data": {
                                                      "data-item-1": "DATA-ITEM-1-OK"}})
        
        assert response.status_code == 403
        assert response.json() == {"detail": "Forbidden"}

class TestPostAddUser():

    def test_success(self, client_with_fake_db, fake_db):
        response = client_with_fake_db.post(url='/users/add_user',
                                            headers={"api-key": "TEST-KEY-123"},
                                            json={"email": "TEST-MAIL-456@test3.com",
                                                  "first_name": "FIRST-NAME-456",
                                                  "last_name": "LAST-NAME-456",
                                                  "is_admin": False,
                                                  "can_read": True,
                                                  "can_write": False})
        
        assert response.status_code == 200
        assert response.json()['message'] == "Success"
        assert response.json()['new_user']['email'] == "TEST-MAIL-456@test3.com"
        assert isinstance(response.json()['new_user']['api_key'], str)
        
        # Verifying that a new user got added to the users table.
        check_tb_users = fake_db.query(Users).filter(Users.user_id == 3).first()
        assert check_tb_users.first_name == "FIRST-NAME-456"
        assert check_tb_users.last_name == "LAST-NAME-456"
        assert check_tb_users.is_admin == False
        assert check_tb_users.can_read == True
        assert check_tb_users.can_write == False

        # Verifying that a new key with corresponding user id got added to the apikeys table
        check_tb_apikeys = fake_db.query(ApiKeys).filter(ApiKeys.user_id == 3).first()
        assert check_tb_apikeys.user_id == 3
        assert isinstance(check_tb_apikeys.hashed_api_key, str)
        assert response.json()['new_user']['api_key'] != check_tb_apikeys.hashed_api_key

    def test_api_key_invalid(self, client_with_fake_db):
        response = client_with_fake_db.post(url='/users/add_user',
                                            headers={"api-key": "TEST-KEY-XYZ"},
                                            json={"email": "TEST-MAIL-456@test3.com",
                                                  "first_name": "FIRST-NAME-456",
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
        response = client_with_fake_db.post(url='/users/add_user',
                                            headers={},
                                            json={"first_name": "FIRST-NAME-456",
                                                  "last_name": "LAST-NAME-456",
                                                  "access_type": "Read-only"})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_payload_missing(self, client_with_fake_db):
        response = client_with_fake_db.post(url='/users/add_user',
                                            headers={"api-key": "TEST-KEY-123"})
        
        assert response.status_code == 422

    def test_payload_incomplete(self, client_with_fake_db):
        response = client_with_fake_db.post(url='/users/add_user',
                                            headers={"api-key": "TEST-KEY-123"},
                                            json={"last_name": "LAST-NAME-456",
                                                  "access_type": "Read-only"})
        
        assert response.status_code == 422

    def test_invalid_access_rights(self, client_with_fake_db):
        response = client_with_fake_db.post(url='/users/add_user',
                                            headers={"api-key": "TEST-KEY-789"},
                                            json={"email": "TEST-MAIL-XYZ@test4.com",
                                                  "first_name": "FIRST-NAME-456",
                                                  "last_name": "LAST-NAME-456",
                                                  "is_admin": False,
                                                  "can_read": True,
                                                  "can_write": False,
                                                  "is_active": True})
        
        assert response.status_code == 403
        assert response.json() == {"detail": "Forbidden"}

class TestGetDataSources():

    def test_success(self, client_with_fake_db):
        response = client_with_fake_db.get(url='/data/sources',
                                           headers={"api-key": "TEST-KEY-123"})
        
        assert response.status_code == 200
        assert response.json() == {"message": "Success",
                                   "sources": {
                                       "test_url_1": [
                                           "test_ext_1",
                                           "test_ext_2"],
                                       "test_url_2": [
                                           "test_ext_1"]}}

    def test_api_key_missing(self, client_with_fake_db):
        response = client_with_fake_db.get(url='/data/sources',
                                            headers={})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_api_key_invalid(self, client_with_fake_db):
        response = client_with_fake_db.get(url='/data/sources',
                                           headers={"api-key": "RANDOM-TEST-KEY-123"})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid API key"}

    def test_invalid_access_rights(self, client_with_fake_db):
        response = client_with_fake_db.get(url='/data/sources',
                                           headers={"api-key": "TEST-KEY-789"})
        
        assert response.status_code == 403
        assert response.json() == {"detail": "Forbidden"}

class TestGetUsers():

    def test_success(self, client_with_fake_db):
        response = client_with_fake_db.get(url='/users',
                                           headers={"api-key": "TEST-KEY-123"})
        
        assert response.status_code == 200
        assert response.json() == {"message": "Success",
                                   "users": {
                                       "1": "TEST-MAIL-123@test.com",
                                       "2": "TEST-MAIL-789@test2.com"}}
        
    def test_api_key_missing(self, client_with_fake_db):
        response = client_with_fake_db.get(url='/users',
                                            headers={})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_api_key_invalid(self, client_with_fake_db):
        response = client_with_fake_db.get(url='/users',
                                           headers={"api-key": "RANDOM-TEST-KEY-123"})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid API key"}

    def test_invalid_access_rights(self, client_with_fake_db):
        response = client_with_fake_db.get(url='/users',
                                           headers={"api-key": "TEST-KEY-789"})
        
        assert response.status_code == 403
        assert response.json() == {"detail": "Forbidden"}

class TestGetUser():

    def test_success(self, client_with_fake_db):
        response = client_with_fake_db.get(url='/users/1',
                                           headers={"api-key": "TEST-KEY-123"})
        
        assert response.status_code == 200
        assert response.json() == {"message": "Success",
                                   "user": {
                                       "user_id": 1}}
        
    def test_incorrect_path_parameter(self, client_with_fake_db):
        response = client_with_fake_db.get(url='users/t',
                                           headers={"api-key": "TEST-KEY-123"})
        
        assert response.status_code == 422
        
    def test_api_key_missing(self, client_with_fake_db):
        response = client_with_fake_db.get(url='/users/1',
                                            headers={})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_api_key_invalid(self, client_with_fake_db):
        response = client_with_fake_db.get(url='/users/1',
                                           headers={"api-key": "RANDOM-TEST-KEY-123"})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid API key"}

    def test_invalid_access_rights(self, client_with_fake_db):
        response = client_with_fake_db.get(url='/users/1',
                                           headers={"api-key": "TEST-KEY-789"})
        
        assert response.status_code == 403
        assert response.json() == {"detail": "Forbidden"}

class TestRetireUser():

    def test_success(self, client_with_fake_db, fake_db):
        assert fake_db.query(Users).filter(Users.user_id == 2).first() != None
        response = client_with_fake_db.put(url='/users/retire/2',
                                           headers={"api-key": "TEST-KEY-123"})
        
        assert response.status_code == 200
        assert response.json() == {"message": "Success"}
        assert fake_db.query(Users).filter(Users.user_id == 2).first().is_active == False

    def test_nonexistant_user(self, client_with_fake_db):
        response = client_with_fake_db.put(url='users/retire/7',
                                           headers={"api-key": "TEST-KEY-123"})
        
        assert response.status_code == 404
        assert response.json() == {"detail": "User does not exist"}

    def test_api_key_missing(self, client_with_fake_db):
        response = client_with_fake_db.put(url='/users/retire/2',
                                           headers={})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_api_key_invalid(self, client_with_fake_db):
        response = client_with_fake_db.put(url='/users/retire/2',
                                           headers={"api-key": "RANDOM-TEST-KEY-123"})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid API key"}

    def test_invalid_access_rights(self, client_with_fake_db):
        response = client_with_fake_db.put(url='/users/retire/2',
                                           headers={"api-key": "TEST-KEY-789"})
        
        assert response.status_code == 403
        assert response.json() == {"detail": "Forbidden"}