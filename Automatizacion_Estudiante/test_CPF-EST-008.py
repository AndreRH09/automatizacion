import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class TeammatesFeedbackValidationTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.base_url = "https://teammates-hormiga-1.uc.r.appspot.com"

    def test_RF_EST_011_formatos_no_permitidos(self):
        """
        Test Case: RF-EST-011 / TCN-PE-EST-001
        Caso de Prueba: CPF-EST-008
        Objetivo: Validar entrada con formatos no permitidos
        """
        try:
            print("\nEjecutando caso de prueba: RF-EST-011 / TCN-PE-EST-001 (CPF-EST-008)")
            print("Objetivo: Validar que se rechace, ignore o sanitice contenido malicioso")

            self._login_as_student()
            self._access_active_session()

            print("➡ Ingresando texto con formatos potencialmente maliciosos...")
            invalid_text = """<script>alert(\"hola\")</script>
<h1>Título</h1>
[Link]()
Texto con #ff0000
**sin cerrar"""

            if not self._input_invalid_text(invalid_text):
                raise Exception("No se pudo ingresar el texto inválido")

            print("➡ Validaciones de seguridad y funcionamiento...")
            no_malicious_code = self._check_no_malicious_execution()
            submission_success = self._verify_submission_works()

            print("\nRESULTADO DE LAS VALIDACIONES:")
            print("Correcto: No se ejecutó código malicioso" if no_malicious_code else "❌ Fallo: Se ejecutó código malicioso")
            print("Correcto: El envío funcionó" if submission_success else "❌ Fallo: El envío falló")

            test_passed = no_malicious_code and submission_success

            print("\n🎉 RESULTADO FINAL: TEST PASÓ" if test_passed else "\n💥 RESULTADO FINAL: TEST FALLÓ")
            self.assertTrue(test_passed, "El sistema no gestionó adecuadamente contenido malicioso")

        except Exception as e:
            print(f"ERROR durante la ejecución del test: {e}")
            self.driver.save_screenshot("error_RF_EST_011.png")
            raise

    def _login_as_student(self):
        self.driver.get(self.base_url + "/web/front/home")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login') and @ngbdropdowntoggle]"))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "student-login-btn"))).click()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys("atacoh@unsa.edu.pe")
        self.driver.find_element(By.ID, "identifierNext").click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, "Passwd"))).send_keys("Zodiaco24")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "passwordNext"))).click()
        WebDriverWait(self.driver, 15).until(EC.url_contains("/web/student/home"))
        print("✓ Login exitoso")

    def _access_active_session(self):
        time.sleep(2)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "edit-submit-btn-2"))).click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe | //div[@contenteditable]")))
        print("✓ Sesión activa accedida")

    def _input_invalid_text(self, text):
        try:
            iframe = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//iframe")))
            self.driver.switch_to.frame(iframe)
            editor = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//body[@contenteditable='true']")))
            editor.clear()
            editor.send_keys(text)
            self.driver.switch_to.default_content()
            print("✓ Texto inválido ingresado")
            return True
        except:
            self.driver.switch_to.default_content()
            print("✗ Error al ingresar texto")
            return False

    def _check_no_malicious_execution(self):
        time.sleep(2)
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            print(f"✗ Código malicioso ejecutado: {alert_text}")
            alert.accept()
            return False
        except:
            return True

    def _verify_submission_works(self):
        try:
            btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "btn-submit-qn-2")))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", btn)
            notif = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(., 'Response to question 2 submitted successfully!')]"))
            )
            return notif.is_displayed()
        except:
            return False

    def tearDown(self):
        self.driver.save_screenshot("final_state_RF_EST_011.png")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)
