# Conftest is special, pytest will pre-load conftest fixtures.
# The file must always be known as conftest.py

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app, get_database
from app.database import base, Permissions

test_db_url = "sqlite:///:memory:"
test_engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
test_session_local = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="function")
def fake_db():

    base.metadata.create_all(bind=test_engine)

    connection = test_engine.connect()
    transaction = connection.begin()
    db_session = test_session_local(bind=connection)

    new_permissions = Permissions(first_name='fn-123',
                                  last_name='ln-123',
                                  api_key='test-key-123',
                                  is_admin=True)
    
    db_session.add(new_permissions)
    db_session.flush()

    yield db_session

    db_session.close()
    transaction.rollback()
    connection.close()

    base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def client_with_fake_db(fake_db):
    def override_db():
        try:
            yield fake_db
        finally:
            pass

    app.dependency_overrides[get_database] = override_db

    try:
        with TestClient(app) as client:
            yield client

    finally:
        app.dependency_overrides.clear()