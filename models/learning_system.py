"""
Modelo del Sistema de Aprendizaje.

Este modelo representa el estado completo del sistema de aprendizaje de IA,
incluyendo todas las rutinas generadas, histórico de usuarios y patrones
identificados.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
from datetime import datetime
from collections import defaultdict

from config import AIConfig


@dataclass
class LearningSystem:
    """
    Estado del sistema de aprendizaje.
    
    Attributes:
        rutinas_generadas: Lista de todas las rutinas generadas
        historico_usuarios: Lista con histórico de experiencias
        patrones_exitosos: Patrones identificados que funcionan bien
        combinaciones_ejercicios: Ejercicios que funcionan bien juntos
        parametros_optimos: Parámetros óptimos por perfil
        generacion: Generación actual del sistema
        tasa_aprendizaje: Velocidad de aprendizaje
        factor_exploracion: Probabilidad de explorar vs explotar
    """
    
    rutinas_generadas: List[Dict[str, Any]] = field(default_factory=list)
    historico_usuarios: List[Dict[str, Any]] = field(default_factory=list)
    patrones_exitosos: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    combinaciones_ejercicios: Dict[str, Dict[str, int]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(int))
    )
    parametros_optimos: Dict[str, Any] = field(default_factory=dict)
    generacion: int = 0
    tasa_aprendizaje: float = AIConfig.LEARNING_RATE
    factor_exploracion: float = AIConfig.EXPLORATION_FACTOR
    
    def add_generated_routine(self, routine_data: Dict[str, Any]):
        """
        Registra una rutina generada.
        
        Args:
            routine_data: Datos de la rutina generada
        """
        self.rutinas_generadas.append(routine_data)
    
    def add_user_experience(self, experience: Dict[str, Any]):
        """
        Registra una experiencia de usuario.
        
        Args:
            experience: Diccionario con perfil, rutina y feedback
        """
        self.historico_usuarios.append(experience)
        
        # Verificar si debe evolucionar generación
        if len(self.historico_usuarios) % AIConfig.USERS_PER_GENERATION == 0:
            self.evolve_generation()
    
    def add_successful_pattern(self, key: str, pattern: Dict[str, Any]):
        """
        Registra un patrón exitoso.
        
        Args:
            key: Clave del patrón (ej: "principiante_ganar_masa")
            pattern: Diccionario con el patrón exitoso
        """
        if key not in self.patrones_exitosos:
            self.patrones_exitosos[key] = []
        
        self.patrones_exitosos[key].append(pattern)
    
    def increment_exercise_combination(self, grupo: str, ejercicio: str):
        """
        Incrementa el contador de una combinación de ejercicio.
        
        Args:
            grupo: Grupo muscular
            ejercicio: Nombre del ejercicio
        """
        if grupo not in self.combinaciones_ejercicios:
            self.combinaciones_ejercicios[grupo] = defaultdict(int)
        
        self.combinaciones_ejercicios[grupo][ejercicio] += 1
    
    def get_popular_exercises(self, grupo: str, top_n: int = 5) -> List[str]:
        """
        Obtiene los ejercicios más populares para un grupo.
        
        Args:
            grupo: Grupo muscular
            top_n: Número de ejercicios a retornar
            
        Returns:
            Lista de ejercicios más usados
        """
        if grupo not in self.combinaciones_ejercicios:
            return []
        
        ejercicios = self.combinaciones_ejercicios[grupo]
        sorted_exercises = sorted(
            ejercicios.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [ex for ex, _ in sorted_exercises[:top_n]]
    
    def evolve_generation(self):
        """
        Evoluciona el sistema a la siguiente generación.
        Ajusta parámetros de aprendizaje basándose en resultados.
        """
        self.generacion += 1
        
        # Analizar satisfacción reciente
        if len(self.historico_usuarios) >= 10:
            recent = self.historico_usuarios[-10:]
            avg_satisfaction = sum(u.get('satisfaccion', 3) for u in recent) / 10
            
            # Ajustar factor de exploración
            if avg_satisfaction >= 4:
                # Si funciona bien, explorar menos
                self.factor_exploracion = max(0.1, self.factor_exploracion - 0.01)
            elif avg_satisfaction <= 3:
                # Si no funciona bien, explorar más
                self.factor_exploracion = min(0.4, self.factor_exploracion + 0.02)
    
    def should_explore(self) -> bool:
        """
        Decide si explorar (probar cosas nuevas) o explotar (usar conocimiento).
        
        Returns:
            True si debe explorar
        """
        import random
        return random.random() < self.factor_exploracion
    
    def get_total_users(self) -> int:
        """
        Obtiene el número total de usuarios.
        
        Returns:
            Número de usuarios
        """
        return len(self.historico_usuarios)
    
    def get_total_routines(self) -> int:
        """
        Obtiene el número total de rutinas generadas.
        
        Returns:
            Número de rutinas
        """
        return len(self.rutinas_generadas)
    
    def get_average_satisfaction(self) -> float:
        """
        Calcula la satisfacción promedio de todos los usuarios.
        
        Returns:
            Satisfacción promedio
        """
        if not self.historico_usuarios:
            return 0.0
        
        satisfacciones = [
            u.get('satisfaccion', 0)
            for u in self.historico_usuarios
            if u.get('satisfaccion')
        ]
        
        if not satisfacciones:
            return 0.0
        
        return sum(satisfacciones) / len(satisfacciones)
    
    def get_success_rate(self) -> float:
        """
        Calcula el porcentaje de rutinas exitosas (satisfacción >= 4).
        
        Returns:
            Tasa de éxito (0-1)
        """
        if not self.historico_usuarios:
            return 0.0
        
        successful = sum(
            1 for u in self.historico_usuarios
            if u.get('satisfaccion', 0) >= 4
        )
        
        return successful / len(self.historico_usuarios)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas completas del sistema.
        
        Returns:
            Diccionario con estadísticas
        """
        return {
            'generacion': self.generacion,
            'total_usuarios': self.get_total_users(),
            'total_rutinas': self.get_total_routines(),
            'promedio_satisfaccion': round(self.get_average_satisfaction(), 2),
            'tasa_exito': round(self.get_success_rate() * 100, 1),
            'patrones_exitosos': len(self.patrones_exitosos),
            'factor_exploracion': round(self.factor_exploracion, 2)
        }
    
    def get_patterns_for_profile(self, nivel: str, objetivo: str) -> List[Dict[str, Any]]:
        """
        Obtiene patrones exitosos para un perfil específico.
        
        Args:
            nivel: Nivel de experiencia
            objetivo: Objetivo de entrenamiento
            
        Returns:
            Lista de patrones exitosos
        """
        key = f"{nivel}_{objetivo}"
        return self.patrones_exitosos.get(key, [])
    
    def has_sufficient_data(self) -> bool:
        """
        Verifica si hay suficientes datos para aprendizaje.
        
        Returns:
            True si hay suficientes datos
        """
        return len(self.historico_usuarios) >= AIConfig.MIN_SIMILAR_USERS
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el sistema de aprendizaje a diccionario.
        
        Returns:
            Diccionario con todo el estado del sistema
        """
        return {
            'rutinas_generadas': self.rutinas_generadas,
            'historico_usuarios': self.historico_usuarios,
            'patrones_exitosos': self.patrones_exitosos,
            'combinaciones_ejercicios': {
                grupo: dict(ejercicios)
                for grupo, ejercicios in self.combinaciones_ejercicios.items()
            },
            'parametros_optimos': self.parametros_optimos,
            'generacion': self.generacion,
            'tasa_aprendizaje': self.tasa_aprendizaje,
            'factor_exploracion': self.factor_exploracion
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LearningSystem':
        """
        Crea un sistema de aprendizaje desde un diccionario.
        
        Args:
            data: Diccionario con datos del sistema
            
        Returns:
            Instancia de LearningSystem
        """
        # Reconstruir combinaciones_ejercicios con defaultdict
        combinaciones = defaultdict(lambda: defaultdict(int))
        for grupo, ejercicios in data.get('combinaciones_ejercicios', {}).items():
            for ejercicio, count in ejercicios.items():
                combinaciones[grupo][ejercicio] = count
        
        return cls(
            rutinas_generadas=data.get('rutinas_generadas', []),
            historico_usuarios=data.get('historico_usuarios', []),
            patrones_exitosos=data.get('patrones_exitosos', {}),
            combinaciones_ejercicios=dict(combinaciones),
            parametros_optimos=data.get('parametros_optimos', {}),
            generacion=data.get('generacion', 0),
            tasa_aprendizaje=data.get('tasa_aprendizaje', AIConfig.LEARNING_RATE),
            factor_exploracion=data.get('factor_exploracion', AIConfig.EXPLORATION_FACTOR)
        )
    
    def __repr__(self) -> str:
        """Representación del sistema."""
        return (f"LearningSystem(gen={self.generacion}, "
                f"users={self.get_total_users()}, "
                f"avg_sat={self.get_average_satisfaction():.2f})")