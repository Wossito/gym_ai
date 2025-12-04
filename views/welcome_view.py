"""
Vista de Bienvenida.

Pantalla inicial que muestra información del sistema
y da la bienvenida al usuario.
"""

import tkinter as tk
from views.base_view import BaseView


class WelcomeView(BaseView):
    """
    Vista de bienvenida del sistema.
    
    Muestra:
    - Mensaje de bienvenida
    - Descripción del sistema
    - Estadísticas actuales
    - Botón para comenzar
    """
    
    def build(self):
        """Construye la interfaz de bienvenida."""
        self.frame = tk.Frame(
            self.parent,
            bg=self.colors['bg_dark']
        )
        
        # Frame central
        center_frame = tk.Frame(
            self.frame,
            bg=self.colors['bg_medium'],
            padx=40,
            pady=40
        )
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Logo/Título
        welcome_label = tk.Label(
            center_frame,
            text="💪 ¡BIENVENIDO!",
            font=('Helvetica', 24, 'bold'),
            bg=self.colors['bg_medium'],
            fg=self.colors['accent']
        )
        welcome_label.pack(pady=20)
        
        # Descripción del sistema
        description = """Sistema de Inteligencia Artificial que aprende de cada usuario
para generar rutinas de gimnasio cada vez más precisas y personalizadas.

El sistema analiza tu perfil, busca patrones en usuarios similares
y genera una rutina completamente personalizada para ti.

¡Mientras más personas lo usen, más inteligente se vuelve!"""
        
        desc_label = self.create_text_label(
            center_frame,
            description,
            justify='center',
            font=self.fonts['normal']
        )
        desc_label.pack(pady=20)
        
        # Estadísticas del sistema
        self._build_statistics_section(center_frame)
        
        # Botón comenzar
        start_button = self.create_button(
            center_frame,
            "COMENZAR →",
            command=self._on_start_clicked,
            font=('Helvetica', 14, 'bold'),
            padx=40,
            pady=15
        )
        start_button.pack(pady=20)
    
    def _build_statistics_section(self, parent: tk.Widget):
        """
        Construye la sección de estadísticas.
        
        Args:
            parent: Widget padre
        """
        # Obtener estadísticas del controlador
        stats = self.controller.get_system_statistics()
        
        stats_text = f"""
🧠 Generación actual del sistema: {stats['generacion']}
👥 Usuarios que han ayudado a entrenar la IA: {stats['total_usuarios']}
📊 Patrones exitosos identificados: {stats['patrones_exitosos']}
🎯 Tasa de satisfacción promedio: {stats['promedio_satisfaccion']:.2f}/5
"""
        
        stats_label = self.create_text_label(
            parent,
            stats_text,
            justify='left',
            fg=self.colors['success']
        )
        stats_label.pack(pady=15)
    
    def _on_start_clicked(self):
        """Maneja el clic en el botón comenzar."""
        self.navigate_to('form')