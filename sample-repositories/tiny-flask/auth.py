"""Simplified demonstration authentication module."""


def verify_user(username: str, password: str) -> bool:
    """Illustrative placeholder; never use hardcoded authentication in production."""
    return bool(username.strip()) and len(password) >= 8
