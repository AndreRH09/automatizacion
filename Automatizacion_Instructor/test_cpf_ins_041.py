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

class TestCPFINS041:
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
        self.EXPECTED_COURSE_ID = "CS2025-S2"
        self.EXPECTED_ENROLL_HREF = f"/web/instructor/courses/enroll?courseid={self.EXPECTED_COURSE_ID}&user=aanazcoh@unsa.edu.pe"
        self.EXPECTED_EDIT_HREF = f"/web/instructor/courses/edit?courseid={self.EXPECTED_COURSE_ID}&user=aanazcoh@unsa.edu.pe"

    def teardown_method(self, method):
        self.driver.quit()

    def test_verificar_elementos_curso(self):
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
        
        # Navegar a la página de edición del curso
        edit_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f"[id='{self.EXPECTED_COURSE_ID}'] .btn-edit"))
        )
        edit_button.click()
        
        # Verificar elementos en la página de edición
        
        # 1. Verificando el elemento con el ID del curso
        td_course = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "course-id-0"))
        )
        assert td_course.text == self.EXPECTED_COURSE_ID
        
        # 2. Verificando botón 'Enroll'
        btn_enroll = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "btn-enroll-0"))
        )
        assert btn_enroll.get_attribute("href").endswith(self.EXPECTED_ENROLL_HREF)
        
        # 3. Verificando botón 'Edit'
        btn_edit = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Edit"))
        )
        assert btn_edit.get_attribute("href").endswith(self.EXPECTED_EDIT_HREF)
        
        # 4. Verificando botón 'Add New Instructor'
        btn_add_instructor = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "btn-add-instructor"))
        )
        assert btn_add_instructor is not None
        
        print("✓ Test CPF-INS-041")
