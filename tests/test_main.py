import pytest

from app.database import base
from app.main import app, db_con
from datetime import datetime
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

test_in_memory_db_url = "sqlite:///:memory:"
test_engine = create_engine(test_in_memory_db_url, connect_args={"check_same_thread": False})
test_session_local = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

client = TestClient(app=app)

class TestRoot:

    def test_success(self):
        response = client.get(url='/')
        assert response.status_code == 200
        assert response.json() == {"message": "Hello There",
                                   "version": app.version,
                                   "contact": app.contact}

class TestPostSingle:

    def test_success(self):
        pass

    def test_api_key_invalid(self):
        pass

    def test_api_key_server_error(self):
        pass

    def test_api_key_missing(self):
        pass

    def test_payload_missing(self):
        pass

    def test_payload_incomplete(self):
        pass

class TestAddUser():

    def test_success(self):
        pass

    def test_api_key_invalid(self):
        pass

    def test_api_key_server_error(self):
        pass

    def test_api_key_missing(self):
        pass

    def test_payload_missing(self):
        pass

    def test_payload_incomplete(self):
        pass