"""
Controlador de Usuario.

Este controlador maneja la gestión de usuarios,
clasificación y reportes personales.
"""

from typing import Dict, Any, Optional, List

from models.user import User
from models.profile import Profile
from models.routine import Routine
from services.inference_service import InferenceService
from services.ai_service import AIService


class UserController:
    """
    Controlador para gestión de usuarios.
    
    Responsabilidades:
    - Clasificar usuarios
    - Generar reportes personales
    - Obtener recomendaciones
    - Analizar progreso
    """
    
    def __init__(self, inference_service: InferenceService,
                 ai_service: AIService):
        """
        Inicializa el controlador.
        
        Args:
            inference_service: Servicio de inferencia
            ai_service: Servicio de IA
        """
        self.inference_service = inference_service
        self.ai_service = ai_service
    
    def classify_user(self, user: User,
                     user_history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Clasifica al usuario según su experiencia.
        
        Args:
            user: Usuario a clasificar
            user_history: Histórico opcional del usuario
            
        Returns:
            Diccionario con clasificación
        """
        try:
            classification = self.inference_service.classify_user(
                user.perfil, user_history
            )
            
            print(f"\n👤 Usuario clasificado:")
            print(f"   • Categoría: {classification['categoria']}")
            print(f"   • Rendimiento: {classification['rendimiento']}")
            
            return classification
            
        except Exception as e:
            print(f"❌ Error clasificando usuario: {e}")
            return {
                'error': str(e),
                'categoria': 'desconocido'
            }
    
    def generate_user_report(self, user: User,
                           routines: List[Routine]) -> Dict[str, Any]:
        """
        Genera reporte completo del usuario.
        
        Args:
            user: Usuario
            routines: Lista de rutinas del usuario
            
        Returns:
            Diccionario con reporte
        """
        try:
            report = self.ai_service.export_user_report(
                user.perfil, routines
            )
            
            print(f"\n📋 Reporte generado para {user.nombre}")
            print(f"   • Rutinas: {report['estadisticas']['rutinas_totales']}")
            print(f"   • Éxito: {report['estadisticas']['tasa_exito']}%")
            
            return report
            
        except Exception as e:
            print(f"❌ Error generando reporte: {e}")
            return {'error': str(e)}
    
    def get_user_recommendations(self, user: User,
                                classification: Dict[str, Any]) -> List[str]:
        """
        Obtiene recomendaciones personalizadas.
        
        Args:
            user: Usuario
            classification: Clasificación del usuario
            
        Returns:
            Lista de recomendaciones
        """
        recommendations = classification.get('recomendaciones', [])
        
        # Agregar recomendaciones adicionales según perfil
        if user.has_limitations():
            recommendations.insert(0, 
                "Importante: Considera tus limitaciones al entrenar"
            )
        
        if user.perfil.imc < 18.5:
            recommendations.append(
                "Enfócate en ganar masa muscular y consulta con un nutricionista"
            )
        elif user.perfil.imc > 30:
            recommendations.append(
                "Combina entrenamiento con cardio y alimentación saludable"
            )
        
        return recommendations
    
    def get_profile_summary(self, user: User) -> str:
        """
        Obtiene resumen del perfil del usuario.
        
        Args:
            user: Usuario
            
        Returns:
            String con resumen
        """
        return user.get_profile_summary()
    
    def analyze_user_progress(self, user: User,
                             routines: List[Routine]) -> Dict[str, Any]:
        """
        Analiza el progreso del usuario.
        
        Args:
            user: Usuario
            routines: Rutinas del usuario
            
        Returns:
            Diccionario con análisis de progreso
        """
        if not routines:
            return {
                'tiene_progreso': False,
                'mensaje': 'No hay rutinas para analizar'
            }
        
        # Filtrar rutinas con feedback
        with_feedback = [r for r in routines if r.has_feedback()]
        
        if not with_feedback:
            return {
                'tiene_progreso': False,
                'mensaje': 'No hay feedback para analizar progreso'
            }
        
        # Calcular tendencias
        satisfactions = [r.satisfaccion for r in with_feedback]
        
        # Tendencia simple: comparar primera mitad vs segunda mitad
        if len(satisfactions) >= 4:
            mid = len(satisfactions) // 2
            first_half_avg = sum(satisfactions[:mid]) / mid
            second_half_avg = sum(satisfactions[mid:]) / (len(satisfactions) - mid)
            
            if second_half_avg > first_half_avg + 0.5:
                trend = "mejorando"
            elif second_half_avg < first_half_avg - 0.5:
                trend = "decreciendo"
            else:
                trend = "estable"
        else:
            trend = "sin_suficientes_datos"
        
        return {
            'tiene_progreso': True,
            'rutinas_totales': len(routines),
            'rutinas_con_feedback': len(with_feedback),
            'satisfacciones': satisfactions,
            'promedio': round(sum(satisfactions) / len(satisfactions), 2),
            'tendencia': trend,
            'mejor_satisfaccion': max(satisfactions),
            'peor_satisfaccion': min(satisfactions)
        }
    
    def get_optimal_parameters(self, profile: Profile) -> Dict[str, Any]:
        """
        Obtiene parámetros óptimos para el perfil.
        
        Args:
            profile: Perfil del usuario
            
        Returns:
            Diccionario con parámetros óptimos
        """
        try:
            params = self.inference_service.infer_optimal_parameters(profile)
            return params
            
        except Exception as e:
            print(f"❌ Error obteniendo parámetros: {e}")
            return {'error': str(e)}