"""
Vista Base Abstracta.

Esta clase define la interfaz común para todas las vistas
del sistema, proporcionando funcionalidad compartida.
"""

from abc import ABC, abstractmethod
import tkinter as tk
from typing import Dict, Any, Optional, Callable


class BaseView(ABC):
    """
    Clase base abstracta para todas las vistas.
    
    Proporciona:
    - Configuración de estilos común
    - Métodos de navegación
    - Utilidades de UI compartidas
    """
    
    def __init__(self, parent: tk.Widget, controller: Any):
        """
        Inicializa la vista base.
        
        Args:
            parent: Widget padre (container principal)
            controller: Controlador de la aplicación
        """
        self.parent = parent
        self.controller = controller
        self.frame = None
        
        # Colores del tema
        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_medium': '#16213e',
            'bg_light': '#0f3460',
            'accent': '#00adb5',
            'text': '#eeeeee',
            'success': '#06d6a0',
            'warning': '#ffd93d',
            'error': '#ef476f'
        }
        
        # Fuentes
        self.fonts = {
            'title': ('Helvetica', 18, 'bold'),
            'subtitle': ('Helvetica', 14, 'bold'),
            'normal': ('Helvetica', 11),
            'small': ('Helvetica', 9)
        }
    
    @abstractmethod
    def build(self):
        """
        Construye la interfaz de la vista.
        Debe ser implementado por cada vista hija.
        """
        pass
    
    def show(self):
        """Muestra la vista."""
        if self.frame is None:
            self.build()
        
        # Limpiar el parent
        self.clear_parent()
        
        # Mostrar esta vista
        if self.frame:
            self.frame.pack(fill='both', expand=True)
    
    def hide(self):
        """Oculta la vista."""
        if self.frame:
            self.frame.pack_forget()
    
    def clear_parent(self):
        """Oculta widgets previos sin destruirlos."""
        for widget in self.parent.winfo_children():
            widget.pack_forget()

    
    def destroy(self):
        """Destruye la vista."""
        if self.frame:
            self.frame.destroy()
            self.frame = None
    
    # ========================================================================
    # UTILIDADES DE UI
    # ========================================================================
    
    def create_title_label(self, parent: tk.Widget, text: str, 
                          **kwargs) -> tk.Label:
        """
        Crea un label de título.
        
        Args:
            parent: Widget padre
            text: Texto del título
            **kwargs: Argumentos adicionales
            
        Returns:
            Label creado
        """
        defaults = {
            'font': self.fonts['title'],
            'bg': self.colors['bg_medium'],
            'fg': self.colors['accent']
        }
        defaults.update(kwargs)
        
        return tk.Label(parent, text=text, **defaults)
    
    def create_text_label(self, parent: tk.Widget, text: str,
                         **kwargs) -> tk.Label:
        """
        Crea un label de texto normal.
        
        Args:
            parent: Widget padre
            text: Texto del label
            **kwargs: Argumentos adicionales
            
        Returns:
            Label creado
        """
        defaults = {
            'font': self.fonts['normal'],
            'bg': self.colors['bg_medium'],
            'fg': self.colors['text']
        }
        defaults.update(kwargs)
        
        return tk.Label(parent, text=text, **defaults)
    
    def create_button(self, parent: tk.Widget, text: str,
                     command: Callable, **kwargs) -> tk.Button:
        """
        Crea un botón estilizado.
        
        Args:
            parent: Widget padre
            text: Texto del botón
            command: Función a ejecutar
            **kwargs: Argumentos adicionales
            
        Returns:
            Botón creado
        """
        defaults = {
            'font': self.fonts['subtitle'],
            'bg': self.colors['accent'],
            'fg': 'white',
            'activebackground': self.colors['success'],
            'activeforeground': 'white',
            'padx': 30,
            'pady': 12,
            'border': 0,
            'cursor': 'hand2'
        }
        defaults.update(kwargs)
        
        return tk.Button(parent, text=text, command=command, **defaults)
    
    def create_entry(self, parent: tk.Widget, **kwargs) -> tk.Entry:
        """
        Crea un campo de entrada estilizado.
        
        Args:
            parent: Widget padre
            **kwargs: Argumentos adicionales
            
        Returns:
            Entry creado
        """
        defaults = {
            'font': self.fonts['normal'],
            'bg': self.colors['bg_light'],
            'fg': self.colors['text'],
            'insertbackground': self.colors['text'],
            'relief': 'flat',
            'width': 30
        }
        defaults.update(kwargs)
        
        return tk.Entry(parent, **defaults)
    
    def create_scrollable_frame(self, parent: tk.Widget) -> tuple:
        """
        Crea un frame con scrollbar.
        
        Args:
            parent: Widget padre
            
        Returns:
            Tupla (canvas, scrollbar, scrollable_frame)
        """
        canvas = tk.Canvas(
            parent, 
            bg=self.colors['bg_dark'],
            highlightthickness=0
        )
        
        scrollbar = tk.Scrollbar(
            parent,
            orient="vertical",
            command=canvas.yview
        )
        
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_medium'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        return canvas, scrollbar, scrollable_frame
    
    def create_info_frame(self, parent: tk.Widget, 
                         title: str, content: str) -> tk.Frame:
        """
        Crea un frame informativo.
        
        Args:
            parent: Widget padre
            title: Título del frame
            content: Contenido del frame
            
        Returns:
            Frame creado
        """
        frame = tk.Frame(
            parent,
            bg=self.colors['bg_medium'],
            padx=20,
            pady=15
        )
        
        if title:
            title_label = self.create_title_label(frame, title)
            title_label.pack(anchor='w', pady=(0, 10))
        
        content_label = self.create_text_label(
            frame,
            content,
            justify='left'
        )
        content_label.pack(anchor='w')
        
        return frame
    
    # ========================================================================
    # NAVEGACIÓN
    # ========================================================================
    
    def navigate_to(self, view_name: str, **kwargs):
        """
        Navega a otra vista.
        
        Args:
            view_name: Nombre de la vista destino
            **kwargs: Datos a pasar a la vista
        """
        if hasattr(self.controller, 'show_view'):
            self.controller.show_view(view_name, **kwargs)
    
    def show_error(self, title: str, message: str):
        """
        Muestra un mensaje de error.
        
        Args:
            title: Título del error
            message: Mensaje del error
        """
        from tkinter import messagebox
        messagebox.showerror(title, message)
    
    def show_info(self, title: str, message: str):
        """
        Muestra un mensaje informativo.
        
        Args:
            title: Título del mensaje
            message: Contenido del mensaje
        """
        from tkinter import messagebox
        messagebox.showinfo(title, message)
    
    def show_warning(self, title: str, message: str):
        """
        Muestra un mensaje de advertencia.
        
        Args:
            title: Título de la advertencia
            message: Contenido de la advertencia
        """
        from tkinter import messagebox
        messagebox.showwarning(title, message)