from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as CO

from CFC_LOGIN import login, out_login
import time

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\Dock-8\AppData\Local\Google\Chrome\User Data\SeleniumProfile")

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://teammatesv4.appspot.com/web/front/home")

wait = WebDriverWait(driver, 90)
login(wait)
edit_button = wait.until(CO.element_to_be_clickable((By.ID,"edit-submit-btn-2")))
edit_button.click()
iframe = wait.until(CO.presence_of_element_located((By.CSS_SELECTOR, "iframe.tox-edit-area__iframe")))
driver.switch_to.frame(iframe)
question = wait.until(CO.presence_of_element_located((By.ID,"tinymce")))
question.clear()
question.send_keys("Probamos el poder restaurar la respuesta")
time.sleep(10)
question.send_keys(", Probamos por segunda vezel poder restaurar la respuesta")
driver.save_screenshot("CFC_037_EV1.png")
driver.switch_to.default_content()
out_login(wait)
driver.quit()