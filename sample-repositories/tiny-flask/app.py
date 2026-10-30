"""Tiny illustrative web application for Repo Séance demos."""
from auth import verify_user

APP_NAME = "Tiny Flask Demo"


def create_app():
    """Create and configure the illustrative application."""
    return {"name": APP_NAME, "auth_enabled": True}


def login(username: str, password: str):
    """Delegate login verification to the auth module."""
    return verify_user(username, password)


if __name__ == "__main__":
    print(create_app())
