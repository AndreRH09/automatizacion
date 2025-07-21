import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

class TeammatesFeedbackValidationTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.base_url = "https://teammates-hormiga-1.uc.r.appspot.com"

    def test_TCN_BVA_EST_002_distribucion_incorrecta(self):
        try:
            print("=== INICIANDO TEST TCN-BVA-EST-002 ===")

            self.driver.get(self.base_url + "/web/front/home")
            login_dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login') and @ngbdropdowntoggle]"))
            )
            login_dropdown.click()
            student_login_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "student-login-btn"))
            )
            student_login_btn.click()

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys("atacoh@unsa.edu.pe")
            self.driver.find_element(By.ID, "identifierNext").click()

            password_field = None
            password_selectors = [
                (By.NAME, "Passwd"), (By.NAME, "password"), (By.ID, "password"),
                (By.XPATH, "//input[@type='password']"), (By.CSS_SELECTOR, "input[type='password']"),
                (By.XPATH, "//input[@name='Passwd']")
            ]
            for sel in password_selectors:
                try:
                    password_field = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(sel))
                    break
                except TimeoutException:
                    continue
            if password_field is None:
                raise Exception("No se encontró el campo de contraseña")
            password_field.send_keys("Zodiaco24")

            next_selectors = [
                (By.ID, "passwordNext"),
                (By.XPATH, "//div[@id='passwordNext']"),
                (By.XPATH, "//button[@type='submit']"),
                (By.CSS_SELECTOR, "button[type='submit']")
            ]
            for sel in next_selectors:
                try:
                    WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(sel)).click()
                    break
                except TimeoutException:
                    continue

            WebDriverWait(self.driver, 15).until(EC.url_contains("/web/student/home"))
            time.sleep(2)

            edit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "edit-submit-btn-2"))
            )
            edit_button.click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='number']"))
            )

            evaluation_inputs = self.driver.find_elements(By.XPATH, "//input[@type='number']")
            self.assertEqual(len(evaluation_inputs), 4, "Se esperaban 4 inputs de evaluación")

            for i, input_elem in enumerate(evaluation_inputs):
                input_elem.clear()
                input_elem.send_keys("0" if i == 0 else "100")

            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Submit Response for Question 1']/parent::button"))
            )
            submit_button.click()

            try:
                error_msg = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        "//span[contains(text(),'Some response submissions failed') or " +
                        "contains(text(),'Invalid responses provided') or " +
                        "contains(text(),'question constraints')]"
                    ))
                )
                print("✓ Mensaje detectado:", error_msg.text)
                resultado_validacion = True
            except TimeoutException:
                print("✗ No se detectó mensaje de error por distribución incorrecta")
                resultado_validacion = False

            if resultado_validacion:
                print("TEST PASÓ: El sistema informó correctamente sobre la distribución no uniforme.")
            else:
                print("TEST FALLÓ: El sistema no detectó la distribución incorrecta.")

            self.assertTrue(resultado_validacion, "El sistema debe advertir sobre distribución no uniforme")

        except AssertionError as ae:
            print("TEST FALLÓ (Assertion):", ae)
            raise
        except Exception as e:
            print("ERROR EN TEST:", e)
            self.driver.save_screenshot("error_TCN_BVA_EST_002.png")
            raise

    def tearDown(self):
        self.driver.save_screenshot("final_state_TCN_BVA_EST_002.png")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)
