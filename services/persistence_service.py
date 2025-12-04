"""
Servicio de Persistencia.

Este servicio maneja toda la persistencia de datos del sistema,
incluyendo carga y guardado de datos en JSON.
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from config import DATA_FILE
from models.learning_system import LearningSystem


class PersistenceService:
    """
    Servicio para persistencia de datos.
    
    Maneja la carga y guardado del estado completo del sistema
    en formato JSON.
    """
    
    def __init__(self, data_file: Path = DATA_FILE):
        """
        Inicializa el servicio de persistencia.
        
        Args:
            data_file: Ruta al archivo de datos
        """
        self.data_file = data_file
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Asegura que el directorio de datos exista."""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
    
    def load_learning_system(self) -> Optional[LearningSystem]:
        """
        Carga el sistema de aprendizaje desde el archivo.
        
        Returns:
            LearningSystem si existe, None si no hay datos previos
        """
        if not self.data_file.exists():
            print("📂 No se encontró archivo de datos previo")
            return None
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            learning_data = data.get('learning_system', {})
            learning_system = LearningSystem.from_dict(learning_data)
            
            print(f"✓ Datos cargados - Generación {learning_system.generacion}")
            print(f"  • {learning_system.get_total_users()} usuarios")
            print(f"  • {learning_system.get_total_routines()} rutinas generadas")
            print(f"  • Satisfacción promedio: {learning_system.get_average_satisfaction():.2f}/5")
            
            return learning_system
            
        except json.JSONDecodeError as e:
            print(f"❌ Error al decodificar JSON: {e}")
            return None
        except Exception as e:
            print(f"❌ Error al cargar datos: {e}")
            return None
    
    def save_learning_system(self, learning_system: LearningSystem) -> bool:
        """
        Guarda el sistema de aprendizaje en el archivo.
        
        Args:
            learning_system: Sistema de aprendizaje a guardar
            
        Returns:
            True si se guardó exitosamente
        """
        try:
            data = {
                'learning_system': learning_system.to_dict(),
                'metricas': self._generate_metrics(learning_system),
                'last_update': datetime.now().isoformat()
            }
            
            # Crear backup del archivo anterior si existe
            if self.data_file.exists():
                self._create_backup()
            
            # Guardar nuevos datos
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print("💾 Datos guardados exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error al guardar datos: {e}")
            return False
    
    def _create_backup(self):
        """Crea un backup del archivo de datos actual."""
        try:
            backup_dir = self.data_file.parent / 'backups'
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = backup_dir / f"backup_{timestamp}.json"
            
            # Copiar archivo actual a backup
            import shutil
            shutil.copy2(self.data_file, backup_file)
            
            # Mantener solo los últimos 5 backups
            self._cleanup_old_backups(backup_dir, keep=5)
            
        except Exception as e:
            print(f"⚠️  No se pudo crear backup: {e}")
    
    def _cleanup_old_backups(self, backup_dir: Path, keep: int = 5):
        """
        Elimina backups antiguos, manteniendo solo los más recientes.
        
        Args:
            backup_dir: Directorio de backups
            keep: Número de backups a mantener
        """
        try:
            backups = sorted(backup_dir.glob('backup_*.json'))
            
            # Eliminar backups antiguos
            if len(backups) > keep:
                for backup in backups[:-keep]:
                    backup.unlink()
                    
        except Exception as e:
            print(f"⚠️  Error al limpiar backups: {e}")
    
    def _generate_metrics(self, learning_system: LearningSystem) -> Dict[str, Any]:
        """
        Genera métricas del sistema.
        
        Args:
            learning_system: Sistema de aprendizaje
            
        Returns:
            Diccionario con métricas
        """
        return {
            'precision_predicciones': [],  # Por implementar
            'satisfaccion_promedio_por_generacion': self._get_satisfaction_by_generation(learning_system),
            'mejores_rutinas': []  # Por implementar
        }
    
    def _get_satisfaction_by_generation(self, learning_system: LearningSystem) -> list:
        """
        Obtiene satisfacción promedio por cada feedback.
        
        Args:
            learning_system: Sistema de aprendizaje
            
        Returns:
            Lista con satisfacción por generación
        """
        return [
            {
                'generacion': learning_system.generacion,
                'satisfaccion': exp.get('satisfaccion', 0)
            }
            for exp in learning_system.historico_usuarios
        ]
    
    def export_statistics(self, learning_system: LearningSystem, 
                         output_file: Optional[Path] = None) -> bool:
        """
        Exporta estadísticas del sistema a un archivo separado.
        
        Args:
            learning_system: Sistema de aprendizaje
            output_file: Archivo de salida (opcional)
            
        Returns:
            True si se exportó exitosamente
        """
        if output_file is None:
            output_file = self.data_file.parent / 'statistics.json'
        
        try:
            stats = {
                'timestamp': datetime.now().isoformat(),
                'statistics': learning_system.get_statistics(),
                'details': {
                    'satisfaction_history': [
                        {
                            'fecha': exp.get('fecha', ''),
                            'satisfaccion': exp.get('satisfaccion', 0),
                            'nivel': exp.get('perfil', {}).get('nivel_str', ''),
                            'objetivo': exp.get('perfil', {}).get('objetivo_str', '')
                        }
                        for exp in learning_system.historico_usuarios
                    ],
                    'patterns_count': {
                        key: len(patterns)
                        for key, patterns in learning_system.patrones_exitosos.items()
                    }
                }
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
            
            print(f"📊 Estadísticas exportadas a {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error al exportar estadísticas: {e}")
            return False
    
    def clear_data(self) -> bool:
        """
        Elimina el archivo de datos (reinicia el sistema).
        
        Returns:
            True si se eliminó exitosamente
        """
        try:
            if self.data_file.exists():
                # Crear backup antes de eliminar
                self._create_backup()
                self.data_file.unlink()
                print("🗑️  Datos eliminados (backup creado)")
                return True
            else:
                print("ℹ️  No hay datos para eliminar")
                return False
                
        except Exception as e:
            print(f"❌ Error al eliminar datos: {e}")
            return False
    
    def file_exists(self) -> bool:
        """
        Verifica si existe el archivo de datos.
        
        Returns:
            True si existe
        """
        return self.data_file.exists()
    
    def get_file_size(self) -> int:
        """
        Obtiene el tamaño del archivo de datos.
        
        Returns:
            Tamaño en bytes
        """
        if self.file_exists():
            return self.data_file.stat().st_size
        return 0
    
    def get_last_modified(self) -> Optional[datetime]:
        """
        Obtiene la fecha de última modificación del archivo.
        
        Returns:
            Datetime de última modificación
        """
        if self.file_exists():
            timestamp = self.data_file.stat().st_mtime
            return datetime.fromtimestamp(timestamp)
        return None