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
time.sleep(10)
driver.save_screenshot("CFC_034_EV1.png")
question.clear()
question.send_keys("Nueva respuesta para el Test")
driver.save_screenshot("CFC_034_EV2.png")
driver.switch_to.default_content()
time.sleep(10)
out_login(wait)
driver.quit()