from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as CO

from CFC_LOGIN import login, out_login
import time

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\Dock-8\AppData\Local\Google\Chrome\User Data\HormigaProfile")

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/front/home")

wait = WebDriverWait(driver, 90)
login(wait)
wait.until(CO.visibility_of_element_located((By.ID,"notification-banner")))
driver.save_screenshot("CFC_045_EV1.png")
button_accept = wait.until(CO.element_to_be_clickable((By.ID,"btn-mark-as-read")))
button_accept.click()
wait.until(CO.visibility_of_element_located((By.CLASS_NAME,"toast-body")))
driver.save_screenshot("CFC_045_EV2.png")
out_login(wait)
driver.quit()