# CPF-ADM-002 - Agregar instructor individualmente

import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv

class TestADM002():
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

    def test_adm002(self):
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

        # Login con Google
        email_input = self.wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
        email_input.send_keys(self.email)
        email_input.send_keys(Keys.ENTER)

        password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)

        # Esperar a redirección a vista de instructor
        self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Home")))

        # Abrir el menú de usuario (último dropdown de la navbar)
        user_dropdowns = self.driver.find_elements(By.CSS_SELECTOR, ".dropdown-toggle")
        if user_dropdowns:
            user_dropdowns[-1].click()  # Último: menú del usuario (admin)
        else:
            raise Exception("No se encontró el menú de usuario.")

        # Click en "To admin pages"
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "To admin pages"))).click()

        # Agregar instructor individualmente - caso válido
        self.wait.until(EC.presence_of_element_located((By.ID, "instructor-name"))).send_keys("Gersson Huichi")
        self.driver.find_element(By.ID, "instructor-email").send_keys("ghuichi@unsa.edu.pe")
        self.driver.find_element(By.ID, "instructor-institution").send_keys("UNSA")
        self.driver.find_element(By.ID, "add-instructor").click()

        # Intento de agregar instructor con email ya existente (repetido)
        self.driver.find_element(By.ID, "instructor-email").clear()
        self.driver.find_element(By.ID, "instructor-email").send_keys("ghuichi@unsa.edu.pe")
        self.driver.find_element(By.ID, "add-instructor").click()

        # Intento de agregar instructor con datos incompletos (falta email)
        self.driver.find_element(By.ID, "instructor-name").send_keys("A")
        self.driver.find_element(By.ID, "instructor-institution").clear()
        self.driver.find_element(By.ID, "instructor-institution").send_keys("Z")
        self.driver.find_element(By.ID, "instructor-email").clear()
        self.driver.find_element(By.ID, "instructor-email").send_keys("a@b")  # inválido
        self.driver.find_element(By.ID, "add-instructor").click()
