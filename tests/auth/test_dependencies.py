import pytest

from fastapi import HTTPException

from auth.dependencies import get_user, cache
from auth.hashing import hash_sha256

class TestGetUser:

    @pytest.mark.asyncio
    async def test_success(self, mocker):
        db = mocker.Mock()

        user = mocker.Mock()
        user.is_active = True

        db.query().filter().scalar.return_value = 1
        db.query().filter().first.return_value = user

        result = await get_user(db=db, api_key="test")

        assert result == user

    @pytest.mark.asyncio
    async def test_api_key_missing(self):
        with pytest.raises(HTTPException) as exc:
            await get_user(db=None, api_key=None)

        assert exc.value.status_code == 401
        assert exc.value.detail == "Missing API key"

    @pytest.mark.asyncio
    async def test_api_key_invalid(self, mocker):
        db = mocker.Mock()

        # Mock query chain
        db.query().filter().scalar.return_value = None

        with pytest.raises(HTTPException) as exc:
            await get_user(db=db, api_key="test")

        assert exc.value.status_code == 403
        assert exc.value.detail == "Invalid API key"

    @pytest.mark.asyncio
    async def test_user_not_found(self, mocker):
        db = mocker.Mock()

        db.query().filter().scalar.return_value = 1
        db.query().filter().first.return_value = None

        with pytest.raises(HTTPException) as exc:
            await get_user(db=db, api_key="test")

        assert exc.value.status_code == 403
        assert exc.value.detail == "User not found"

    @pytest.mark.asyncio
    async def test_inactive_user(self, mocker):
        db = mocker.Mock()

        user = mocker.Mock()
        user.is_active = False

        db.query().filter().scalar.return_value = 1
        db.query().filter().first.return_value = user

        with pytest.raises(HTTPException) as exc:
            await get_user(db=db, api_key="test")

        assert exc.value.status_code == 403
        assert exc.value.detail == "User inactive"

    @pytest.mark.asyncio
    async def test_cache_hit(self, mocker):
        db = mocker.Mock()

        api_key = "test"
        hashed = hash_sha256(api_key)

        user = mocker.Mock()
        cache[hashed] = user

        result = await get_user(db=db, api_key=api_key)

        assert result == user
        db.query.assert_not_called()