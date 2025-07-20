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

    def test_CPF_EST_006_distribucion_superada_101(self):
        print("=== INICIANDO TEST CPF-EST-006 ===")

        resultado = False

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

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            email_field = self.driver.find_element(By.ID, "identifierId")
            email_field.clear()
            email_field.send_keys("atacoh@unsa.edu.pe")
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
            for selector_type, selector_value in password_selectors:
                try:
                    password_field = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((selector_type, selector_value))
                    )
                    break
                except TimeoutException:
                    continue

            if password_field is None:
                raise Exception("No se pudo encontrar el campo de contraseña")

            password_field.clear()
            password_field.send_keys("Zodiaco24")

            password_next = None
            next_selectors = [
                (By.ID, "passwordNext"),
                (By.XPATH, "//button[@type='submit']"),
                (By.XPATH, "//div[@id='passwordNext']"),
                (By.CSS_SELECTOR, "button[type='submit']")
            ]
            for selector_type, selector_value in next_selectors:
                try:
                    password_next = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((selector_type, selector_value))
                    )
                    break
                except TimeoutException:
                    continue

            if password_next is None:
                raise Exception("No se pudo encontrar el botón 'Siguiente' para la contraseña")

            password_next.click()

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
            self.assertEqual(len(inputs), 4)

            for i, input_elem in enumerate(inputs):
                input_elem.clear()
                input_elem.send_keys("101" if i == 0 else "100")

            submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//span[contains(text(),'Submit Response for Question 1')]/ancestor::button"
                ))
            )
            submit_btn.click()
            time.sleep(2)

            try:
                WebDriverWait(self.driver, 4).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        "//span[contains(.,'Some response submissions failed')]"
                    ))
                )
                print("✓ Mensaje detectado: Some response submissions failed!")
                resultado = True
            except TimeoutException:
                resultado = False

            if resultado:
                print("=== RESULTADO: TEST PASÓ ===")
            else:
                print("=== RESULTADO: TEST FALLÓ ===")

            self.assertTrue(resultado, "El sistema debe rechazar la distribución [101, 100, 100, 100]")

        except Exception as e:
            self.driver.save_screenshot("error_CPF_EST_006.png")
            raise

    def tearDown(self):
        self.driver.save_screenshot("final_state_CPF_EST_006.png")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)
