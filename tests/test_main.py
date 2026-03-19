def test_app_starts(client):
    """
    Ensure the FastAPI application starts.
    """
    response = client.get("/docs")
    assert response.status_code == 200

def test_openapi_schema(client):
    """
    Ensure OpenAPI schema is available.
    """
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "paths" in response.json()

def test_endpoint_status(client):
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    assert response.json() == {
        "message": "OK"
    }

def test_endpoint_root(client):
    response = client.get("/api/v1/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello There",
        "application_name": "DIA: Data Ingest API",
        "contact": {
            "maintainer": "Toasted-ctrl"
        },
        "version": "0.1.2"
    }