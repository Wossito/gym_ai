"""
Servicio de Inferencia.

Este servicio encapsula toda la lógica del motor de inferencia,
proporcionando predicciones, clasificaciones y detección de anomalías.
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict
import math

from models.profile import Profile
from models.routine import Routine
from models.learning_system import LearningSystem
from config import AIConfig
from utils.calculations import (
    calculate_profile_similarity,
    calculate_bayesian_adjustment,
    calculate_confidence_score,
    calculate_average,
    calculate_std_dev
)


class InferenceService:
    """
    Servicio de inferencia que implementa predicciones y análisis.
    
    Este servicio es responsable de:
    - Predecir satisfacción de rutinas antes de asignarlas
    - Inferir parámetros óptimos (series, reps, descanso)
    - Clasificar usuarios según experiencia
    - Detectar anomalías en el rendimiento
    """
    
    def __init__(self, learning_system: LearningSystem):
        """
        Inicializa el servicio de inferencia.
        
        Args:
            learning_system: Sistema de aprendizaje con datos históricos
        """
        self.learning_system = learning_system
        self._initialize_thresholds()
    
    def _initialize_thresholds(self):
        """Inicializa umbrales para decisiones."""
        self.umbrales = {
            'similitud_alta': AIConfig.SIMILARITY_HIGH,
            'similitud_media': AIConfig.SIMILARITY_MEDIUM,
            'similitud_baja': AIConfig.SIMILARITY_LOW,
            'confianza_alta': AIConfig.CONFIDENCE_HIGH,
            'confianza_media': AIConfig.CONFIDENCE_MEDIUM,
            'confianza_baja': AIConfig.CONFIDENCE_LOW
        }
    
    # ========================================================================
    # PREDICCIÓN DE SATISFACCIÓN
    # ========================================================================
    
    def predict_satisfaction(self, profile: Profile, 
                           routine: Optional[Routine] = None) -> Dict[str, Any]:
        """
        Predice la satisfacción esperada de una rutina.
        
        Args:
            profile: Perfil del usuario
            routine: Rutina propuesta (opcional)
            
        Returns:
            Diccionario con predicción y confianza
        """
        print("\n🔮 Prediciendo satisfacción...")
        
        # Buscar usuarios similares
        similar_users = self._find_similar_users(profile)
        
        if not similar_users:
            return self._baseline_prediction()
        
        # Analizar factores
        factors = self._analyze_satisfaction_factors(profile, routine, similar_users)
        
        # Calcular predicción bayesiana
        predicted_satisfaction = self._calculate_bayesian_prediction(
            similar_users, factors
        )
        
        # Calcular confianza
        confidence = self._calculate_prediction_confidence(similar_users, factors)
        
        # Decidir recomendación
        recommend = (
            predicted_satisfaction >= 3.5 and
            confidence >= self.umbrales['confianza_baja']
        )
        
        result = {
            'satisfaccion_predicha': round(predicted_satisfaction, 2),
            'confianza': round(confidence, 2),
            'factores': factors,
            'recomendacion': recommend,
            'usuarios_similares': len(similar_users),
            'metodo': 'bayesiano'
        }
        
        print(f"   ✓ Satisfacción predicha: {result['satisfaccion_predicha']}/5")
        print(f"   ✓ Confianza: {result['confianza']*100:.0f}%")
        print(f"   ✓ Recomendación: {'SÍ' if recommend else 'NO'}")
        
        return result
    
    def _baseline_prediction(self) -> Dict[str, Any]:
        """Predicción base cuando no hay datos históricos."""
        return {
            'satisfaccion_predicha': 3.5,
            'confianza': 0.3,
            'factores': {'sin_datos': True},
            'recomendacion': True,
            'usuarios_similares': 0,
            'metodo': 'baseline'
        }
    
    def _find_similar_users(self, profile: Profile, 
                           threshold: float = 0.7) -> List[Dict[str, Any]]:
        """
        Busca usuarios similares en el histórico.
        
        Args:
            profile: Perfil a comparar
            threshold: Umbral mínimo de similitud
            
        Returns:
            Lista de usuarios similares con sus similitudes
        """
        similar = []
        
        for user_exp in self.learning_system.historico_usuarios:
            user_profile_data = user_exp.get('perfil', {})
            if not user_profile_data:
                continue
            
            try:
                similarity = calculate_profile_similarity(
                    profile.to_dict(),
                    user_profile_data
                )
                
                if similarity >= threshold:
                    similar.append({
                        'usuario': user_exp,
                        'similitud': similarity
                    })
            except Exception:
                continue
        
        # Ordenar por similitud
        similar.sort(key=lambda x: x['similitud'], reverse=True)
        return similar[:10]  # Top 10
    
    def _analyze_satisfaction_factors(self, profile: Profile,
                                     routine: Optional[Routine],
                                     similar_users: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analiza factores que influyen en la satisfacción."""
        factors = {}
        
        # Factor 1: Promedio de similares
        if similar_users:
            satisfactions = [
                u['usuario'].get('satisfaccion', 3)
                for u in similar_users
            ]
            factors['promedio_similares'] = calculate_average(satisfactions)
            factors['cantidad_similares'] = len(similar_users)
            factors['similitud_promedio'] = calculate_average(
                [u['similitud'] for u in similar_users]
            )
        else:
            factors['promedio_similares'] = 3.5
            factors['cantidad_similares'] = 0
            factors['similitud_promedio'] = 0
        
        # Factor 2: Complejidad de la rutina
        if routine:
            complexity = routine.get_exercises_per_day()
            ideal_complexity = self._get_ideal_complexity(profile)
            factors['ajuste_complejidad'] = 1 - abs(complexity - ideal_complexity) / ideal_complexity
        else:
            factors['ajuste_complejidad'] = 1.0
        
        # Factor 3: Patrones consolidados
        patterns = self.learning_system.get_patterns_for_profile(
            profile.nivel_str,
            profile.objetivo_str
        )
        factors['patron_existe'] = len(patterns) > 0
        factors['cantidad_patrones'] = len(patterns)
        
        return factors
    
    def _get_ideal_complexity(self, profile: Profile) -> float:
        """Obtiene la complejidad ideal según el nivel."""
        complexity_map = {
            'principiante': 4,
            'intermedio': 5,
            'avanzado': 6
        }
        return complexity_map.get(profile.nivel_str, 5)
    
    def _calculate_bayesian_prediction(self, similar_users: List[Dict[str, Any]],
                                      factors: Dict[str, Any]) -> float:
        """Calcula predicción usando enfoque bayesiano."""
        if not similar_users:
            return 3.5
        
        # Prior: promedio de usuarios similares
        satisfactions = [u['usuario'].get('satisfaccion', 3) for u in similar_users]
        prior = calculate_average(satisfactions)
        
        # Ajustes basados en factores
        adjustment = calculate_bayesian_adjustment(factors, self.umbrales)
        
        # Posterior
        posterior = prior + adjustment
        
        # Limitar a rango [1, 5]
        return max(1.0, min(5.0, posterior))
    
    def _calculate_prediction_confidence(self, similar_users: List[Dict[str, Any]],
                                        factors: Dict[str, Any]) -> float:
        """Calcula confianza de la predicción."""
        if not similar_users:
            return 0.3
        
        # Calcular desviación estándar
        satisfactions = [u['usuario'].get('satisfaccion', 3) for u in similar_users]
        std_dev = calculate_std_dev(satisfactions) if len(satisfactions) > 1 else 1.0
        
        return calculate_confidence_score(
            n_samples=len(similar_users),
            similarity_avg=factors.get('similitud_promedio', 0),
            std_dev=std_dev
        )
    
    # ========================================================================
    # INFERENCIA DE PARÁMETROS ÓPTIMOS
    # ========================================================================
    
    def infer_optimal_parameters(self, profile: Profile) -> Dict[str, Any]:
        """
        Infiere parámetros óptimos (series, reps, descanso) para un perfil.
        
        Args:
            profile: Perfil del usuario
            
        Returns:
            Diccionario con parámetros óptimos y confianza
        """
        print("\n🎯 Infiriendo parámetros óptimos...")
        
        # Buscar usuarios similares exitosos
        similar_users = self._find_similar_users(profile, threshold=0.75)
        successful_users = [
            u for u in similar_users
            if u['usuario'].get('satisfaccion', 0) >= 4
        ]
        
        if not successful_users:
            return self._parameters_by_heuristics(profile)
        
        # Extraer parámetros de rutinas exitosas
        params = self._extract_parameters_from_routines(successful_users)
        
        # Calcular valores óptimos
        optimal_params = self._calculate_optimal_values(params, profile)
        
        # Calcular confianza
        confidence = min(1.0, len(successful_users) / 10)
        optimal_params['confianza'] = round(confidence, 2)
        optimal_params['basado_en'] = len(successful_users)
        optimal_params['metodo'] = 'inferencia_datos'
        
        print(f"   ✓ Series: {optimal_params['series']}")
        print(f"   ✓ Reps: {optimal_params['repeticiones_min']}-{optimal_params['repeticiones_max']}")
        print(f"   ✓ Descanso: {optimal_params['descanso']}")
        print(f"   ✓ Confianza: {optimal_params['confianza']*100:.0f}%")
        
        return optimal_params
    
    def _extract_parameters_from_routines(self, 
                                         successful_users: List[Dict[str, Any]]) -> Dict[str, List]:
        """Extrae parámetros de rutinas exitosas."""
        series_list = []
        reps_list = []
        
        for user_data in successful_users:
            routine_data = user_data['usuario'].get('rutina_exitosa', {})
            if not routine_data or 'rutina_semanal' not in routine_data:
                continue
            
            for day, exercises in routine_data['rutina_semanal'].items():
                for ex in exercises:
                    if 'series' in ex:
                        series_list.append(ex['series'])
                    if 'repeticiones' in ex:
                        # Extraer promedio del rango
                        reps_str = str(ex['repeticiones'])
                        if '-' in reps_str:
                            try:
                                parts = reps_str.split('-')
                                avg = (int(parts[0]) + int(parts[1])) / 2
                                reps_list.append(avg)
                            except:
                                pass
        
        return {
            'series': series_list,
            'reps': reps_list
        }
    
    def _calculate_optimal_values(self, params: Dict[str, List],
                                 profile: Profile) -> Dict[str, Any]:
        """Calcula valores óptimos desde parámetros extraídos."""
        if params['series']:
            series = int(round(np.median(params['series'])))
        else:
            series = 4
        
        if params['reps']:
            reps_median = int(round(np.median(params['reps'])))
        else:
            reps_median = 10
        
        return {
            'series': series,
            'repeticiones_min': max(4, reps_median - 2),
            'repeticiones_max': reps_median + 2,
            'descanso': self._infer_rest_time(profile, series, reps_median)
        }
    
    def _parameters_by_heuristics(self, profile: Profile) -> Dict[str, Any]:
        """Parámetros basados en heurísticas cuando no hay datos."""
        from config import RoutineConfig
        
        objetivo = profile.objetivo_str
        params_config = RoutineConfig.PARAMS_BY_GOAL.get(
            objetivo,
            RoutineConfig.PARAMS_BY_GOAL['ganar_masa']
        )
        
        series = RoutineConfig.SERIES_BY_LEVEL.get(profile.nivel_str, 4)
        
        return {
            'series': series,
            'repeticiones_min': params_config['reps_min'],
            'repeticiones_max': params_config['reps_max'],
            'descanso': f"{params_config['rest_min']}-{params_config['rest_max']}s",
            'confianza': 0.5,
            'basado_en': 0,
            'metodo': 'heuristica'
        }
    
    def _infer_rest_time(self, profile: Profile, series: int, reps: int) -> str:
        """Infiere tiempo de descanso óptimo."""
        objetivo = profile.objetivo_str
        
        if objetivo == 'fuerza' or series >= 5:
            return "120-180s"
        elif objetivo == 'ganar_masa':
            return "60-90s"
        elif objetivo == 'resistencia' or reps >= 15:
            return "30-45s"
        else:
            return "45-60s"
    
    # ========================================================================
    # CLASIFICACIÓN DE USUARIOS
    # ========================================================================
    
    def classify_user(self, profile: Profile,
                     user_history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Clasifica al usuario según experiencia y rendimiento.
        
        Args:
            profile: Perfil del usuario
            user_history: Histórico personal del usuario
            
        Returns:
            Diccionario con clasificación y características
        """
        print("\n👤 Clasificando usuario...")
        
        num_experiences = len(user_history) if user_history else 0
        
        # Calcular satisfacción promedio
        if user_history:
            satisfactions = [exp.get('satisfaccion', 3) for exp in user_history]
            avg_satisfaction = calculate_average(satisfactions)
        else:
            avg_satisfaction = 0
        
        # Clasificar por experiencias
        category = self._get_user_category(num_experiences)
        
        # Clasificar rendimiento
        performance = self._get_performance_level(avg_satisfaction)
        
        result = {
            'categoria': category['name'],
            'descripcion': category['description'],
            'experiencias': num_experiences,
            'satisfaccion_promedio': round(avg_satisfaction, 2),
            'rendimiento': performance,
            'recomendaciones': self._generate_recommendations(
                category['name'], performance, profile
            )
        }
        
        print(f"   ✓ Categoría: {category['name'].upper()}")
        print(f"   ✓ Experiencias: {num_experiences}")
        print(f"   ✓ Satisfacción promedio: {avg_satisfaction:.2f}/5")
        print(f"   ✓ Rendimiento: {performance}")
        
        return result
    
    def _get_user_category(self, num_experiences: int) -> Dict[str, str]:
        """Obtiene la categoría del usuario según experiencias."""
        if num_experiences == 0:
            return {'name': 'novato', 'description': 'Primera vez usando el sistema'}
        elif num_experiences <= 5:
            return {'name': 'regular', 'description': 'Usuario regular con algunas experiencias'}
        elif num_experiences <= 15:
            return {'name': 'experimentado', 'description': 'Usuario experimentado con buen historial'}
        elif num_experiences <= 50:
            return {'name': 'veterano', 'description': 'Usuario veterano con amplia experiencia'}
        else:
            return {'name': 'experto', 'description': 'Usuario experto del sistema'}
    
    def _get_performance_level(self, avg_satisfaction: float) -> str:
        """Determina el nivel de rendimiento."""
        if avg_satisfaction >= 4.5:
            return "excelente"
        elif avg_satisfaction >= 4.0:
            return "bueno"
        elif avg_satisfaction >= 3.5:
            return "aceptable"
        else:
            return "necesita_ajuste"
    
    def _generate_recommendations(self, category: str, performance: str,
                                 profile: Profile) -> List[str]:
        """Genera recomendaciones según categoría y rendimiento."""
        from utils.constants import USER_RECOMMENDATIONS
        
        recommendations = USER_RECOMMENDATIONS.get(category, [])
        
        if isinstance(recommendations, dict):
            return recommendations.get(performance, recommendations.get('default', []))
        
        return recommendations
    
    # ========================================================================
    # DETECCIÓN DE ANOMALÍAS
    # ========================================================================
    
    def detect_anomalies(self, profile: Profile,
                        feedback_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Detecta patrones anómalos en el rendimiento.
        
        Args:
            profile: Perfil del usuario
            feedback_history: Histórico de feedbacks
            
        Returns:
            Diccionario con anomalías detectadas
        """
        if not feedback_history or len(feedback_history) < 3:
            return {'anomalias': [], 'estado': 'normal'}
        
        satisfactions = [f.get('satisfaccion', 3) for f in feedback_history]
        anomalies = []
        
        # Detectar tendencia negativa
        if len(satisfactions) >= 3:
            last_3 = satisfactions[-3:]
            if all(last_3[i] > last_3[i+1] for i in range(len(last_3)-1)):
                anomalies.append({
                    'tipo': 'tendencia_negativa',
                    'descripcion': 'Satisfacción en descenso constante',
                    'recomendacion': 'Revisar intensidad o variedad de ejercicios'
                })
        
        # Detectar caída abrupta
        if len(satisfactions) >= 2:
            if satisfactions[-2] >= 4 and satisfactions[-1] <= 2:
                anomalies.append({
                    'tipo': 'caida_abrupta',
                    'descripcion': 'Caída súbita en satisfacción',
                    'recomendacion': 'Verificar posibles lesiones o sobreentrenamiento'
                })
        
        # Detectar estancamiento
        avg = calculate_average(satisfactions)
        if 3.0 <= avg <= 3.5 and len(satisfactions) >= 5:
            anomalies.append({
                'tipo': 'estancamiento',
                'descripcion': 'Satisfacción estancada en nivel medio',
                'recomendacion': 'Considerar cambio de enfoque o metodología'
            })
        
        return {
            'anomalias': anomalies,
            'estado': 'anomalo' if anomalies else 'normal',
            'satisfaccion_promedio': avg
        }