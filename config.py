"""
Configuración central del sistema de IA para gimnasio.

Este módulo contiene todas las configuraciones, constantes y parámetros
del sistema en un solo lugar, facilitando mantenimiento y ajustes.
"""

import os
from pathlib import Path

# ============================================================================
# RUTAS Y ARCHIVOS
# ============================================================================

# Directorio base del proyecto
BASE_DIR = Path(__file__).parent

# Directorio de datos
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

# Archivo de persistencia principal
DATA_FILE = DATA_DIR / 'gym_ai_advanced_data.json'

# ============================================================================
# CONFIGURACIÓN DE LA INTERFAZ GRÁFICA
# ============================================================================

class UIConfig:
    """Configuración de la interfaz de usuario"""
    
    # Dimensiones de ventana
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 700
    WINDOW_TITLE = "🏋️ Sistema de IA Adaptativo - Gimnasio"
    
    # Esquema de colores
    COLORS = {
        'bg_dark': '#1a1a2e',
        'bg_medium': '#16213e',
        'bg_light': '#0f3460',
        'accent': '#00adb5',
        'text': '#eeeeee',
        'success': '#06d6a0',
        'warning': '#ffd93d',
        'error': '#ef476f'
    }
    
    # Fuentes
    FONT_FAMILY = 'Helvetica'
    FONT_SIZES = {
        'title': 18,
        'subtitle': 14,
        'normal': 11,
        'small': 9
    }

# ============================================================================
# CONFIGURACIÓN DEL SISTEMA DE IA
# ============================================================================

class AIConfig:
    """Configuración del sistema de Inteligencia Artificial"""
    
    # Parámetros de aprendizaje
    LEARNING_RATE = 0.1
    EXPLORATION_FACTOR = 0.2  # 20% exploración, 80% explotación
    
    # Umbrales de similitud
    SIMILARITY_HIGH = 0.85
    SIMILARITY_MEDIUM = 0.70
    SIMILARITY_LOW = 0.50
    
    # Umbrales de satisfacción
    SATISFACTION_EXCELLENT = 4.5
    SATISFACTION_GOOD = 4.0
    SATISFACTION_ACCEPTABLE = 3.5
    
    # Umbrales de confianza
    CONFIDENCE_HIGH = 0.80
    CONFIDENCE_MEDIUM = 0.60
    CONFIDENCE_LOW = 0.40
    
    # Patrones exitosos
    MIN_SIMILAR_USERS = 3
    MIN_CONFIDENCE = 0.6
    TOP_SIMILAR_USERS = 5  # Número de usuarios similares a considerar
    
    # Evolución del sistema
    USERS_PER_GENERATION = 10  # Usuarios necesarios para evolucionar generación

# ============================================================================
# CONFIGURACIÓN DE RUTINAS
# ============================================================================

class RoutineConfig:
    """Configuración de generación de rutinas"""
    
    # Estructuras de entrenamiento
    STRUCTURES = {
        'fullbody': 'Full Body',
        'upper_lower': 'Upper/Lower Split',
        'split': 'Split por Músculo'
    }
    
    # Parámetros por nivel
    SERIES_BY_LEVEL = {
        'principiante': 3,
        'intermedio': 4,
        'avanzado': 5
    }
    
    # Parámetros por objetivo
    PARAMS_BY_GOAL = {
        'perder_peso': {
            'reps_min': 12,
            'reps_max': 20,
            'rest_min': 30,
            'rest_max': 60,
            'cardio_probability': 0.8
        },
        'ganar_masa': {
            'reps_min': 8,
            'reps_max': 12,
            'rest_min': 60,
            'rest_max': 90,
            'cardio_probability': 0.3
        },
        'resistencia': {
            'reps_min': 15,
            'reps_max': 25,
            'rest_min': 20,
            'rest_max': 45,
            'cardio_probability': 0.9
        },
        'fuerza': {
            'reps_min': 4,
            'reps_max': 8,
            'rest_min': 120,
            'rest_max': 180,
            'cardio_probability': 0.3
        }
    }
    
    # Número de ejercicios según estructura y nivel
    EXERCISES_PER_STRUCTURE = {
        'fullbody': {
            'principiante': 1,
            'intermedio': 2,
            'avanzado': 2
        },
        'upper_lower': {
            'principiante': 1,
            'intermedio': 2,
            'avanzado': 2
        },
        'split': {
            'principiante': 2,
            'intermedio': 2,
            'avanzado': 3
        }
    }

# ============================================================================
# CONFIGURACIÓN DE CLASIFICACIÓN DE USUARIOS
# ============================================================================

class UserClassificationConfig:
    """Configuración de clasificación de usuarios"""
    
    CATEGORIES = {
        'novato': {
            'max_experiences': 0,
            'description': 'Primera vez usando el sistema'
        },
        'regular': {
            'min_experiences': 1,
            'max_experiences': 5,
            'description': 'Usuario regular con algunas experiencias'
        },
        'experimentado': {
            'min_experiences': 6,
            'max_experiences': 15,
            'description': 'Usuario experimentado con buen historial'
        },
        'veterano': {
            'min_experiences': 16,
            'max_experiences': 50,
            'description': 'Usuario veterano con amplia experiencia'
        },
        'experto': {
            'min_experiences': 51,
            'description': 'Usuario experto del sistema'
        }
    }
    
    PERFORMANCE_LEVELS = {
        'excelente': 4.5,
        'bueno': 4.0,
        'aceptable': 3.5,
        'necesita_ajuste': 0
    }

# ============================================================================
# CONFIGURACIÓN DE VALIDACIÓN
# ============================================================================

class ValidationConfig:
    """Configuración de validación de datos"""
    
    # Rangos válidos para perfil de usuario
    AGE_MIN = 10
    AGE_MAX = 100
    
    WEIGHT_MIN = 30  # kg
    WEIGHT_MAX = 300  # kg
    
    HEIGHT_MIN = 1.0  # metros
    HEIGHT_MAX = 2.5  # metros
    
    DAYS_MIN = 2
    DAYS_MAX = 7
    
    # Validación de satisfacción
    SATISFACTION_MIN = 1
    SATISFACTION_MAX = 5

# ============================================================================
# MAPEOS Y ENUMERACIONES
# ============================================================================

class Mappings:
    """Mapeos entre valores numéricos y strings"""
    
    LEVEL_STR_TO_NUM = {
        'principiante': 1,
        'intermedio': 2,
        'avanzado': 3
    }
    
    LEVEL_NUM_TO_STR = {
        1: 'principiante',
        2: 'intermedio',
        3: 'avanzado'
    }
    
    GOAL_STR_TO_NUM = {
        'perder_peso': 1,
        'ganar_masa': 2,
        'resistencia': 3,
        'fuerza': 4
    }
    
    GOAL_NUM_TO_STR = {
        1: 'perder_peso',
        2: 'ganar_masa',
        3: 'resistencia',
        4: 'fuerza'
    }
    
    GOAL_DISPLAY_NAMES = {
        'perder_peso': 'Perder Peso',
        'ganar_masa': 'Ganar Masa Muscular',
        'resistencia': 'Resistencia',
        'fuerza': 'Fuerza'
    }
    
    LEVEL_DISPLAY_NAMES = {
        'principiante': 'Principiante',
        'intermedio': 'Intermedio',
        'avanzado': 'Avanzado'
    }

# ============================================================================
# BASE DE EJERCICIOS
# ============================================================================

class ExerciseDatabase:
    """Base de datos de ejercicios disponibles"""
    
    EXERCISES = {
        'pecho': {
            'compuestos': [
                'Press banca',
                'Press inclinado',
                'Fondos en paralelas',
                'Press declinado'
            ],
            'aislamiento': [
                'Aperturas con mancuernas',
                'Cruces en polea',
                'Pullover',
                'Press con mancuernas'
            ]
        },
        'espalda': {
            'compuestos': [
                'Dominadas',
                'Peso muerto',
                'Remo con barra',
                'Remo en polea'
            ],
            'aislamiento': [
                'Jalón al pecho',
                'Remo con mancuerna',
                'Face pulls',
                'Pullover espalda'
            ]
        },
        'piernas': {
            'compuestos': [
                'Sentadilla',
                'Prensa',
                'Peso muerto rumano',
                'Sentadilla búlgara'
            ],
            'aislamiento': [
                'Extensiones de cuádriceps',
                'Curl femoral',
                'Elevación de pantorrillas',
                'Hip thrust'
            ]
        },
        'hombros': {
            'compuestos': [
                'Press militar',
                'Press Arnold',
                'Remo al mentón'
            ],
            'aislamiento': [
                'Elevaciones laterales',
                'Elevaciones frontales',
                'Pájaros',
                'Face pulls'
            ]
        },
        'brazos': {
            'compuestos': [
                'Press cerrado',
                'Dominadas cerradas'
            ],
            'aislamiento': [
                'Curl con barra',
                'Extensiones de tríceps',
                'Curl martillo',
                'Curl concentrado',
                'Fondos tríceps'
            ]
        },
        'core': {
            'compuestos': [
                'Plancha',
                'Crunches',
                'Elevación de piernas',
                'Russian twists'
            ]
        },
        'cardio': [
            'Caminata',
            'Trote',
            'HIIT',
            'Bicicleta',
            'Remo',
            'Elíptica',
            'Escaladora',
            'Sprints'
        ]
    }

# ============================================================================
# CONFIGURACIÓN DE LOGGING (OPCIONAL)
# ============================================================================

class LogConfig:
    """Configuración de logging del sistema"""
    
    ENABLED = True
    LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR
    LOG_FILE = DATA_DIR / 'gym_ai.log'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# ============================================================================
# EXPORTAR CONFIGURACIONES
# ============================================================================

# Instancias globales para fácil acceso
ui_config = UIConfig()
ai_config = AIConfig()
routine_config = RoutineConfig()
user_classification_config = UserClassificationConfig()
validation_config = ValidationConfig()
mappings = Mappings()
exercise_db = ExerciseDatabase()
log_config = LogConfig()