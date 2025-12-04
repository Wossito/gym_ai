"""
Modelo de Usuario.

Este modelo representa un usuario del sistema con toda su información
personal y su perfil de entrenamiento.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime

from models.profile import Profile
from utils.validators import validate_name, sanitize_string


@dataclass
class User:
    """
    Modelo de usuario del sistema.
    
    Attributes:
        nombre: Nombre del usuario
        perfil: Perfil numérico del usuario
        limitaciones: Limitaciones físicas o lesiones
        fecha_inicio: Fecha de inicio en el sistema
        user_id: ID único del usuario
    """
    
    nombre: str
    perfil: Profile
    limitaciones: str = "ninguna"
    fecha_inicio: str = field(default_factory=lambda: datetime.now().isoformat())
    user_id: Optional[str] = None
    
    def __post_init__(self):
        """Valida y sanitiza datos después de la inicialización."""
        # Validar nombre
        valid, msg = validate_name(self.nombre)
        if not valid:
            raise ValueError(msg)
        
        # Sanitizar nombre y limitaciones
        self.nombre = sanitize_string(self.nombre, max_length=50)
        self.limitaciones = sanitize_string(self.limitaciones, max_length=500)
        
        # Generar ID si no existe
        if not self.user_id:
            self.user_id = self._generate_user_id()
    
    def _generate_user_id(self) -> str:
        """
        Genera un ID único para el usuario.
        
        Returns:
            ID único basado en timestamp y nombre
        """
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        name_part = self.nombre[:3].upper()
        return f"USER_{name_part}_{timestamp}"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el usuario a diccionario.
        
        Returns:
            Diccionario con toda la información del usuario
        """
        return {
            'user_id': self.user_id,
            'nombre': self.nombre,
            'perfil': self.perfil.to_dict(),
            'limitaciones': self.limitaciones,
            'fecha_inicio': self.fecha_inicio
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """
        Crea un usuario desde un diccionario.
        
        Args:
            data: Diccionario con datos del usuario
            
        Returns:
            Instancia de User
        """
        return cls(
            nombre=data['nombre'],
            perfil=Profile.from_dict(data['perfil']),
            limitaciones=data.get('limitaciones', 'ninguna'),
            fecha_inicio=data.get('fecha_inicio', datetime.now().isoformat()),
            user_id=data.get('user_id')
        )
    
    @classmethod
    def from_form_data(cls, form_data: Dict[str, Any]) -> 'User':
        """
        Crea un usuario desde datos del formulario.
        
        Args:
            form_data: Datos del formulario de registro
            
        Returns:
            Instancia de User
        """
        profile = Profile.from_user_data(form_data)
        
        return cls(
            nombre=form_data['nombre'],
            perfil=profile,
            limitaciones=form_data.get('limitaciones', 'ninguna'),
            fecha_inicio=form_data.get('fecha_inicio', datetime.now().isoformat())
        )
    
    def get_profile_summary(self) -> str:
        """
        Obtiene un resumen del perfil del usuario.
        
        Returns:
            String con resumen del perfil
        """
        return (
            f"{self.nombre} - {self.perfil.edad} años - "
            f"IMC: {self.perfil.imc:.1f} ({self.perfil.get_imc_display_name()}) - "
            f"{self.perfil.get_level_display_name()} - "
            f"{self.perfil.get_goal_display_name()}"
        )
    
    def has_limitations(self) -> bool:
        """
        Verifica si el usuario tiene limitaciones.
        
        Returns:
            True si tiene limitaciones
        """
        return (
            self.limitaciones and 
            self.limitaciones.lower() not in ['ninguna', 'ninguno', '']
        )
    
    def __repr__(self) -> str:
        """Representación del usuario."""
        return f"User(id={self.user_id}, nombre={self.nombre}, perfil={self.perfil})"
    
    def __str__(self) -> str:
        """Representación en string del usuario."""
        return self.get_profile_summary()