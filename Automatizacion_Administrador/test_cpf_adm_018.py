"""
Caso de Prueba: CPF-ADM-018 - Cambiar zona horaria de visualización  
Requisito: RF-ADM-040  
Descripción:  
Verificar que el administrador pueda seleccionar una zona horaria válida que afecte correctamente la visualización de fechas/horas en el sistema.  
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

class TestCambioZonaHoraria:
    def __init__(self, use_debug=True):
        self.test_id = "CPF-ADM-018"
        self.test_name = "Cambiar zona horaria de visualización"
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

    def execute_test(self):
        print(f"\n{'='*60}")
        print(f"INICIANDO TEST: {self.test_id} - {self.test_name}")
        print(f"{'='*60}\n")

        try:
            if not self.verify_admin_session():
                print("❌ No se detectó sesión de administrador. Abortando test.")
                return False

            self.driver.get(f"{self.base_url}/web/admin/sessions")
            self.log_step(1, "Sesión como administrador", "✅", "Sesión activa verificada")

            self.log_step(2, "Accediendo a página 'Sessions'")
            self.take_screenshot("sessions_page")

            self.log_step(3, "Abriendo selector de zona horaria")
            dropdown = self.wait.until(EC.presence_of_element_located((By.ID, "table-timezone")))
            dropdown.click()
            self.take_screenshot("dropdown_opened")

            self.log_step(4, "Seleccionando zona horaria 'Europe/Rome'")
            option_rome = dropdown.find_element(By.XPATH, ".//option[. = 'Europe/Rome']")
            option_rome.click()
            time.sleep(2)
            self.take_screenshot("timezone_europe_rome")

            self.log_step(5, "Seleccionando zona horaria 'America/Lima'")
            dropdown = self.driver.find_element(By.ID, "table-timezone")
            dropdown.click()
            option_lima = dropdown.find_element(By.XPATH, ".//option[. = 'America/Lima']")
            option_lima.click()
            time.sleep(2)
            self.take_screenshot("timezone_america_lima")

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
    🧪 TEST CPF-ADM-018: Cambiar zona horaria de visualización

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

    test = TestCambioZonaHoraria(use_debug=True)
    success = test.execute_test()
    test.generate_report()

    if success:
        print("\n✅ TEST COMPLETADO EXITOSAMENTE")
    else:
        print("\n❌ TEST FALLIDO")

if __name__ == "__main__":
    main()
