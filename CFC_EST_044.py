from datetime import datetime
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

driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/admin/home")

wait = WebDriverWait(driver, 90)
notification = wait.until(CO.element_to_be_clickable((By.XPATH,"//a[text()='Notifications']")))
notification.click()
button_n = wait.until(CO.element_to_be_clickable((By.ID,"btn-add-notification")))
button_n.click()
select_element = wait.until(CO.visibility_of_element_located((By.ID, "notification-target-user")))
selector = Select(select_element)
selector.select_by_visible_text("Students")
title = wait.until(CO.element_to_be_clickable((By.ID,"notification-title")))
title.send_keys("Notificacion de Pruebas")
iframe = wait.until(CO.presence_of_element_located((By.CSS_SELECTOR, "iframe.tox-edit-area__iframe")))
driver.switch_to.frame(iframe)
question = wait.until(CO.presence_of_element_located((By.TAG_NAME,"P")))
question.send_keys("Esto es una prueba de notificaciones")
driver.switch_to.default_content()
hora_actual = datetime.now().hour
hora_texto = f"{hora_actual:02d}:00H"
print(hora_texto)
select_element = driver.find_element(By.XPATH, "//select[@aria-label='Select time']")
select = Select(select_element)
select.select_by_visible_text(hora_texto)
create = wait.until(CO.element_to_be_clickable((By.ID,"btn-create-notification")))
create.click()
driver.save_screenshot("CFC_044_EV1.png")
#ESTUDENT FALTA TERMINAR
drop = wait.until(CO.element_to_be_clickable((By.XPATH, "//button[text()='fayamamani@unsa.edu.pe']")))
drop.click()
student = wait.until(CO.element_to_be_clickable((By.XPATH,'//a[text()="To student pages"]')))
student.click()
wait.until(CO.visibility_of_element_located((By.ID,"notification-banner")))
driver.save_screenshot("CFC_044_EV2.png")
"""drop = wait.until(CO.element_to_be_clickable((By.XPATH, "//button[text()='fayamamani@unsa.edu.pe']")))
drop.click()
admin = wait.until(CO.element_to_be_clickable((By.XPATH,'//a[text()="To admin pages"]')))
admin.click()
notification = wait.until(CO.element_to_be_clickable((By.XPATH,"//a[text()='Notifications']")))
notification.click()
delete_button = wait.until(CO.element_to_be_clickable((By.XPATH, "//table/tbody/tr[1]//button[contains(text(), 'Delete')]")))
delete_button.click()
accept = wait.until(CO.element_to_be_clickable((By.CLASS_NAME,"modal-btn-ok")))
accept.click()"""
driver.quit()