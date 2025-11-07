"""
Database models for the financial simulator with user profiles and gamification
"""
import pandas as pd
import numpy as np
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()

class User(db.Model):
    """User model for anonymous profiles using UUID"""
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Profile information (optional for anonymous users)
    display_name = db.Column(db.String(50), nullable=True)
    preferences = db.Column(db.JSON, default=dict)

    # Statistics
    total_simulations = db.Column(db.Integer, default=0)
    total_templates_created = db.Column(db.Integer, default=0)
    total_achievements = db.Column(db.Integer, default=0)

    # Relationships
    simulations = db.relationship('Simulation', backref='user', lazy=True, cascade='all, delete-orphan')
    achievements = db.relationship('UserAchievement', backref='user', lazy=True, cascade='all, delete-orphan')
    templates = db.relationship('Template', backref='creator', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_active': self.last_active.isoformat() if self.last_active else None,
            'display_name': self.display_name,
            'total_simulations': self.total_simulations,
            'total_templates_created': self.total_templates_created,
            'total_achievements': self.total_achievements
        }

class Simulation(db.Model):
    """Simulation model to store user calculations"""
    __tablename__ = 'simulations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    module_type = db.Column(db.String(20), nullable=False)  # 'cartera', 'jubilacion', 'bonos', etc.

    # Simulation data (stored as JSON)
    input_data = db.Column(db.JSON, nullable=False)
    results_data = db.Column(db.JSON, nullable=False)

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_favorite = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)

    # Relationships
    shares = db.relationship('SimulationShare', backref='simulation', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Simulation {self.id}: {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'module_type': self.module_type,
            'input_data': self.input_data,
            'results_data': self.results_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_favorite': self.is_favorite,
            'is_public': self.is_public
        }

class Template(db.Model):
    """Template model for sharing simulation configurations"""
    __tablename__ = 'templates'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    module_type = db.Column(db.String(20), nullable=False)

    # Template data
    template_data = db.Column(db.JSON, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    tags = db.Column(db.JSON, default=list)  # List of tags

    # Community features
    is_public = db.Column(db.Boolean, default=True)
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    downloads = db.Column(db.Integer, default=0)

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    votes = db.relationship('TemplateVote', backref='template', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Template {self.id}: {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'creator_id': self.creator_id,
            'name': self.name,
            'description': self.description,
            'module_type': self.module_type,
            'template_data': self.template_data,
            'category': self.category,
            'tags': self.tags,
            'is_public': self.is_public,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'views': self.views,
            'downloads': self.downloads,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Achievement(db.Model):
    """Achievement definitions"""
    __tablename__ = 'achievements'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(50), nullable=False)  # 'simulations', 'templates', 'social', etc.

    # Achievement criteria
    criteria_type = db.Column(db.String(50), nullable=False)  # 'count', 'value', 'streak', etc.
    criteria_value = db.Column(db.Integer, nullable=False)
    criteria_target = db.Column(db.String(50), nullable=False)  # What to track: 'simulations_created', 'templates_shared', etc.

    # Rarity and points
    rarity = db.Column(db.String(20), default='common')  # 'common', 'rare', 'epic', 'legendary'
    points = db.Column(db.Integer, default=10)

    # Metadata
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user_achievements = db.relationship('UserAchievement', backref='achievement', lazy=True)

    def __repr__(self):
        return f'<Achievement {self.id}: {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'category': self.category,
            'criteria_type': self.criteria_type,
            'criteria_value': self.criteria_value,
            'criteria_target': self.criteria_target,
            'rarity': self.rarity,
            'points': self.points,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class UserAchievement(db.Model):
    """User achievements progress and completion"""
    __tablename__ = 'user_achievements'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.id'), nullable=False)

    # Progress tracking
    current_value = db.Column(db.Integer, default=0)
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    __table_args__ = (db.UniqueConstraint('user_id', 'achievement_id', name='unique_user_achievement'),)

    def __repr__(self):
        return f'<UserAchievement {self.user_id}:{self.achievement_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'achievement_id': self.achievement_id,
            'current_value': self.current_value,
            'is_completed': self.is_completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class TemplateVote(db.Model):
    """Template voting system"""
    __tablename__ = 'template_votes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'), nullable=False)
    vote_type = db.Column(db.String(10), nullable=False)  # 'upvote', 'downvote'

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    __table_args__ = (db.UniqueConstraint('user_id', 'template_id', name='unique_user_template_vote'),)

    def __repr__(self):
        return f'<TemplateVote {self.user_id}:{self.template_id}:{self.vote_type}>'

class SimulationShare(db.Model):
    """Simulation sharing for social features"""
    __tablename__ = 'simulation_shares'

    id = db.Column(db.Integer, primary_key=True)
    simulation_id = db.Column(db.Integer, db.ForeignKey('simulations.id'), nullable=False)
    shared_by_user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    share_type = db.Column(db.String(20), default='public')  # 'public', 'private', 'community'

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<SimulationShare {self.id}>'

# Utility functions for user management
def get_or_create_user(user_id=None):
    """Get existing user or create new anonymous user"""
    if user_id:
        user = User.query.get(user_id)
        if user:
            user.last_active = datetime.utcnow()
            db.session.commit()
            return user

    # Create new anonymous user
    user = User()
    db.session.add(user)
    db.session.commit()
    return user

def update_user_stats(user_id):
    """Update user statistics"""
    user = User.query.get(user_id)
    if user:
        user.total_simulations = Simulation.query.filter_by(user_id=user_id).count()
        user.total_templates_created = Template.query.filter_by(creator_id=user_id).count()
        user.total_achievements = UserAchievement.query.filter_by(user_id=user_id, is_completed=True).count()
        db.session.commit()

def check_achievements(user_id):
    """Check and award achievements for user"""
    user = User.query.get(user_id)
    if not user:
        return []

    awarded_achievements = []

    # Get all active achievements
    achievements = Achievement.query.filter_by(is_active=True).all()

    for achievement in achievements:
        # Check if user already has this achievement
        user_achievement = UserAchievement.query.filter_by(
            user_id=user_id,
            achievement_id=achievement.id
        ).first()

        if not user_achievement:
            user_achievement = UserAchievement(
                user_id=user_id,
                achievement_id=achievement.id
            )
            db.session.add(user_achievement)

        # Calculate current value based on criteria target
        current_value = 0
        if achievement.criteria_target == 'simulations_created':
            current_value = Simulation.query.filter_by(user_id=user_id).count()
        elif achievement.criteria_target == 'templates_created':
            current_value = Template.query.filter_by(creator_id=user_id).count()
        elif achievement.criteria_target == 'templates_shared':
            current_value = Template.query.filter_by(creator_id=user_id, is_public=True).count()
        elif achievement.criteria_target == 'achievements_earned':
            current_value = UserAchievement.query.filter_by(user_id=user_id, is_completed=True).count()

        # Update progress
        user_achievement.current_value = current_value

        # Check if achievement is completed
        if not user_achievement.is_completed and current_value >= achievement.criteria_value:
            user_achievement.is_completed = True
            user_achievement.completed_at = datetime.utcnow()
            awarded_achievements.append(achievement)

    db.session.commit()
