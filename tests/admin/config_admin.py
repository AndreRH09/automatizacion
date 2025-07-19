"""
Configuración base para todas las pruebas del módulo Administrador
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime

class AdminTestBase:
    """Clase base para todos los tests de administrador"""
    
    def __init__(self, test_id, test_name, use_debug=True):
        self.test_id = test_id
        self.test_name = test_name
        self.base_url = "https://teammates-hormiga-1.uc.r.appspot.com"
        self.results = []
        self.screenshots = []
        
        # Configurar driver
        if use_debug:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            self.driver = webdriver.Chrome(options=options)
        else:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service)
        
        self.wait = WebDriverWait(self.driver, 10)
        self.short_wait = WebDriverWait(self.driver, 3)
        
        # Crear carpetas para resultados
        self.create_test_folders()
    
    def create_test_folders(self):
        """Crea las carpetas necesarias para guardar resultados"""
        self.test_folder = f"results/{self.test_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.test_folder, exist_ok=True)
        os.makedirs(f"{self.test_folder}/screenshots", exist_ok=True)
        os.makedirs(f"{self.test_folder}/reports", exist_ok=True)
    
    def log_step(self, step_num, description, status="⏳", details=""):
        """Registra cada paso del test"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if status == "⏳":
            # Solo imprimir en progreso
            print(f"[{timestamp}] Paso {step_num}: {description}...")
        else:
            # Imprimir resultado final
            log_entry = {
                "step": step_num,
                "time": timestamp,
                "description": description,
                "status": status,
                "details": details
            }
            self.results.append(log_entry)
            
            status_icon = "✓" if status == "PASS" else "✗" if status == "FAIL" else "⚠️"
            print(f"[{timestamp}] Paso {step_num}: {description} - {status_icon} {status}")
            if details:
                print(f"           Detalles: {details}")
    
    def take_screenshot(self, name):
        """Captura pantalla y la guarda en la carpeta del test"""
        filename = f"{name}_{datetime.now().strftime('%H%M%S')}.png"
        filepath = f"{self.test_folder}/screenshots/{filename}"
        self.driver.save_screenshot(filepath)
        self.screenshots.append(filename)
        print(f"📸 Captura: {filename}")
        return filepath
    
    def verify_admin_session(self):
        """Verifica que estamos logueados como administrador"""
        try:
            # Verificar URL o elemento que indique sesión de admin
            admin_menu = self.short_wait.until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/admin')]"))
            )
            return True
        except:
            return False
    
    def wait_for_element(self, by, value, timeout=10):
        """Espera un elemento con manejo de errores mejorado"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except:
            self.take_screenshot(f"element_not_found_{value}")
            raise
    
    def click_element(self, by, value, timeout=10):
        """Hace clic en un elemento con reintentos"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            return True
        except:
            self.take_screenshot(f"click_failed_{value}")
            return False
    
    def generate_html_report(self):
        """Genera un reporte HTML con los resultados"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Reporte de Test: {self.test_id}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .info {{ background: #f0f0f0; padding: 10px; margin: 10px 0; }}
                .pass {{ color: green; font-weight: bold; }}
                .fail {{ color: red; font-weight: bold; }}
                .warning {{ color: orange; font-weight: bold; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .screenshot {{ max-width: 200px; margin: 5px; border: 1px solid #ddd; }}
            </style>
        </head>
        <body>
            <h1>Reporte de Test: {self.test_id}</h1>
            <div class="info">
                <p><strong>Nombre:</strong> {self.test_name}</p>
                <p><strong>Fecha:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>URL Base:</strong> {self.base_url}</p>
            </div>
            
            <h2>Resultados de Pasos</h2>
            <table>
                <tr>
                    <th>Paso</th>
                    <th>Hora</th>
                    <th>Descripción</th>
                    <th>Estado</th>
                    <th>Detalles</th>
                </tr>
        """
        
        for result in self.results:
            status_class = "pass" if result["status"] == "PASS" else "fail" if result["status"] == "FAIL" else "warning"
            html_content += f"""
                <tr>
                    <td>{result["step"]}</td>
                    <td>{result["time"]}</td>
                    <td>{result["description"]}</td>
                    <td class="{status_class}">{result["status"]}</td>
                    <td>{result["details"]}</td>
                </tr>
            """
        
        html_content += """
            </table>
            
            <h2>Capturas de Pantalla</h2>
            <div>
        """
        
        for screenshot in self.screenshots:
            html_content += f'<img src="screenshots/{screenshot}" class="screenshot" alt="{screenshot}"/>'
        
        html_content += """
            </div>
        </body>
        </html>
        """
        
        report_path = f"{self.test_folder}/reports/report.html"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n📊 Reporte HTML generado: {report_path}")
        return report_path

# Utilidades comunes para tests de admin
class AdminTestUtils:
    """Utilidades reutilizables para tests de administrador"""
    
    @staticmethod
    def navigate_to_sessions(driver, wait):
        """Navega a la sección de sesiones"""
        sessions_link = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sessions"))
        )
        sessions_link.click()
        
    @staticmethod
    def navigate_to_accounts(driver, wait):
        """Navega a la sección de cuentas"""
        accounts_link = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Accounts"))
        )
        accounts_link.click()
    
    @staticmethod
    def search_in_table(driver, search_term):
        """Busca en una tabla usando el campo de búsqueda"""
        search_box = driver.find_element(By.CSS_SELECTOR, "input[type='search']")
        search_box.clear()
        search_box.send_keys(search_term)
        
    @staticmethod
    def count_table_rows(driver):
        """Cuenta las filas en una tabla (excluyendo header)"""
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        return len(rows)