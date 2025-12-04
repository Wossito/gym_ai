"""
Servicio de IA.

Este servicio contiene toda la lógica de generación de rutinas
usando inteligencia artificial y aprendizaje automático.

PARTE 1: Inicialización y generación principal
"""

import random
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from models.profile import Profile
from models.exercise import Exercise
from models.routine import Routine
from models.learning_system import LearningSystem
from config import ExerciseDatabase, RoutineConfig, AIConfig
from services.inference_service import InferenceService
from services.learning_service import LearningService


class AIService:
    """
    Servicio principal de IA para generación de rutinas.
    
    Este servicio utiliza:
    - Algoritmos de búsqueda de patrones
    - Aprendizaje basado en experiencias previas
    - Exploración vs Explotación
    - Inferencia bayesiana para predicciones
    """
    
    def __init__(self, learning_system: LearningSystem):
        """
        Inicializa el servicio de IA.
        
        Args:
            learning_system: Sistema de aprendizaje
        """
        self.learning_system = learning_system
        self.exercise_db = ExerciseDatabase()
        
        # Inicializar servicios auxiliares
        self.inference_service = InferenceService(learning_system)
        self.learning_service = LearningService(learning_system)
    
    # ========================================================================
    # GENERACIÓN PRINCIPAL DE RUTINAS
    # ========================================================================
    
    def generate_intelligent_routine(self, profile: Profile) -> Routine:
        """
        Genera una rutina inteligente basándose en el perfil y datos históricos.
        
        Este es el método principal que:
        1. Decide si explorar o explotar conocimiento
        2. Consulta servicios de inferencia
        3. Genera la rutina apropiada
        4. Registra la rutina generada
        
        Args:
            profile: Perfil del usuario
            
        Returns:
            Rutina generada
        """
        print("\n🧠 Generando rutina con IA...")
        
        # Paso 1: Inferir parámetros óptimos
        optimal_params = self.inference_service.infer_optimal_parameters(profile)
        
        # Paso 2: Clasificar usuario
        classification = self.inference_service.classify_user(profile)
        
        # Paso 3: Decidir modo de generación
        should_exploit = self.learning_service.should_use_learning_mode(profile)
        
        if should_exploit:
            print("   → Modo EXPLOTACIÓN: Basándose en conocimiento previo")
            routine_dict = self._generate_learned_routine(profile)
        else:
            print("   → Modo EXPLORACIÓN: Generando rutina innovadora")
            routine_dict = self._generate_exploration_routine(profile)
        
        # Paso 4: Aplicar parámetros optimizados
        if optimal_params['confianza'] >= 0.6:
            print("\n   ✓ Aplicando parámetros optimizados")
            routine_dict = self._apply_optimal_parameters(routine_dict, optimal_params)
        
        # Paso 5: Crear objeto Routine
        routine = Routine(
            perfil=profile,
            rutina_semanal=routine_dict['rutina_semanal'],
            estructura=routine_dict['estructura'],
            metadatos=routine_dict['metadatos']
        )
        
        # Paso 6: Predecir satisfacción
        prediction = self.inference_service.predict_satisfaction(profile, routine)
        
        # Paso 7: Registrar rutina generada
        routine_data = {
            'id': routine.routine_id,
            'perfil': profile.to_dict(),
            'rutina': routine.to_dict(),
            'fecha_generacion': routine.fecha_generacion,
            'modo': 'explotacion' if should_exploit else 'exploracion',
            'generacion': self.learning_system.generacion,
            'parametros_inferidos': optimal_params,
            'clasificacion_usuario': classification,
            'prediccion_satisfaccion': prediction
        }
        
        self.learning_system.add_generated_routine(routine_data)
        
        print(f"\n   🎯 Satisfacción predicha: {prediction['satisfaccion_predicha']}/5")
        print(f"   🎯 Confianza: {prediction['confianza']*100:.0f}%")
        
        return routine
    
    # ========================================================================
    # GENERACIÓN EN MODO EXPLORACIÓN
    # ========================================================================
    
    def _generate_exploration_routine(self, profile: Profile) -> Dict[str, Any]:
        """
        Genera rutina explorando nuevas combinaciones.
        
        Args:
            profile: Perfil del usuario
            
        Returns:
            Diccionario con rutina generada
        """
        # Decidir estructura según días
        structure = self._decide_structure(profile.dias)
        
        # Decidir grupos por día según estructura
        groups_per_day = self._decide_groups_per_day(structure, profile.dias)
        
        # Generar ejercicios para cada día
        weekly_routine = {}
        for day_num, groups in enumerate(groups_per_day, 1):
            day_exercises = []
            
            for group in groups:
                num_exercises = self._decide_exercises_per_group(
                    group, structure, profile.nivel_str
                )
                
                exercises = self._select_innovative_exercises(
                    group, num_exercises, profile.nivel_str
                )
                
                for exercise_name in exercises:
                    params = self._generate_experimental_parameters(
                        profile.objetivo_str, profile.nivel_str, group
                    )
                    
                    if group == 'cardio':
                        exercise = Exercise.create_cardio_exercise(
                            exercise_name,
                            params['duracion'],
                            params['intensidad']
                        )
                    else:
                        exercise = Exercise.create_strength_exercise(
                            exercise_name,
                            group,
                            params['series'],
                            params['repeticiones'],
                            params['descanso']
                        )
                    
                    day_exercises.append(exercise)
            
            # Agregar cardio si es necesario
            if self._needs_cardio(profile.objetivo_str, day_num):
                cardio_ex = self._generate_cardio_exercise(profile.objetivo_str)
                day_exercises.append(cardio_ex)
            
            weekly_routine[f"Día {day_num}"] = day_exercises
        
        return {
            'rutina_semanal': weekly_routine,
            'estructura': structure,
            'metadatos': {
                'modo_generacion': 'exploracion',
                'innovacion_level': 'alta'
            }
        }
    
    def _decide_structure(self, days: int) -> str:
        """Decide la estructura de entrenamiento según días disponibles."""
        if days <= 3:
            return 'fullbody'
        elif days == 4:
            return 'upper_lower'
        else:
            return 'split'
    
    def _decide_groups_per_day(self, structure: str, days: int) -> List[List[str]]:
        """Decide qué grupos trabajar cada día según estructura."""
        if structure == 'fullbody':
            # Todos los grupos cada día
            groups = ['pecho', 'espalda', 'piernas', 'hombros', 'brazos']
            return [groups] * days
        
        elif structure == 'upper_lower':
            # Alternar tren superior e inferior
            return [
                ['pecho', 'espalda', 'hombros', 'brazos'],
                ['piernas', 'core'],
                ['pecho', 'espalda', 'brazos'],
                ['piernas', 'hombros', 'core']
            ][:days]
        
        else:  # split
            # Un grupo principal por día
            base_split = [
                ['pecho', 'brazos'],
                ['espalda'],
                ['piernas'],
                ['hombros', 'brazos'],
                ['pecho', 'espalda'],
                ['piernas', 'core']
            ]
            return base_split[:days]
    
    def _decide_exercises_per_group(self, group: str, structure: str, 
                                   level: str) -> int:
        """Decide cuántos ejercicios hacer por grupo."""
        from config import RoutineConfig
        
        if group == 'cardio':
            return 1
        
        config = RoutineConfig.EXERCISES_PER_STRUCTURE.get(structure, {})
        return config.get(level, 2)
    
    def _select_innovative_exercises(self, group: str, count: int, 
                                    level: str) -> List[str]:
        """Selecciona ejercicios innovadores mezclando tipos."""
        if group not in self.exercise_db.EXERCISES:
            return []
        
        available = self.exercise_db.EXERCISES[group]
        
        if isinstance(available, dict):
            # Mezclar compuestos y aislamiento
            if level == 'principiante':
                # Principiantes: más compuestos
                pool = available.get('compuestos', [])
            else:
                # Otros: mezclar
                pool = (available.get('compuestos', []) + 
                       available.get('aislamiento', []))
            
            return random.sample(pool, min(count, len(pool)))
        else:
            # Lista simple (como cardio o core)
            return random.sample(available, min(count, len(available)))
    
    def _generate_experimental_parameters(self, objetivo: str, nivel: str, 
                                         grupo: str) -> Dict[str, Any]:
        """Genera parámetros experimentales."""
        from config import RoutineConfig
        
        params_config = RoutineConfig.PARAMS_BY_GOAL.get(objetivo)
        series_config = RoutineConfig.SERIES_BY_LEVEL.get(nivel, 4)
        
        if grupo == 'cardio':
            return {
                'duracion': f"{random.randint(15, 30)} min",
                'intensidad': random.choice(['moderada', 'alta', 'HIIT'])
            }
        
        reps_min = params_config['reps_min']
        reps_max = params_config['reps_max']
        
        return {
            'series': series_config,
            'repeticiones': f"{random.randint(reps_min, reps_min+2)}-{random.randint(reps_max-2, reps_max)}",
            'descanso': f"{random.randint(params_config['rest_min'], params_config['rest_max'])}s"
        }
    
    def _needs_cardio(self, objetivo: str, day_num: int) -> bool:
        """Decide si agregar cardio según objetivo."""
        from config import RoutineConfig
        
        params = RoutineConfig.PARAMS_BY_GOAL.get(objetivo)
        probability = params['cardio_probability']
        
        return random.random() < probability
    
    def _generate_cardio_exercise(self, objetivo: str) -> Exercise:
        """Genera un ejercicio de cardio."""
        cardio_options = self.exercise_db.EXERCISES['cardio']
        cardio_name = random.choice(cardio_options)
        
        if objetivo == 'perder_peso':
            duration = f"{random.randint(20, 30)} min"
            intensity = random.choice(['alta', 'HIIT'])
        elif objetivo == 'resistencia':
            duration = f"{random.randint(25, 40)} min"
            intensity = random.choice(['moderada', 'alta'])
        else:
            duration = f"{random.randint(15, 20)} min"
            intensity = 'moderada'
        
        return Exercise.create_cardio_exercise(cardio_name, duration, intensity)
    
    def _apply_optimal_parameters(self, routine_dict: Dict[str, Any],
                                 optimal_params: Dict[str, Any]) -> Dict[str, Any]:
        """Aplica parámetros optimizados a la rutina."""
        series = optimal_params['series']
        reps_min = optimal_params['repeticiones_min']
        reps_max = optimal_params['repeticiones_max']
        rest = optimal_params['descanso']
        
        for day, exercises in routine_dict['rutina_semanal'].items():
            for exercise in exercises:
                if not exercise.is_cardio():
                    exercise.series = series
                    exercise.repeticiones = f"{reps_min}-{reps_max}"
                    exercise.descanso = rest
        
        # Actualizar metadatos
        if 'metadatos' not in routine_dict:
            routine_dict['metadatos'] = {}
        
        routine_dict['metadatos']['parametros_optimizados'] = True
        routine_dict['metadatos']['confianza_parametros'] = optimal_params['confianza']
        
        return routine_dict
    
    """
CONTINUACIÓN DEL SERVICIO DE IA

PARTE 2: Generación en modo aprendizaje y utilidades

IMPORTANTE: Este archivo debe agregarse al final de ai_service.py (Parte 1)
"""

    # ========================================================================
    # GENERACIÓN EN MODO APRENDIZAJE (EXPLOTACIÓN)
    # ========================================================================
    
    def _generate_learned_routine(self, profile: Profile) -> Dict[str, Any]:
        """
        Genera rutina basándose en patrones aprendidos.
        
        Args:
            profile: Perfil del usuario
            
        Returns:
            Diccionario con rutina generada
        """
        # Obtener mejores prácticas para este perfil
        best_practices = self.learning_service.get_best_practices(profile)
        
        if not best_practices['tiene_patrones']:
            # No hay patrones, usar exploración
            return self._generate_exploration_routine(profile)
        
        # Extraer información de mejores prácticas
        structure = best_practices['estructura_preferida']
        popular_exercises = best_practices['ejercicios_populares']
        
        # Decidir grupos por día
        groups_per_day = self._decide_groups_per_day(structure, profile.dias)
        
        # Generar rutina usando conocimiento aprendido
        weekly_routine = {}
        for day_num, groups in enumerate(groups_per_day, 1):
            day_exercises = []
            
            for group in groups:
                num_exercises = self._decide_exercises_per_group(
                    group, structure, profile.nivel_str
                )
                
                # 70% usar ejercicios aprendidos, 30% innovar
                if random.random() < 0.7 and group in popular_exercises:
                    exercises = self._select_learned_exercises(
                        group, num_exercises, popular_exercises[group]
                    )
                else:
                    exercises = self._select_innovative_exercises(
                        group, num_exercises, profile.nivel_str
                    )
                
                # Generar ejercicios con parámetros
                for exercise_name in exercises:
                    params = self._generate_experimental_parameters(
                        profile.objetivo_str, profile.nivel_str, group
                    )
                    
                    exercise = Exercise.create_strength_exercise(
                        exercise_name,
                        group,
                        params['series'],
                        params['repeticiones'],
                        params['descanso']
                    )
                    
                    day_exercises.append(exercise)
            
            # Agregar cardio si es necesario
            if self._needs_cardio(profile.objetivo_str, day_num):
                cardio_ex = self._generate_cardio_exercise(profile.objetivo_str)
                day_exercises.append(cardio_ex)
            
            weekly_routine[f"Día {day_num}"] = day_exercises
        
        return {
            'rutina_semanal': weekly_routine,
            'estructura': structure,
            'metadatos': {
                'modo_generacion': 'aprendizaje',
                'basado_en': best_practices['cantidad_patrones'],
                'confianza': best_practices['confianza']
            }
        }
    
    def _select_learned_exercises(self, group: str, count: int,
                                 popular_list: List[str]) -> List[str]:
        """
        Selecciona ejercicios de la lista de populares.
        
        Args:
            group: Grupo muscular
            count: Cantidad a seleccionar
            popular_list: Lista de ejercicios populares
            
        Returns:
            Lista de ejercicios seleccionados
        """
        if not popular_list:
            return self._select_innovative_exercises(group, count, 'intermedio')
        
        # Seleccionar de los populares
        available_count = min(count, len(popular_list))
        selected = random.sample(popular_list, available_count)
        
        # Si necesita más, complementar con innovadores
        if available_count < count:
            additional = self._select_innovative_exercises(
                group, count - available_count, 'intermedio'
            )
            selected.extend(additional)
        
        return selected
    
    # ========================================================================
    # ANÁLISIS Y OPTIMIZACIÓN
    # ========================================================================
    
    def analyze_routine_effectiveness(self, routine: Routine) -> Dict[str, Any]:
        """
        Analiza la efectividad de una rutina.
        
        Args:
            routine: Rutina a analizar
            
        Returns:
            Diccionario con análisis
        """
        analysis = {
            'tiene_feedback': routine.has_feedback(),
            'es_exitosa': routine.is_successful(),
            'satisfaccion': routine.satisfaccion,
            'complejidad': round(routine.get_complexity_score(), 2),
            'dias_totales': routine.get_total_days(),
            'ejercicios_totales': routine.get_total_exercises(),
            'ejercicios_por_dia': round(routine.get_exercises_per_day(), 1),
            'grupos_trabajados': len(routine.get_muscle_groups_worked()),
            'tiene_cardio': routine.has_cardio(),
            'frecuencia_cardio': routine.get_cardio_frequency()
        }
        
        # Calcular balance muscular
        groups_worked = routine.get_muscle_groups_worked()
        major_groups = {'pecho', 'espalda', 'piernas', 'hombros'}
        covered_major = major_groups.intersection(groups_worked)
        
        analysis['balance_muscular'] = len(covered_major) / len(major_groups)
        
        return analysis
    
    def recommend_adjustments(self, profile: Profile, 
                            routine: Routine,
                            satisfaction: int) -> List[str]:
        """
        Recomienda ajustes basándose en feedback.
        
        Args:
            profile: Perfil del usuario
            routine: Rutina evaluada
            satisfaction: Satisfacción reportada
            
        Returns:
            Lista de recomendaciones
        """
        recommendations = []
        
        analysis = self.analyze_routine_effectiveness(routine)
        
        # Recomendaciones según satisfacción
        if satisfaction <= 2:
            # Muy difícil
            recommendations.append("Reducir intensidad: disminuir series o peso")
            recommendations.append("Aumentar tiempo de descanso entre series")
            
            if analysis['ejercicios_por_dia'] > 6:
                recommendations.append("Reducir número de ejercicios por día")
        
        elif satisfaction == 3:
            # Adecuada pero puede mejorar
            if analysis['balance_muscular'] < 0.75:
                recommendations.append("Mejorar balance: agregar grupos musculares faltantes")
            
            if not analysis['tiene_cardio'] and profile.objetivo_str == 'perder_peso':
                recommendations.append("Agregar cardio para mejorar resultados")
        
        elif satisfaction >= 4:
            # Buena rutina, mantener o progresar
            recommendations.append("¡Excelente! Mantén la consistencia")
            
            if profile.nivel_str == 'principiante':
                recommendations.append("Considera progresar a ejercicios más desafiantes")
        
        # Recomendaciones según objetivo
        if profile.objetivo_str == 'ganar_masa' and analysis['ejercicios_por_dia'] < 4:
            recommendations.append("Considera aumentar volumen de entrenamiento")
        
        if profile.objetivo_str == 'resistencia' and analysis['frecuencia_cardio'] < 2:
            recommendations.append("Aumentar frecuencia de cardio")
        
        return recommendations
    
    # ========================================================================
    # UTILIDADES
    # ========================================================================
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas completas del sistema.
        
        Returns:
            Diccionario con estadísticas
        """
        return self.learning_system.get_statistics()
    
    def export_user_report(self, user_profile: Profile,
                          routines: List[Routine]) -> Dict[str, Any]:
        """
        Genera un reporte completo para un usuario.
        
        Args:
            user_profile: Perfil del usuario
            routines: Lista de rutinas del usuario
            
        Returns:
            Diccionario con reporte completo
        """
        # Calcular estadísticas de rutinas
        if routines:
            satisfactions = [r.satisfaccion for r in routines if r.satisfaccion]
            avg_satisfaction = sum(satisfactions) / len(satisfactions) if satisfactions else 0
            successful_count = sum(1 for r in routines if r.is_successful())
        else:
            avg_satisfaction = 0
            successful_count = 0
        
        # Clasificación
        user_history = [
            {'satisfaccion': r.satisfaccion} for r in routines if r.satisfaccion
        ]
        classification = self.inference_service.classify_user(
            user_profile, user_history
        )
        
        # Detectar anomalías
        anomalies = self.inference_service.detect_anomalies(
            user_profile, user_history
        )
        
        return {
            'perfil': user_profile.to_dict(),
            'clasificacion': classification,
            'estadisticas': {
                'rutinas_totales': len(routines),
                'rutinas_con_feedback': len([r for r in routines if r.has_feedback()]),
                'rutinas_exitosas': successful_count,
                'satisfaccion_promedio': round(avg_satisfaction, 2),
                'tasa_exito': round(successful_count / len(routines) * 100, 1) if routines else 0
            },
            'anomalias': anomalies,
            'recomendaciones': classification.get('recomendaciones', [])
        }
    
    def validate_routine_quality(self, routine: Routine) -> Tuple[bool, List[str]]:
        """
        Valida la calidad de una rutina generada.
        
        Args:
            routine: Rutina a validar
            
        Returns:
            Tupla (es_válida, lista_de_problemas)
        """
        problems = []
        
        # Validar que tenga ejercicios
        if routine.get_total_exercises() == 0:
            problems.append("La rutina no tiene ejercicios")
        
        # Validar balance muscular
        groups = routine.get_muscle_groups_worked()
        major_groups = {'pecho', 'espalda', 'piernas'}
        missing_major = major_groups - groups
        
        if missing_major:
            problems.append(f"Falta trabajar: {', '.join(missing_major)}")
        
        # Validar complejidad
        exercises_per_day = routine.get_exercises_per_day()
        if exercises_per_day < 3:
            problems.append("Muy pocos ejercicios por día")
        elif exercises_per_day > 8:
            problems.append("Demasiados ejercicios por día")
        
        # Validar que los ejercicios tengan parámetros correctos
        for day, exercises in routine.rutina_semanal.items():
            for exercise in exercises:
                if not exercise.is_cardio():
                    if exercise.series is None or exercise.series < 2:
                        problems.append(f"{day}: {exercise.ejercicio} tiene pocas series")
        
        return (len(problems) == 0, problems)
    
    def get_generation_summary(self) -> str:
        """
        Obtiene un resumen de la generación actual.
        
        Returns:
            String con resumen
        """
        stats = self.get_system_statistics()
        
        return f"""
🧠 SISTEMA DE IA - GENERACIÓN {stats['generacion']}

📊 Estadísticas:
   • {stats['total_usuarios']} usuarios han entrenado
   • {stats['total_rutinas']} rutinas generadas
   • {stats['promedio_satisfaccion']:.2f}/5 satisfacción promedio
   • {stats['tasa_exito']:.1f}% tasa de éxito
   • {stats['patrones_exitosos']} patrones identificados

🎯 Modo actual: {stats['factor_exploracion']*100:.0f}% exploración
""".strip()


# NOTA: Las líneas anteriores completan la clase AIService.
# Recuerda que esta es la PARTE 2 que debe agregarse después de la PARTE 1.