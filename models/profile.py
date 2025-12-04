"""
Modelo de Perfil de Usuario.

Este modelo representa el perfil numérico de un usuario utilizado
por el sistema de IA para generar rutinas personalizadas.
"""

from dataclasses import dataclass, field
from typing import Dict, Any
from datetime import datetime

from config import Mappings
from utils.calculations import calculate_imc
from utils.validators import (
    validate_age, validate_weight, validate_height,
    validate_experience_level, validate_goal, validate_training_days
)


@dataclass
class Profile:
    """
    Perfil numérico de usuario para el sistema de IA.
    
    Attributes:
        edad: Edad del usuario
        peso: Peso en kilogramos
        altura: Altura en metros
        imc: Índice de Masa Corporal (calculado)
        nivel_num: Nivel de experiencia (numérico: 1-3)
        nivel_str: Nivel de experiencia (string)
        objetivo_num: Objetivo de entrenamiento (numérico: 1-4)
        objetivo_str: Objetivo de entrenamiento (string)
        dias: Días de entrenamiento por semana
        created_at: Timestamp de creación
    """
    
    edad: int
    peso: float
    altura: float
    nivel_str: str
    objetivo_str: str
    dias: int
    
    # Campos calculados
    imc: float = field(init=False)
    nivel_num: int = field(init=False)
    objetivo_num: int = field(init=False)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def __post_init__(self):
        """
        Valida y calcula campos derivados después de la inicialización.
        """
        # Validar datos básicos
        self._validate()
        
        # Calcular IMC
        self.imc = calculate_imc(self.peso, self.altura)
        
        # Mapear nivel a numérico
        self.nivel_num = Mappings.LEVEL_STR_TO_NUM.get(self.nivel_str, 2)
        
        # Mapear objetivo a numérico
        self.objetivo_num = Mappings.GOAL_STR_TO_NUM.get(self.objetivo_str, 2)
    
    def _validate(self):
        """Valida los datos del perfil."""
        errors = []
        
        valid, msg = validate_age(self.edad)
        if not valid:
            errors.append(msg)
        
        valid, msg = validate_weight(self.peso)
        if not valid:
            errors.append(msg)
        
        valid, msg = validate_height(self.altura)
        if not valid:
            errors.append(msg)
        
        valid, msg = validate_experience_level(self.nivel_str)
        if not valid:
            errors.append(msg)
        
        valid, msg = validate_goal(self.objetivo_str)
        if not valid:
            errors.append(msg)
        
        valid, msg = validate_training_days(self.dias)
        if not valid:
            errors.append(msg)
        
        if errors:
            raise ValueError(f"Errores de validación: {'; '.join(errors)}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el perfil a diccionario.
        
        Returns:
            Diccionario con todos los campos del perfil
        """
        return {
            'edad': self.edad,
            'peso': self.peso,
            'altura': self.altura,
            'imc': round(self.imc, 2),
            'nivel_num': self.nivel_num,
            'nivel_str': self.nivel_str,
            'objetivo_num': self.objetivo_num,
            'objetivo_str': self.objetivo_str,
            'dias': self.dias,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Profile':
        """
        Crea un perfil desde un diccionario.
        
        Args:
            data: Diccionario con datos del perfil
            
        Returns:
            Instancia de Profile
        """
        return cls(
            edad=data['edad'],
            peso=data['peso'],
            altura=data['altura'],
            nivel_str=data['nivel_str'],
            objetivo_str=data['objetivo_str'],
            dias=data['dias']
        )
    
    @classmethod
    def from_user_data(cls, user_data: Dict[str, Any]) -> 'Profile':
        """
        Crea un perfil desde datos del formulario de usuario.
        
        Args:
            user_data: Datos del formulario (con campos como 'nivel_experiencia')
            
        Returns:
            Instancia de Profile
        """
        return cls(
            edad=int(user_data['edad']),
            peso=float(user_data['peso']),
            altura=float(user_data['altura']),
            nivel_str=user_data['nivel_experiencia'],
            objetivo_str=user_data['objetivo'],
            dias=int(user_data['dias_entrenamiento'])
        )
    
    def get_imc_category(self) -> str:
        """
        Obtiene la categoría del IMC.
        
        Returns:
            Categoría del IMC
        """
        from utils.calculations import get_imc_category
        return get_imc_category(self.imc)
    
    def get_imc_display_name(self) -> str:
        """
        Obtiene el nombre para mostrar de la categoría de IMC.
        
        Returns:
            Nombre para mostrar
        """
        from utils.calculations import get_imc_display_name
        return get_imc_display_name(self.imc)
    
    def get_level_display_name(self) -> str:
        """
        Obtiene el nombre para mostrar del nivel.
        
        Returns:
            Nombre para mostrar
        """
        return Mappings.LEVEL_DISPLAY_NAMES.get(self.nivel_str, self.nivel_str.title())
    
    def get_goal_display_name(self) -> str:
        """
        Obtiene el nombre para mostrar del objetivo.
        
        Returns:
            Nombre para mostrar
        """
        return Mappings.GOAL_DISPLAY_NAMES.get(
            self.objetivo_str, 
            self.objetivo_str.replace('_', ' ').title()
        )
    
    def __repr__(self) -> str:
        """Representación del perfil."""
        return (f"Profile(edad={self.edad}, imc={self.imc:.1f}, "
                f"nivel={self.nivel_str}, objetivo={self.objetivo_str}, "
                f"dias={self.dias})")
    
    def __eq__(self, other) -> bool:
        """Compara dos perfiles."""
        if not isinstance(other, Profile):
            return False
        
        return (
            self.edad == other.edad and
            self.peso == other.peso and
            self.altura == other.altura and
            self.nivel_str == other.nivel_str and
            self.objetivo_str == other.objetivo_str and
            self.dias == other.dias
        )
    
    def calculate_similarity_to(self, other: 'Profile') -> float:
        """
        Calcula la similitud con otro perfil.
        
        Args:
            other: Otro perfil para comparar
            
        Returns:
            Similitud entre 0 y 1
        """
        from utils.calculations import calculate_profile_similarity
        return calculate_profile_similarity(self.to_dict(), other.to_dict())