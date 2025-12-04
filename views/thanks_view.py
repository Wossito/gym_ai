"""
Vista de Agradecimiento.

Muestra agradecimiento después del feedback y estadísticas actualizadas.
"""

import tkinter as tk
from views.base_view import BaseView


class ThanksView(BaseView):
    """
    Vista de agradecimiento después del feedback.
    
    Muestra:
    - Mensaje de agradecimiento
    - Estadísticas actualizadas del sistema
    - Opciones para continuar
    """
    
    def __init__(self, parent: tk.Widget, controller, satisfaccion: int = 3):
        super().__init__(parent, controller)
        self.satisfaccion = satisfaccion
    
    def build(self):
        """Construye la interfaz de agradecimiento."""
        self.frame = tk.Frame(
            self.parent,
            bg=self.colors['bg_dark']
        )
        
        # Frame central
        center_frame = tk.Frame(
            self.frame,
            bg=self.colors['bg_medium'],
            padx=60,
            pady=50
        )
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Icono según satisfacción
        icon = self._get_icon_for_satisfaction()
        
        # Título con icono
        thanks_label = tk.Label(
            center_frame,
            text=f"{icon} ¡GRACIAS POR TU FEEDBACK!",
            font=('Helvetica', 20, 'bold'),
            bg=self.colors['bg_medium'],
            fg=self.colors['success']
        )
        thanks_label.pack(pady=20)
        
        # Mensaje de aprendizaje
        self._build_learning_message(center_frame)
        
        # Botones de navegación
        self._build_navigation_buttons(center_frame)
    
    def _get_icon_for_satisfaction(self) -> str:
        """Obtiene el icono según el nivel de satisfacción."""
        if self.satisfaccion >= 4:
            return "🎉"
        elif self.satisfaccion == 3:
            return "👍"
        else:
            return "🔄"
    
    def _build_learning_message(self, parent: tk.Widget):
        """Construye el mensaje de aprendizaje."""
        # Obtener estadísticas actualizadas
        stats = self.controller.get_system_statistics()
        
        message = f"""Tu opinión ha sido procesada y guardada.
        
El sistema ha aprendido de tu experiencia y usará
este conocimiento para mejorar las futuras rutinas.

📊 Estado actual del sistema:
   • Generación: {stats['generacion']}
   • Total usuarios: {stats['total_usuarios']}
   • Satisfacción promedio: {stats['promedio_satisfaccion']:.2f}/5
   • Tasa de éxito: {stats['tasa_exito']:.1f}%
   
¡Cada feedback hace que la IA sea más inteligente!"""
        
        message_label = self.create_text_label(
            parent,
            message,
            justify='center'
        )
        message_label.pack(pady=20)
    
    def _build_navigation_buttons(self, parent: tk.Widget):
        """Construye los botones de navegación."""
        btn_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        btn_frame.pack(pady=20)
        
        # Botón inicio
        home_btn = self.create_button(
            btn_frame,
            "🏠 INICIO",
            command=self._on_home_clicked,
            padx=30,
            pady=12
        )
        home_btn.pack(side='left', padx=10)
        
        # Botón nueva rutina
        new_btn = self.create_button(
            btn_frame,
            "➕ NUEVA RUTINA",
            command=self._on_new_routine_clicked,
            bg=self.colors['bg_light'],
            padx=30,
            pady=12
        )
        new_btn.pack(side='left', padx=10)
    
    def _on_home_clicked(self):
        """Maneja el clic en inicio."""
        self.navigate_to('welcome')
    
    def _on_new_routine_clicked(self):
        """Maneja el clic en nueva rutina."""
        self.navigate_to('form')
    
    def set_satisfaccion(self, satisfaccion: int):
        """
        Actualiza el nivel de satisfacción.
        
        Args:
            satisfaccion: Nivel de satisfacción (1-5)
        """
        self.satisfaccion = satisfaccion
        
        # Reconstruir si ya está visible
        if self.frame and self.frame.winfo_ismapped():
            self.destroy()
            self.build()
            self.show()