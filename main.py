"""
Punto de entrada principal de la aplicación.

Este archivo inicia la aplicación con interfaz gráfica (GUI)
o en modo consola si no está disponible Tkinter.
"""

import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controllers.app_controller import AppController
from utils.constants import SYSTEM_NAME, SYSTEM_VERSION


def print_banner():
    """Imprime el banner de inicio."""
    banner = f"""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🏋️  {SYSTEM_NAME}                                    ║
║   Version {SYSTEM_VERSION}                                       ║
║                                                                   ║
║   Sistema de Inteligencia Artificial para                        ║
║   Generación de Rutinas de Gimnasio                              ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def run_gui_mode():
    """Ejecuta la aplicación con interfaz gráfica."""
    try:
        import tkinter as tk
        # CORRECCIÓN: Importar desde el módulo correcto
        from views.main_window import MainWindow
        
        print("🖥️  Iniciando interfaz gráfica...")
        
        # Inicializar controlador de aplicación
        app_controller = AppController()
        
        # Crear ventana principal
        root = tk.Tk()
        
        # CORRECCIÓN: Usar MainWindow correctamente
        main_window = MainWindow(root, app_controller)
        
        # Ejecutar loop de eventos
        root.mainloop()
        
        # Al cerrar, guardar estado
        app_controller.shutdown()
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("❌ Tkinter no disponible. Cambiando a modo consola...")
        run_console_mode()
    except Exception as e:
        print(f"❌ Error en modo GUI: {e}")
        import traceback
        traceback.print_exc()
        print("\nCambiando a modo consola...")
        run_console_mode()


def run_console_mode():
    """Ejecuta la aplicación en modo consola."""
    print("💻 Modo consola iniciado\n")
    
    # Inicializar controlador
    app_controller = AppController()
    
    print("\n" + "="*70)
    print("MENÚ PRINCIPAL")
    print("="*70)
    print("1. Crear usuario y generar rutina")
    print("2. Ver estadísticas del sistema")
    print("3. Exportar estadísticas")
    print("4. Reiniciar sistema")
    print("5. Salir")
    print("="*70)
    
    while True:
        try:
            opcion = input("\nSelecciona una opción (1-5): ").strip()
            
            if opcion == '1':
                create_user_and_routine(app_controller)
            
            elif opcion == '2':
                show_statistics(app_controller)
            
            elif opcion == '3':
                export_statistics(app_controller)
            
            elif opcion == '4':
                reset_system(app_controller)
            
            elif opcion == '5':
                app_controller.shutdown()
                print("\n👋 ¡Hasta pronto!")
                break
            
            else:
                print("❌ Opción inválida. Por favor selecciona 1-5.")
        
        except KeyboardInterrupt:
            print("\n\n🔄 Cerrando aplicación...")
            app_controller.shutdown()
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def create_user_and_routine(app_controller: AppController):
    """Flujo para crear usuario y generar rutina."""
    print("\n" + "="*70)
    print("CREAR USUARIO Y GENERAR RUTINA")
    print("="*70)
    
    try:
        # Recopilar datos
        nombre = input("Nombre: ").strip()
        edad = int(input("Edad: "))
        peso = float(input("Peso (kg): "))
        altura = float(input("Altura (m): "))
        
        print("\nNivel de experiencia:")
        print("1. Principiante")
        print("2. Intermedio")
        print("3. Avanzado")
        nivel_num = int(input("Selecciona (1-3): "))
        nivel_map = {1: 'principiante', 2: 'intermedio', 3: 'avanzado'}
        nivel = nivel_map.get(nivel_num, 'intermedio')
        
        print("\nObjetivo:")
        print("1. Perder peso")
        print("2. Ganar masa muscular")
        print("3. Resistencia")
        print("4. Fuerza")
        objetivo_num = int(input("Selecciona (1-4): "))
        objetivo_map = {
            1: 'perder_peso',
            2: 'ganar_masa',
            3: 'resistencia',
            4: 'fuerza'
        }
        objetivo = objetivo_map.get(objetivo_num, 'ganar_masa')
        
        dias = int(input("Días de entrenamiento por semana (2-7): "))
        limitaciones = input("Limitaciones físicas (o presiona Enter): ").strip()
        
        # Crear form data
        form_data = {
            'nombre': nombre,
            'edad': edad,
            'peso': peso,
            'altura': altura,
            'nivel_experiencia': nivel,
            'objetivo': objetivo,
            'dias_entrenamiento': dias,
            'limitaciones': limitaciones or 'ninguna'
        }
        
        # Ejecutar flujo
        result = app_controller.complete_user_flow(form_data)
        
        if result['success']:
            print("\n✅ Usuario creado y rutina generada exitosamente!")
            print(f"\n📋 Resumen:")
            print(f"   Usuario: {result['user'].nombre}")
            print(f"   Rutina: {result['routine'].get_summary()}")
            
            # Preguntar por feedback
            print("\n¿Deseas dar feedback? (s/n): ", end='')
            if input().strip().lower() == 's':
                satisfaction = int(input("Satisfacción (1-5): "))
                comments = input("Comentarios (opcional): ").strip()
                
                success, feedback_result = app_controller.feedback_controller.submit_feedback(
                    result['user'],
                    result['routine'],
                    satisfaction,
                    comments
                )
                
                if success:
                    print("✅ Feedback procesado")
        else:
            print(f"❌ Error: {result.get('error', 'Desconocido')}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def show_statistics(app_controller: AppController):
    """Muestra estadísticas del sistema."""
    print("\n" + "="*70)
    print("ESTADÍSTICAS DEL SISTEMA")
    print("="*70)
    
    stats = app_controller.get_system_statistics()
    
    print(f"\n📊 Generación: {stats['generacion']}")
    print(f"👥 Usuarios totales: {stats['total_usuarios']}")
    print(f"🏋️  Rutinas generadas: {stats['total_rutinas']}")
    print(f"⭐ Satisfacción promedio: {stats['promedio_satisfaccion']:.2f}/5")
    print(f"✅ Tasa de éxito: {stats['tasa_exito']:.1f}%")
    print(f"🎯 Patrones identificados: {stats['patrones_exitosos']}")
    print(f"🔬 Factor de exploración: {stats['factor_exploracion']:.2%}")


def export_statistics(app_controller: AppController):
    """Exporta estadísticas."""
    print("\n📊 Exportando estadísticas...")
    
    if app_controller.export_statistics():
        print("✅ Estadísticas exportadas exitosamente")
    else:
        print("❌ Error al exportar estadísticas")


def reset_system(app_controller: AppController):
    """Reinicia el sistema."""
    print("\n⚠️  ADVERTENCIA: Esto eliminará todos los datos del sistema.")
    confirm = input("¿Estás seguro? (escribe 'CONFIRMAR'): ").strip()
    
    if confirm == 'CONFIRMAR':
        if app_controller.reset_system():
            print("✅ Sistema reiniciado")
        else:
            print("❌ Error al reiniciar")
    else:
        print("❌ Operación cancelada")


def main():
    """Función principal."""
    print_banner()
    
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == '--console' or mode == '-c':
            run_console_mode()
            return
    
    # Por defecto, intentar GUI
    try:
        import tkinter
        run_gui_mode()
    except ImportError:
        print("ℹ️  Tkinter no disponible. Usando modo consola.")
        print("   Para forzar modo consola: python main.py --console\n")
        run_console_mode()


if __name__ == "__main__":
    main()