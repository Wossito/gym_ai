"""
Ventana Principal de la Aplicación.

Esta clase actúa como coordinador entre las vistas y el controlador,
implementando el patrón MVC.
"""

import tkinter as tk
from typing import Dict, Any, Optional

from views.welcome_view import WelcomeView
from views.form_view import FormView
from views.routine_view import RoutineView
from views.feedback_view import FeedbackView
from views.thanks_view import ThanksView


class MainWindow:
    """
    Ventana principal que gestiona todas las vistas.
    
    Responsabilidades:
    - Crear y gestionar las vistas
    - Coordinar la navegación entre vistas
    - Comunicarse con el controlador de la aplicación
    - Mantener el header con estadísticas
    """
    
    def __init__(self, root: tk.Tk, app_controller):
        """
        Inicializa la ventana principal.
        
        Args:
            root: Ventana raíz de Tkinter
            app_controller: Controlador principal de la aplicación
        """
        self.root = root
        self.app_controller = app_controller
        
        # Configurar ventana
        self._setup_window()
        
        # Colores del tema
        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_medium': '#16213e',
            'bg_light': '#0f3460',
            'accent': '#00adb5',
            'text': '#eeeeee'
        }
        
        # Contenedores
        self.header_frame = None
        self.main_container = None
        
        # Vistas
        self.views: Dict[str, Any] = {}
        self.current_view = None
        
        # Datos de sesión
        self.session_data = {
            'user_data': None,
            'routine': None
        }
        
        # Construir UI
        self._build_ui()
        
        # Mostrar vista inicial
        self.show_view('welcome')
    
    def _setup_window(self):
        """Configura la ventana principal."""
        self.root.title("🏋️ Sistema de IA Adaptativo - Gimnasio")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a2e')
        
        # Centrar ventana
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _build_ui(self):
        """Construye la interfaz principal."""
        # Header
        self._build_header()
        
        # Contenedor principal para las vistas
        self.main_container = tk.Frame(
            self.root,
            bg=self.colors['bg_dark']
        )
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Inicializar vistas (lazy loading)
        # Las vistas se crean cuando se necesitan
    
    def _build_header(self):
        """Construye el header de la aplicación."""
        self.header_frame = tk.Frame(
            self.root,
            bg=self.colors['bg_light'],
            height=80
        )
        self.header_frame.pack(fill='x', side='top')
        self.header_frame.pack_propagate(False)
        
        # Título
        title = tk.Label(
            self.header_frame,
            text="🏋️ SISTEMA DE IA ADAPTATIVO PARA GIMNASIO",
            font=('Helvetica', 18, 'bold'),
            bg=self.colors['bg_light'],
            fg=self.colors['accent']
        )
        title.pack(pady=20)
        
        # Estadísticas (se actualiza dinámicamente)
        self.stats_label = tk.Label(
            self.header_frame,
            text="",
            font=('Helvetica', 9),
            bg=self.colors['bg_light'],
            fg=self.colors['text']
        )
        self.stats_label.pack()
        
        self._update_header_stats()
    
    def _update_header_stats(self):
        """Actualiza las estadísticas del header."""
        stats = self.app_controller.get_system_statistics()
        
        stats_text = (
            f"Generación: {stats['generacion']} | "
            f"Usuarios: {stats['total_usuarios']} | "
            f"Satisfacción: {stats['promedio_satisfaccion']:.1f}/5"
        )
        
        self.stats_label.config(text=stats_text)
    
    def show_view(self, view_name: str, **kwargs):
        """
        Muestra una vista específica.
        
        Args:
            view_name: Nombre de la vista ('welcome', 'form', etc.)
            **kwargs: Datos adicionales para la vista
        """
        # Actualizar estadísticas del header
        self._update_header_stats()
        
        # Ocultar vista actual
        if self.current_view:
            self.current_view.hide()
        
        # Obtener o crear la vista
        view = self._get_or_create_view(view_name, **kwargs)
        
        if view:
            # Actualizar datos si es necesario
            if hasattr(view, 'set_data'):
                if view_name == 'routine':
                    view.set_data(
                        kwargs.get('user_data', self.session_data.get('user_data', {})),
                        kwargs.get('routine', self.session_data.get('routine', {}))
                    )
                elif view_name == 'feedback':
                    view.set_data(
                        kwargs.get('user_data', self.session_data.get('user_data', {})),
                        kwargs.get('routine', self.session_data.get('routine', {}))
                    )
                elif view_name == 'thanks' and 'satisfaccion' in kwargs:
                    view.set_satisfaccion(kwargs['satisfaccion'])
            
            # Mostrar vista
            view.show()
            self.current_view = view
            
            # Manejar vista de carga (loading)
            if view_name == 'loading':
                self._handle_loading_view(kwargs.get('user_data', {}))
    
    def _get_or_create_view(self, view_name: str, **kwargs):
        """
        Obtiene una vista existente o crea una nueva.
        
        Args:
            view_name: Nombre de la vista
            **kwargs: Datos adicionales
            
        Returns:
            Instancia de la vista
        """
        # Vistas que NO se reutilizan (se crean cada vez)
        non_reusable = ['loading']
        
        if view_name in non_reusable or view_name not in self.views:
            view = self._create_view(view_name, **kwargs)
            if view and view_name not in non_reusable:
                self.views[view_name] = view
            return view
        
        return self.views[view_name]
    
    def _create_view(self, view_name: str, **kwargs):
        """
        Crea una nueva instancia de vista.
        
        Args:
            view_name: Nombre de la vista
            **kwargs: Datos adicionales
            
        Returns:
            Instancia de la vista
        """
        view_map = {
            'welcome': lambda: WelcomeView(self.main_container, self),
            'form': lambda: FormView(self.main_container, self),
            'routine': lambda: RoutineView(
                self.main_container,
                self,
                kwargs.get('user_data'),
                kwargs.get('routine')
            ),
            'feedback': lambda: FeedbackView(
                self.main_container,
                self,
                kwargs.get('user_data'),
                kwargs.get('routine')
            ),
            'thanks': lambda: ThanksView(
                self.main_container,
                self,
                kwargs.get('satisfaccion', 3)
            ),
            'loading': lambda: self._create_loading_view(kwargs.get('user_data', {}))
        }
        
        factory = view_map.get(view_name)
        return factory() if factory else None
    
    def _create_loading_view(self, user_data: dict):
        """
        Crea una vista de carga temporal.
        
        Args:
            user_data: Datos del usuario
            
        Returns:
            Vista temporal
        """
        from views.base_view import BaseView
        
        class LoadingView(BaseView):
            def build(self):
                self.frame = tk.Frame(
                    self.parent,
                    bg=self.colors['bg_dark']
                )
                
                center_frame = tk.Frame(
                    self.frame,
                    bg=self.colors['bg_medium'],
                    padx=60,
                    pady=60
                )
                center_frame.place(relx=0.5, rely=0.5, anchor='center')
                
                loading_label = self.create_title_label(
                    center_frame,
                    "🧠 IA TRABAJANDO...",
                    font=('Helvetica', 20, 'bold')
                )
                loading_label.pack(pady=20)
                
                status_texts = [
                    "🔍 Analizando tu perfil...",
                    "📊 Calculando IMC y métricas...",
                    "🎯 Buscando patrones en usuarios similares...",
                    "💡 Generando combinaciones de ejercicios...",
                    "⚡ Optimizando parámetros de entrenamiento...",
                    "✨ Creando tu rutina personalizada..."
                ]
                
                for text in status_texts:
                    label = self.create_text_label(center_frame, text)
                    label.pack(pady=5, anchor='w')
        
        view = LoadingView(self.main_container, self)
        
        # Guardar datos de usuario en sesión
        self.session_data['user_data'] = user_data
        
        return view
    
    def _handle_loading_view(self, user_data: dict):
        """
        Maneja la vista de carga y genera la rutina.
        
        Args:
            user_data: Datos del usuario
        """
        # Programar generación de rutina después de mostrar la vista
        self.root.after(1500, lambda: self._generate_routine(user_data))
    
    def _generate_routine(self, user_data: dict):
        """
        Genera la rutina usando el controlador.
        
        Args:
            user_data: Datos del usuario
        """
        # Obtener controlador de rutinas
        routine_controller = self.app_controller.get_routine_controller()
        
        # Crear usuario
        success, user_or_error = routine_controller.create_user_from_form(user_data)
        
        if not success:
            self.show_error("Error", user_or_error)
            self.show_view('form')
            return
        
        user = user_or_error
        
        # Generar rutina
        success, routine_or_error = routine_controller.generate_routine(user)
        
        if not success:
            self.show_error("Error", routine_or_error)
            self.show_view('form')
            return
        
        routine = routine_or_error
        
        # Preparar datos para mostrar
        user_data_with_profile = user_data.copy()
        user_data_with_profile['perfil'] = user.perfil.to_dict()
        
        routine_dict = routine.to_dict()
        
        # Guardar en sesión
        self.session_data['user_data'] = user_data_with_profile
        self.session_data['routine'] = routine_dict
        self.session_data['user_object'] = user
        self.session_data['routine_object'] = routine
        
        # Mostrar rutina
        self.show_view(
            'routine',
            user_data=user_data_with_profile,
            routine=routine_dict
        )
    
    def submit_feedback(self, user_data: dict, routine: dict, 
                       satisfaction: int, comments: str):
        """
        Procesa el feedback del usuario.
        
        Args:
            user_data: Datos del usuario
            routine: Rutina evaluada
            satisfaction: Nivel de satisfacción
            comments: Comentarios
            
        Returns:
            Tupla (success, result)
        """
        feedback_controller = self.app_controller.get_feedback_controller()
        
        # Obtener objetos de la sesión
        user = self.session_data.get('user_object')
        routine_obj = self.session_data.get('routine_object')
        
        if not user or not routine_obj:
            return False, "Datos de sesión no disponibles"
        
        return feedback_controller.submit_feedback(
            user,
            routine_obj,
            satisfaction,
            comments
        )
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del sistema.
        
        Returns:
            Diccionario con estadísticas
        """
        return self.app_controller.get_system_statistics()
    
    def show_error(self, title: str, message: str):
        """Muestra un mensaje de error."""
        from tkinter import messagebox
        messagebox.showerror(title, message)