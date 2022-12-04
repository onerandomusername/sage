import secrets
from typing import Literal

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sage.settings import get_settings


__all__ = ("REQUIRE_ADMIN",)


auth_scheme = HTTPBasic()


ADMIN_USER = get_settings().admin


def require_admin(
    creds: HTTPBasicCredentials = Depends(auth_scheme),  # noqa: B008
) -> Literal[True]:
    """Require authorisation matching the admin user provided in settings."""
    current_username_bytes = creds.username.encode("utf8")

    is_valid_user = secrets.compare_digest(current_username_bytes, ADMIN_USER.username)
    # get the user
    ...
    current_password_bytes = creds.password.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, ADMIN_USER.password.get_secret_value()
    )
    if not (is_valid_user and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True


REQUIRE_ADMIN = Depends(require_admin)
