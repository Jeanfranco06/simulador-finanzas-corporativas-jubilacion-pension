from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, RadioField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, ValidationError
from config import Config

class CarteraForm(FlaskForm):
    """Form for Módulo A: Crecimiento de Cartera"""
    edad_actual = IntegerField('Edad Actual',
                              validators=[DataRequired(), NumberRange(min=18, max=100)],
                              default=30)

    monto_inicial = FloatField('Monto Inicial (USD)',
                              validators=[NumberRange(min=0)],
                              default=0.0)

    aporte_periodico = FloatField('Aporte Periódico (USD)',
                                 validators=[NumberRange(min=0)],
                                 default=500.0)

    frecuencia = SelectField('Frecuencia de Aportes',
                            choices=[('Mensual', 'Mensual'),
                                   ('Bimestral', 'Bimestral'),
                                   ('Trimestral', 'Trimestral'),
                                   ('Cuatrimestral', 'Cuatrimestral'),
                                   ('Semestral', 'Semestral'),
                                   ('Anual', 'Anual')],
                            default='Mensual')

    tipo_plazo = RadioField('Especificar plazo por:',
                           choices=[('años', 'Años'), ('edad', 'Edad de Jubilación')],
                           default='años')

    años = IntegerField('Plazo (Años)',
                       validators=[Optional(), NumberRange(min=1, max=100)],
                       default=35)

    edad_retiro = IntegerField('Edad de Jubilación',
                              validators=[Optional(), NumberRange(min=18, max=120)],
                              default=65)

    tea = FloatField('TEA (%)',
                    validators=[DataRequired(), NumberRange(min=Config.MIN_TEA, max=Config.MAX_TEA)],
                    default=8.0)

    submit = SubmitField('Calcular Proyección')

    def validate(self, extra_validators=None):
        """Custom validation for the portfolio form"""
        if not super().validate(extra_validators):
            return False

        # Basic validation: ensure required fields are present
        if self.tipo_plazo.data == 'años':
            if self.años.data is None or self.años.data <= 0:
                self.años.errors.append('Debe especificar un número válido de años.')
                return False
            # Validate that retirement age equals current age + years
            expected_retirement_age = self.edad_actual.data + self.años.data
            if self.edad_retiro.data != expected_retirement_age:
                self.edad_retiro.errors.append(f'La edad de jubilación debe ser {expected_retirement_age} años (edad actual {self.edad_actual.data} + {self.años.data} años).')
                return False
        elif self.tipo_plazo.data == 'edad':
            if self.edad_retiro.data is None or self.edad_retiro.data <= 0:
                self.edad_retiro.errors.append('Debe especificar una edad de jubilación válida.')
                return False
            # Validate that retirement age is at least 1 year greater than current age
            if self.edad_retiro.data < self.edad_actual.data + 1:
                self.edad_retiro.errors.append('La edad de jubilación debe ser al menos 1 año mayor que la edad actual.')
                return False
            # Validate that years equals retirement age - current age
            expected_years = self.edad_retiro.data - self.edad_actual.data
            if self.años.data != expected_years:
                self.años.errors.append(f'El plazo debe ser {expected_years} años (edad de jubilación {self.edad_retiro.data} - edad actual {self.edad_actual.data}).')
                return False

        return True

class JubilacionForm(FlaskForm):
    """Form for Módulo B: Proyección de Jubilación"""
    tipo_retiro = RadioField('Tipo de Retiro',
                            choices=[('pension', 'Pensión Mensual'),
                                   ('total', 'Cobro Total'),
                                   ('dividendos', 'Renta vía Dividendos')],
                            default='pension')

    tipo_impuesto = SelectField('Tipo de Impuesto sobre Ganancia',
                               choices=[('29.5', '29.5% Fuente Extranjera'),
                                      ('5', '5% Bolsa Local')],
                               default='29.5')

    ingresos_adicionales = FloatField('Ingresos Adicionales Mensuales (USD)',
                                     validators=[NumberRange(min=0)],
                                     default=0.0)

    costos_mensuales = FloatField('Costos Mensuales (USD)',
                                 validators=[NumberRange(min=0)],
                                 default=0.0)

    edad_jubilacion = IntegerField('Edad de Jubilación',
                                  validators=[Optional(), NumberRange(min=18, max=120)],
                                  default=65)

    usar_misma_tea = BooleanField('Usar la misma TEA del Módulo A',
                                 default=True)

    tea_retiro = FloatField('TEA durante el Retiro (%)',
                           validators=[Optional(), NumberRange(min=Config.MIN_TEA, max=Config.MAX_TEA)],
                           default=5.0)

    submit = SubmitField('Calcular Jubilación')

class BonosForm(FlaskForm):
    """Form for Módulo C: Valoración de Bonos"""
    valor_nominal = FloatField('Valor Nominal (USD)',
                              validators=[DataRequired(), NumberRange(min=0)],
                              default=1000.0)

    tasa_cupon = FloatField('Tasa Cupón Anual (%)',
                           validators=[DataRequired(), NumberRange(min=0, max=Config.MAX_TEA)],
                           default=5.0)

    frecuencia_pago = SelectField('Frecuencia de Pago de Cupones',
                                 choices=[('Mensual', 'Mensual'),
                                        ('Bimestral', 'Bimestral'),
                                        ('Trimestral', 'Trimestral'),
                                        ('Cuatrimestral', 'Cuatrimestral'),
                                        ('Semestral', 'Semestral'),
                                        ('Anual', 'Anual')],
                                 default='Semestral')

    años_bono = IntegerField('Plazo al Vencimiento (Años)',
                            validators=[DataRequired(), NumberRange(min=1, max=50)],
                            default=5)

    tea_retorno = FloatField('Tasa de Retorno Esperada - TEA (%)',
                            validators=[DataRequired(), NumberRange(min=Config.MIN_TEA, max=Config.MAX_TEA)],
                            default=6.0)

    submit = SubmitField('Valorar Bono')
