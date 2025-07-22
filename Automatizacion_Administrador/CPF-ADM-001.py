# CPF-ADM-001.py – Agregar múltiples instructores
import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv

class TestADM001:
    def setup_method(self, method):
        # Cargar credenciales desde .env
        load_dotenv(dotenv_path='cred.env')
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")

        # Iniciar navegador
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)

    def teardown_method(self, method):
        self.driver.quit()

    def test_adm001(self):
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/front/home")

        # Intentar abrir menú (vista móvil)
        try:
            toggler = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".navbar-toggler-icon"))
            )
            toggler.click()
        except:
            pass

        # Login → Instructor
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-item:nth-child(1) > .dropdown-toggle"))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, "instructor-login-btn"))).click()

        # Google login
        email_input = self.wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
        email_input.send_keys(self.email)
        email_input.send_keys(Keys.ENTER)

        password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)

        # Esperar redirección al Home de Instructor
        self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Home")))

        # Usar selector más específico para el dropdown correcto (último de la navbar)
        user_dropdowns = self.driver.find_elements(By.CSS_SELECTOR, ".dropdown-toggle")
        if user_dropdowns:
            user_dropdowns[-1].click()  # El último suele ser el de usuario
        else:
            raise Exception("No se encontró el menú de usuario.")

        # Ir a página de administración
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "To admin pages"))).click()

        # Esperar campo para ingresar instructores
        self.wait.until(EC.presence_of_element_located((By.ID, "instructor-details-single-line")))

        # Ingresar instructores válidos e inválidos
        data = (
            "Juan Pérez | juan.perez@unsa.edu.pe | UNSA\n"
            "María Rojas | maria.rojas@unmsm.edu.pe | UNMSM\n"
            "María Rojas | maria.rojas@unmsm.edu.pe |\n"
            "juan.perez@unsa.edu.pe | UNSA"
        )
        self.driver.find_element(By.ID, "instructor-details-single-line").send_keys(data)

        # Click en botón para agregar
        self.driver.find_element(By.ID, "add-instructor-single-line").click()

        # Acción extra: mover mouse para evitar congelamiento visual
        actions = ActionChains(self.driver)
        element = self.driver.find_element(By.ID, "add-instructor-single-line")
        actions.move_to_element(element).perform()
