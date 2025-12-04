"""
Modelo de Rutina.

Este modelo representa una rutina de entrenamiento completa generada
por el sistema de IA, con todos sus días y ejercicios.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set
from datetime import datetime

from models.exercise import Exercise
from models.profile import Profile


@dataclass
class Routine:
    """
    Modelo de rutina de entrenamiento.
    
    Attributes:
        routine_id: ID único de la rutina
        perfil: Perfil del usuario para quien se generó
        rutina_semanal: Diccionario con ejercicios por día
        estructura: Tipo de estructura (fullbody, upper_lower, split)
        metadatos: Información adicional sobre la generación
        fecha_generacion: Timestamp de generación
        satisfaccion: Satisfacción reportada (None si no hay feedback)
        comentarios: Comentarios del usuario
    """
    
    perfil: Profile
    rutina_semanal: Dict[str, List[Exercise]]
    estructura: str
    metadatos: Dict[str, Any] = field(default_factory=dict)
    routine_id: Optional[str] = None
    fecha_generacion: str = field(default_factory=lambda: datetime.now().isoformat())
    satisfaccion: Optional[int] = None
    comentarios: Optional[str] = None
    
    def __post_init__(self):
        """Valida y genera ID después de la inicialización."""
        if not self.routine_id:
            self.routine_id = self._generate_routine_id()
        
        # Validar estructura
        if self.estructura not in ['fullbody', 'upper_lower', 'split']:
            raise ValueError(
                f"Estructura inválida: {self.estructura}. "
                f"Debe ser 'fullbody', 'upper_lower' o 'split'"
            )
        
        # Validar que tenga ejercicios
        if not self.rutina_semanal:
            raise ValueError("La rutina debe tener al menos un día con ejercicios")
    
    def _generate_routine_id(self) -> str:
        """
        Genera un ID único para la rutina.
        
        Returns:
            ID único basado en timestamp
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"RUT_{timestamp}"
    
    def get_total_days(self) -> int:
        """
        Obtiene el número total de días de la rutina.
        
        Returns:
            Número de días
        """
        return len(self.rutina_semanal)
    
    def get_total_exercises(self) -> int:
        """
        Obtiene el número total de ejercicios en la rutina.
        
        Returns:
            Número total de ejercicios
        """
        return sum(len(exercises) for exercises in self.rutina_semanal.values())
    
    def get_exercises_per_day(self) -> float:
        """
        Calcula el promedio de ejercicios por día.
        
        Returns:
            Promedio de ejercicios por día
        """
        total_days = self.get_total_days()
        if total_days == 0:
            return 0
        return self.get_total_exercises() / total_days
    
    def get_muscle_groups_worked(self) -> Set[str]:
        """
        Obtiene el conjunto de grupos musculares trabajados.
        
        Returns:
            Set con grupos musculares
        """
        groups = set()
        for exercises in self.rutina_semanal.values():
            for exercise in exercises:
                if exercise.grupo != 'cardio':
                    groups.add(exercise.grupo)
        return groups
    
    def has_cardio(self) -> bool:
        """
        Verifica si la rutina incluye cardio.
        
        Returns:
            True si tiene cardio
        """
        for exercises in self.rutina_semanal.values():
            for exercise in exercises:
                if exercise.is_cardio():
                    return True
        return False
    
    def get_cardio_frequency(self) -> int:
        """
        Cuenta cuántos días tienen cardio.
        
        Returns:
            Número de días con cardio
        """
        count = 0
        for exercises in self.rutina_semanal.values():
            if any(ex.is_cardio() for ex in exercises):
                count += 1
        return count
    
    def is_successful(self) -> bool:
        """
        Determina si la rutina fue exitosa (satisfacción >= 4).
        
        Returns:
            True si fue exitosa
        """
        return self.satisfaccion is not None and self.satisfaccion >= 4
    
    def has_feedback(self) -> bool:
        """
        Verifica si la rutina tiene feedback del usuario.
        
        Returns:
            True si tiene feedback
        """
        return self.satisfaccion is not None
    
    def set_feedback(self, satisfaccion: int, comentarios: str = ""):
        """
        Establece el feedback del usuario.
        
        Args:
            satisfaccion: Nivel de satisfacción (1-5)
            comentarios: Comentarios opcionales
        """
        if not (1 <= satisfaccion <= 5):
            raise ValueError("La satisfacción debe estar entre 1 y 5")
        
        self.satisfaccion = satisfaccion
        self.comentarios = comentarios
    
    def get_complexity_score(self) -> float:
        """
        Calcula un score de complejidad de la rutina.
        
        Returns:
            Score de complejidad
        """
        # Factores: ejercicios por día, variedad de grupos, tiene cardio
        exercises_per_day = self.get_exercises_per_day()
        num_groups = len(self.get_muscle_groups_worked())
        has_cardio_score = 1 if self.has_cardio() else 0
        
        # Normalizar y promediar
        complexity = (
            (exercises_per_day / 7) * 0.4 +  # Max ~7 ejercicios/día
            (num_groups / 6) * 0.4 +          # Max 6 grupos
            has_cardio_score * 0.2
        )
        
        return min(1.0, complexity)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la rutina a diccionario.
        
        Returns:
            Diccionario con toda la información de la rutina
        """
        return {
            'routine_id': self.routine_id,
            'perfil': self.perfil.to_dict(),
            'rutina_semanal': {
                dia: [ex.to_dict() for ex in ejercicios]
                for dia, ejercicios in self.rutina_semanal.items()
            },
            'estructura': self.estructura,
            'metadatos': self.metadatos,
            'fecha_generacion': self.fecha_generacion,
            'satisfaccion': self.satisfaccion,
            'comentarios': self.comentarios
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Routine':
        """
        Crea una rutina desde un diccionario.
        
        Args:
            data: Diccionario con datos de la rutina
            
        Returns:
            Instancia de Routine
        """
        # Reconstruir perfil
        perfil = Profile.from_dict(data['perfil'])
        
        # Reconstruir ejercicios
        rutina_semanal = {}
        for dia, ejercicios_data in data['rutina_semanal'].items():
            rutina_semanal[dia] = [
                Exercise.from_dict(ex_data) for ex_data in ejercicios_data
            ]
        
        return cls(
            perfil=perfil,
            rutina_semanal=rutina_semanal,
            estructura=data['estructura'],
            metadatos=data.get('metadatos', {}),
            routine_id=data.get('routine_id'),
            fecha_generacion=data.get('fecha_generacion', datetime.now().isoformat()),
            satisfaccion=data.get('satisfaccion'),
            comentarios=data.get('comentarios')
        )
    
    def get_summary(self) -> str:
        """
        Obtiene un resumen de la rutina.
        
        Returns:
            String con resumen
        """
        return (
            f"Rutina {self.estructura.upper()} - "
            f"{self.get_total_days()} días - "
            f"{self.get_total_exercises()} ejercicios - "
            f"{len(self.get_muscle_groups_worked())} grupos musculares"
        )
    
    def get_day_summary(self, day: str) -> str:
        """
        Obtiene un resumen de un día específico.
        
        Args:
            day: Nombre del día
            
        Returns:
            String con resumen del día
        """
        if day not in self.rutina_semanal:
            return f"{day}: Sin ejercicios"
        
        exercises = self.rutina_semanal[day]
        groups = set(ex.grupo for ex in exercises if not ex.is_cardio())
        
        return (
            f"{day}: {len(exercises)} ejercicios - "
            f"Grupos: {', '.join(g.title() for g in groups)}"
        )
    
    def __repr__(self) -> str:
        """Representación de la rutina."""
        return (f"Routine(id={self.routine_id}, "
                f"estructura={self.estructura}, "
                f"dias={self.get_total_days()}, "
                f"ejercicios={self.get_total_exercises()})")
    
    def __str__(self) -> str:
        """Representación en string de la rutina."""
        return self.get_summary()