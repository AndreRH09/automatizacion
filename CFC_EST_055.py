from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as CO

from CFC_LOGIN import login, out_login, addCourse
import time

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\Dock-8\AppData\Local\Google\Chrome\User Data\HormigaProfile")

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/front/home")

wait = WebDriverWait(driver, 90)
drop_down = wait.until(CO.element_to_be_clickable((By.XPATH,"//button[text()='Login']")))
drop_down.click()
button_login = wait.until(CO.element_to_be_clickable((By.ID, "instructor-login-btn")))
button_login.click()
addCourse(wait)
time.sleep(20)
driver.get("https://mail.google.com/mail/u/0/#inbox")
correo = wait.until(CO.element_to_be_clickable((By.XPATH,"//tr[contains(@class, 'zA')][.//span[@email='huichi.santander.gersson@gmail.com']]")))
correo.click()
wait.until(CO.presence_of_element_located((By.XPATH,"//div[contains(@class,'adn')]")))
enlace = wait.until(CO.presence_of_element_located((By.XPATH,"//a[contains(@href, 'teammates') or contains(@href, 'sendgrid')]")))
url = enlace.get_attribute("href")
driver.get(url)
registrarse = wait.until(CO.element_to_be_clickable((By.ID,"btn-confirm")))
registrarse.click()
time.sleep(10)
driver.save_screenshot("CFC_055_EV.png")
out_login(wait)
driver.quit()