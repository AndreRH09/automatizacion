import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time

class TestCPFINS011:
    def setup_method(self, method):
        load_dotenv("cred.env")
        self.email = os.getenv("APP_EMAIL")
        self.password = os.getenv("APP_PASSWORD")
        assert self.email is not None, "ERROR: APP_EMAIL no está definido"
        assert self.password is not None, "ERROR: APP_PASSWORD no está definido"

        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1050, 721)

    def teardown_method(self, method):
        self.driver.quit()

    def test_curso_no_seleccionado(self):
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/front/home")
        # Login
        self.driver.find_element(By.CSS_SELECTOR, ".nav-item:nth-child(1) > .dropdown-toggle").click()
        self.driver.find_element(By.ID, "instructor-login-btn").click()
        email_input = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.send_keys(self.email)
        email_input.send_keys(Keys.ENTER)
        password_input = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.NAME, "Passwd"))
        )
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        # Esperar redirección
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Home"))
        )
        # Hacer clic en el botón Copy de la sesión
        copy_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#sessions-table-1 > .ng-star-inserted .ng-star-inserted:nth-child(1) .d-flex > .btn:nth-child(3)"))
        )
        copy_btn.click()
        # Esperar campo nombre, escribir "SesionTest"
        name_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "copy-session-name"))
        )
        name_input.clear()
        name_input.send_keys("SesionTest")
        # Esperar y verificar que el botón esté deshabilitado
        confirm_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "btn-confirm-copy-course"))
        )
        # Verificar que no está habilitado
        assert not confirm_btn.is_enabled(), "El botón de confirmar debería estar deshabilitado si no se selecciona un curso destino"


        print("✓ Test CPF-INS-011 completado")
