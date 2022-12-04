import pytest
from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

from sage.core.dependencies.security import REQUIRE_ADMIN, require_admin


def test_dependency_is_require_admin() -> None:
    """Test the exported Depends uses the same method we are testing."""
    # in the event security is refactored, the dependency may have a different internal dependency
    assert REQUIRE_ADMIN.dependency is require_admin


class TestRequireAdmin:
    """Test the require_admin method."""

    @pytest.mark.parametrize(
        ("username", "password"),
        [
            ("anything", "invalid"),
            ("admin", "wrong pass"),
            ("wrong user", "password"),
        ],
    )
    def test_invalid(self, username: str, password: str) -> None:
        """Test invalid credentials are rejected."""
        creds = HTTPBasicCredentials(username=username, password=password)

        with pytest.raises(HTTPException) as pye:
            require_admin(creds)

        err = pye.value
        assert err.status_code == 401
        assert err.detail == "Incorrect username or password"

    def test_valid_password(self) -> None:
        """Test the valid username and password are accepted."""
        # these are set in pyproject.toml under pytest.ini_options.env
        creds = HTTPBasicCredentials(username="admin", password="password")  # noqa: S106
        result = require_admin(creds)

        assert result is True
