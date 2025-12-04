"""
Constantes del sistema.

Este módulo contiene todas las constantes utilizadas en el sistema
que no son configuraciones, sino valores fijos del dominio.
"""

# ============================================================================
# CATEGORÍAS DE IMC (Índice de Masa Corporal)
# ============================================================================

IMC_CATEGORIES = {
    'bajo_peso': (0, 18.5),
    'normal': (18.5, 25),
    'sobrepeso': (25, 30),
    'obesidad': (30, 100)
}

IMC_DISPLAY_NAMES = {
    'bajo_peso': 'Bajo peso',
    'normal': 'Peso normal',
    'sobrepeso': 'Sobrepeso',
    'obesidad': 'Obesidad'
}

# ============================================================================
# INTENSIDADES DE CARDIO
# ============================================================================

CARDIO_INTENSITIES = ['baja', 'moderada', 'alta', 'HIIT']

# ============================================================================
# GRUPOS MUSCULARES
# ============================================================================

MUSCLE_GROUPS = [
    'pecho',
    'espalda',
    'piernas',
    'hombros',
    'brazos',
    'core',
    'cardio'
]

MUSCLE_GROUP_DISPLAY_NAMES = {
    'pecho': 'Pecho',
    'espalda': 'Espalda',
    'piernas': 'Piernas',
    'hombros': 'Hombros',
    'brazos': 'Brazos',
    'core': 'Core/Abdomen',
    'cardio': 'Cardio'
}

# ============================================================================
# ESTRUCTURAS DE RUTINA
# ============================================================================

ROUTINE_STRUCTURES = {
    'fullbody': {
        'name': 'Full Body',
        'description': 'Entrenar todos los grupos musculares en cada sesión',
        'ideal_days': [3, 4]
    },
    'upper_lower': {
        'name': 'Upper/Lower Split',
        'description': 'Dividir entre tren superior e inferior',
        'ideal_days': [4, 5]
    },
    'split': {
        'name': 'Split por Músculo',
        'description': 'Un grupo muscular principal por día',
        'ideal_days': [5, 6, 7]
    }
}

# ============================================================================
# MODOS DE GENERACIÓN
# ============================================================================

GENERATION_MODES = {
    'exploracion': 'Exploración (Innovación)',
    'explotacion': 'Explotación (Aprendizaje)',
    'hibrido': 'Híbrido'
}

# ============================================================================
# EMOJIS PARA UI
# ============================================================================

EMOJIS = {
    'brain': '🧠',
    'muscle': '💪',
    'fire': '🔥',
    'star': '⭐',
    'check': '✅',
    'warning': '⚠️',
    'stats': '📊',
    'calendar': '📅',
    'target': '🎯',
    'trophy': '🏆',
    'party': '🎉',
    'thumbs_up': '👍',
    'thinking': '🤔',
    'rocket': '🚀'
}

# ============================================================================
# RATINGS DE SATISFACCIÓN
# ============================================================================

SATISFACTION_RATINGS = [
    (1, "😫 Muy difícil", "Demasiado exigente, no pude completarla"),
    (2, "😕 Difícil", "Muy desafiante, pero terminé"),
    (3, "😊 Adecuada", "Balance correcto, me sentí bien"),
    (4, "😄 Buena", "Perfecta para mi nivel, gran rutina"),
    (5, "🤩 Perfecta", "Exactamente lo que necesitaba, excelente")
]

# ============================================================================
# MENSAJES DEL SISTEMA
# ============================================================================

SYSTEM_MESSAGES = {
    'welcome': """Sistema de Inteligencia Artificial que aprende de cada usuario
para generar rutinas de gimnasio cada vez más precisas y personalizadas.

El sistema analiza tu perfil, busca patrones en usuarios similares
y genera una rutina completamente personalizada para ti.

¡Mientras más personas lo usen, más inteligente se vuelve!""",
    
    'generating': [
        "🔍 Analizando tu perfil...",
        "📊 Calculando IMC y métricas...",
        "🎯 Buscando patrones en usuarios similares...",
        "💡 Generando combinaciones de ejercicios...",
        "⚡ Optimizando parámetros de entrenamiento...",
        "✨ Creando tu rutina personalizada..."
    ],
    
    'feedback_thanks': """Tu opinión ha sido procesada y guardada.

El sistema ha aprendido de tu experiencia y usará
este conocimiento para mejorar las futuras rutinas.

¡Cada feedback hace que la IA sea más inteligente!""",
    
    'no_data': """Sin suficientes datos históricos para personalización avanzada.
La rutina se generará usando parámetros estándar optimizados.
¡Tu feedback ayudará al sistema a mejorar!"""
}

# ============================================================================
# NORMALIZACIÓN DE VALORES PARA CÁLCULOS
# ============================================================================

NORMALIZATION_FACTORS = {
    'edad': 100,      # Normalizar edad por 100
    'imc': 20,        # Normalizar IMC por 20
    'nivel': 3,       # Normalizar nivel por 3
    'dias': 7         # Normalizar días por 7
}

# ============================================================================
# PESOS PARA SCORING
# ============================================================================

SCORING_WEIGHTS = {
    'satisfaccion': 0.40,      # 40% del score
    'nivel': 0.20,             # 20% del score
    'objetivo': 0.20,          # 20% del score
    'variedad': 0.20           # 20% del score
}

# ============================================================================
# RECOMENDACIONES POR CATEGORÍA DE USUARIO
# ============================================================================

USER_RECOMMENDATIONS = {
    'novato': [
        "Comienza con rutinas Full Body 3 días/semana",
        "Enfócate en aprender técnica correcta",
        "Da feedback detallado para ayudar al sistema"
    ],
    'regular': {
        'necesita_ajuste': [
            "Considera ajustar días de entrenamiento",
            "Revisa si la intensidad es adecuada"
        ],
        'default': [
            "Continúa con la consistencia",
            "Considera aumentar días de entrenamiento"
        ]
    },
    'experimentado': {
        'excelente': [
            "Excelente progreso, mantén el ritmo",
            "Considera técnicas avanzadas"
        ],
        'default': [
            "Revisa objetivos cada 4-6 semanas"
        ]
    },
    'veterano': {
        'excelente': [
            "Excelente progreso, mantén el ritmo",
            "Considera técnicas avanzadas"
        ],
        'default': [
            "Revisa objetivos cada 4-6 semanas"
        ]
    },
    'experto': [
        "Usuario experimentado del sistema",
        "Considera compartir feedback detallado",
        "Experimenta con variaciones avanzadas"
    ]
}

# ============================================================================
# TIPOS DE ANOMALÍAS DETECTABLES
# ============================================================================

ANOMALY_TYPES = {
    'tendencia_negativa': {
        'description': 'Satisfacción en descenso constante',
        'recommendation': 'Revisar intensidad o variedad de ejercicios'
    },
    'caida_abrupta': {
        'description': 'Caída súbita en satisfacción',
        'recommendation': 'Verificar posibles lesiones o sobreentrenamiento'
    },
    'estancamiento': {
        'description': 'Satisfacción estancada en nivel medio',
        'recommendation': 'Considerar cambio de enfoque o metodología'
    },
    'sobreentrenamiento': {
        'description': 'Señales de fatiga acumulada',
        'recommendation': 'Reducir volumen o aumentar descanso'
    }
}

# ============================================================================
# VERSIÓN DEL SISTEMA
# ============================================================================

SYSTEM_VERSION = "2.0.0-MVC"
SYSTEM_NAME = "Gym AI Advanced"
SYSTEM_DESCRIPTION = "Sistema de IA Adaptativo para Generación de Rutinas de Gimnasio"