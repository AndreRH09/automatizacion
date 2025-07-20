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

    def test_CPF_EST_004_distribucion_incorrecta_99(self):
        print("=== INICIANDO TEST CPF-EST-004 ===")
        resultado = False

        try:
            self.driver.get(self.base_url + "/web/front/home")

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login') and @ngbdropdowntoggle]"))
            ).click()

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "student-login-btn"))
            ).click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            ).send_keys("atacoh@unsa.edu.pe")

            self.driver.find_element(By.ID, "identifierNext").click()

            password_field = None
            password_selectors = [
                (By.NAME, "Passwd"),
                (By.NAME, "password"),
                (By.ID, "password"),
                (By.XPATH, "//input[@type='password']"),
                (By.CSS_SELECTOR, "input[type='password']"),
                (By.XPATH, "//input[@name='Passwd']")
            ]

            for selector in password_selectors:
                try:
                    password_field = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable(selector)
                    )
                    break
                except TimeoutException:
                    continue

            if not password_field:
                raise Exception("No se pudo encontrar el campo de contraseña")

            password_field.clear()
            password_field.send_keys("Zodiaco24")

            next_selectors = [
                (By.ID, "passwordNext"),
                (By.XPATH, "//button[@type='submit']"),
                (By.XPATH, "//div[@id='passwordNext']"),
                (By.CSS_SELECTOR, "button[type='submit']")
            ]

            password_next = None
            for selector in next_selectors:
                try:
                    password_next = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable(selector)
                    )
                    password_next.click()
                    break
                except TimeoutException:
                    continue

            if not password_next:
                raise Exception("No se pudo encontrar el botón 'Siguiente' para la contraseña")

            WebDriverWait(self.driver, 15).until(
                EC.url_contains("/web/student/home")
            )

            time.sleep(2)

            edit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "edit-submit-btn-2"))
            )
            edit_button.click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='number']"))
            )

            inputs = self.driver.find_elements(By.XPATH, "//input[@type='number']")
            self.assertEqual(len(inputs), 4, "Se esperaban 4 inputs de evaluación")

            for i, input_elem in enumerate(inputs):
                input_elem.clear()
                input_elem.send_keys("99" if i == 0 else "100")

            submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//span[contains(text(),'Submit Response for Question 1')]/ancestor::button"
                ))
            )
            submit_btn.click()
            time.sleep(2)

            try:
                error_msg = WebDriverWait(self.driver, 4).until(
                    EC.presence_of_element_located((By.XPATH,
                        "//span[contains(.,'Some response submissions failed')]"
                    ))
                )
                print("✓ Mensaje detectado:", error_msg.text)
                resultado = True
            except TimeoutException:
                print("✗ No se detectó mensaje de error por distribución incorrecta")
                resultado = False

            if resultado:
                print("=== RESULTADO: TEST PASÓ ===")
            else:
                print("=== RESULTADO: TEST FALLÓ ===")

            self.assertTrue(resultado, "El sistema debe advertir sobre distribución no uniforme")

        except Exception as e:
            print(f"✗ Error durante la ejecución del test: {e}")
            self.driver.save_screenshot("error_CPF_EST_004.png")
            raise

    def tearDown(self):
        self.driver.save_screenshot("final_state_CPF_EST_004.png")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=0)
