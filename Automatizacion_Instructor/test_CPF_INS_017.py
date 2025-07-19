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

class TestCPFINS017:
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

    def teardown_method(self, method):
        self.driver.quit()

    def test_validacion_campo_vacio_sin_seleccion_curso(self):
        """CPF-INS-017: Validación campo vacío sin selección de curso"""
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/front/home")
        
        # Login como instructor
        self.driver.find_element(By.CSS_SELECTOR, ".nav-item:nth-child(1) > .dropdown-toggle").click()
        self.driver.find_element(By.ID, "instructor-login-btn").click()
        
        # Ingresar correo
        email_input = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.send_keys(self.email)
        email_input.send_keys(Keys.ENTER)
        
        # Ingresar contraseña
        password_input = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.NAME, "Passwd"))
        )
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        
        # Esperar a que redireccione al home
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Home"))
        )
        
        # Hacer clic en botón Copy de "Session with different question types"
        copy_btn = WebDriverWait(self.driver, 25).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#sessions-table-1 > .ng-star-inserted .ng-star-inserted:nth-child(1) .d-flex > .btn:nth-child(3)"))
        )
        copy_btn.click()
        
        # Dejar campo nombre vacío
        copy_session_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "copy-session-name"))
        )
        actions = ActionChains(self.driver)
        actions.double_click(copy_session_input).perform()
        copy_session_input.clear()
                # A veces Angular necesita algo de interacción para detectar cambios
        copy_session_input.send_keys(" ")  # Ingresa un espacio
        copy_session_input.send_keys(Keys.BACKSPACE)  # Y lo elimina para forzar update
        
        # Seleccionar checkbox "Sample Course 101" (primer checkbox)
        option_checkbox_1 = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".form-check:nth-child(2) > .form-check-label"))
        )
        option_checkbox_1.click()
        
        # Seleccionar checkbox "Curso Distinto" (segundo checkbox)
        option_checkbox_2 = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".form-check:nth-child(3) > .form-check-label"))
        )
        option_checkbox_2.click()
        
        #Esperar y verificar que el botón esté deshabilitado
        confirm_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "btn-confirm-copy-course"))
        )
        # Verificar que no está habilitado
        confirm_btn = self.driver.find_element(By.ID, "btn-confirm-copy-course")
        assert confirm_btn.get_attribute("disabled") is not None, \
            "El botón de confirmar debería estar deshabilitado cuando el nombre está vacío"
        
        
        time.sleep(2)
        print("✓ Test CPF-INS-017 completado")
