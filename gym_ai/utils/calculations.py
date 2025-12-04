"""
Utilidades de cálculo.

Este módulo contiene todas las funciones puras de cálculo utilizadas
en el sistema: IMC, similitudes, distancias, normalizaciones, etc.
"""

import math
from typing import Dict, Any, Tuple
from config import Mappings, AIConfig
from utils.constants import IMC_CATEGORIES, IMC_DISPLAY_NAMES, NORMALIZATION_FACTORS


# ============================================================================
# CÁLCULOS DE IMC
# ============================================================================

def calculate_imc(weight: float, height: float) -> float:
    """
    Calcula el Índice de Masa Corporal (IMC).
    
    Args:
        weight: Peso en kilogramos
        height: Altura en metros
        
    Returns:
        IMC calculado
        
    Examples:
        >>> calculate_imc(70, 1.75)
        22.86
    """
    if height <= 0:
        raise ValueError("La altura debe ser mayor a 0")
    
    return weight / (height ** 2)


def get_imc_category(imc: float) -> str:
    """
    Obtiene la categoría del IMC.
    
    Args:
        imc: Índice de Masa Corporal
        
    Returns:
        Categoría del IMC como string
        
    Examples:
        >>> get_imc_category(22.5)
        'normal'
        >>> get_imc_category(27)
        'sobrepeso'
    """
    for category, (min_val, max_val) in IMC_CATEGORIES.items():
        if min_val <= imc < max_val:
            return category
    
    return 'obesidad'  # Por defecto si supera todos los rangos


def get_imc_display_name(imc: float) -> str:
    """
    Obtiene el nombre para mostrar de la categoría de IMC.
    
    Args:
        imc: Índice de Masa Corporal
        
    Returns:
        Nombre para mostrar
        
    Examples:
        >>> get_imc_display_name(22.5)
        'Peso normal'
    """
    category = get_imc_category(imc)
    return IMC_DISPLAY_NAMES.get(category, 'Desconocido')


# ============================================================================
# CÁLCULOS DE SIMILITUD ENTRE PERFILES
# ============================================================================

def calculate_profile_similarity(profile1: Dict[str, Any], 
                                profile2: Dict[str, Any]) -> float:
    """
    Calcula la similitud entre dos perfiles de usuario usando distancia euclidiana.
    
    La similitud se calcula considerando:
    - Edad (normalizada por 100)
    - IMC (normalizado por 20)
    - Nivel de experiencia (normalizado por 3)
    - Objetivo (comparación binaria)
    - Días de entrenamiento (normalizado por 7)
    
    Args:
        profile1: Primer perfil de usuario
        profile2: Segundo perfil de usuario
        
    Returns:
        Similitud entre 0 y 1 (1 = idénticos, 0 = muy diferentes)
        
    Examples:
        >>> p1 = {'edad': 25, 'imc': 22, 'nivel_num': 2, 'objetivo_str': 'ganar_masa', 'dias': 4}
        >>> p2 = {'edad': 26, 'imc': 23, 'nivel_num': 2, 'objetivo_str': 'ganar_masa', 'dias': 4}
        >>> calculate_profile_similarity(p1, p2)
        0.95  # Alta similitud
    """
    try:
        # Extraer valores con defaults
        edad1 = profile1.get('edad', 30)
        edad2 = profile2.get('edad', 30)
        
        imc1 = profile1.get('imc', 22)
        imc2 = profile2.get('imc', 22)
        
        nivel1 = profile1.get('nivel_num', 2)
        nivel2 = profile2.get('nivel_num', 2)
        
        dias1 = profile1.get('dias', 4)
        dias2 = profile2.get('dias', 4)
        
        # Comparación de objetivo (binaria: 0 si igual, 1 si diferente)
        obj1 = profile1.get('objetivo_str', '')
        obj2 = profile2.get('objetivo_str', '')
        diff_obj = 0 if obj1 == obj2 else 1
        
        # Normalizar diferencias usando factores de normalización
        diff_edad = abs(edad1 - edad2) / NORMALIZATION_FACTORS['edad']
        diff_imc = abs(imc1 - imc2) / NORMALIZATION_FACTORS['imc']
        diff_nivel = abs(nivel1 - nivel2) / NORMALIZATION_FACTORS['nivel']
        diff_dias = abs(dias1 - dias2) / NORMALIZATION_FACTORS['dias']
        
        # Calcular distancia euclidiana
        distance = math.sqrt(
            diff_edad**2 + 
            diff_imc**2 + 
            diff_nivel**2 + 
            diff_obj**2 + 
            diff_dias**2
        )
        
        # Convertir distancia a similitud (inversamente proporcional)
        similarity = 1 / (1 + distance)
        
        return similarity
        
    except Exception as e:
        # En caso de error, retornar similitud media
        return 0.5


def calculate_normalized_distance(value1: float, value2: float, 
                                 norm_factor: float) -> float:
    """
    Calcula la diferencia normalizada entre dos valores.
    
    Args:
        value1: Primer valor
        value2: Segundo valor
        norm_factor: Factor de normalización
        
    Returns:
        Diferencia normalizada
    """
    return abs(value1 - value2) / norm_factor


# ============================================================================
# CÁLCULOS BAYESIANOS PARA PREDICCIONES
# ============================================================================

def calculate_bayesian_adjustment(factors: Dict[str, Any], 
                                 thresholds: Dict[str, float]) -> float:
    """
    Calcula ajustes bayesianos para predicción de satisfacción.
    
    Args:
        factors: Factores que influyen en la predicción
        thresholds: Umbrales de configuración
        
    Returns:
        Ajuste total a aplicar
    """
    adjustments = []
    
    # Ajuste por similitud promedio
    if 'similitud_promedio' in factors:
        sim = factors['similitud_promedio']
        if sim > thresholds.get('similitud_alta', AIConfig.SIMILARITY_HIGH):
            adjustments.append(0.3)
        elif sim > thresholds.get('similitud_media', AIConfig.SIMILARITY_MEDIUM):
            adjustments.append(0.1)
        else:
            adjustments.append(-0.1)
    
    # Ajuste por cantidad de datos
    if 'cantidad_similares' in factors:
        cantidad = factors['cantidad_similares']
        if cantidad >= 5:
            adjustments.append(0.2)
        elif cantidad >= 3:
            adjustments.append(0.1)
    
    # Ajuste por complejidad
    if 'ajuste_complejidad' in factors:
        comp = factors['ajuste_complejidad']
        if comp > 0.8:
            adjustments.append(0.2)
        elif comp > 0.6:
            adjustments.append(0.0)
        else:
            adjustments.append(-0.2)
    
    # Ajuste por patrones consolidados
    if factors.get('patron_existe') and factors.get('cantidad_patrones', 0) >= 5:
        adjustments.append(0.3)
    
    return sum(adjustments)


def calculate_confidence_score(n_samples: int, similarity_avg: float, 
                              std_dev: float = None) -> float:
    """
    Calcula un score de confianza basado en cantidad de datos y similitud.
    
    Args:
        n_samples: Número de muestras
        similarity_avg: Similitud promedio
        std_dev: Desviación estándar (opcional)
        
    Returns:
        Score de confianza entre 0 y 1
    """
    confidence = 0.5  # Base
    
    # Factor por cantidad de datos (máx +0.3)
    if n_samples >= 10:
        confidence += 0.3
    elif n_samples >= 5:
        confidence += 0.2
    elif n_samples >= 3:
        confidence += 0.1
    
    # Factor por similitud (máx +0.3)
    if similarity_avg > AIConfig.SIMILARITY_HIGH:
        confidence += 0.3
    elif similarity_avg > AIConfig.SIMILARITY_MEDIUM:
        confidence += 0.2
    elif similarity_avg > AIConfig.SIMILARITY_LOW:
        confidence += 0.1
    
    # Factor por consistencia (máx +0.2)
    if std_dev is not None:
        if std_dev < 0.5:
            confidence += 0.2
        elif std_dev < 1.0:
            confidence += 0.1
    
    return min(1.0, confidence)


# ============================================================================
# CÁLCULOS DE SCORING
# ============================================================================

def calculate_routine_complexity(routine: Dict[str, Any], days: int) -> float:
    """
    Calcula la complejidad de una rutina (ejercicios por día).
    
    Args:
        routine: Rutina a evaluar
        days: Número de días de entrenamiento
        
    Returns:
        Complejidad (ejercicios por día)
    """
    if not routine or 'rutina_semanal' not in routine:
        return 0.0
    
    total_exercises = sum(
        len(exercises) 
        for exercises in routine['rutina_semanal'].values()
    )
    
    return total_exercises / days if days > 0 else 0.0


def calculate_routine_score(satisfaction: float, level_match: float, 
                           goal_match: float, variety: float, 
                           weights: Dict[str, float] = None) -> float:
    """
    Calcula el score total de una rutina.
    
    Args:
        satisfaction: Score de satisfacción (0-100)
        level_match: Score de adecuación al nivel (0-100)
        goal_match: Score de adecuación al objetivo (0-100)
        variety: Score de variedad (0-100)
        weights: Pesos de cada componente (opcional)
        
    Returns:
        Score total (0-100)
    """
    from utils.constants import SCORING_WEIGHTS
    
    if weights is None:
        weights = SCORING_WEIGHTS
    
    total = (
        satisfaction * weights.get('satisfaccion', 0.4) +
        level_match * weights.get('nivel', 0.2) +
        goal_match * weights.get('objetivo', 0.2) +
        variety * weights.get('variedad', 0.2)
    )
    
    return round(total, 2)


# ============================================================================
# CÁLCULOS ESTADÍSTICOS
# ============================================================================

def calculate_average(values: list) -> float:
    """
    Calcula el promedio de una lista de valores.
    
    Args:
        values: Lista de valores numéricos
        
    Returns:
        Promedio
    """
    if not values:
        return 0.0
    return sum(values) / len(values)


def calculate_median(values: list) -> float:
    """
    Calcula la mediana de una lista de valores.
    
    Args:
        values: Lista de valores numéricos
        
    Returns:
        Mediana
    """
    if not values:
        return 0.0
    
    sorted_values = sorted(values)
    n = len(sorted_values)
    
    if n % 2 == 0:
        return (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
    else:
        return sorted_values[n//2]


def calculate_std_dev(values: list) -> float:
    """
    Calcula la desviación estándar de una lista de valores.
    
    Args:
        values: Lista de valores numéricos
        
    Returns:
        Desviación estándar
    """
    if len(values) < 2:
        return 0.0
    
    avg = calculate_average(values)
    variance = sum((x - avg) ** 2 for x in values) / (len(values) - 1)
    
    return math.sqrt(variance)


# ============================================================================
# FUNCIONES DE NORMALIZACIÓN
# ============================================================================

def normalize_value(value: float, min_val: float, max_val: float) -> float:
    """
    Normaliza un valor al rango [0, 1].
    
    Args:
        value: Valor a normalizar
        min_val: Valor mínimo del rango
        max_val: Valor máximo del rango
        
    Returns:
        Valor normalizado
    """
    if max_val == min_val:
        return 0.5
    
    return (value - min_val) / (max_val - min_val)


def clamp_value(value: float, min_val: float, max_val: float) -> float:
    """
    Limita un valor a un rango específico.
    
    Args:
        value: Valor a limitar
        min_val: Valor mínimo
        max_val: Valor máximo
        
    Returns:
        Valor limitado
    """
    return max(min_val, min(max_val, value))


# ============================================================================
# CONVERSIONES DE UNIDADES
# ============================================================================

def extract_rep_range(rep_str: str) -> Tuple[int, int]:
    """
    Extrae el rango de repeticiones de un string.
    
    Args:
        rep_str: String con rango (ej: "8-12")
        
    Returns:
        Tupla (min, max)
        
    Examples:
        >>> extract_rep_range("8-12")
        (8, 12)
    """
    try:
        if '-' in str(rep_str):
            parts = str(rep_str).split('-')
            return (int(parts[0]), int(parts[1]))
        else:
            val = int(rep_str)
            return (val, val)
    except:
        return (8, 12)  # Default


def format_rep_range(min_reps: int, max_reps: int) -> str:
    """
    Formatea un rango de repeticiones.
    
    Args:
        min_reps: Repeticiones mínimas
        max_reps: Repeticiones máximas
        
    Returns:
        String formateado
        
    Examples:
        >>> format_rep_range(8, 12)
        '8-12'
    """
    return f"{min_reps}-{max_reps}"


def format_rest_time(min_seconds: int, max_seconds: int) -> str:
    """
    Formatea un tiempo de descanso.
    
    Args:
        min_seconds: Segundos mínimos
        max_seconds: Segundos máximos
        
    Returns:
        String formateado
        
    Examples:
        >>> format_rest_time(60, 90)
        '60-90s'
    """
    return f"{min_seconds}-{max_seconds}s"