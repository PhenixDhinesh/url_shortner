import os
import logging

from flask import Flask
from flask_cors import CORS

from config import config_by_name
from extensions import db, migrate

from api import api_bp

def create_app(config_name=None):
    """
    Create a Flask app with the specified configuration.
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # add CORS
    app.logger.info("CORS resources: %s", app.config['CORS_ORIGINS'])
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)

    # Register blueprints
    app.register_blueprint(api_bp)

    # Simple logging configuration
    logging.basicConfig(
        level=app.config.get('LOG_LEVEL', logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    app.logger.info("App created with `%s` configuration.", config_name)
    app.logger.info("Base URL: %s", app.config['BASE_URL'])

    return app

# Command to create database tables
@api_bp.cli.command('create-db')
def create_db_command():
    """
    Create database tables.
    """
    db.create_all()
    print("Database tables created.")

if __name__ == '__main__':
    # When running directly, default to development config
    server = create_app('development')
    server.run(host='0.0.0.0', port=5000)