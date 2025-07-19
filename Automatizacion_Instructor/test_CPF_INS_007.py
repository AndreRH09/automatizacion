import time
import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv


class TestCPFINS007:
    def setup_method(self, method):
        chrome_options = Options()
        
        # Usa un nuevo directorio temporal de sesión
        load_dotenv("cred.env")

        self.email = os.getenv("APP_EMAIL")
        self.password = os.getenv("APP_PASSWORD")
        assert self.email is not None, "ERROR: APP_EMAIL no está definido"
        assert self.password is not None, "ERROR: APP_PASSWORD no está definido"

        self.driver = webdriver.Chrome(options=chrome_options)

    def teardown_method(self, method):
        self.driver.quit()

    def test_nombre_con_caracteres_especiales_pipe(self):
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

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Home"))
        )

        # Botón Copy de "Session with different question types"
        copy_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#sessions-table-1 > .ng-star-inserted .ng-star-inserted:nth-child(1) .d-flex > .btn:nth-child(3)"))
        )
        copy_btn.click()

        # Ingresar nombre con carácter especial "|"
        name_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "copy-session-name"))
        )
        name_input.clear()
        name_input.send_keys("Sesion|123")

        # Seleccionar checkbox "Curso Distinto"
        checkbox = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".form-check:nth-child(2) > .form-check-label"))
        )
        checkbox.click()

        # Esperar para que Angular valide el nombre
        time.sleep(1.5)
        
        confirm_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btn-confirm-copy-course"))
        )
        confirm_btn.click()
        print("✓ Test CPF-INS-007 completado")
