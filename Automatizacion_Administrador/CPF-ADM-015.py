import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv

class TestADM015:
    def setup_method(self, method):
        load_dotenv(dotenv_path='cred.env')
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        assert self.email and self.password, "Credenciales no encontradas en cred.env"

        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def teardown_method(self, method):
        self.driver.quit()

    def test_adm014(self):
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/front/home")

        # Abrir menú responsive si está
        try:
            toggler = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".navbar-toggler-icon")))
            toggler.click()
        except TimeoutException:
            pass

        # Login como instructor
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-item:nth-child(1) > .dropdown-toggle"))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, "instructor-login-btn"))).click()

        # Google login
        email_input = self.wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
        email_input.send_keys(self.email)
        email_input.send_keys(Keys.ENTER)

        password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)

        # Esperar redirección a vista de instructor
        self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Home")))
        self.driver.save_screenshot("01_instructor_home.png")

        # Ir al menú de usuario (último dropdown)
        dropdowns = self.driver.find_elements(By.CSS_SELECTOR, ".dropdown-toggle")
        dropdowns[-1].click()

        # Ir a admin pages
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "To admin pages"))).click()
        self.wait.until(EC.url_contains("/admin"))
        self.driver.save_screenshot("02_admin_dashboard.png")

        # Ir a la sección Sessions
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sessions"))).click()
        self.driver.save_screenshot("03_admin_sessions_list.png")

        # Esperar a que aparezca al menos un botón Show
        try:
            self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Show")))
        except TimeoutException:
            self.driver.save_screenshot("04_no_show_buttons_found.png")
            raise Exception("No se encontró ningún botón 'Show' tras esperar.")

        # Clic en el primer Show
        show_buttons = self.driver.find_elements(By.LINK_TEXT, "Show")
        show_buttons[0].click()
        self.driver.save_screenshot("05_first_show_clicked.png")

        # Si hay otro botón "Show", hacer clic también
        if len(show_buttons) > 1:
            show_buttons[1].click()
            self.driver.save_screenshot("06_second_show_clicked.png")

        # Verificar que cargó la tabla
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".card .table, .table-responsive")))
            self.driver.save_screenshot("07_table_loaded.png")
        except TimeoutException:
            self.driver.save_screenshot("07_table_NOT_loaded.png")
            raise Exception("No se encontró la tabla de sesiones después de hacer clic en 'Show'.")
