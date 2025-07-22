# CPF-ADM-003.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import os

class TestADM003():
    def setup_method(self, method):
        load_dotenv(dotenv_path='cred.env')
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        assert self.email is not None, "EMAIL no encontrada en cred.env"
        assert self.password is not None, "PASSWORD no encontrada en cred.env"

        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self, method):
        self.driver.quit()

    def esperar_cierre_modal(self):
        try:
            self.driver.find_element(By.CLASS_NAME, "modal")
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "modal")))
        except:
            pass

    def test_adm003(self):
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/front/home")

        try:
            toggler = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".navbar-toggler-icon")))
            toggler.click()
        except TimeoutException:
            pass

        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-item:nth-child(1) > .dropdown-toggle"))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, "instructor-login-btn"))).click()

        email_input = self.wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
        email_input.send_keys(self.email)
        email_input.send_keys(Keys.ENTER)

        password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)

        self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Home")))

        # Ir al menú de usuario
        user_dropdowns = self.driver.find_elements(By.CSS_SELECTOR, ".dropdown-toggle")
        if user_dropdowns:
            user_dropdowns[-1].click()
        else:
            raise Exception("No se encontró el menú de usuario.")

        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "To admin pages"))).click()

        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#edit-account-request-0 > .fa-solid")))
        solicitudes = self.driver.find_elements(By.CSS_SELECTOR, "#edit-account-request-0 > .fa-solid")

        if not solicitudes:
            raise Exception("No hay solicitudes disponibles.")
        solicitudes[0].click()

        actions = ActionChains(self.driver)

        # Nombre válido
        name = self.wait.until(EC.presence_of_element_located((By.ID, "request-name")))
        actions.double_click(name).perform()
        name.send_keys("Prueba03")
        self.driver.find_element(By.ID, "btn-confirm-edit-request").click()
        self.esperar_cierre_modal()

        solicitudes[0].click()

        # Email inválido
        email = self.wait.until(EC.presence_of_element_located((By.ID, "request-email")))
        actions.double_click(email).perform()
        email.send_keys("huichi789_789@")
        self.driver.find_element(By.ID, "btn-confirm-edit-request").click()
        self.esperar_cierre_modal()

        solicitudes[0].click()

        # Comentario
        comments = self.wait.until(EC.presence_of_element_located((By.ID, "request-comments")))
        actions.double_click(comments).perform()
        comments.send_keys("Comentario de prueba")
        self.driver.find_element(By.ID, "btn-confirm-edit-request").click()
        self.esperar_cierre_modal()

        solicitudes[0].click()

        # Rechazar solicitud (último paso)
        self.driver.find_element(By.CSS_SELECTOR, ".d-block").click()
        self.driver.find_element(By.CSS_SELECTOR, "#reject-account-request-modal > div:nth-child(3)").click()
        self.esperar_cierre_modal()

        # 🔒 Ya no se edita más porque la solicitud fue rechazada.
