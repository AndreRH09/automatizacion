# test_suite_admin.py
"""
Suite de pruebas automatizadas para el módulo Administrador de TEAMMATES
Ejecuta todos los casos de prueba de forma secuencial
"""

import os
import sys
from datetime import datetime
import importlib
import time

class AdminTestSuite:
    def __init__(self):
        self.test_cases = [
            {
                "id": "CPF-ADM-006",
                "module": "test_cpf_adm_006",
                "class": "TestVisualizacionSesiones",
                "name": "Visualización de sesiones en curso"
            },
            {
                "id": "CPF-ADM-007", 
                "module": "test_cpf_adm_007",
                "class": "TestNotificacionesSistema",
                "name": "Ver notificaciones del sistema"
            }
            # Agregar más casos de prueba aquí
        ]
        
        self.results = []
        self.start_time = None
        self.end_time = None
    
    def setup_chrome_debug(self):
        """Verifica o configura Chrome en modo debug"""
        print("🔧 Verificando Chrome en modo debug...")
        
        try:
            import requests
            response = requests.get("http://localhost:9222/json", timeout=2)
            if response.status_code == 200:
                print("✅ Chrome ya está en modo debug")
                return True
        except:
            pass
        
        print("❌ Chrome no está en modo debug")
        print("\nPor favor:")
        print("1. Ejecuta: python setup_chrome_debug.py")
        print("2. Inicia sesión como ADMINISTRADOR en TEAMMATES")
        print("3. Vuelve a ejecutar este script")
        
        return False
    
    def run_test_case(self, test_info):
        """Ejecuta un caso de prueba individual"""
        print(f"\n{'='*60}")
        print(f"Ejecutando: {test_info['id']} - {test_info['name']}")
        print(f"{'='*60}")
        
        try:
            # Importar el módulo de prueba
            test_module = importlib.import_module(test_info['module'])
            
            # Obtener la clase de prueba
            test_class = getattr(test_module, test_info['class'])
            
            # Crear instancia y ejecutar
            test_instance = test_class()
            result = test_instance.execute_test()
            
            # Registrar resultado
            self.results.append({
                "id": test_info['id'],
                "name": test_info['name'],
                "result": "PASS" if result else "FAIL",
                "timestamp": datetime.now()
            })
            
            return result
            
        except Exception as e:
            print(f"❌ Error ejecutando {test_info['id']}: {str(e)}")
            self.results.append({
                "id": test_info['id'],
                "name": test_info['name'],
                "result": "ERROR",
                "error": str(e),
                "timestamp": datetime.now()
            })
            return False
    
    def run_all_tests(self, test_ids=None):
        """Ejecuta todos los tests o solo los especificados"""
        if not self.setup_chrome_debug():
            return False
        
        print("\n" + "="*60)
        print("INICIANDO SUITE DE PRUEBAS - MÓDULO ADMINISTRADOR")
        print("="*60)
        
        self.start_time = datetime.now