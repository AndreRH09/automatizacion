"""
Caso de Prueba: CPF-ADM-019 - Regenerar enlace de registro y feedback para instructor
Requisito: RF-ADM-041
Descripción:
Validar que el sistema permita al administrador regenerar correctamente el enlace de acceso
de instructores que han perdido su link de registro y sesiones. El sistema debe enviar el nuevo enlace vía correo tras la confirmación.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

class TestRegenerarEnlaceInstructor:
    def __init__(self, use_debug=True):
        self.test_id = "CPF-ADM-019"
        self.test_name = "Regenerar enlace de registro y feedback para instructor"
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

            # Paso 1: Acceder a sección Admin Search
            self.driver.get(f"{self.base_url}/web/admin/search")
            self.log_step(1, "Accediendo a sección Admin Search", "✅")
            self.take_screenshot("admin_search")

            # Paso 2: Buscar al instructor por email
            email_input = self.wait.until(EC.presence_of_element_located((By.ID, "search-box")))
            email_input.clear()
            email_input.send_keys("fgonzales@gmail.com")
            self.driver.find_element(By.ID, "search-button").click()
            self.log_step(2, "Buscando instructor por email", "✅", "Email ingresado correctamente")
            self.take_screenshot("search_results")

            # Paso 3: Clic en botón “Regenerate key”
            regenerate_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "reset-instructor-id-0")))
            regenerate_btn.click()
            self.log_step(3, "Clic en botón 'Regenerate key'", "✅")
            self.take_screenshot("modal_opened")

            # Paso 4: Confirmar aparición del modal
            modal_body = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-body > .ng-star-inserted")))
            self.log_step(4, "Modal de confirmación mostrado", "✅")

            # Paso 5: Clic en “Yes”
            self.driver.find_element(By.CSS_SELECTOR, ".modal-btn-ok").click()
            self.log_step(5, "Confirmación realizada (Yes)", "✅")
            time.sleep(2)
            self.take_screenshot("confirmation_done")

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
    🧪 TEST CPF-ADM-019: Regenerar enlace de registro y feedback para instructor

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

    test = TestRegenerarEnlaceInstructor(use_debug=True)
    success = test.execute_test()
    test.generate_report()

    if success:
        print("\n✅ TEST COMPLETADO EXITOSAMENTE")
    else:
        print("\n❌ TEST FALLIDO")

if __name__ == "__main__":
    main()
