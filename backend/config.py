import os
import logging

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class Config:
    """
    Base configuration.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_default_secret_key_for_dev')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CORS_ORIGINS = [
        'http://localhost:3000',
    ]

    REDIS_TTL_IN_MIN = 5


class DevelopmentConfig(Config):
    """
    Development configuration.
    """
    DEBUG = True
    # Ensure your PostgreSQL is running and accessible at this URI
    # Format: postgresql://user:password@host:port/database_name
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    # Log all SQL queries in debug mode
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configuration.
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') # Must be set in production
    # SQLALCHEMY_ECHO = False # Disable in production for performance and security

# Dictionary to easily select config class
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig # Default to development
}
