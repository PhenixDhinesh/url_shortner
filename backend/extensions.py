from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_extensions(app):
    """
    Initialize extensions
    """
    redis_helper.init_app(app.redis)

class RedisHelper:
    """
    Redis helper class
    """
    def __init__(self, redis = None):
        self.redis = redis

    def init_app(self, redis):
        """
        Initialize Redis helper
        """
        self.redis = redis

    def get_value(self, key):
        """
        Get value from Redis
        """
        return self.redis.get(key)

    def set_value(self, key, value, ttl):
        """
        Set value in Redis

        Args:
            key (str): The key to set
            value (str): The value to set
            ttl (int): The time to live in minutes
        """
        return self.redis.set(key, value, ex=ttl * 60)

    def get_string(self, key):
        """
        Get string from Redis
        """
        value = self.get_value(key)

        if value is None:
            return None

        return value.decode('utf-8')

redis_helper = RedisHelper()