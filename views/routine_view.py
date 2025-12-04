"""
Vista de Rutina.

Muestra la rutina generada con todos sus detalles.
"""

import tkinter as tk
from views.base_view import BaseView


class RoutineView(BaseView):
    """
    Vista para mostrar la rutina generada.
    
    Muestra:
    - Análisis del perfil del usuario
    - Rutina semanal completa
    - Botones de acción (feedback, nueva rutina)
    """
    
    def __init__(self, parent: tk.Widget, controller, user_data: dict = None, routine: dict = None):
        super().__init__(parent, controller)
        self.user_data = user_data or {}
        self.routine = routine or {}
    
    def build(self):
        """Construye la interfaz de la rutina."""
        self.frame = tk.Frame(
            self.parent,
            bg=self.colors['bg_dark']
        )
        
        # Frame con scroll
        canvas, scrollbar, scrollable_frame = self.create_scrollable_frame(
            self.frame
        )
        
        canvas.pack(side="left", fill="both", expand=True, padx=(0, 10))
        scrollbar.pack(side="right", fill="y")
        
        # Contenido
        content_frame = tk.Frame(
            scrollable_frame,
            bg=self.colors['bg_dark'],
            padx=20,
            pady=20
        )
        content_frame.pack(fill='both', expand=True)
        
        # Título personalizado
        nombre = self.user_data.get('nombre', 'Usuario').upper()
        title = self.create_title_label(
            content_frame,
            f"🎯 RUTINA PERSONALIZADA PARA {nombre}",
            bg=self.colors['bg_dark']
        )
        title.pack(pady=(0, 20))
        
        # Análisis del perfil
        self._build_profile_analysis(content_frame)
        
        # Rutina semanal
        self._build_weekly_routine(content_frame)
        
        # Botones de acción
        self._build_action_buttons(content_frame)
    
    def _build_profile_analysis(self, parent: tk.Widget):
        """Construye la sección de análisis del perfil."""
        perfil = self.user_data.get('perfil', {})
        metadatos = self.routine.get('metadatos', {})
        
        imc = perfil.get('imc', 0)
        imc_category = self._get_imc_category(imc)
        
        info_text = f"""📊 ANÁLISIS DE TU PERFIL
        
IMC: {imc:.1f} - {imc_category}
Edad: {perfil.get('edad')} años | Nivel: {perfil.get('nivel_str', '').title()} | Objetivo: {perfil.get('objetivo_str', '').replace('_', ' ').title()}

🧠 Modo de generación: {metadatos.get('modo_generacion', 'IA').upper()}"""
        
        if 'basado_en' in metadatos:
            info_text += f"\n📚 Basado en {metadatos['basado_en']} perfiles similares exitosos"
            info_text += f"\n✅ Nivel de confianza: {metadatos.get('confianza', 0)*100:.0f}%"
        
        info_frame = tk.Frame(
            parent,
            bg=self.colors['bg_medium'],
            padx=20,
            pady=15
        )
        info_frame.pack(fill='x', pady=(0, 20))
        
        info_label = self.create_text_label(
            info_frame,
            info_text,
            justify='left'
        )
        info_label.pack(anchor='w')
    
    def _build_weekly_routine(self, parent: tk.Widget):
        """Construye la rutina semanal."""
        rutina_semanal = self.routine.get('rutina_semanal', {})
        
        for dia, ejercicios in rutina_semanal.items():
            dia_frame = tk.Frame(
                parent,
                bg=self.colors['bg_medium'],
                padx=20,
                pady=15
            )
            dia_frame.pack(fill='x', pady=10)
            
            # Título del día
            dia_label = tk.Label(
                dia_frame,
                text=f"📅 {dia.upper()}",
                font=('Helvetica', 13, 'bold'),
                bg=self.colors['bg_medium'],
                fg=self.colors['accent']
            )
            dia_label.pack(anchor='w', pady=(0, 10))
            
            # Ejercicios del día
            for idx, ejercicio in enumerate(ejercicios, 1):
                self._build_exercise_item(dia_frame, idx, ejercicio)
    
    def _build_exercise_item(self, parent: tk.Widget, idx: int, ejercicio: dict):
        """Construye un item de ejercicio."""
        # Nombre del ejercicio
        ej_text = f"{idx}. {ejercicio['ejercicio']} ({ejercicio['grupo'].title()})"
        
        # Parámetros según tipo
        if 'series' in ejercicio:
            ej_text += f"\n   Series: {ejercicio['series']} | "
            ej_text += f"Reps: {ejercicio['repeticiones']} | "
            ej_text += f"Descanso: {ejercicio['descanso']}"
        else:
            ej_text += f"\n   Duración: {ejercicio['duracion']} | "
            ej_text += f"Intensidad: {ejercicio['intensidad'].title()}"
        
        ej_label = self.create_text_label(
            parent,
            ej_text,
            justify='left'
        )
        ej_label.pack(anchor='w', pady=5)
    
    def _build_action_buttons(self, parent: tk.Widget):
        """Construye los botones de acción."""
        btn_frame = tk.Frame(parent, bg=self.colors['bg_dark'])
        btn_frame.pack(pady=30)
        
        # Botón feedback
        feedback_btn = self.create_button(
            btn_frame,
            "💬 DAR FEEDBACK",
            command=self._on_feedback_clicked,
            bg=self.colors['success'],
            padx=30,
            pady=12
        )
        feedback_btn.pack(side='left', padx=10)
        
        # Botón nueva rutina
        new_btn = self.create_button(
            btn_frame,
            "🔄 NUEVA RUTINA",
            command=self._on_new_routine_clicked,
            bg=self.colors['bg_light'],
            padx=30,
            pady=12
        )
        new_btn.pack(side='left', padx=10)
    
    def _get_imc_category(self, imc: float) -> str:
        """Obtiene la categoría del IMC."""
        if imc < 18.5:
            return "Bajo peso"
        elif imc < 25:
            return "Peso normal"
        elif imc < 30:
            return "Sobrepeso"
        else:
            return "Obesidad"
    
    def _on_feedback_clicked(self):
        """Maneja el clic en dar feedback."""
        self.navigate_to(
            'feedback',
            user_data=self.user_data,
            routine=self.routine
        )
    
    def _on_new_routine_clicked(self):
        """Maneja el clic en nueva rutina."""
        self.navigate_to('form')
    
    def set_data(self, user_data: dict, routine: dict):
        """
        Actualiza los datos de la vista.
        
        Args:
            user_data: Datos del usuario
            routine: Rutina generada
        """
        self.user_data = user_data
        self.routine = routine
        
        # Reconstruir si ya está visible
        if self.frame and self.frame.winfo_ismapped():
            self.destroy()
            self.build()
            self.show()