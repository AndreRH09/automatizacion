"""
Caso de Prueba: CPF-ADM-016 - Búsqueda y monitoreo de solicitudes de cuenta por institución
Requisito: RF-ADM-38
Descripción:
Verificar la funcionalidad de búsqueda administrativa que permite filtrar y monitorear solicitudes de cuenta agrupadas por institución,
mostrando estados, fechas de registro y permitiendo acciones de aprobación/rechazo individuales o masivas.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

class TestBusquedaPorInstitucion:
    def __init__(self, use_debug=True):
        self.test_id = "CPF-ADM-016"
        self.test_name = "Búsqueda y monitoreo de solicitudes de cuenta por institución"
        self.base_url = "https://teammates-hormiga-1.uc.r.appspot.com"

        if use_debug:
            print("🔧 Conectando a Chrome en modo debug...")
            options = webdriver.ChromeOptions()
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Chrome()

        self.wait = WebDriverWait(self.driver, 10)
        self.results = []

    def log_step(self, step_num, description, status="⏳", details=""):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if status == "⏳":
            print(f"[{timestamp}] Paso {step_num}: {description}...")
        else:
            log_entry = f"[{timestamp}] Paso {step_num}: {description} - {status}"
            if details:
                log_entry += f" - {details}"
            print(log_entry)
            self.results.append(log_entry)

    def take_screenshot(self, name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{self.test_id}_{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"📸 Captura guardada: {filename}")

    def verify_admin_session(self):
        current_url = self.driver.current_url
        if "/admin/" not in current_url:
            self.driver.get(f"{self.base_url}/web/admin/home")
            time.sleep(2)
        return "/admin/" in self.driver.current_url

    def navigate_to_search(self):
        try:
            link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Search")))
            link.click()
            time.sleep(2)
            return True
        except:
            return False

    def execute_test(self):
        print(f"\n{'='*60}")
        print(f"INICIANDO TEST: {self.test_id} - {self.test_name}")
        print(f"{'='*60}\n")

        try:
            if not self.verify_admin_session():
                print("❌ No se detectó sesión de administrador. Abortando test.")
                return False

            self.driver.get(f"{self.base_url}/web/admin/home")
            self.log_step(1, "Sesión como administrador", "✅", "Sesión activa verificada")

            self.log_step(2, "Navegando a página 'Admin Search'")
            if self.navigate_to_search():
                self.log_step(2, "Navegación a Admin Search", "✅")
                self.take_screenshot("search_page")
            else:
                self.log_step(2, "Navegación a Admin Search", "❌")
                return False

            self.log_step(3, "Ingresando término de búsqueda 'UNSA'")
            search_input = self.wait.until(EC.presence_of_element_located((By.ID, "search-box")))
            search_input.clear()
            search_input.send_keys("UNSA")
            time.sleep(1)

            self.take_screenshot("search_filled")

            self.log_step(4, "Haciendo clic en botón Search")
            self.driver.find_element(By.ID, "search-button").click()
            time.sleep(3)
            self.take_screenshot("search_results")

            self.log_step(5, "Verificando resultados de búsqueda")
            results_section = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Account Requests Found')]")
            if results_section:
                self.log_step(5, "Sección 'Account Requests Found' visible", "✅")
            else:
                self.log_step(5, "Sección de resultados no encontrada", "❌")
                return False

            self.log_step(6, "Verificando columnas y estados")
            columns_expected = ["Name", "Email", "Status", "Institute, Country", "Created At", "Registered At", "Comments", "Options"]
            headers = self.driver.find_elements(By.CSS_SELECTOR, "table thead th")
            header_texts = [h.text.strip() for h in headers]

            if all(col in header_texts for col in columns_expected):
                self.log_step(6, "Todas las columnas esperadas están presentes", "✅")
            else:
                self.log_step(6, "Faltan columnas en la tabla", "❌", f"Detectadas: {header_texts}")
                return False

            self.log_step(7, "Validando que aparezca 'UNSA, Perú' resaltado")
            highlighted = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'highlight') and contains(text(), 'UNSA')]")
            if highlighted:
                self.log_step(7, "Institución resaltada correctamente", "✅")
            else:
                self.log_step(7, "No se encontró resaltado de institución", "❌")
                return False

            print(f"\n{'='*60}")
            print(f"TEST COMPLETADO")
            print(f"{'='*60}")
            return True

        except Exception as e:
            self.log_step("X", "Error inesperado", "❌", str(e))
            self.take_screenshot("error_unexpected")
            return False

    def generate_report(self):
        print("\n📋 RESUMEN DE EJECUCIÓN:")
        for result in self.results:
            print(result)

def main():
    print("""
    🧪 TEST CPF-ADM-016: Búsqueda y monitoreo de solicitudes de cuenta por institución

    Verificando conexión con Chrome...
    """)
    try:
        import requests
        response = requests.get("http://localhost:9222/json")
        if response.status_code == 200:
            print("✅ Chrome en modo debug detectado")
            data = response.json()
            if data:
                print("✅ Sesión activa en:", data[0]['url'])
        else:
            print("❌ Chrome no responde en modo debug")
            return
    except:
        print("❌ No se puede conectar a Chrome en modo debug")
        return

    print("\nIniciando test en 3 segundos...")
    time.sleep(3)

    test = TestBusquedaPorInstitucion(use_debug=True)
    success = test.execute_test()
    test.generate_report()

    if success:
        print("\n✅ TEST COMPLETADO EXITOSAMENTE")
    else:
        print("\n❌ TEST FALLIDO")

if __name__ == "__main__":
    main()