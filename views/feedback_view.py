"""
Vista de Feedback.

Permite al usuario dar feedback sobre la rutina generada.
"""

import tkinter as tk
from views.base_view import BaseView


class FeedbackView(BaseView):
    """
    Vista para recopilar feedback del usuario.
    
    Recopila:
    - Nivel de satisfacción (1-5)
    - Comentarios adicionales
    """
    
    def __init__(self, parent: tk.Widget, controller, user_data: dict = None, routine: dict = None):
        super().__init__(parent, controller)
        self.user_data = user_data or {}
        self.routine = routine or {}
        self.satisfaccion_var = None
        self.comment_text = None
    
    def build(self):
        """Construye la interfaz de feedback."""
        self.frame = tk.Frame(
            self.parent,
            bg=self.colors['bg_dark']
        )
        
        # Frame central
        center_frame = tk.Frame(
            self.frame,
            bg=self.colors['bg_medium'],
            padx=50,
            pady=40
        )
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Título
        title = self.create_title_label(
            center_frame,
            "💬 TU OPINIÓN AYUDA A LA IA A MEJORAR",
            font=('Helvetica', 16, 'bold')
        )
        title.pack(pady=(0, 30))
        
        # Explicación
        explanation = """El sistema aprende de tu feedback para generar
rutinas cada vez más precisas y personalizadas."""
        
        exp_label = self.create_text_label(
            center_frame,
            explanation,
            justify='center'
        )
        exp_label.pack(pady=(0, 20))
        
        # Pregunta
        question = tk.Label(
            center_frame,
            text="¿Cómo te sientes con esta rutina?",
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['bg_medium'],
            fg=self.colors['text']
        )
        question.pack(pady=10)
        
        # Escala de satisfacción
        self._build_satisfaction_scale(center_frame)
        
        # Comentarios
        self._build_comments_section(center_frame)
        
        # Botón enviar
        submit_btn = self.create_button(
            center_frame,
            "✅ ENVIAR FEEDBACK",
            command=self._on_submit_clicked,
            font=('Helvetica', 13, 'bold'),
            bg=self.colors['success'],
            padx=40,
            pady=15
        )
        submit_btn.pack(pady=20)
    
    def _build_satisfaction_scale(self, parent: tk.Widget):
        """Construye la escala de satisfacción."""
        self.satisfaccion_var = tk.IntVar(value=3)
        
        scale_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        scale_frame.pack(pady=20)
        
        ratings = [
            (1, "😫 Muy difícil", "Demasiado exigente, no pude completarla"),
            (2, "😕 Difícil", "Muy desafiante, pero terminé"),
            (3, "😊 Adecuada", "Balance correcto, me sentí bien"),
            (4, "😄 Buena", "Perfecta para mi nivel, gran rutina"),
            (5, "🤩 Perfecta", "Exactamente lo que necesitaba, excelente")
        ]
        
        for value, text, description in ratings:
            rb = tk.Radiobutton(
                scale_frame,
                text=text,
                variable=self.satisfaccion_var,
                value=value,
                font=self.fonts['normal'],
                bg=self.colors['bg_medium'],
                fg=self.colors['text'],
                selectcolor=self.colors['bg_light'],
                activebackground=self.colors['bg_medium'],
                activeforeground=self.colors['accent']
            )
            rb.pack(anchor='w', pady=5)
    
    def _build_comments_section(self, parent: tk.Widget):
        """Construye la sección de comentarios."""
        comment_label = tk.Label(
            parent,
            text="Comentarios adicionales (opcional):",
            font=self.fonts['normal'],
            bg=self.colors['bg_medium'],
            fg=self.colors['text']
        )
        comment_label.pack(pady=(20, 5))
        
        self.comment_text = tk.Text(
            parent,
            height=4,
            width=50,
            font=self.fonts['normal'],
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief='flat'
        )
        self.comment_text.pack(pady=10)
    
    def _on_submit_clicked(self):
        """Maneja el envío del feedback."""
        satisfaccion = self.satisfaccion_var.get()
        comentarios = self.comment_text.get('1.0', 'end').strip()
        
        # Procesar feedback a través del controlador
        success, result = self.controller.submit_feedback(
            self.user_data,
            self.routine,
            satisfaccion,
            comentarios
        )
        
        if success:
            # Navegar a pantalla de agradecimiento
            self.navigate_to(
                'thanks',
                satisfaccion=satisfaccion
            )
        else:
            self.show_error("Error", f"No se pudo procesar el feedback: {result}")
    
    def set_data(self, user_data: dict, routine: dict):
        """
        Actualiza los datos de la vista.
        
        Args:
            user_data: Datos del usuario
            routine: Rutina evaluada
        """
        self.user_data = user_data
        self.routine = routine