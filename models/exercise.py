"""
Modelo de Ejercicio.

Este modelo representa un ejercicio individual dentro de una rutina,
con todos sus parámetros (series, repeticiones, descanso, etc.).
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class Exercise:
    """
    Modelo de ejercicio.
    
    Attributes:
        ejercicio: Nombre del ejercicio
        grupo: Grupo muscular trabajado
        series: Número de series (opcional, para ejercicios de fuerza)
        repeticiones: Rango de repeticiones (opcional)
        descanso: Tiempo de descanso (opcional)
        duracion: Duración del ejercicio (opcional, para cardio)
        intensidad: Intensidad del ejercicio (opcional, para cardio)
        notas: Notas adicionales
    """
    
    ejercicio: str
    grupo: str
    series: Optional[int] = None
    repeticiones: Optional[str] = None
    descanso: Optional[str] = None
    duracion: Optional[str] = None
    intensidad: Optional[str] = None
    notas: Optional[str] = None
    
    def __post_init__(self):
        """Valida el ejercicio después de la inicialización."""
        if not self.ejercicio or not self.ejercicio.strip():
            raise ValueError("El nombre del ejercicio no puede estar vacío")
        
        if not self.grupo or not self.grupo.strip():
            raise ValueError("El grupo muscular no puede estar vacío")
        
        # Validar que tenga los campos apropiados según el tipo
        if self.is_cardio():
            if not self.duracion:
                raise ValueError("Ejercicio de cardio debe tener duración")
            if not self.intensidad:
                raise ValueError("Ejercicio de cardio debe tener intensidad")
        else:
            if self.series is None:
                raise ValueError("Ejercicio de fuerza debe tener series")
            if not self.repeticiones:
                raise ValueError("Ejercicio de fuerza debe tener repeticiones")
            if not self.descanso:
                raise ValueError("Ejercicio de fuerza debe tener descanso")
    
    def is_cardio(self) -> bool:
        """
        Verifica si el ejercicio es de tipo cardio.
        
        Returns:
            True si es cardio
        """
        return self.grupo.lower() == 'cardio'
    
    def is_compound(self) -> bool:
        """
        Determina si el ejercicio es compuesto basándose en su nombre.
        
        Returns:
            True si es compuesto
        """
        compound_keywords = [
            'press', 'squat', 'sentadilla', 'deadlift', 'peso muerto',
            'dominadas', 'pull', 'remo', 'fondos', 'prensa'
        ]
        
        ejercicio_lower = self.ejercicio.lower()
        return any(keyword in ejercicio_lower for keyword in compound_keywords)
    
    def get_type(self) -> str:
        """
        Obtiene el tipo de ejercicio.
        
        Returns:
            'cardio', 'compuesto' o 'aislamiento'
        """
        if self.is_cardio():
            return 'cardio'
        elif self.is_compound():
            return 'compuesto'
        else:
            return 'aislamiento'
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el ejercicio a diccionario.
        
        Returns:
            Diccionario con todos los campos del ejercicio
        """
        data = {
            'ejercicio': self.ejercicio,
            'grupo': self.grupo
        }
        
        if self.series is not None:
            data['series'] = self.series
        if self.repeticiones:
            data['repeticiones'] = self.repeticiones
        if self.descanso:
            data['descanso'] = self.descanso
        if self.duracion:
            data['duracion'] = self.duracion
        if self.intensidad:
            data['intensidad'] = self.intensidad
        if self.notas:
            data['notas'] = self.notas
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Exercise':
        """
        Crea un ejercicio desde un diccionario.
        
        Args:
            data: Diccionario con datos del ejercicio
            
        Returns:
            Instancia de Exercise
        """
        return cls(
            ejercicio=data['ejercicio'],
            grupo=data['grupo'],
            series=data.get('series'),
            repeticiones=data.get('repeticiones'),
            descanso=data.get('descanso'),
            duracion=data.get('duracion'),
            intensidad=data.get('intensidad'),
            notas=data.get('notas')
        )
    
    @classmethod
    def create_strength_exercise(cls, nombre: str, grupo: str,
                                series: int, reps: str, descanso: str,
                                notas: str = None) -> 'Exercise':
        """
        Crea un ejercicio de fuerza.
        
        Args:
            nombre: Nombre del ejercicio
            grupo: Grupo muscular
            series: Número de series
            reps: Rango de repeticiones
            descanso: Tiempo de descanso
            notas: Notas adicionales
            
        Returns:
            Instancia de Exercise
        """
        return cls(
            ejercicio=nombre,
            grupo=grupo,
            series=series,
            repeticiones=reps,
            descanso=descanso,
            notas=notas
        )
    
    @classmethod
    def create_cardio_exercise(cls, nombre: str, duracion: str,
                              intensidad: str, notas: str = None) -> 'Exercise':
        """
        Crea un ejercicio de cardio.
        
        Args:
            nombre: Nombre del ejercicio
            duracion: Duración del ejercicio
            intensidad: Intensidad del ejercicio
            notas: Notas adicionales
            
        Returns:
            Instancia de Exercise
        """
        return cls(
            ejercicio=nombre,
            grupo='cardio',
            duracion=duracion,
            intensidad=intensidad,
            notas=notas
        )
    
    def get_display_text(self) -> str:
        """
        Obtiene texto formateado para mostrar.
        
        Returns:
            Texto formateado del ejercicio
        """
        if self.is_cardio():
            return (f"{self.ejercicio}\n"
                   f"   Duración: {self.duracion} | "
                   f"Intensidad: {self.intensidad}")
        else:
            return (f"{self.ejercicio} ({self.grupo.title()})\n"
                   f"   Series: {self.series} | "
                   f"Reps: {self.repeticiones} | "
                   f"Descanso: {self.descanso}")
    
    def __repr__(self) -> str:
        """Representación del ejercicio."""
        if self.is_cardio():
            return f"Exercise(cardio={self.ejercicio}, {self.duracion}, {self.intensidad})"
        else:
            return (f"Exercise({self.ejercicio}, {self.grupo}, "
                   f"{self.series}x{self.repeticiones})")
    
    def __str__(self) -> str:
        """Representación en string del ejercicio."""
        return self.get_display_text()
    
    def __eq__(self, other) -> bool:
        """Compara dos ejercicios."""
        if not isinstance(other, Exercise):
            return False
        
        return (
            self.ejercicio == other.ejercicio and
            self.grupo == other.grupo
        )
    
    def __hash__(self) -> int:
        """Hash del ejercicio para usar en sets."""
        return hash((self.ejercicio, self.grupo))