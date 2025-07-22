import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import os

class TestADM014:
    def setup_method(self, method):
        load_dotenv(dotenv_path='cred.env')
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")

        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self, method):
        self.driver.quit()

    def test_adm014(self):
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/front/home")

        # Menú responsive
        try:
            toggler = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".navbar-toggler-icon")))
            toggler.click()
        except TimeoutException:
            pass

        # Login como instructor
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-item:nth-child(1) > .dropdown-toggle"))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, "instructor-login-btn"))).click()

        # Login con Google
        email_input = self.wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
        email_input.send_keys(self.email)
        email_input.send_keys(Keys.ENTER)

        password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)

        # Esperar vista de instructor
        self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Home")))

        # Ir al menú de usuario
        dropdowns = self.driver.find_elements(By.CSS_SELECTOR, ".dropdown-toggle")
        dropdowns[-1].click()

        # Ir a admin
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "To admin pages"))).click()
        self.wait.until(EC.url_contains("/admin"))

        # Ir a "Sessions"
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sessions"))).click()

        # Abrir filtros
        self.wait.until(EC.element_to_be_clickable((By.ID, "btn-toggle-filter"))).click()

        # Fecha inicio (elige manualmente alguna)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-xl-4:nth-child(1) .fas"))).click()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ngb-dp-week:nth-child(4) .ngb-dp-day:nth-child(5) .btn-light"))).click()

        # Fecha fin
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-xl-4:nth-child(2) .fas"))).click()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ngb-dp-today .btn-light"))).click()

        # Ejecutar búsqueda
        self.wait.until(EC.element_to_be_clickable((By.ID, "btn-get-sessions"))).click()

        # Validación: verificar si se cargaron resultados
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".card .table")))
