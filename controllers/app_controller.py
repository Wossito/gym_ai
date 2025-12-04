"""
Controlador Principal de la Aplicación.

Este es el controlador maestro que coordina todos los demás controladores
y gestiona el flujo general de la aplicación.
"""

from typing import Optional, Dict, Any

from models.learning_system import LearningSystem
from services.persistence_service import PersistenceService
from services.ai_service import AIService
from services.inference_service import InferenceService
from services.learning_service import LearningService

from controllers.routine_controller import RoutineController
from controllers.feedback_controller import FeedbackController
from controllers.user_controller import UserController


class AppController:
    """
    Controlador principal de la aplicación.
    
    Este controlador:
    - Inicializa todos los servicios
    - Coordina entre controladores
    - Gestiona el ciclo de vida de la aplicación
    """
    
    def __init__(self):
        """Inicializa el controlador y todos los servicios."""
        print("\n🚀 Inicializando Sistema de IA...")
        print("="*70)
        
        # Inicializar servicios en orden correcto
        self._initialize_services()
        
        # Inicializar controladores
        self._initialize_controllers()
        
        print("="*70)
        print("✅ Sistema inicializado correctamente\n")
    
    def _initialize_services(self):
        """Inicializa todos los servicios."""
        # 1. Servicio de persistencia
        self.persistence_service = PersistenceService()
        print("✓ Servicio de persistencia iniciado")
        
        # 2. Cargar o crear sistema de aprendizaje
        loaded_system = self.persistence_service.load_learning_system()
        
        if loaded_system:
            self.learning_system = loaded_system
            print("✓ Sistema de aprendizaje cargado desde archivo")
        else:
            self.learning_system = LearningSystem()
            print("✓ Nuevo sistema de aprendizaje creado")
        
        # 3. Servicios de IA
        self.inference_service = InferenceService(self.learning_system)
        print("✓ Servicio de inferencia iniciado")
        
        self.learning_service = LearningService(self.learning_system)
        print("✓ Servicio de aprendizaje iniciado")
        
        self.ai_service = AIService(self.learning_system)
        print("✓ Servicio de IA iniciado")
    
    def _initialize_controllers(self):
        """Inicializa todos los controladores."""
        self.routine_controller = RoutineController(
            self.ai_service,
            self.inference_service
        )
        print("✓ Controlador de rutinas iniciado")
        
        self.feedback_controller = FeedbackController(
            self.learning_service,
            self.inference_service,
            self.persistence_service
        )
        print("✓ Controlador de feedback iniciado")
        
        self.user_controller = UserController(
            self.inference_service,
            self.ai_service
        )
        print("✓ Controlador de usuarios iniciado")
    
    # ========================================================================
    # MÉTODOS PÚBLICOS PARA LA INTERFAZ
    # ========================================================================
    
    def get_routine_controller(self) -> RoutineController:
        """Obtiene el controlador de rutinas."""
        return self.routine_controller
    
    def get_feedback_controller(self) -> FeedbackController:
        """Obtiene el controlador de feedback."""
        return self.feedback_controller
    
    def get_user_controller(self) -> UserController:
        """Obtiene el controlador de usuarios."""
        return self.user_controller
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del sistema.
        
        Returns:
            Diccionario con estadísticas
        """
        return self.learning_system.get_statistics()
    
    def save_system_state(self) -> bool:
        """
        Guarda el estado actual del sistema.
        
        Returns:
            True si se guardó exitosamente
        """
        return self.persistence_service.save_learning_system(self.learning_system)
    
    def reset_system(self) -> bool:
        """
        Reinicia el sistema (elimina todos los datos).
        
        Returns:
            True si se reinició exitosamente
        """
        print("\n⚠️  REINICIANDO SISTEMA...")
        
        # Eliminar datos
        success = self.persistence_service.clear_data()
        
        if success:
            # Crear nuevo sistema de aprendizaje
            self.learning_system = LearningSystem()
            
            # Re-inicializar servicios
            self._initialize_services()
            
            print("✅ Sistema reiniciado")
            return True
        else:
            print("❌ Error al reiniciar sistema")
            return False
    
    def export_statistics(self) -> bool:
        """
        Exporta estadísticas del sistema.
        
        Returns:
            True si se exportó exitosamente
        """
        return self.feedback_controller.export_statistics()
    
    def get_generation_summary(self) -> str:
        """
        Obtiene resumen de la generación actual.
        
        Returns:
            String con resumen
        """
        return self.ai_service.get_generation_summary()
    
    def shutdown(self):
        """Cierra la aplicación guardando el estado."""
        print("\n🔄 Cerrando aplicación...")
        
        # Guardar estado actual
        if self.save_system_state():
            print("✓ Estado guardado")
        else:
            print("⚠️  No se pudo guardar el estado")
        
        print("👋 Hasta pronto!")
    
    # ========================================================================
    # FLUJO COMPLETO DE USUARIO
    # ========================================================================
    
    def complete_user_flow(self, form_data: Dict[str, Any],
                          satisfaction: Optional[int] = None,
                          comments: str = "") -> Dict[str, Any]:
        """
        Ejecuta el flujo completo: crear usuario, generar rutina, procesar feedback.
        
        Args:
            form_data: Datos del formulario
            satisfaction: Satisfacción (opcional, para feedback)
            comments: Comentarios (opcional)
            
        Returns:
            Diccionario con resultados del flujo
        """
        results = {}
        
        # Paso 1: Crear usuario
        success, user_or_error = self.routine_controller.create_user_from_form(form_data)
        
        if not success:
            return {
                'success': False,
                'error': user_or_error,
                'step': 'user_creation'
            }
        
        user = user_or_error
        results['user'] = user
        results['user_created'] = True
        
        # Paso 2: Generar rutina
        success, routine_or_error = self.routine_controller.generate_routine(user)
        
        if not success:
            return {
                'success': False,
                'error': routine_or_error,
                'step': 'routine_generation',
                'user': user
            }
        
        routine = routine_or_error
        results['routine'] = routine
        results['routine_generated'] = True
        
        # Paso 3: Procesar feedback (si se proporciona)
        if satisfaction is not None:
            success, feedback_result = self.feedback_controller.submit_feedback(
                user, routine, satisfaction, comments
            )
            
            if success:
                results['feedback_processed'] = True
                results['feedback_result'] = feedback_result
            else:
                results['feedback_error'] = feedback_result
        
        results['success'] = True
        return results