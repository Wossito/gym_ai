"""
Controlador de Rutinas.

Este controlador coordina la generación de rutinas,
actuando como intermediario entre las vistas y los servicios.
"""

from typing import Dict, Any, Optional, List

from models.user import User
from models.profile import Profile
from models.routine import Routine
from services.ai_service import AIService
from services.inference_service import InferenceService
from utils.validators import validate_user_profile, format_validation_errors


class RoutineController:
    """
    Controlador para gestión de rutinas.
    
    Responsabilidades:
    - Validar datos de entrada
    - Coordinar generación de rutinas
    - Manejar predicciones
    - Gestionar flujo de creación
    """
    
    def __init__(self, ai_service: AIService, 
                 inference_service: InferenceService):
        """
        Inicializa el controlador.
        
        Args:
            ai_service: Servicio de IA
            inference_service: Servicio de inferencia
        """
        self.ai_service = ai_service
        self.inference_service = inference_service
        self.current_user: Optional[User] = None
        self.current_routine: Optional[Routine] = None
    
    def create_user_from_form(self, form_data: Dict[str, Any]) -> tuple[bool, User | str]:
        """
        Crea un usuario desde datos del formulario.
        
        Args:
            form_data: Datos del formulario
            
        Returns:
            Tupla (éxito, usuario_o_mensaje_error)
        """
        # Validar datos
        is_valid, errors = validate_user_profile(form_data)
        
        if not is_valid:
            error_msg = format_validation_errors(errors)
            return False, error_msg
        
        try:
            # Crear usuario
            user = User.from_form_data(form_data)
            self.current_user = user
            
            print(f"✓ Usuario creado: {user.get_profile_summary()}")
            return True, user
            
        except Exception as e:
            error_msg = f"Error al crear usuario: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def generate_routine(self, user: Optional[User] = None) -> tuple[bool, Routine | str]:
        """
        Genera una rutina para el usuario.
        
        Args:
            user: Usuario (usa current_user si no se proporciona)
            
        Returns:
            Tupla (éxito, rutina_o_mensaje_error)
        """
        if user is None:
            user = self.current_user
        
        if user is None:
            return False, "No hay usuario activo"
        
        try:
            print(f"\n{'='*70}")
            print(f"GENERANDO RUTINA PARA {user.nombre.upper()}")
            print(f"{'='*70}")
            
            # Generar rutina usando IA
            routine = self.ai_service.generate_intelligent_routine(user.perfil)
            
            # Validar calidad
            is_valid, problems = self.ai_service.validate_routine_quality(routine)
            
            if not is_valid:
                print(f"⚠️  Advertencias de calidad:")
                for problem in problems:
                    print(f"   • {problem}")
            
            self.current_routine = routine
            
            print(f"\n✅ Rutina generada exitosamente: {routine.routine_id}")
            print(f"   • Estructura: {routine.estructura}")
            print(f"   • Días: {routine.get_total_days()}")
            print(f"   • Ejercicios: {routine.get_total_exercises()}")
            
            return True, routine
            
        except Exception as e:
            error_msg = f"Error al generar rutina: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def predict_routine_satisfaction(self, profile: Profile,
                                    routine: Optional[Routine] = None) -> Dict[str, Any]:
        """
        Predice la satisfacción esperada de una rutina.
        
        Args:
            profile: Perfil del usuario
            routine: Rutina a evaluar (opcional)
            
        Returns:
            Diccionario con predicción
        """
        try:
            prediction = self.inference_service.predict_satisfaction(
                profile, routine
            )
            return prediction
            
        except Exception as e:
            print(f"❌ Error en predicción: {e}")
            return {
                'satisfaccion_predicha': 3.5,
                'confianza': 0.0,
                'error': str(e)
            }
    
    def get_routine_analysis(self, routine: Optional[Routine] = None) -> Dict[str, Any]:
        """
        Obtiene análisis detallado de una rutina.
        
        Args:
            routine: Rutina a analizar (usa current_routine si no se proporciona)
            
        Returns:
            Diccionario con análisis
        """
        if routine is None:
            routine = self.current_routine
        
        if routine is None:
            return {'error': 'No hay rutina para analizar'}
        
        try:
            analysis = self.ai_service.analyze_routine_effectiveness(routine)
            return analysis
            
        except Exception as e:
            print(f"❌ Error en análisis: {e}")
            return {'error': str(e)}
    
    def get_routine_recommendations(self, user: User, routine: Routine,
                                   satisfaction: int) -> List[str]:
        """
        Obtiene recomendaciones para mejorar.
        
        Args:
            user: Usuario
            routine: Rutina evaluada
            satisfaction: Satisfacción reportada
            
        Returns:
            Lista de recomendaciones
        """
        try:
            recommendations = self.ai_service.recommend_adjustments(
                user.perfil, routine, satisfaction
            )
            return recommendations
            
        except Exception as e:
            print(f"❌ Error obteniendo recomendaciones: {e}")
            return []
    
    def get_routine_summary(self, routine: Optional[Routine] = None) -> str:
        """
        Obtiene resumen legible de la rutina.
        
        Args:
            routine: Rutina a resumir
            
        Returns:
            String con resumen
        """
        if routine is None:
            routine = self.current_routine
        
        if routine is None:
            return "No hay rutina disponible"
        
        return routine.get_summary()
    
    def get_current_user(self) -> Optional[User]:
        """Obtiene el usuario actual."""
        return self.current_user
    
    def get_current_routine(self) -> Optional[Routine]:
        """Obtiene la rutina actual."""
        return self.current_routine
    
    def clear_current_session(self):
        """Limpia la sesión actual."""
        self.current_user = None
        self.current_routine = None
        print("🔄 Sesión limpiada")