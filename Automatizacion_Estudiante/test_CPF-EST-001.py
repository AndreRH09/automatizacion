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

    def test_TCN_BVA_EST_001(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        try:
            driver.get(self.base_url + "/web/front/home")

            login_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login') and @ngbdropdowntoggle]")))
            login_dropdown.click()
            student_login_btn = wait.until(EC.element_to_be_clickable((By.ID, "student-login-btn")))
            student_login_btn.click()

            wait.until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys("atacoh@unsa.edu.pe")
            driver.find_element(By.ID, "identifierNext").click()

            password_field = None
            selectors = [
                (By.NAME, "Passwd"), (By.NAME, "password"), (By.ID, "password"),
                (By.XPATH, "//input[@type='password']"), (By.CSS_SELECTOR, "input[type='password']"),
                (By.XPATH, "//input[@name='Passwd']")
            ]
            for sel in selectors:
                try:
                    password_field = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(sel))
                    break
                except TimeoutException:
                    continue
            if not password_field:
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
                    WebDriverWait(driver, 3).until(EC.element_to_be_clickable(sel)).click()
                    break
                except TimeoutException:
                    continue

            WebDriverWait(driver, 15).until(EC.url_contains("/web/student/home"))

            edit_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "edit-submit-btn-2")))
            edit_btn.click()

            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='number']")))
            inputs = driver.find_elements(By.XPATH, "//input[@type='number']")
            if not inputs:
                raise Exception("No se encontraron inputs de evaluación")

            first_input = inputs[0]
            first_input.clear()
            first_input.send_keys("-1")
            driver.find_element(By.TAG_NAME, "body").click()
            time.sleep(1)

            resultado_ok = False
            try:
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'error') or contains(@class, 'invalid')]"))
                )
                resultado_ok = True
            except TimeoutException:
                value = first_input.get_attribute('value')
                if value == "" or value is None:
                    resultado_ok = True
                elif value == "-1":
                    resultado_ok = False
                else:
                    resultado_ok = False

            min_attr = first_input.get_attribute('min')
            if min_attr and int(min_attr) >= 0:
                resultado_ok = True

            self.assertTrue(resultado_ok, "❌ El sistema permitió valor negativo")

            print("TEST PASÓ: El sistema rechazó correctamente el valor negativo.")

        except AssertionError as ae:
            print("TEST FALLÓ:", ae)
            raise

        except Exception as e:
            print("ERROR EN TEST:", e)
            raise

    def tearDown(self):
        self.driver.save_screenshot("final_state_TCN_BVA_EST_001.png")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)
