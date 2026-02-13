import pytest

from app.main import app
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

client = TestClient(app=app)

class TestReadRoot:

    def test_read_root(self):
        response = client.get(url='/')
        
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

class TestPostSingleEntry:

    def test_missing_api_key(self):
        response = client.post(url='/post_single')
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_incorrect_api_key(self): # TODO: Rewrite test with patch for database connection 
        response = client.post(url='/post_single',
                               headers={"API_KEY": "122"},
                               json={"table": "test_table",
                                     "url": "test_url",
                                     "data": {
                                         "data_1": "data_1_ok"
                                     }})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}

    def test_database_server_error(self):
        response = client.post(url='/post_single',
                               headers={"API_KEY": "122"},
                               json={"table": "test_table",
                                     "url": "test_url",
                                     "data": {
                                         "data_1": "data_1_ok"
                                     }})
        
        assert response.status_code == 500
        assert response.json() == {"detail": "Internal Server Error"}

    def test_missing_data(self):
        response = client.post(url='/post_single',
                               headers ={"API_KEY": "123"})
        
        assert response.status_code == 422