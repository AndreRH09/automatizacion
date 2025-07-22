# CPF-ADM-012 – Ver uso de estadísticas por fecha
import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

class TestADM012:
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

    def test_adm012(self):
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/front/home")

        # Menú responsive
        try:
            toggler = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".navbar-toggler-icon")))
            toggler.click()
        except:
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

        # Ir a páginas de administración
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "To admin pages"))).click()
        self.wait.until(EC.url_contains("/admin"))

        # Navegar a "Usage Statistics"
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-item:nth-child(6) > .dropdown-toggle"))).click()
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Usage Statistics"))).click()

        # Elegir fecha final (hoy)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-4:nth-child(2) .btn"))).click()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ngb-dp-today > .btn-light"))).click()

        # Hacer primera consulta
        self.wait.until(EC.element_to_be_clickable((By.ID, "query-button"))).click()

        # Elegir fecha inicio (hoy)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-4:nth-child(1) .btn"))).click()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ngb-dp-today > .btn-light"))).click()

        # Hacer segunda consulta
        self.wait.until(EC.element_to_be_clickable((By.ID, "query-button"))).click()

        # Cambiar año en selector
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-4:nth-child(1) .btn"))).click()
        year_dropdown = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ngb-dp-navigation-select > .form-select:nth-child(2)")))
        year_dropdown.click()
        year_dropdown.find_element(By.XPATH, "//option[. = '2024']").click()

        # Seleccionar día activo y consultar
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ngb-dp-day .btn-light"))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, "query-button"))).click()

        # Verificación básica
        assert "Usage Statistics" in self.driver.page_source
