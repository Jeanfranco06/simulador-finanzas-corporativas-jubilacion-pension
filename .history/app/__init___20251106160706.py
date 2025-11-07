import os
from flask import Flask
from config import config

def create_app(config_name=None):
    """Application factory function"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV') or 'default'

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config.get(config_name, config['default']))

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
