import os

class Config:
    """Set Flask configuration vars from .env file."""

    # General
   #TESTING = os.environ["TESTING"]
    FLASK_DEBUG = os.environ["FLASK_DEBUG"]

    # Database
    SQLALCHEMY_DATABASE_URI = 'postgres://gvlkwgxs:E4envhZd5EMvB5KSHbPV9n3oeCoRHgpj@hansken.db.elephantsql.com:5432/gvlkwgxs'
