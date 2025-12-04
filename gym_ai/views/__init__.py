# ============================================================================
# views/__init__.py
# ============================================================================

"""
Vistas de la interfaz gráfica.
"""

from views.gym_ai_gui import BaseView
from views.gym_ai_gui import WelcomeView
from views.gym_ai_gui import FormView
from views.gym_ai_gui import RoutineView
from views.gym_ai_gui import FeedbackView
from views.gym_ai_gui import ThanksView

__all__ = [
    'BaseView',
    'WelcomeView',
    'FormView',
    'RoutineView',
    'FeedbackView',
    'ThanksView'
]