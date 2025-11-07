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
    """User model for anonymous and registered profiles"""
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Authentication (optional for registered users)
    email = db.Column(db.String(120), nullable=True)
    password_hash = db.Column(db.String(128), nullable=True)
    display_name = db.Column(db.String(50), nullable=True)

    # Profile settings
    is_registered = db.Column(db.Boolean, default=False)
    preferences = db.Column(db.JSON, default=dict)

    # Statistics
    total_simulations = db.Column(db.Integer, default=0)
    total_templates_created = db.Column(db.Integer, default=0)
    total_achievements = db.Column(db.Integer, default=0)

    # Relationships
    simulations = db.relationship('Simulation', backref='user', lazy=True, cascade='all, delete-orphan')
    achievements = db.relationship('UserAchievement', backref='user', lazy=True, cascade='all, delete-orphan')
    templates = db.relationship('Template', backref='creator', lazy=True, cascade='all, delete-orphan')

    __table_args__ = (
        db.UniqueConstraint('email', name='unique_user_email'),
    )

    # Flask-Login properties
    @property
    def is_authenticated(self):
        return self.is_registered

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return not self.is_registered

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        """Set password hash for registered users"""
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password for registered users"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

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
        elif achievement.criteria_target == 'social_comparison_viewed':
            # This would be tracked separately, for now just check if user exists
            current_value = 1 if user_id else 0
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
    return awarded_achievements

def calcular_cartera(datos):
    """
    Calculate portfolio growth (Módulo A)

    Args:
        datos: Dictionary with form data

    Returns:
        Dictionary with calculation results
    """
    # Extract data
    edad_actual = datos['edad_actual']
    monto_inicial = datos['monto_inicial']
    aporte_periodico = datos['aporte_periodico'] or 0
    frecuencia = datos['frecuencia']
    tea = datos['tea'] / 100  # Convert to decimal

    # Calculate years
    if datos['tipo_plazo'] == 'años':
        años = datos['años']
        if años is None:
            raise ValueError("Debe especificar el número de años cuando el tipo de plazo es 'años'")
        edad_retiro = edad_actual + años
    else:
        edad_retiro = datos['edad_retiro']
        if edad_retiro is None:
            raise ValueError("Debe especificar la edad de retiro cuando el tipo de plazo es 'edad'")
        años = edad_retiro - edad_actual

    # Calculate periods per year
    periodos_por_año = {
        'Mensual': 12,
        'Bimestral': 6,
        'Trimestral': 4,
        'Cuatrimestral': 3,
        'Semestral': 2,
        'Anual': 1
    }

    periodos_año = periodos_por_año[frecuencia]
    total_periodos = años * periodos_año

    # Calculate periodic rate
    tasa_periodica = (1 + tea) ** (1 / periodos_año) - 1

    # Initialize variables
    saldo = monto_inicial
    aportes_acumulados = monto_inicial
    resultados = []

    # Add period 0 (initial balance)
    resultados.append({
        'Periodo': 0,
        'Saldo Inicial': 0,
        'Aportes': monto_inicial,
        'Interés': 0,
        'Saldo Final': monto_inicial,
        'Aportes Acumulados': monto_inicial
    })

    # Calculate growth period by period (starting from period 1)
    for periodo in range(1, total_periodos + 1):
        # Add periodic contribution
        saldo_anterior = saldo
        saldo += aporte_periodico
        aportes_acumulados += aporte_periodico

        # Apply interest
        interes = saldo * tasa_periodica
        saldo += interes

        # Record results
        resultados.append({
            'Periodo': periodo,
            'Saldo Inicial': saldo_anterior,
            'Aportes': aporte_periodico,
            'Interés': interes,
            'Saldo Final': saldo,
            'Aportes Acumulados': aportes_acumulados
        })

    # Create DataFrame
    df = pd.DataFrame(resultados)

    # Calculate summary
    capital_final = df['Saldo Final'].iloc[-1]
    aportes_totales = df['Aportes Acumulados'].iloc[-1]
    ganancia_bruta = capital_final - aportes_totales
    rentabilidad = (ganancia_bruta / aportes_totales * 100) if aportes_totales > 0 else 0

    # Calculate equivalent TEA (periodic rate for the selected frequency)
    # This shows the periodic rate that gets applied according to contribution frequency
    tea_equivalente = tasa_periodica

    return {
        'dataframe': df,
        'resumen': {
            'capital_final': capital_final,
            'aportes_totales': aportes_totales,
            'ganancia_bruta': ganancia_bruta,
            'rentabilidad': rentabilidad,
            'edad_retiro': edad_retiro,
            'años': años,
            'frecuencia': frecuencia,
            'tea_ingresada': tea * 100,  # TEA entered by user
            'tea_equivalente': tea_equivalente * 100  # Equivalent TEA considering compounding
        }
    }

def calcular_jubilacion(datos):
    """
    Calculate retirement projection (Módulo B)

    Args:
        datos: Dictionary with form data and portfolio data from session

    Returns:
        Dictionary with calculation results
    """
    from flask import session

    # Get portfolio data from session
    resumen_cartera = session.get('cartera_resumen')
    cartera_datos = session.get('cartera_datos')

    if not resumen_cartera or not cartera_datos:
        return {
            'tipo_retiro': datos['tipo_retiro'],
            'tipo_impuesto': datos['tipo_impuesto'],
            'mensaje': 'Este módulo requiere datos del Módulo A primero'
        }

    # Extract portfolio summary
    capital_final = resumen_cartera['capital_final']
    # Use the original TEA from portfolio divided by 12 for monthly pension rate
    tea_cartera = cartera_datos['tea'] / 100 / 12  # Monthly rate from annual TEA

    # Extract retirement parameters
    tipo_retiro = datos['tipo_retiro']
    tipo_impuesto = datos['tipo_impuesto']
    ingresos_adicionales = datos.get('ingresos_adicionales', 0.0)
    costos_mensuales = datos.get('costos_mensuales', 0.0)
    edad_jubilacion = datos.get('edad_jubilacion', 65)

    # Calculate years of retirement from current age and retirement age
    edad_actual = cartera_datos['edad_actual']
    años_retiro = max(1, edad_jubilacion - edad_actual)  # Ensure at least 1 year

    usar_misma_tea = datos.get('usar_misma_tea', True)
    tea_retiro = datos.get('tea_retiro', tea_cartera * 100) / 100 if not usar_misma_tea else tea_cartera

    # Calculate RENTA DISPONIBLE: Capital acumulado + Ingresos adicionales - Costos mensuales
    renta_disponible = capital_final + ingresos_adicionales - costos_mensuales

    # Calculate monthly pension based on retirement type and available income
    if tipo_retiro == 'pension':
        # Calculate monthly pension that lasts for the specified years
        # Using annuity formula: PMT = PV / [(1 - (1+r)^-n)/r]
        # tea_retiro is already monthly rate, so use it directly
        r_mensual = tea_retiro
        n_meses = años_retiro * 12

        if r_mensual == 0:
            pension_mensual = renta_disponible / n_meses
        else:
            pension_mensual = renta_disponible * (r_mensual * (1 + r_mensual)**n_meses) / ((1 + r_mensual)**n_meses - 1)
    elif tipo_retiro == 'dividendos':
        # Renta vía dividendos: solo dividendos sin tocar capital
        # Paso 1: Determinar el capital acumulado (capital_final)
        # Paso 2: Definir el porcentaje de la tasa aplicada (50% de la TEA según ejemplo del profesor)
        porcentaje_distribucion = 0.5  # 50% de la TEA se reparte como dividendo

        # Paso 3: Calcular dividendos anuales
        # Dividendos anuales = Capital acumulado × (TEA × porcentaje_distribucion)
        dividendos_anuales = capital_final * (cartera_datos['tea'] / 100 * porcentaje_distribucion)

        # Paso 4: Convertir a dividendos mensuales
        # Dividendos mensuales = Dividendos anuales ÷ 12
        pension_mensual = dividendos_anuales / 12
    else:
        # Lump sum withdrawal (tipo_retiro == 'total')
        pension_mensual = renta_disponible  # One-time payment

    # Calculate taxes based on form choices
    if tipo_impuesto == '29.5':
        tasa_impuesto = 0.295  # 29.5% tax
        impuesto_mensual = pension_mensual * tasa_impuesto
        pension_neta_mensual = pension_mensual - impuesto_mensual
    elif tipo_impuesto == '5':
        tasa_impuesto = 0.05  # 5% tax
        impuesto_mensual = pension_mensual * tasa_impuesto
        pension_neta_mensual = pension_mensual - impuesto_mensual
    else:
        # Default to no tax if unknown type
        impuesto_mensual = 0
        pension_neta_mensual = pension_mensual

    # Calculate annual amounts
    pension_anual = pension_mensual * 12
    impuesto_anual = impuesto_mensual * 12
    pension_neta_anual = pension_neta_mensual * 12

    # Calculate total withdrawal over retirement period
    if tipo_retiro == 'pension':
        retiro_total = pension_mensual * 12 * años_retiro
    else:
        retiro_total = capital_final

    return {
        'tipo_retiro': tipo_retiro,
        'tipo_impuesto': tipo_impuesto,
        'ingresos_adicionales': ingresos_adicionales,
        'costos_mensuales': costos_mensuales,
        'renta_disponible': renta_disponible,
        'capital_inicial': capital_final,
        'pension_mensual_bruta': pension_mensual,
        'impuesto_mensual': impuesto_mensual,
        'pension_mensual_neta': pension_neta_mensual,
        'pension_anual_bruta': pension_anual,
        'impuesto_anual': impuesto_anual,
        'pension_anual_neta': pension_neta_anual,
        'años_retiro': años_retiro,
        'retiro_total': retiro_total,
        'edad_jubilacion': edad_jubilacion,
        'tea_retiro': tea_retiro * 100,
        'mensaje': 'Cálculo de jubilación completado exitosamente'
    }

def calcular_bonos(datos):
    """
    Calculate bond valuation (Módulo C)

    Args:
        datos: Dictionary with form data

    Returns:
        Dictionary with calculation results
    """
    # Extract data
    valor_nominal = datos['valor_nominal']
    tasa_cupon = datos['tasa_cupon'] / 100  # Convert to decimal
    frecuencia_pago = datos['frecuencia_pago']
    años = datos['años_bono']
    tea_retorno = datos['tea_retorno'] / 100  # Convert to decimal

    # Calculate periods per year
    periodos_por_año = {
        'Mensual': 12,
        'Bimestral': 6,
        'Trimestral': 4,
        'Cuatrimestral': 3,
        'Semestral': 2,
        'Anual': 1
    }

    periodos_año = periodos_por_año[frecuencia_pago]
    total_periodos = años * periodos_año

    # Calculate periodic rates
    cupon_periodico = valor_nominal * tasa_cupon / periodos_año
    tasa_descuento_periodica = (1 + tea_retorno) ** (1 / periodos_año) - 1

    # Calculate cash flows
    flujos = []
    valor_presente_total = 0

    for periodo in range(1, total_periodos + 1):
        # Determine if it's the last period (includes face value)
        if periodo == total_periodos:
            flujo_nominal = cupon_periodico + valor_nominal
        else:
            flujo_nominal = cupon_periodico

        # Calculate present value
        valor_presente = flujo_nominal / ((1 + tasa_descuento_periodica) ** periodo)
        valor_presente_total += valor_presente

        flujos.append({
            'Periodo': periodo,
            'Flujo (USD)': flujo_nominal,
            'Valor Presente (USD)': valor_presente
        })

    # Create DataFrame
    df = pd.DataFrame(flujos)

    # Determine if premium, discount, or par
    if valor_presente_total > valor_nominal:
        estado = 'Prima'
    elif valor_presente_total < valor_nominal:
        estado = 'Descuento'
    else:
        estado = 'Par'

    return {
        'dataframe': df,
        'resumen': {
            'valor_presente_total': valor_presente_total,
            'valor_nominal': valor_nominal,
            'diferencia': valor_presente_total - valor_nominal,
            'estado': estado,
            'tasa_cupon': tasa_cupon * 100,
            'tea_retorno': tea_retorno * 100
        }
    }
