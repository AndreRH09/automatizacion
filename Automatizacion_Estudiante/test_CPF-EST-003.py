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

    def test_TCN_BVA_EST_003_distribucion_incorrecta(self):
        driver = self.driver
        resultado_final = False

        try:
            driver.get(self.base_url + "/web/front/home")

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login') and @ngbdropdowntoggle]"))
            ).click()

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "student-login-btn"))
            ).click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            ).send_keys("atacoh@unsa.edu.pe")
            driver.find_element(By.ID, "identifierNext").click()

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
                    password_field = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(selector)
                    )
                    break
                except TimeoutException:
                    continue
            if not password_field:
                raise Exception("No se encontró campo de contraseña.")

            password_field.send_keys("Zodiaco24")

            next_selectors = [
                (By.ID, "passwordNext"),
                (By.XPATH, "//div[@id='passwordNext']"),
                (By.XPATH, "//button[@type='submit']")
            ]
            password_next = None
            for selector in next_selectors:
                try:
                    password_next = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(selector)
                    )
                    password_next.click()
                    break
                except TimeoutException:
                    continue
            if not password_next:
                raise Exception("No se encontró botón 'Siguiente' para contraseña.")

            WebDriverWait(driver, 15).until(EC.url_contains("/web/student/home"))

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "edit-submit-btn-2"))
            ).click()

            inputs = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//input[@type='number']"))
            )
            self.assertEqual(len(inputs), 4, "Debe haber 4 inputs de evaluación")

            for i, inp in enumerate(inputs):
                inp.clear()
                inp.send_keys("1" if i == 3 else "100")

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//span[contains(text(),'Submit Response for Question 1')]/parent::button"
                ))
            ).click()

            try:
                warning = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        "//span[contains(text(), 'Some response submissions failed') or " +
                        "contains(text(),'Invalid responses provided') or contains(text(),'question constraints')]"
                    ))
                )
                print("✓ Mensaje detectado:", warning.text)
                print("=== RESULTADO: TEST PASÓ ===")
                resultado_final = True
            except TimeoutException:
                print("✗ No se detectó advertencia de error")
                print("=== RESULTADO: TEST FALLÓ ===")

            self.assertTrue(resultado_final, "El sistema debe advertir sobre distribución no uniforme")

        except Exception as e:
            driver.save_screenshot("error_TCN_BVA_EST_003.png")
            raise

    def tearDown(self):
        self.driver.save_screenshot("final_state_TCN_BVA_EST_003.png")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=0)
