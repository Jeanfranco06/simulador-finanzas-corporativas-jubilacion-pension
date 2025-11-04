from flask import Flask
from config import config

def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
