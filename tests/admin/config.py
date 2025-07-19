"""
Configuración global del proyecto
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno si existen
load_dotenv()

class Config:
    # URLs
    BASE_URL = "https://teammates-hormiga-1.uc.r.appspot.com"
    
    # Credenciales (usar variables de entorno por seguridad)
    INSTRUCTOR_EMAIL = os.getenv('INSTRUCTOR_EMAIL', 'instructor@example.com')
    INSTRUCTOR_PASSWORD = os.getenv('INSTRUCTOR_PASSWORD', 'password123')
    
    # Rutas
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    TEST_DATA_DIR = os.path.join(PROJECT_ROOT, 'test_data')
    REPORTS_DIR = os.path.join(PROJECT_ROOT, 'reports')
    
    # Configuración de pruebas
    SCREENSHOT_ON_FAILURE = True
    TIMEOUT = 10
    
    @classmethod
    def get_test_data_path(cls, filename):
        """Obtiene la ruta completa de un archivo de datos de prueba"""
        return os.path.join(cls.TEST_DATA_DIR, filename)