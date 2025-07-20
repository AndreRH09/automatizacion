import os
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from pathlib import Path

class TestCPFINS043:
    def setup_method(self, method):
        # Cargar .env con ruta absoluta
        env_path = Path(__file__).parent.parent / "cred.env"
        load_dotenv(dotenv_path=env_path.resolve())

        self.email = os.getenv("APP_EMAIL")
        self.password = os.getenv("APP_PASSWORD")

        # Evitar errores si las variables no existen
        assert self.email is not None, "ERROR: APP_EMAIL no se encontró en cred.env"
        assert self.password is not None, "ERROR: APP_PASSWORD no se encontró en cred.env"

        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1050, 721)
        self.vars = {}
        
        # Constantes para la prueba
        self.NEW_INSTRUCTOR_NAME = "Maria Perez"
        self.NEW_INSTRUCTOR_EMAIL = "mperez_unsa.edu.pe"  # Email inválido sin @
        self.ACCESS_LEVEL = "Manager"

    def teardown_method(self, method):
        self.driver.quit()

    def test_validar_email_instructor(self):
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/front/home")
        
        # Ir a login como instructor
        self.driver.find_element(By.CSS_SELECTOR, ".nav-item:nth-child(1) > .dropdown-toggle").click()
        self.driver.find_element(By.ID, "instructor-login-btn").click()
        
        # Ingresar correo
        email_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.send_keys(self.email)
        email_input.send_keys(Keys.ENTER)
        
        # Ingresar contraseña
        password_input = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.NAME, "Passwd"))
        )
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        
        # Esperar a que redireccione al home
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Home"))
        )
        
        # Navegar a la página de cursos
        courses_link = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Courses"))
        )
        courses_link.click()
        
        # Navegar a la página de edición del curso CS2025-S2
        edit_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[id='CS2025-S2'] .btn-edit"))
        )
        edit_button.click()
        
        # Click en "Add New Instructor"
        add_instructor_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, "btn-add-instructor"))
        )
        add_instructor_button.click()
        
        # Llenar datos del nuevo instructor con email inválido
        name_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "name-instructor-2"))
        )
        name_field.send_keys(self.NEW_INSTRUCTOR_NAME)
        
        email_field = self.driver.find_element(By.ID, "email-instructor-2")
        email_field.send_keys(self.NEW_INSTRUCTOR_EMAIL)
        
        # Seleccionar permisos de Co-owner
        coowner_checkbox = self.driver.find_element(By.ID, "INSTRUCTOR_PERMISSION_ROLE_COOWNER11")
        coowner_checkbox.click()
        
        # Hacer clic en botón "Add Instructor"
        add_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Add Instructor')]"))
        )
        add_btn.click()
        
        # Verificar notificación de error
        error_notification = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "toast-body"))
        )
        
        # Validar que se muestra un mensaje de error relacionado con el email inválido
        error_text = error_notification.text
        assert "error" in error_text.lower() or "invalid" in error_text.lower() or "email" in error_text.lower()
        
        print("✓ Test CPF-INS-043")
