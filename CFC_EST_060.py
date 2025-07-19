from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
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
team = wait.until(CO.element_to_be_clickable((By.ID,"view-team-btn-1")))
team.click()
target_element = wait.until(CO.presence_of_element_located((By.CLASS_NAME, "fill-plain")))
driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", target_element)
driver.save_screenshot("CFC_060_EV.png")
out_login(wait)
driver.quit()