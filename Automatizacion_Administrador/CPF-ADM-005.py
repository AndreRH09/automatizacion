from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import os
import time

class TestADM005:
    def setup_method(self, method):
        load_dotenv(dotenv_path='cred.env')
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        assert self.email is not None and self.password is not None

        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self, method):
        self.driver.quit()

    def esperar_carga_busqueda(self):
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loading-spinner")))
        except TimeoutException:
            pass
        time.sleep(1)

    def buscar(self, texto):
        try:
            search_box = self.wait.until(EC.element_to_be_clickable((By.ID, "search-box")))
            search_box.clear()
            search_box.send_keys(texto)
            self.driver.find_element(By.ID, "search-button").click()
            self.esperar_carga_busqueda()
        except Exception as e:
            print(f"[!] Error buscando '{texto}': {e}")

    def test_adm005(self):
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/front/home")

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

        # Ir a "To admin pages"
        dropdowns = self.driver.find_elements(By.CSS_SELECTOR, ".dropdown-toggle")
        if dropdowns:
            dropdowns[-1].click()
        else:
            raise Exception("No se encontró el menú desplegable del usuario.")

        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "To admin pages"))).click()
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Search"))).click()

        entradas = [
            "ghuichi@unsa.edu.pe",   # válida
            "noexiste123",           # no existente
            "     ",                 # espacios
            "",                      # vacío
            "a" * 100                # texto largo
        ]

        for entrada in entradas:
            print(f"[*] Buscando: '{entrada}'")
            self.buscar(entrada)
