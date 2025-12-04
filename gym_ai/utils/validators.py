"""
Validadores de datos.

Este módulo contiene todas las funciones de validación de entrada
utilizadas en el sistema para garantizar integridad de datos.
"""

from typing import Any, Dict, List, Tuple
from config import ValidationConfig, Mappings


# ============================================================================
# VALIDACIONES DE PERFIL DE USUARIO
# ============================================================================

def validate_age(age: Any) -> Tuple[bool, str]:
    """
    Valida la edad del usuario.
    
    Args:
        age: Edad a validar
        
    Returns:
        Tupla (es_válido, mensaje_error)
    """
    try:
        age_int = int(age)
        if age_int < ValidationConfig.AGE_MIN:
            return False, f"La edad debe ser mayor a {ValidationConfig.AGE_MIN}"
        if age_int > ValidationConfig.AGE_MAX:
            return False, f"La edad debe ser menor a {ValidationConfig.AGE_MAX}"
        return True, ""
    except (ValueError, TypeError):
        return False, "La edad debe ser un número entero"


def validate_weight(weight: Any) -> Tuple[bool, str]:
    """
    Valida el peso del usuario.
    
    Args:
        weight: Peso a validar (kg)
        
    Returns:
        Tupla (es_válido, mensaje_error)
    """
    try:
        weight_float = float(weight)
        if weight_float < ValidationConfig.WEIGHT_MIN:
            return False, f"El peso debe ser mayor a {ValidationConfig.WEIGHT_MIN} kg"
        if weight_float > ValidationConfig.WEIGHT_MAX:
            return False, f"El peso debe ser menor a {ValidationConfig.WEIGHT_MAX} kg"
        return True, ""
    except (ValueError, TypeError):
        return False, "El peso debe ser un número"


def validate_height(height: Any) -> Tuple[bool, str]:
    """
    Valida la altura del usuario.
    
    Args:
        height: Altura a validar (metros)
        
    Returns:
        Tupla (es_válido, mensaje_error)
    """
    try:
        height_float = float(height)
        if height_float < ValidationConfig.HEIGHT_MIN:
            return False, f"La altura debe ser mayor a {ValidationConfig.HEIGHT_MIN} m"
        if height_float > ValidationConfig.HEIGHT_MAX:
            return False, f"La altura debe ser menor a {ValidationConfig.HEIGHT_MAX} m"
        return True, ""
    except (ValueError, TypeError):
        return False, "La altura debe ser un número"


def validate_training_days(days: Any) -> Tuple[bool, str]:
    """
    Valida los días de entrenamiento.
    
    Args:
        days: Días a validar
        
    Returns:
        Tupla (es_válido, mensaje_error)
    """
    try:
        days_int = int(days)
        if days_int < ValidationConfig.DAYS_MIN:
            return False, f"Los días deben ser al menos {ValidationConfig.DAYS_MIN}"
        if days_int > ValidationConfig.DAYS_MAX:
            return False, f"Los días no pueden ser más de {ValidationConfig.DAYS_MAX}"
        return True, ""
    except (ValueError, TypeError):
        return False, "Los días deben ser un número entero"


def validate_experience_level(level: str) -> Tuple[bool, str]:
    """
    Valida el nivel de experiencia.
    
    Args:
        level: Nivel a validar
        
    Returns:
        Tupla (es_válido, mensaje_error)
    """
    valid_levels = list(Mappings.LEVEL_STR_TO_NUM.keys())
    if level not in valid_levels:
        return False, f"Nivel debe ser uno de: {', '.join(valid_levels)}"
    return True, ""


def validate_goal(goal: str) -> Tuple[bool, str]:
    """
    Valida el objetivo de entrenamiento.
    
    Args:
        goal: Objetivo a validar
        
    Returns:
        Tupla (es_válido, mensaje_error)
    """
    valid_goals = list(Mappings.GOAL_STR_TO_NUM.keys())
    if goal not in valid_goals:
        return False, f"Objetivo debe ser uno de: {', '.join(valid_goals)}"
    return True, ""


def validate_name(name: str) -> Tuple[bool, str]:
    """
    Valida el nombre del usuario.
    
    Args:
        name: Nombre a validar
        
    Returns:
        Tupla (es_válido, mensaje_error)
    """
    if not name or not name.strip():
        return False, "El nombre no puede estar vacío"
    if len(name.strip()) < 2:
        return False, "El nombre debe tener al menos 2 caracteres"
    if len(name) > 50:
        return False, "El nombre no puede tener más de 50 caracteres"
    return True, ""


# ============================================================================
# VALIDACIÓN COMPLETA DE PERFIL
# ============================================================================

def validate_user_profile(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Valida un perfil de usuario completo.
    
    Args:
        data: Diccionario con datos del usuario
        
    Returns:
        Tupla (es_válido, lista_de_errores)
    """
    errors = []
    
    # Validar nombre
    if 'nombre' in data:
        valid, msg = validate_name(data['nombre'])
        if not valid:
            errors.append(msg)
    else:
        errors.append("Falta el nombre")
    
    # Validar edad
    if 'edad' in data:
        valid, msg = validate_age(data['edad'])
        if not valid:
            errors.append(msg)
    else:
        errors.append("Falta la edad")
    
    # Validar peso
    if 'peso' in data:
        valid, msg = validate_weight(data['peso'])
        if not valid:
            errors.append(msg)
    else:
        errors.append("Falta el peso")
    
    # Validar altura
    if 'altura' in data:
        valid, msg = validate_height(data['altura'])
        if not valid:
            errors.append(msg)
    else:
        errors.append("Falta la altura")
    
    # Validar nivel
    if 'nivel_experiencia' in data:
        valid, msg = validate_experience_level(data['nivel_experiencia'])
        if not valid:
            errors.append(msg)
    else:
        errors.append("Falta el nivel de experiencia")
    
    # Validar objetivo
    if 'objetivo' in data:
        valid, msg = validate_goal(data['objetivo'])
        if not valid:
            errors.append(msg)
    else:
        errors.append("Falta el objetivo")
    
    # Validar días
    if 'dias_entrenamiento' in data:
        valid, msg = validate_training_days(data['dias_entrenamiento'])
        if not valid:
            errors.append(msg)
    else:
        errors.append("Faltan los días de entrenamiento")
    
    return (len(errors) == 0, errors)


# ============================================================================
# VALIDACIONES DE FEEDBACK
# ============================================================================

def validate_satisfaction(satisfaction: Any) -> Tuple[bool, str]:
    """
    Valida la satisfacción del usuario.
    
    Args:
        satisfaction: Satisfacción a validar (1-5)
        
    Returns:
        Tupla (es_válido, mensaje_error)
    """
    try:
        sat_int = int(satisfaction)
        if sat_int < ValidationConfig.SATISFACTION_MIN:
            return False, f"La satisfacción debe ser al menos {ValidationConfig.SATISFACTION_MIN}"
        if sat_int > ValidationConfig.SATISFACTION_MAX:
            return False, f"La satisfacción no puede ser mayor a {ValidationConfig.SATISFACTION_MAX}"
        return True, ""
    except (ValueError, TypeError):
        return False, "La satisfacción debe ser un número del 1 al 5"


def validate_feedback(satisfaction: Any, comments: str = "") -> Tuple[bool, List[str]]:
    """
    Valida el feedback completo del usuario.
    
    Args:
        satisfaction: Nivel de satisfacción
        comments: Comentarios opcionales
        
    Returns:
        Tupla (es_válido, lista_de_errores)
    """
    errors = []
    
    valid, msg = validate_satisfaction(satisfaction)
    if not valid:
        errors.append(msg)
    
    # Los comentarios son opcionales, pero si existen validar longitud
    if comments and len(comments) > 500:
        errors.append("Los comentarios no pueden tener más de 500 caracteres")
    
    return (len(errors) == 0, errors)


# ============================================================================
# VALIDACIONES DE RUTINA
# ============================================================================

def validate_routine_structure(routine: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Valida la estructura de una rutina.
    
    Args:
        routine: Rutina a validar
        
    Returns:
        Tupla (es_válido, lista_de_errores)
    """
    errors = []
    
    if not routine:
        errors.append("La rutina no puede estar vacía")
        return (False, errors)
    
    if 'rutina_semanal' not in routine:
        errors.append("La rutina debe tener 'rutina_semanal'")
    else:
        weekly = routine['rutina_semanal']
        if not weekly:
            errors.append("La rutina semanal no puede estar vacía")
        
        for day, exercises in weekly.items():
            if not exercises:
                errors.append(f"{day} no tiene ejercicios")
            
            for idx, exercise in enumerate(exercises):
                if 'ejercicio' not in exercise:
                    errors.append(f"{day}, ejercicio {idx+1}: falta nombre")
                if 'grupo' not in exercise:
                    errors.append(f"{day}, ejercicio {idx+1}: falta grupo muscular")
    
    if 'estructura' not in routine:
        errors.append("La rutina debe tener 'estructura'")
    
    return (len(errors) == 0, errors)


def validate_exercise(exercise: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Valida un ejercicio individual.
    
    Args:
        exercise: Ejercicio a validar
        
    Returns:
        Tupla (es_válido, lista_de_errores)
    """
    errors = []
    
    required_fields = ['ejercicio', 'grupo']
    for field in required_fields:
        if field not in exercise:
            errors.append(f"Falta el campo '{field}'")
    
    # Si no es cardio, debe tener series, repeticiones y descanso
    if exercise.get('grupo') != 'cardio':
        if 'series' not in exercise:
            errors.append("Falta el campo 'series'")
        if 'repeticiones' not in exercise:
            errors.append("Falta el campo 'repeticiones'")
        if 'descanso' not in exercise:
            errors.append("Falta el campo 'descanso'")
    else:
        # Cardio debe tener duración e intensidad
        if 'duracion' not in exercise:
            errors.append("Cardio debe tener 'duracion'")
        if 'intensidad' not in exercise:
            errors.append("Cardio debe tener 'intensidad'")
    
    return (len(errors) == 0, errors)


# ============================================================================
# VALIDACIONES GENERALES
# ============================================================================

def validate_required_fields(data: Dict[str, Any], 
                            required: List[str]) -> Tuple[bool, List[str]]:
    """
    Valida que existan campos requeridos en un diccionario.
    
    Args:
        data: Diccionario a validar
        required: Lista de campos requeridos
        
    Returns:
        Tupla (es_válido, lista_de_errores)
    """
    errors = []
    
    for field in required:
        if field not in data:
            errors.append(f"Falta el campo requerido: {field}")
        elif data[field] is None:
            errors.append(f"El campo '{field}' no puede ser None")
    
    return (len(errors) == 0, errors)


def is_valid_percentage(value: float) -> bool:
    """
    Verifica si un valor es un porcentaje válido (0-1 o 0-100).
    
    Args:
        value: Valor a verificar
        
    Returns:
        True si es válido
    """
    return 0 <= value <= 100 or 0 <= value <= 1


def sanitize_string(text: str, max_length: int = 100) -> str:
    """
    Sanitiza un string eliminando caracteres peligrosos y limitando longitud.
    
    Args:
        text: Texto a sanitizar
        max_length: Longitud máxima
        
    Returns:
        Texto sanitizado
    """
    if not text:
        return ""
    
    # Eliminar caracteres de control
    sanitized = ''.join(char for char in text if char.isprintable())
    
    # Limitar longitud
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized.strip()


# ============================================================================
# MENSAJES DE ERROR
# ============================================================================

def format_validation_errors(errors: List[str]) -> str:
    """
    Formatea una lista de errores en un mensaje legible.
    
    Args:
        errors: Lista de errores
        
    Returns:
        Mensaje formateado
    """
    if not errors:
        return ""
    
    if len(errors) == 1:
        return errors[0]
    
    return "Se encontraron los siguientes errores:\n• " + "\n• ".join(errors)