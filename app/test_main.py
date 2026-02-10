from fastapi.testclient import TestClient
from main import app

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

    def test_incorrect_api_key(self):
        response = client.post(url='/post_single',
                               headers={"API_KEY":"122"},
                               json={"database": "test_database",
                                     "table": "test_table",
                                     "url": "test_url",
                                     "data": {
                                         "data_1": "data_1_ok"
                                     }})
        
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}