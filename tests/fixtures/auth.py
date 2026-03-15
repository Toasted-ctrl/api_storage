import pytest

from fastapi import HTTPException
from types import SimpleNamespace

import auth.dependencies

@pytest.fixture
def admin_user():
    return SimpleNamespace(
        is_admin=True,
        can_write=True,
        can_read=True
    )

@pytest.fixture
def read_only_user():
    return SimpleNamespace(
        is_admin=False,
        can_write=False,
        can_read=True
    )

@pytest.fixture
def override_user(app):
    """
    Allows tests to override the authenticated user dynamically.
    """

    def _override(user):
        def fake_user():
            return user

        app.dependency_overrides[auth.dependencies.get_user] = fake_user

    yield _override
    app.dependency_overrides.pop(auth.dependencies.get_user, None)

@pytest.fixture
def override_auth_error(app):
    def _override(status_code=403, detail="Forbidden"):
        def fake_user():
            raise HTTPException(status_code=status_code, detail=detail)

        app.dependency_overrides[auth.dependencies.get_user] = fake_user

    yield _override

    app.dependency_overrides.pop(auth.dependencies.get_user, None)