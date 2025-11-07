import os
from flask import Flask
from config import config
from flask_migrate import Migrate

def create_app(config_name=None):
    """Application factory function"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV') or 'default'

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config.get(config_name, config['default']))

    # Initialize extensions
    from .models import db
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    # Create database tables and seed initial data
    with app.app_context():
        db.create_all()
        seed_achievements()

    return app

def seed_achievements():
    """Seed initial achievements into the database"""
    from .models import Achievement, db

    # Check if achievements already exist
    if Achievement.query.count() > 0:
        return

    achievements_data = [
        # Simulation achievements
        {
            'name': 'Primer Cálculo',
            'description': 'Realiza tu primera simulación financiera',
            'icon': 'fa-calculator',
            'category': 'simulations',
            'criteria_type': 'count',
            'criteria_value': 1,
            'criteria_target': 'simulations_created',
            'rarity': 'common',
            'points': 10
        },
        {
            'name': 'Analista Experto',
            'description': 'Crea 10 simulaciones diferentes',
            'icon': 'fa-chart-line',
            'category': 'simulations',
            'criteria_type': 'count',
            'criteria_value': 10,
            'criteria_target': 'simulations_created',
            'rarity': 'rare',
            'points': 25
        },
        {
            'name': 'Planificador Maestro',
            'description': 'Crea 50 simulaciones para planificar tu futuro financiero',
            'icon': 'fa-crown',
            'category': 'simulations',
            'criteria_type': 'count',
            'criteria_value': 50,
            'criteria_target': 'simulations_created',
            'rarity': 'epic',
            'points': 50
        },

        # Social achievements
        {
            'name': 'Comparador Social',
            'description': 'Revisa las estadísticas de comparación social',
            'icon': 'fa-users',
            'category': 'social',
            'criteria_type': 'count',
            'criteria_value': 1,
            'criteria_target': 'social_comparison_viewed',
            'rarity': 'common',
            'points': 15
        },

        # Achievement collector
        {
            'name': 'Coleccionista de Logros',
            'description': 'Obtén 3 logros diferentes',
            'icon': 'fa-trophy',
            'category': 'achievements',
            'criteria_type': 'count',
            'criteria_value': 3,
            'criteria_target': 'achievements_earned',
            'rarity': 'rare',
            'points': 40
        },
        {
            'name': 'Maestro de Finanzas',
            'description': 'Obtén todos los logros disponibles',
            'icon': 'fa-star',
            'category': 'achievements',
            'criteria_type': 'count',
            'criteria_value': 5,  # Total achievements
            'criteria_target': 'achievements_earned',
            'rarity': 'legendary',
            'points': 100
        }
    ]

    for achievement_data in achievements_data:
        achievement = Achievement(**achievement_data)
        db.session.add(achievement)

    db.session.commit()
