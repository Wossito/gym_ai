"""
Servicio de Aprendizaje.

Este servicio maneja todo el aprendizaje del sistema:
- Procesamiento de feedback
- Actualización de patrones
- Evolución del sistema
"""

from typing import Dict, Any, List
from datetime import datetime
from collections import defaultdict

from models.profile import Profile
from models.routine import Routine
from models.learning_system import LearningSystem
from models.user import User
from config import AIConfig


class LearningService:
    """
    Servicio de aprendizaje del sistema.
    
    Responsable de:
    - Procesar feedback de usuarios
    - Identificar y guardar patrones exitosos
    - Actualizar combinaciones de ejercicios
    - Evolucionar el sistema basándose en resultados
    """
    
    def __init__(self, learning_system: LearningSystem):
        """
        Inicializa el servicio de aprendizaje.
        
        Args:
            learning_system: Sistema de aprendizaje a gestionar
        """
        self.learning_system = learning_system
    
    def process_feedback(self, user: User, routine: Routine,
                        satisfaction: int, comments: str = "") -> Dict[str, Any]:
        """
        Procesa el feedback del usuario y actualiza el conocimiento.
        
        Args:
            user: Usuario que da feedback
            routine: Rutina evaluada
            satisfaction: Nivel de satisfacción (1-5)
            comments: Comentarios opcionales
            
        Returns:
            Diccionario con resultado del procesamiento
        """
        print("\n🎓 Procesando feedback y aprendiendo...")
        
        # Actualizar rutina con feedback
        routine.set_feedback(satisfaction, comments)
        
        # Crear experiencia
        experience = {
            'perfil': user.perfil.to_dict(),
            'rutina_id': routine.routine_id,
            'rutina_exitosa': routine.to_dict() if routine.is_successful() else None,
            'satisfaccion': satisfaction,
            'comentarios': comments,
            'fecha': datetime.now().isoformat()
        }
        
        # Registrar experiencia
        self.learning_system.add_user_experience(experience)
        
        # Aprender de la experiencia
        learning_results = {
            'patrones_actualizados': False,
            'combinaciones_actualizadas': False,
            'exploracion_ajustada': False,
            'generacion_evolucionada': False
        }
        
        # APRENDIZAJE 1: Actualizar patrones exitosos
        if routine.is_successful():
            self._update_successful_patterns(user.perfil, routine, satisfaction)
            learning_results['patrones_actualizados'] = True
        
        # APRENDIZAJE 2: Actualizar combinaciones de ejercicios
        if routine.is_successful():
            self._update_exercise_combinations(routine)
            learning_results['combinaciones_actualizadas'] = True
        
        # APRENDIZAJE 3: Ajustar factor de exploración
        exploration_adjusted = self._adjust_exploration_factor(satisfaction, routine)
        learning_results['exploracion_ajustada'] = exploration_adjusted
        
        # APRENDIZAJE 4: Verificar evolución de generación
        current_gen = self.learning_system.generacion
        # La evolución se maneja automáticamente en add_user_experience
        if self.learning_system.generacion > current_gen:
            learning_results['generacion_evolucionada'] = True
            print(f"   🎉 Sistema evolucionó a Generación {self.learning_system.generacion}")
        
        print("   💾 Conocimiento actualizado")
        
        return learning_results
    
    def _update_successful_patterns(self, profile: Profile, 
                                   routine: Routine, satisfaction: int):
        """
        Actualiza patrones exitosos.
        
        Args:
            profile: Perfil del usuario
            routine: Rutina exitosa
            satisfaction: Nivel de satisfacción
        """
        pattern_key = f"{profile.nivel_str}_{profile.objetivo_str}"
        
        pattern = {
            'rutina': routine.to_dict(),
            'satisfaccion': satisfaction,
            'fecha': datetime.now().isoformat()
        }
        
        self.learning_system.add_successful_pattern(pattern_key, pattern)
        print(f"   ✓ Patrón exitoso guardado para: {pattern_key}")
    
    def _update_exercise_combinations(self, routine: Routine):
        """
        Actualiza combinaciones de ejercicios que funcionan bien.
        
        Args:
            routine: Rutina exitosa
        """
        for day, exercises in routine.rutina_semanal.items():
            for exercise in exercises:
                if not exercise.is_cardio():
                    self.learning_system.increment_exercise_combination(
                        exercise.grupo,
                        exercise.ejercicio
                    )
        
        print("   ✓ Combinaciones de ejercicios actualizadas")
    
    def _adjust_exploration_factor(self, satisfaction: int, 
                                  routine: Routine) -> bool:
        """
        Ajusta el factor de exploración basándose en resultados.
        
        Args:
            satisfaction: Nivel de satisfacción
            routine: Rutina evaluada
            
        Returns:
            True si se ajustó el factor
        """
        mode = routine.metadatos.get('modo_generacion', 'exploracion')
        
        # Si rutina basada en aprendizaje funcionó bien, explorar menos
        if satisfaction >= 4 and mode == 'explotacion':
            old_factor = self.learning_system.factor_exploracion
            self.learning_system.factor_exploracion = max(
                0.1,
                self.learning_system.factor_exploracion - 0.01
            )
            if old_factor != self.learning_system.factor_exploracion:
                print(f"   ✓ Reduciendo exploración: {self.learning_system.factor_exploracion:.2f}")
                return True
        
        # Si resultados malos, explorar más
        elif satisfaction <= 2:
            old_factor = self.learning_system.factor_exploracion
            self.learning_system.factor_exploracion = min(
                0.4,
                self.learning_system.factor_exploracion + 0.02
            )
            if old_factor != self.learning_system.factor_exploracion:
                print(f"   ✓ Aumentando exploración: {self.learning_system.factor_exploracion:.2f}")
                return True
        
        return False
    
    def analyze_learning_progress(self) -> Dict[str, Any]:
        """
        Analiza el progreso del aprendizaje del sistema.
        
        Returns:
            Diccionario con análisis del progreso
        """
        stats = self.learning_system.get_statistics()
        
        # Analizar tendencias
        recent_users = self.learning_system.historico_usuarios[-10:] if len(
            self.learning_system.historico_usuarios) >= 10 else self.learning_system.historico_usuarios
        
        if recent_users:
            recent_satisfactions = [u.get('satisfaccion', 0) for u in recent_users]
            recent_avg = sum(recent_satisfactions) / len(recent_satisfactions)
            
            trend = "mejorando" if recent_avg > stats['promedio_satisfaccion'] else "estable"
        else:
            recent_avg = 0
            trend = "sin_datos"
        
        return {
            'estadisticas_generales': stats,
            'satisfaccion_reciente': round(recent_avg, 2),
            'tendencia': trend,
            'usuarios_recientes': len(recent_users),
            'patrones_por_categoria': self._count_patterns_by_category()
        }
    
    def _count_patterns_by_category(self) -> Dict[str, int]:
        """Cuenta patrones por categoría."""
        return {
            key: len(patterns)
            for key, patterns in self.learning_system.patrones_exitosos.items()
        }
    
    def get_best_practices(self, profile: Profile) -> Dict[str, Any]:
        """
        Obtiene las mejores prácticas para un perfil.
        
        Args:
            profile: Perfil del usuario
            
        Returns:
            Diccionario con mejores prácticas
        """
        patterns = self.learning_system.get_patterns_for_profile(
            profile.nivel_str,
            profile.objetivo_str
        )
        
        if not patterns:
            return {
                'tiene_patrones': False,
                'mensaje': 'No hay suficientes datos para este perfil específico'
            }
        
        # Analizar patrones
        best_structure = self._get_most_common_structure(patterns)
        popular_exercises = self._get_popular_exercises_from_patterns(patterns)
        avg_satisfaction = sum(p['satisfaccion'] for p in patterns) / len(patterns)
        
        return {
            'tiene_patrones': True,
            'cantidad_patrones': len(patterns),
            'estructura_preferida': best_structure,
            'ejercicios_populares': popular_exercises,
            'satisfaccion_promedio': round(avg_satisfaction, 2),
            'confianza': min(1.0, len(patterns) / 10)
        }
    
    def _get_most_common_structure(self, patterns: List[Dict[str, Any]]) -> str:
        """Obtiene la estructura más común en los patrones."""
        structures = [
            p['rutina'].get('estructura', 'fullbody')
            for p in patterns
        ]
        
        if not structures:
            return 'fullbody'
        
        return max(set(structures), key=structures.count)
    
    def _get_popular_exercises_from_patterns(self, 
                                            patterns: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Obtiene ejercicios populares de los patrones."""
        exercise_freq = defaultdict(lambda: defaultdict(int))
        
        for pattern in patterns:
            routine_data = pattern['rutina']
            if 'rutina_semanal' not in routine_data:
                continue
            
            for day, exercises in routine_data['rutina_semanal'].items():
                for ex in exercises:
                    if 'grupo' in ex and ex['grupo'] != 'cardio':
                        exercise_freq[ex['grupo']][ex['ejercicio']] += 1
        
        # Top 3 por grupo
        popular = {}
        for grupo, exercises in exercise_freq.items():
            sorted_exercises = sorted(
                exercises.items(),
                key=lambda x: x[1],
                reverse=True
            )
            popular[grupo] = [ex for ex, _ in sorted_exercises[:3]]
        
        return popular
    
    def should_use_learning_mode(self, profile: Profile) -> bool:
        """
        Decide si usar modo aprendizaje (explotación) o exploración.
        
        Args:
            profile: Perfil del usuario
            
        Returns:
            True si debe usar aprendizaje (tiene suficientes datos)
        """
        # Verificar si hay patrones para este perfil
        patterns = self.learning_system.get_patterns_for_profile(
            profile.nivel_str,
            profile.objetivo_str
        )
        
        # Necesita al menos 3 patrones para confiar en el aprendizaje
        has_patterns = len(patterns) >= 3
        
        # Verificar el factor de exploración
        should_explore = self.learning_system.should_explore()
        
        return has_patterns and not should_explore
    
    def get_learning_summary(self) -> str:
        """
        Obtiene un resumen del aprendizaje del sistema.
        
        Returns:
            String con resumen
        """
        stats = self.learning_system.get_statistics()
        
        summary = f"""
📊 RESUMEN DEL SISTEMA DE APRENDIZAJE

Generación: {stats['generacion']}
Usuarios totales: {stats['total_usuarios']}
Rutinas generadas: {stats['total_rutinas']}
Satisfacción promedio: {stats['promedio_satisfaccion']}/5
Tasa de éxito: {stats['tasa_exito']}%
Patrones identificados: {stats['patrones_exitosos']}
Factor de exploración: {stats['factor_exploracion']}
"""
        return summary.strip()