import pytest

from database.schema import Users, ApiKeys, Ingest
from sqlalchemy.exc import IntegrityError

class TestUsers:

    def test_create_user(self, session):

        user = Users(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            is_admin=False,
            can_read=True,
            can_write=False,
            is_active=True,
        )

        session.add(user)
        session.commit()

        assert user.user_id is not None

    def test_user_email_unique(self, session):

        user1 = Users(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            is_admin=False,
            can_read=True,
            can_write=False,
            is_active=True,
        )

        user2 = Users(
            email="test@example.com",
            first_name="Jane",
            last_name="Doe",
            is_admin=False,
            can_read=True,
            can_write=False,
            is_active=True,
        )

        session.add(user1)
        session.commit()

        session.add(user2)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_user_email_not_null(self, session):

        user = Users(
            email=None,
            first_name="John",
            last_name="Doe",
            is_admin=False,
            can_read=True,
            can_write=False,
            is_active=True,
        )

        session.add(user)

        with pytest.raises(Exception):
            session.commit()

class TestApiKeys:

    def test_create_api_key(self, session):

        key = ApiKeys(
            hashed_api_key="abc123",
            user_id=1,
            is_valid=True,
        )

        session.add(key)
        session.commit()

        assert key.hashed_api_key == "abc123"

    def test_api_key_primary_key_unique(self, session):

        key1 = ApiKeys(hashed_api_key="abc123", user_id=1, is_valid=True)
        key2 = ApiKeys(hashed_api_key="abc123", user_id=2, is_valid=True)

        session.add(key1)
        session.commit()

        new_session = session.__class__()

        new_session.add(key2)

        with pytest.raises(Exception):
            new_session.commit()

class TestIngest:

    def test_create_ingest(self, session):

        ingest = Ingest(
            base_url="https://example.com",
            url_ext="/data",
            params={"q": "test"},
            status_code=200,
            data={"result": "ok"},
        )

        session.add(ingest)
        session.commit()

        assert ingest.item_id is not None

    def test_ingest_json_fields(self, session):

        payload = {"key": "value"}

        ingest = Ingest(
            base_url="https://example.com",
            params=payload,
            data=payload,
        )

        session.add(ingest)
        session.commit()

        saved = session.query(Ingest).first()

        assert saved.params == payload
        assert saved.data == payload