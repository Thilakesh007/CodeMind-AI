"""Authentication: user store and credential/role verification.

Moved verbatim from the USERS dict and inline login checks in app.py.
"""
from typing import Optional, TypedDict


class UserRecord(TypedDict):
    password: str
    role: str


# Static demo user store, unchanged from the original app.py.
USERS: dict[str, UserRecord] = {
    "student1": {"password": "student123", "role": "student"},
    "faculty1": {"password": "faculty123", "role": "faculty"},
}


def authenticate(username: str, password: str, role: str) -> bool:
    """Validate username/password/role against the user store.

    Equivalent to the original inline check:
        user = USERS.get(username)
        if user and user["password"] == password and user["role"] == role: ...
    """
    user: Optional[UserRecord] = USERS.get(username)
    return bool(user and user["password"] == password and user["role"] == role)
