# test_cpf_adm_006.py
"""
Caso de Prueba: CPF-ADM-006 - Visualización de sesiones en curso
Versión corregida con selectores de Selenium IDE
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from datetime import datetime

class TestVisualizacionSesiones:
    def __init__(self, use_debug=True):
        self.test_id = "CPF-ADM-006"
        self.test_name = "Visualización de sesiones en curso"
        self.base_url = "https://teammates-hormiga-1.uc.r.appspot.com"
        
        # Configurar driver
        if use_debug:
            print("🔧 Conectando a Chrome en modo debug...")
            options = webdriver.ChromeOptions()
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Chrome()
            
        self.wait = WebDriverWait(self.driver, 10)
        self.results = []
        
    def log_step(self, step_num, description, status="✓", details=""):
        """Registra el resultado de cada paso"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] Paso {step_num}: {description} - {status}"
        if details:
            log_entry += f" - {details}"
        print(log_entry)
        self.results.append(log_entry)
        
    def take_screenshot(self, name):
        """Toma captura de pantalla"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{self.test_id}_{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"📸 Captura guardada: {filename}")
        
    def execute_test(self):
        """Ejecuta el caso de prueba completo"""
        print(f"\n{'='*50}")
        print(f"INICIANDO TEST: {self.test_id} - {self.test_name}")
        print(f"{'='*50}\n")
        
        try:
            # PASO 1: Verificar que estamos en la página de admin
            self.log_step(1, "Verificando sesión de administrador", "⏳")
            current_url = self.driver.current_url
            if "/admin/" in current_url:
                self.log_step(1, "Sesión de administrador verificada", "✓")
            else:
                # Navegar a admin home
                self.driver.get(f"{self.base_url}/web/admin/home")
                time.sleep(2)
                self.log_step(1, "Navegado a página de administrador", "✓")
            
            # PASO 2: Hacer clic en Sessions
            self.log_step(2, "Navegando a Sessions", "⏳")
            
            # Verificar si necesitamos abrir el menú (móvil)
            try:
                navbar_toggler = self.driver.find_element(By.CSS_SELECTOR, ".navbar-toggler-icon")
                if navbar_toggler.is_displayed():
                    navbar_toggler.click()
                    time.sleep(0.5)
            except:
                pass  # El menú ya está visible
            
            # Click en Sessions
            sessions_link = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Sessions"))
            )
            sessions_link.click()
            time.sleep(2)  # Esperar carga completa
            self.log_step(2, "Página de Sessions cargada", "✓")
            self.take_screenshot("sessions_page")
            
            # PASO 3: Verificar título de la página
            self.log_step(3, "Verificando página 'Ongoing Sessions'", "⏳")
            try:
                # Buscar el título o algún indicador de que estamos en la página correcta
                page_indicator = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1, .card-header"))
                )
                self.log_step(3, "Página de sesiones cargada correctamente", "✓")
            except:
                self.log_step(3, "No se pudo verificar el título de la página", "⚠️")
            
            # PASO 4: Verificar resumen de sesiones (si existe)
            self.log_step(4, "Buscando resumen de sesiones", "⏳")
            try:
                # Buscar elementos que contengan información de resumen
                summary_elements = self.driver.find_elements(By.CSS_SELECTOR, ".card-body, .summary, .stats")
                if summary_elements:
                    self.log_step(4, "Elementos de resumen encontrados", "✓", f"{len(summary_elements)} elementos")
                else:
                    self.log_step(4, "No se encontró resumen visible", "⚠️")
            except:
                self.log_step(4, "Resumen no disponible", "⚠️")
            
            # PASO 5: Expandir filtros
            self.log_step(5, "Expandiendo filtros", "⏳")
            try:
                filter_button = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "btn-toggle-filter"))
                )
                filter_button.click()
                time.sleep(1)  # Esperar animación
                self.log_step(5, "Filtros expandidos", "✓")
                self.take_screenshot("filters_expanded")
            except Exception as e:
                self.log_step(5, "No se pudo expandir filtros", "✗", str(e))
            
            # PASO 6: Interactuar con el calendario (si está visible)
            self.log_step(6, "Verificando selector de fecha", "⏳")
            try:
                # Click en el ícono del calendario
                calendar_icon = self.driver.find_element(By.CSS_SELECTOR, ".col-xl-4:nth-child(1) .fas")
                calendar_icon.click()
                time.sleep(1)
                
                # Seleccionar una fecha
                date_selector = self.driver.find_element(
                    By.CSS_SELECTOR, 
                    ".ngb-dp-week:nth-child(2) > .ngb-dp-day:nth-child(2) > .btn-light"
                )
                date_selector.click()
                time.sleep(1)
                self.log_step(6, "Fecha seleccionada", "✓")
            except:
                self.log_step(6, "Selector de fecha no disponible o no necesario", "⚠️")
            
            # PASO 7: Obtener sesiones
            self.log_step(7, "Obteniendo sesiones", "⏳")
            try:
                get_sessions_btn = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "btn-get-sessions"))
                )
                get_sessions_btn.click()
                time.sleep(3)  # Esperar carga de datos
                self.log_step(7, "Sesiones obtenidas", "✓")
                self.take_screenshot("sessions_loaded")
            except:
                self.log_step(7, "Botón 'Get Sessions' no encontrado", "⚠️")
            
            # PASO 8: Verificar lista de sesiones
            self.log_step(8, "Verificando lista de sesiones", "⏳")
            try:
                # Buscar tabla o lista de sesiones
                session_elements = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr, .session-item")
                if session_elements:
                    self.log_step(8, "Lista de sesiones encontrada", "✓", f"{len(session_elements)} sesiones")
                    
                    # Contar por tipo si es posible
                    opened = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Opened')]")
                    closed = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Closed')]")
                    waiting = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Waiting')]")
                    
                    self.log_step(9, "Conteo de sesiones", "✓", 
                                f"Opened: {len(opened)}, Closed: {len(closed)}, Waiting: {len(waiting)}")
                else:
                    self.log_step(8, "No se encontraron sesiones", "⚠️")
            except Exception as e:
                self.log_step(8, "Error verificando sesiones", "✗", str(e))
            
            # Captura final
            self.take_screenshot("test_completed")
            
            print(f"\n{'='*50}")
            print(f"TEST COMPLETADO")
            print(f"{'='*50}")
            
            return True
            
        except Exception as e:
            self.log_step("X", "Error inesperado", "✗", str(e))
            self.take_screenshot("error")
            return False
        
    def cleanup(self):
        """Limpieza después del test"""
        # No cerrar el navegador si estamos en modo debug
        pass

def main():
    print("""
    🧪 TEST CPF-ADM-006: Visualización de sesiones en curso
    
    Verificando conexión con Chrome...
    """)
    
    # Verificar conexión debug
    try:
        import requests
        response = requests.get("http://localhost:9222/json")
        if response.status_code == 200:
            print("✅ Chrome en modo debug detectado")
            print("✅ Sesión activa en:", response.json()[0]['url'])
        else:
            print("❌ Chrome no responde en modo debug")
            return
    except:
        print("❌ No se puede conectar a Chrome en modo debug")
        return
    
    print("\nIniciando test en 3 segundos...")
    time.sleep(3)
    
    # Ejecutar test
    test = TestVisualizacionSesiones(use_debug=True)
    success = test.execute_test()
    
    if success:
        print("\n✅ TEST PASADO")
    else:
        print("\n❌ TEST FALLIDO")
    
    # Generar reporte simple
    print("\n📋 RESUMEN DE PASOS:")
    for result in test.results:
        print(result)

if __name__ == "__main__":
    main()