# CPF-ADM-013: Verificar acceso a "Timezone Listing"
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv

class TestADM013:
    def setup_method(self, method):
        # Cargar credenciales
        load_dotenv(dotenv_path='cred.env')
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        assert self.email is not None, "EMAIL no encontrada en cred.env"
        assert self.password is not None, "PASSWORD no encontrada en cred.env"

        # Inicializar navegador
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self, method):
        self.driver.quit()

    def test_adm013(self):
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/front/home")

        # Menú móvil (opcional)
        try:
            toggler = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".navbar-toggler-icon")))
            toggler.click()
        except TimeoutException:
            pass

        # Login como instructor
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-item:nth-child(1) > .dropdown-toggle"))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, "instructor-login-btn"))).click()

        email_input = self.wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
        email_input.send_keys(self.email)
        email_input.send_keys(Keys.ENTER)

        password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)

        self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Home")))

        # Ir al menú de usuario
        user_dropdowns = self.driver.find_elements(By.CSS_SELECTOR, ".dropdown-toggle")
        if user_dropdowns:
            user_dropdowns[-1].click()
        else:
            raise Exception("No se encontró el menú de usuario.")

        # Acceder a vista de admin
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "To admin pages"))).click()

        # Abrir sección "Timezone Listing"
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-item:nth-child(6) > .dropdown-toggle"))).click()
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Timezone Listing"))).click()

        # Verificar que se cargó la tabla
        assert self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table"))), "No se cargó la tabla de zonas horarias"
