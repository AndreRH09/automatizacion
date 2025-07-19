"""
Caso de Prueba: CPF-ADM-009 - Eliminar notificación existente del sistema
Requisito: RF-ADM-32
Descripción:
Verificar que el sistema maneja correctamente los estados de una notificación durante el proceso de eliminación,
incluyendo la confirmación requerida y la transición desde estado activo hasta eliminado permanentemente.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
import time

class TestEliminarNotificacion:
    def __init__(self, use_debug=True):
        self.test_id = "CPF-ADM-009"
        self.test_name = "Eliminar notificación existente del sistema"
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

    def navigate_to_notifications(self):
        try:
            link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Notifications")))
            link.click()
            time.sleep(2)
            return True
        except:
            return False

    def find_notification_row_by_title(self, title):
        rows = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        for row in rows:
            try:
                cell_text = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip()
                if title.lower() in cell_text.lower():
                    return row
            except:
                continue
        return None

    def execute_test(self):
        print(f"\n{'='*60}")
        print(f"INICIANDO TEST: {self.test_id} - {self.test_name}")
        print(f"{'='*60}\n")

        try:
            if not self.verify_admin_session():
                print("❌ No se detectó sesión de administrador. Abortando test.")
                return False

            self.driver.get(f"{self.base_url}/web/admin/home")
            time.sleep(2)
            self.log_step(1, "Sesión como administrador", "✅", "Sesión activa verificada")

            self.log_step(2, "Navegando a Notifications")
            if self.navigate_to_notifications():
                self.log_step(2, "Navegación a Notifications", "✅")
                self.take_screenshot("notifications_page")
            else:
                self.log_step(2, "Navegación a Notifications", "❌")
                return False

            self.log_step(3, "Buscando notificación a eliminar")
            title_to_delete = "Mantenimiento Programado del Sistema 001 - General Modificado"
            row = self.find_notification_row_by_title(title_to_delete)

            if not row:
                self.log_step(3, "No se encontró la notificación", "❌", f"Título: {title_to_delete}")
                return False

            delete_button = row.find_element(By.CSS_SELECTOR, "button.btn-danger")
            delete_button.click()
            time.sleep(1)

            self.log_step(4, "Verificando modal de confirmación")
            modal = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-content")))
            if "Do you want to delete this notification" in modal.text:
                self.log_step(4, "Modal de confirmación mostrado", "✅")
                self.take_screenshot("delete_modal")
            else:
                self.log_step(4, "Modal de confirmación incorrecto o ausente", "❌")
                return False

            self.log_step(5, "Confirmando eliminación de notificación")
            self.driver.find_element(By.CSS_SELECTOR, ".modal-btn-ok").click()
            time.sleep(2)
            self.take_screenshot("after_delete")

            self.log_step(6, "Verificando que la notificación fue eliminada")
            row_after = self.find_notification_row_by_title(title_to_delete)
            if not row_after:
                self.log_step(6, "Notificación eliminada correctamente", "✅")
            else:
                self.log_step(6, "La notificación aún existe tras la eliminación", "❌")
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
    🧪 TEST CPF-ADM-009: Eliminar notificación existente del sistema

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

    test = TestEliminarNotificacion(use_debug=True)
    success = test.execute_test()
    test.generate_report()

    if success:
        print("\n✅ TEST COMPLETADO EXITOSAMENTE")
    else:
        print("\n❌ TEST FALLIDO")

if __name__ == "__main__":
    main()