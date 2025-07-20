import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class TeammatesFeedbackResponseRegistrationTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.base_url = "https://teammates-hormiga-1.uc.r.appspot.com"

    def test_RF_EST_006_registro_entrega_respuestas(self):
        """
        Test Case: RF-EST-006 / TCN-TE-EST-002
        Objetivo: Validar que el sistema registre correctamente el momento en que el estudiante
                 empieza a redactar una respuesta.
        Datos de entrada: E1[T1]E2
        Resultado esperado: Se activa el botón "Enviar" y el texto se visualiza correctamente.
        """
        try:
            print("=== INICIANDO TEST RF-EST-006 ===")
            
            # Paso 1-3: Login y acceso a sesión
            self._login_and_access_session()
            
            # Paso 4-5: Escribir en campo de respuesta
            text_input = "E1[T1]E2"
            self._write_response(text_input)
            
            # Verificación del resultado esperado
            print("\n=== VERIFICACIÓN ===")
            button_activated = self._verify_submit_button_activated()
            text_displayed = self._verify_text_displayed_correctly(text_input)
            
            # Evaluación
            test_passed = button_activated and text_displayed
            
            print(f"✓ Botón activado: {button_activated}")
            print(f"✓ Texto visualizado: {text_displayed}")
            print(f"\n=== RESULTADO: {'PASÓ' if test_passed else 'FALLÓ'} ===")
            
            self.assertTrue(test_passed, "Test de validación de registro falló")

        except Exception as e:
            print(f"✗ Error: {e}")
            self.driver.save_screenshot("error_RF_EST_006.png")
            raise

    def _login_and_access_session(self):
        """Login como estudiante y acceso a sesión activa"""
        # Login
        self.driver.get(self.base_url + "/web/front/home")
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login') and @ngbdropdowntoggle]"))
        ).click()
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "student-login-btn"))
        ).click()

        # Google login
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "identifierId")))
        
        self.driver.find_element(By.ID, "identifierId").send_keys("atacoh@unsa.edu.pe")
        self.driver.find_element(By.ID, "identifierNext").click()
        
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, "Passwd"))).send_keys("Zodiaco24")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "passwordNext"))).click()
        
        WebDriverWait(self.driver, 15).until(EC.url_contains("/web/student/home"))

        # Acceso a sesión
        time.sleep(2)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "edit-submit-btn-2"))
        ).click()
        
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe")))
        print("✓ Login y acceso a sesión exitoso")

    def _write_response(self, text):
        """Escribir respuesta en el editor"""
        # Cambiar al iframe del editor
        iframe = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe")))
        self.driver.switch_to.frame(iframe)
        
        # Escribir texto
        text_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//body[@contenteditable='true']"))
        )
        text_field.clear()
        text_field.send_keys(text)
        
        self.driver.switch_to.default_content()
        print("✓ Texto ingresado exitosamente")

    def _verify_submit_button_activated(self):
        """Verificar que el botón 'Enviar' se activa"""
        try:
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "btn-submit-qn-2"))
            )
            return submit_button.is_enabled()
        except:
            return False

    def _verify_text_displayed_correctly(self, expected_text):
        """Verificar que el texto se visualiza correctamente"""
        try:
            content = self.driver.execute_script("""
                var iframes = document.querySelectorAll('iframe');
                for (var i = 0; i < iframes.length; i++) {
                    try {
                        var doc = iframes[i].contentDocument || iframes[i].contentWindow.document;
                        if (doc && doc.body && doc.body.contentEditable === 'true') {
                            return doc.body.textContent || doc.body.innerText;
                        }
                    } catch (e) { continue; }
                }
                return null;
            """)
            return content and expected_text in content
        except:
            return False

    def tearDown(self):
        self.driver.save_screenshot("final_state_RF_EST_006.png")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)