"""
Controlador de Feedback.

Este controlador maneja todo el procesamiento de feedback
y aprendizaje del sistema.
"""

from typing import Dict, Any, Optional

from models.user import User
from models.routine import Routine
from services.learning_service import LearningService
from services.inference_service import InferenceService
from services.persistence_service import PersistenceService
from utils.validators import validate_feedback, format_validation_errors


class FeedbackController:
    """
    Controlador para gestión de feedback.
    
    Responsabilidades:
    - Validar feedback del usuario
    - Procesar aprendizaje
    - Guardar datos
    - Generar reportes
    """
    
    def __init__(self, learning_service: LearningService,
                 inference_service: InferenceService,
                 persistence_service: PersistenceService):
        """
        Inicializa el controlador.
        
        Args:
            learning_service: Servicio de aprendizaje
            inference_service: Servicio de inferencia
            persistence_service: Servicio de persistencia
        """
        self.learning_service = learning_service
        self.inference_service = inference_service
        self.persistence_service = persistence_service
    
    def submit_feedback(self, user: User, routine: Routine,
                       satisfaction: int, 
                       comments: str = "") -> tuple[bool, Dict[str, Any] | str]:
        """
        Procesa el feedback del usuario.
        
        Args:
            user: Usuario que da feedback
            routine: Rutina evaluada
            satisfaction: Nivel de satisfacción (1-5)
            comments: Comentarios opcionales
            
        Returns:
            Tupla (éxito, resultado_o_error)
        """
        # Validar feedback
        is_valid, errors = validate_feedback(satisfaction, comments)
        
        if not is_valid:
            error_msg = format_validation_errors(errors)
            return False, error_msg
        
        try:
            print(f"\n{'='*70}")
            print(f"PROCESANDO FEEDBACK DE {user.nombre.upper()}")
            print(f"{'='*70}")
            
            # Procesar aprendizaje
            learning_results = self.learning_service.process_feedback(
                user, routine, satisfaction, comments
            )
            
            # Guardar datos
            save_success = self.persistence_service.save_learning_system(
                self.learning_service.learning_system
            )
            
            if not save_success:
                print("⚠️  Advertencia: No se pudo guardar el feedback")
            
            # Detectar anomalías
            user_history = self._get_user_history(user)
            anomalies = self.inference_service.detect_anomalies(
                user.perfil, user_history
            )
            
            result = {
                'feedback_procesado': True,
                'learning_results': learning_results,
                'anomalias': anomalies,
                'guardado_exitoso': save_success,
                'satisfaccion': satisfaction,
                'es_exitosa': routine.is_successful()
            }
            
            print(f"\n✅ Feedback procesado exitosamente")
            
            if anomalies['anomalias']:
                print(f"⚠️  {len(anomalies['anomalias'])} anomalía(s) detectada(s)")
            
            return True, result
            
        except Exception as e:
            error_msg = f"Error al procesar feedback: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def _get_user_history(self, user: User) -> list:
        """
        Obtiene el histórico del usuario.
        
        Args:
            user: Usuario
            
        Returns:
            Lista de experiencias del usuario
        """
        # Filtrar experiencias del usuario actual
        all_history = self.learning_service.learning_system.historico_usuarios
        
        user_history = [
            exp for exp in all_history
            if exp.get('perfil', {}).get('edad') == user.perfil.edad and
               exp.get('perfil', {}).get('peso') == user.perfil.peso
        ]
        
        return user_history
    
    def get_learning_progress(self) -> Dict[str, Any]:
        """
        Obtiene el progreso del aprendizaje.
        
        Returns:
            Diccionario con análisis del progreso
        """
        try:
            progress = self.learning_service.analyze_learning_progress()
            return progress
            
        except Exception as e:
            print(f"❌ Error obteniendo progreso: {e}")
            return {'error': str(e)}
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del sistema.
        
        Returns:
            Diccionario con estadísticas
        """
        try:
            stats = self.learning_service.learning_system.get_statistics()
            return stats
            
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return {'error': str(e)}
    
    def export_statistics(self) -> bool:
        """
        Exporta estadísticas a archivo.
        
        Returns:
            True si se exportó exitosamente
        """
        try:
            success = self.persistence_service.export_statistics(
                self.learning_service.learning_system
            )
            return success
            
        except Exception as e:
            print(f"❌ Error exportando estadísticas: {e}")
            return False
    
    def get_learning_summary(self) -> str:
        """
        Obtiene resumen del aprendizaje.
        
        Returns:
            String con resumen
        """
        return self.learning_service.get_learning_summary()
    
    def check_for_anomalies(self, user: User) -> Dict[str, Any]:
        """
        Verifica anomalías para un usuario.
        
        Args:
            user: Usuario a verificar
            
        Returns:
            Diccionario con anomalías detectadas
        """
        try:
            user_history = self._get_user_history(user)
            
            if len(user_history) < 3:
                return {
                    'anomalias': [],
                    'estado': 'normal',
                    'mensaje': 'Insuficientes datos para detectar anomalías'
                }
            
            anomalies = self.inference_service.detect_anomalies(
                user.perfil, user_history
            )
            
            return anomalies
            
        except Exception as e:
            print(f"❌ Error detectando anomalías: {e}")
            return {'error': str(e)}