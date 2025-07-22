# test_cpf_adm_008.py
"""
Caso de Prueba: CPF-ADM-008 - Editar notificación existente del sistema
Versión estructurada al estilo del caso anterior CPF-ADM-007
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from datetime import datetime

class TestEditarNotificacion:
    def __init__(self, use_debug=True):
        self.test_id = "CPF-ADM-008"
        self.test_name = "Editar notificación existente del sistema"
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
            notifications_link = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Notifications"))
            )
            notifications_link.click()
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

            self.log_step(3, "Buscando notificación existente para editar")
            title_to_edit = "Mantenimiento Programado del Sistema 001 - General"
            row = self.find_notification_row_by_title(title_to_edit)

            if not row:
                self.log_step(3, "No se encontró la notificación", "❌", f"Título: {title_to_edit}")
                return False

            edit_button = row.find_element(By.CSS_SELECTOR, "button.btn-light")
            edit_button.click()
            time.sleep(1)
            self.take_screenshot("edit_modal_opened")

            self.log_step(4, "Editando campos de la notificación")

            self.driver.find_element(By.ID, "notification-title").clear()
            self.driver.find_element(By.ID, "notification-title").send_keys(
                "Mantenimiento Programado del Sistema 001 - General Modificado"
            )

            style_dropdown = Select(self.driver.find_element(By.ID, "notification-style"))
            style_dropdown.select_by_visible_text("Success (green)")

            self.driver.switch_to.frame(0)
            editor = self.driver.find_element(By.ID, "tinymce")
            self.driver.execute_script(
                "arguments[0].innerHTML = '<p><strong>Mensaje de mantenimiento modificado</strong></p>'",
                editor
            )
            self.driver.switch_to.default_content()

            start_time = Select(self.driver.find_element(By.CSS_SELECTOR, "#notification-start-time > .form-control"))
            start_time.select_by_visible_text("17:00H")

            end_time = Select(self.driver.find_element(By.CSS_SELECTOR, "#notification-end-time > .form-control"))
            end_time.select_by_visible_text("21:00H")

            self.take_screenshot("edit_filled")

            self.driver.find_element(By.ID, "btn-edit-notification").click()
            time.sleep(2)
            self.take_screenshot("edit_success")

            updated_row = self.find_notification_row_by_title(
                "Mantenimiento Programado del Sistema 001 - General Modificado"
            )
            if updated_row:
                self.log_step(5, "Notificación editada correctamente", "✅")
                self.take_screenshot("notification_edited_in_list")
            else:
                self.log_step(5, "No se encontró la notificación editada", "❌")
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
    🧪 TEST CPF-ADM-008: Editar notificaciones del sistema

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

    test = TestEditarNotificacion(use_debug=True)
    success = test.execute_test()
    test.generate_report()

    if success:
        print("\n✅ TEST COMPLETADO EXITOSAMENTE")
    else:
        print("\n❌ TEST FALLIDO")

if __name__ == "__main__":
    main()
