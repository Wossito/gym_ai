"""
Vista de Formulario.

Formulario para recopilar información del usuario
antes de generar la rutina.
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from views.base_view import BaseView


class FormView(BaseView):
    """
    Vista del formulario de datos del usuario.
    
    Recopila:
    - Información personal (nombre, edad, peso, altura)
    - Nivel de experiencia
    - Objetivo de entrenamiento
    - Días disponibles
    - Limitaciones físicas
    """
    
    def __init__(self, parent: tk.Widget, controller):
        super().__init__(parent, controller)
        self.form_vars = {}
    
    def build(self):
        """Construye la interfaz del formulario."""
        self.frame = tk.Frame(
            self.parent,
            bg=self.colors['bg_dark']
        )
        
        # Crear frame con scroll
        canvas, scrollbar, scrollable_frame = self.create_scrollable_frame(
            self.frame
        )
        
        canvas.pack(side="left", fill="both", expand=True, padx=(0, 10))
        scrollbar.pack(side="right", fill="y")
        
        # Contenido del formulario
        content_frame = tk.Frame(
            scrollable_frame,
            bg=self.colors['bg_medium'],
            padx=50,
            pady=30
        )
        content_frame.pack(fill='both', expand=True)
        
        # Título
        title = self.create_title_label(
            content_frame,
            "📝 Cuéntame sobre ti",
            font=('Helvetica', 20, 'bold')
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Construir campos del formulario
        self._build_form_fields(content_frame)
        
        # Botón generar
        btn_frame = tk.Frame(content_frame, bg=self.colors['bg_medium'])
        btn_frame.grid(row=100, column=0, columnspan=2, pady=30)
        
        generate_btn = self.create_button(
            btn_frame,
            "🧠 GENERAR RUTINA CON IA",
            command=self._on_generate_clicked,
            font=('Helvetica', 14, 'bold'),
            padx=40,
            pady=15
        )
        generate_btn.pack()
    
    def _build_form_fields(self, parent: tk.Widget):
        """
        Construye los campos del formulario.
        
        Args:
            parent: Widget padre
        """
        row = 1
        
        # Campos de texto simples
        text_fields = [
            ("Nombre:", "nombre"),
            ("Edad:", "edad"),
            ("Peso (kg):", "peso"),
            ("Altura (m):", "altura"),
        ]
        
        for label_text, var_name in text_fields:
            self._create_text_field(parent, row, label_text, var_name)
            row += 1
        
        # Nivel de experiencia
        self._create_radio_field(
            parent, row,
            "Nivel de experiencia:",
            "nivel",
            ['principiante', 'intermedio', 'avanzado'],
            default='principiante'
        )
        row += 1
        
        # Objetivo
        self._create_radio_field(
            parent, row,
            "Objetivo principal:",
            "objetivo",
            [
                ('Perder peso', 'perder_peso'),
                ('Ganar masa', 'ganar_masa'),
                ('Resistencia', 'resistencia'),
                ('Fuerza', 'fuerza')
            ],
            default='ganar_masa',
            vertical=True
        )
        row += 1
        
        # Días de entrenamiento
        self._create_spinbox_field(
            parent, row,
            "Días disponibles:",
            "dias",
            from_=2,
            to=7,
            default=4
        )
        row += 1
        
        # Limitaciones
        self._create_text_area_field(
            parent, row,
            "Limitaciones (opcional):",
            "limitaciones"
        )
    
    def _create_text_field(self, parent: tk.Widget, row: int,
                          label_text: str, var_name: str):
        """Crea un campo de texto."""
        label = self.create_text_label(
            parent,
            label_text,
            font=('Helvetica', 12)
        )
        label.grid(row=row, column=0, sticky='w', pady=10, padx=(0, 20))
        
        entry = self.create_entry(parent)
        entry.grid(row=row, column=1, pady=10)
        
        self.form_vars[var_name] = entry
    
    def _create_radio_field(self, parent: tk.Widget, row: int,
                           label_text: str, var_name: str,
                           options: list, default: str = None,
                           vertical: bool = False):
        """Crea un campo con radio buttons."""
        label = self.create_text_label(
            parent,
            label_text,
            font=('Helvetica', 12)
        )
        label.grid(row=row, column=0, sticky='w', pady=10, padx=(0, 20))
        
        var = tk.StringVar(value=default or options[0])
        
        radio_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        radio_frame.grid(row=row, column=1, pady=10, sticky='w')
        
        for option in options:
            # Manejar tuplas (texto, valor)
            if isinstance(option, tuple):
                text, value = option
            else:
                text = option.title()
                value = option
            
            rb = tk.Radiobutton(
                radio_frame,
                text=text,
                variable=var,
                value=value,
                font=self.fonts['normal'],
                bg=self.colors['bg_medium'],
                fg=self.colors['text'],
                selectcolor=self.colors['bg_light'],
                activebackground=self.colors['bg_medium'],
                activeforeground=self.colors['accent']
            )
            
            if vertical:
                rb.pack(anchor='w', pady=2)
            else:
                rb.pack(side='left', padx=10)
        
        self.form_vars[var_name] = var
    
    def _create_spinbox_field(self, parent: tk.Widget, row: int,
                             label_text: str, var_name: str,
                             from_: int, to: int, default: int):
        """Crea un campo spinbox."""
        label = self.create_text_label(
            parent,
            label_text,
            font=('Helvetica', 12)
        )
        label.grid(row=row, column=0, sticky='w', pady=10, padx=(0, 20))
        
        var = tk.IntVar(value=default)
        
        spinbox = tk.Spinbox(
            parent,
            from_=from_,
            to=to,
            textvariable=var,
            font=self.fonts['normal'],
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            width=28
        )
        spinbox.grid(row=row, column=1, pady=10)
        
        self.form_vars[var_name] = var
    
    def _create_text_area_field(self, parent: tk.Widget, row: int,
                               label_text: str, var_name: str):
        """Crea un campo de texto multilínea."""
        label = self.create_text_label(
            parent,
            label_text,
            font=('Helvetica', 12)
        )
        label.grid(row=row, column=0, sticky='w', pady=10, padx=(0, 20))
        
        text_widget = tk.Text(
            parent,
            height=3,
            font=self.fonts['normal'],
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief='flat',
            width=30
        )
        text_widget.grid(row=row, column=1, pady=10)
        
        self.form_vars[var_name] = text_widget
    
    def _validate_and_collect_data(self) -> dict:
        """
        Valida y recopila los datos del formulario.
        
        Returns:
            Diccionario con los datos o None si hay error
        """
        try:
            # Recopilar datos
            nombre = self.form_vars['nombre'].get().strip()
            edad = int(self.form_vars['edad'].get())
            peso = float(self.form_vars['peso'].get())
            altura = float(self.form_vars['altura'].get())
            
            # Validar datos básicos
            if not nombre:
                self.show_error("Error", "El nombre es requerido")
                return None
            
            if edad < 10 or edad > 100:
                self.show_error("Error", "Edad inválida (10-100 años)")
                return None
            
            if peso < 30 or peso > 300:
                self.show_error("Error", "Peso inválido (30-300 kg)")
                return None
            
            if altura < 1.0 or altura > 2.5:
                self.show_error("Error", "Altura inválida (1.0-2.5 m)")
                return None
            
            # Obtener limitaciones
            limitaciones = self.form_vars['limitaciones'].get('1.0', 'end').strip()
            
            return {
                'nombre': nombre,
                'edad': edad,
                'peso': peso,
                'altura': altura,
                'nivel_experiencia': self.form_vars['nivel'].get(),
                'objetivo': self.form_vars['objetivo'].get(),
                'dias_entrenamiento': self.form_vars['dias'].get(),
                'limitaciones': limitaciones or 'ninguna',
                'fecha_inicio': datetime.now().isoformat()
            }
            
        except ValueError:
            self.show_error(
                "Error",
                "Por favor, ingresa valores numéricos válidos"
            )
            return None
    
    def _on_generate_clicked(self):
        """Maneja el clic en generar rutina."""
        data = self._validate_and_collect_data()
        
        if data:
            # Navegar a vista de carga con los datos
            self.navigate_to('loading', user_data=data)