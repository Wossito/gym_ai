# ============================================================================
# utils/__init__.py
# ============================================================================

"""
Utilidades del sistema.
"""

from utils.calculations import (
    calculate_imc,
    get_imc_category,
    calculate_profile_similarity,
    calculate_average,
    calculate_median,
    calculate_std_dev
)

from utils.validators import (
    validate_user_profile,
    validate_feedback,
    validate_routine_structure,
    format_validation_errors
)

from utils.constants import (
    IMC_CATEGORIES,
    MUSCLE_GROUPS,
    SATISFACTION_RATINGS,
    SYSTEM_VERSION
)

__all__ = [
    # Calculations
    'calculate_imc',
    'get_imc_category',
    'calculate_profile_similarity',
    'calculate_average',
    'calculate_median',
    'calculate_std_dev',
    
    # Validators
    'validate_user_profile',
    'validate_feedback',
    'validate_routine_structure',
    'format_validation_errors',
    
    # Constants
    'IMC_CATEGORIES',
    'MUSCLE_GROUPS',
    'SATISFACTION_RATINGS',
    'SYSTEM_VERSION'
]