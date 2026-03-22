import pytest
from unittest.mock import MagicMock, patch

from services.user_service import UserService

def test_get_users():
    mock_session = MagicMock()
    mock_query = mock_session.query.return_value
    mock_query.distinct.return_value.all.return_value = [(1, "test@example.com")]

    service = UserService(mock_session)

    result = service.get_users()

    assert result == [(1, "test@example.com")]
    mock_session.query.assert_called_once()

class Test_CheckKeyUnique:

    def test_check_key_unique_true(self):
        mock_session = MagicMock()
        mock_query = mock_session.query.return_value
        mock_query.filter.return_value.scalar.return_value = None

        service = UserService(mock_session)

        assert service._check_key_unique("hashed") is True

    def test_check_key_unique_false(self):
        mock_session = MagicMock()
        mock_query = mock_session.query.return_value
        mock_query.filter.return_value.scalar.return_value = "existing_key"

        service = UserService(mock_session)

        assert service._check_key_unique("hashed") is False

class Test_CreateKeys:

    @patch("services.user_service.generate_keys") # Overriding the imported auth.generate_key.generate_keys function.
    def test_create_keys_unique(self, mock_generate_keys):
        mock_session = MagicMock()

        service = UserService(mock_session)
        service._check_key_unique = MagicMock(return_value=True)

        mock_generate_keys.return_value = ("raw", "hashed")

        result = service._create_keys()

        assert result == ("raw", "hashed")

    @patch("services.user_service.generate_keys") # Overriding the imported auth.generate_key.generate_keys function.
    def test_create_keys_recursion(self, mock_generate_keys):
        mock_session = MagicMock()
        service = UserService(mock_session)

        # First call: not unique, second: unique
        service._check_key_unique = MagicMock(side_effect=[False, True])

        mock_generate_keys.side_effect = [
            ("raw1", "hash1"),
            ("raw2", "hash2"),
        ]

        result = service._create_keys()

        assert result == ("raw2", "hash2")
        assert mock_generate_keys.call_count == 2

def test_get_user_found():
    mock_session = MagicMock()
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = {"user_id": 1}

    service = UserService(mock_session)

    result = service.get_user(1)

    assert result == {"user_id": 1}

class TestPostUser:

    @patch("services.user_service.generate_keys") # Overriding the imported auth.generate_key.generate_keys function.
    def test_post_user_success(self, mock_generate_keys):
        mock_session = MagicMock()

        mock_generate_keys.return_value = ("raw_key", "hashed_key")

        service = UserService(mock_session)

        service._check_key_unique = MagicMock(return_value=True)

        data = {"email": "test@example.com"}

        result = service.post_user(data)

        assert result is not None
        user, key = result

        assert key == "raw_key"
        assert mock_session.add.call_count == 2
        assert mock_session.commit.call_count == 2

    @patch("services.user_service.generate_keys") # Overriding the imported auth.generate_key.generate_keys function.
    def test_post_user_failure(self, mock_generate_keys):
        mock_session = MagicMock()

        mock_generate_keys.return_value = ("raw_key", "hashed_key")

        # Force failure on commit
        mock_session.commit.side_effect = Exception("DB error")

        service = UserService(mock_session)
        service._check_key_unique = MagicMock(return_value=True)

        result = service.post_user({"email": "fail@test.com"})

        assert result is None
        mock_session.rollback.assert_called()

class TestUpdateUser:

    def test_update_user_success(self):
        mock_session = MagicMock()

        user = MagicMock()
        service = UserService(mock_session)
        service.get_user = MagicMock(return_value=user)

        result = service.update_user({"email": "new@test.com"}, 1)

        assert result == user
        assert user.email == "new@test.com"
        mock_session.commit.assert_called_once()

    def test_update_user_not_found(self):
        mock_session = MagicMock()

        service = UserService(mock_session)
        service.get_user = MagicMock(return_value=None)

        result = service.update_user({}, 1)

        assert result is None

    def test_update_user_commit_fail(self):
        mock_session = MagicMock()
        mock_session.commit.side_effect = Exception("fail")

        user = MagicMock()

        service = UserService(mock_session)
        service.get_user = MagicMock(return_value=user)

        result = service.update_user({"email": "x"}, 1)

        assert result is None
        mock_session.rollback.assert_called()