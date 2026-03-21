import pytest

from fastapi import HTTPException

from auth.permissions import require_permission

class MockUser:
    def __init__(self, is_admin=False, can_read=False, can_write=False):
        self.is_admin = is_admin
        self.can_read = can_read
        self.can_write = can_write

class TestRequirePermission:

    @pytest.mark.asyncio
    async def test_success_admin(self):
        user = MockUser(is_admin=True)
        dependency = require_permission(admin=True)
        result = await dependency(user)
        assert result == user

    @pytest.mark.asyncio
    async def test_success_read(self):
        user = MockUser(can_read=True)
        dependency = require_permission(read=True)
        result = await dependency(user)
        assert result == user

    @pytest.mark.asyncio
    async def test_success_write(self):
        user = MockUser(can_write=True)
        dependency = require_permission(write=True)
        result = await dependency(user)
        assert result == user

    @pytest.mark.asyncio
    async def test_success_multiple_permissions(self):
        user = MockUser(is_admin=True, can_read=True, can_write=True)
        dependency = require_permission(admin=True, read=True, write=True)
        result = await dependency(user)
        assert result == user

    @pytest.mark.asyncio
    async def test_admin_permission_failure(self):
        user = MockUser(is_admin=False)
        dependency = require_permission(admin=True)

        with pytest.raises(HTTPException) as exc:
            await dependency(user)

        assert exc.value.status_code == 403
        assert exc.value.detail == "Admin permission required"

    @pytest.mark.asyncio
    async def test_read_permission_failure(self):
        user = MockUser(can_read=False)
        dependency = require_permission(read=True)

        with pytest.raises(HTTPException) as exc:
            await dependency(user)

        assert exc.value.status_code == 403
        assert exc.value.detail == "Read permission required"

    @pytest.mark.asyncio
    async def test_write_permission_failure(self):
        user = MockUser(can_write=False)
        dependency = require_permission(write=True)

        with pytest.raises(HTTPException) as exc:
            await dependency(user)

        assert exc.value.status_code == 403
        assert exc.value.detail == "Write permission required"

    @pytest.mark.asyncio
    async def test_multiple_permissions_one_fails(self):
        user = MockUser(is_admin=True, can_read=False, can_write=True)
        dependency = require_permission(admin=True, read=True, write=True)

        with pytest.raises(HTTPException) as exc:
            await dependency(user)

        assert exc.value.status_code == 403
        assert exc.value.detail == "Read permission required"