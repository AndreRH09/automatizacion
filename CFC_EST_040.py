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
view = wait.until(CO.element_to_be_clickable((By.ID,"view-submit-btn-1")))
view.click()
modal = wait.until(CO.visibility_of_element_located((By.CSS_SELECTOR, "ngb-modal-window[role='dialog']")))
close_button = modal.find_element(By.CLASS_NAME, "btn-close")
close_button.click()
select_element = wait.until(CO.visibility_of_element_located((By.ID, "select-group-by")))
selector = Select(select_element)
selector.select_by_value("Question")
time.sleep(10)
driver.save_screenshot("CFC_040_EV.png")
out_login(wait)
driver.quit()