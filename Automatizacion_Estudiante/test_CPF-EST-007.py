import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time


class TeammatesFeedbackValidationTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.base_url = "https://teammates-hormiga-1.uc.r.appspot.com"
        self.rich_text = """**Negrita**, *cursiva*, 😊, [Link](https://ejemplo.com), E = mc²
- Item 1
- Item 2

## Encabezado

> Cita de ejemplo

### Sublista:
1. Elemento numerado
2. Otro elemento

`Código en línea`

**Combinaciones:** *cursiva en **negrita** anidada*"""

    def test_CPF_EST_007_texto_enriquecido_question2(self):
        print("\nEjecutando caso de prueba: CPF-EST-007 / TCN-PE-EST-001")
        print("Objetivo: Validar entrada enriquecida en Question 2")

        try:
            self.driver.get(self.base_url + "/web/front/home")

            login_dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login') and @ngbdropdowntoggle]"))
            )
            login_dropdown.click()

            student_login_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "student-login-btn"))
            )
            student_login_btn.click()

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "identifierId")))
            self.driver.find_element(By.ID, "identifierId").send_keys("atacoh@unsa.edu.pe")
            self.driver.find_element(By.ID, "identifierNext").click()

            password_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "Passwd"))
            )
            password_field.send_keys("Zodiaco24")

            password_next = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "passwordNext"))
            )
            password_next.click()

            WebDriverWait(self.driver, 15).until(EC.url_contains("/web/student/home"))

            edit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "edit-submit-btn-2"))
            )
            edit_button.click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//iframe | //div[@contenteditable]"))
            )

            success = self._try_iframe_method() or self._try_javascript_method()
            if not success:
                print("No se pudo ingresar texto enriquecido en Question 2")
            self.assertTrue(success, "No se pudo ingresar texto en Question 2")

            submit_btn = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "btn-submit-qn-2"))
            )

            WebDriverWait(self.driver, 10).until(lambda d: submit_btn.is_enabled())
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            time.sleep(1)

            try:
                submit_btn.click()
            except:
                self.driver.execute_script("arguments[0].click();", submit_btn)

            # Verificación del envío exitoso
            success_verified = False
            try:
                success_notification = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(., 'Response to question 2 submitted successfully!')]"))
                )
                success_verified = success_notification.is_displayed()
            except TimeoutException:
                try:
                    alt_success = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, "//span[contains(., 'submitted successfully')] | //div[contains(@class, 'alert-success')]"))
                    )
                    success_verified = alt_success.is_displayed()
                except TimeoutException:
                    pass

            error_detected = False
            try:
                error_notification = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(.,'Error') or contains(.,'failed')]"))
                )
                error_detected = error_notification.is_displayed()
            except TimeoutException:
                pass

            if success_verified and not error_detected:
                print("TEST EXITOSO: El texto enriquecido fue ingresado y enviado correctamente en Question 2.\n")
            else:
                print("TEST FALLIDO:")
                if not success_verified:
                    print("- No se detectó mensaje de éxito tras el envío.")
                if error_detected:
                    print("- Se detectaron errores durante el envío.")
            self.assertTrue(success_verified and not error_detected,
                "Test fallido - Éxito verificado: {}, Errores detectados: {}".format(success_verified, error_detected))

        except Exception as e:
            print(f"🛑 Error crítico durante el test: {e}")
            self.driver.save_screenshot("error_CPF_EST_007.png")
            raise

    def _try_iframe_method(self):
        try:
            iframe = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//iframe[contains(@id, 'tiny')]"))
            )
            self.driver.switch_to.frame(iframe)

            body = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//body[@contenteditable='true']"))
            )
            body.clear()
            body.send_keys(self.rich_text)

            self.driver.switch_to.default_content()
            return True
        except:
            self.driver.switch_to.default_content()
            return False

    def _try_javascript_method(self):
        try:
            escaped_text = self.rich_text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")

            js_script = f"""
            var iframes = document.querySelectorAll('iframe');
            for (var i = 0; i < iframes.length; i++) {{
                try {{
                    var doc = iframes[i].contentDocument || iframes[i].contentWindow.document;
                    if (doc && doc.body && doc.body.contentEditable === 'true') {{
                        doc.body.innerHTML = '<p>{escaped_text}</p>';
                        return 'success';
                    }}
                }} catch (e) {{}}
            }}
            if (typeof tinymce !== 'undefined') {{
                var editors = tinymce.get();
                if (editors && editors.length > 0) {{
                    editors[0].setContent('{escaped_text}');
                    return 'success';
                }}
            }}
            return 'failed';
            """
            result = self.driver.execute_script(js_script)
            return result == "success"
        except:
            return False

    def tearDown(self):
        self.driver.save_screenshot("final_state_CPF_EST_007.png")
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)
