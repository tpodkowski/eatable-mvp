import os


class Config:
    """Set Flask configuration vars from .env file."""

    # General
    # TESTING = os.environ["TESTING"]
    FLASK_DEBUG = os.environ["FLASK_DEBUG"]

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
