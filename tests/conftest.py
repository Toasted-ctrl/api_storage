# Conftest is special, pytest will pre-load conftest fixtures.
# The file must always be known as conftest.py

import pytest

from sqlalchemy import create_engine

# Staticpool to be used so we don't create new tables on new connections, but rather just use one connection.
# Staticpool only to be used in tests, NOT prod.

from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app, get_database
from app.database import base, ApiKeys, Users

test_in_memory_db_url = "sqlite:///:memory:" # Will create an in-memory db
test_engine = create_engine(test_in_memory_db_url,
                            connect_args={"check_same_thread": False},
                            poolclass=StaticPool)

# autocommit=False will prevent automatic commit.
# We'd need to call .commit() explicitly to save the transaction.
# autoflush=False will prevent sending of data to db when using .add()
# autoflush=True would allow us to rollback a change if needed.
# Using .commit() cannot be rolled back, the change is permanent.

test_session_local = sessionmaker(autocommit=False,
                                  autoflush=False,
                                  bind=test_engine)

@pytest.fixture(scope="function")
def fake_db():

    base.metadata.create_all(bind=test_engine)

    db_session = test_session_local()

    # Adding user 1 api key and access rights

    new_api_key_user_1 = ApiKeys(api_key="TEST-KEY-123",
                          user_id=1)
    
    db_session.add(new_api_key_user_1)
    db_session.commit()

    new_permissions_user_1 = Users(email="TEST-MAIL-123@test.com",
                                   first_name="FIRST-NAME-123",
                                   last_name="LAST-NAME-123",
                                   is_admin=True,
                                   can_read=True,
                                   can_write=True)
    
    db_session.add(new_permissions_user_1)
    db_session.commit()

    # Adding user 2 api key and access rights

    new_api_key_user_2 = ApiKeys(api_key="TEST-KEY-789",
                                 user_id=2)
    
    db_session.add(new_api_key_user_2)
    db_session.commit()

    new_permissions_user_2 = Users(email="TEST-MAIL-789@test2.com",
                                   first_name="FIRST-NAME-789",
                                   last_name="LAST-NAME-789",
                                   is_admin=False,
                                   can_read=False,
                                   can_write=False)
    
    db_session.add(new_permissions_user_2)
    db_session.commit()

    yield db_session

    db_session.close()

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