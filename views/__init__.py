"""
Módulo de vistas de la interfaz gráfica.

Este módulo contiene todas las vistas del sistema organizadas
según el patrón MVC.
"""

from views.base_view import BaseView
from views.welcome_view import WelcomeView
from views.form_view import FormView
from views.routine_view import RoutineView
from views.feedback_view import FeedbackView
from views.thanks_view import ThanksView

__all__ = [
    'BaseView',
    'WelcomeView',
    'FormView',
    'RoutineView',
    'FeedbackView',
    'ThanksView'
]