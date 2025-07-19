from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as CO

def login(wait):
    drop_down = wait.until(CO.element_to_be_clickable((By.XPATH,"//button[text()='Login']")))
    drop_down.click()
    button_login = wait.until(CO.element_to_be_clickable((By.ID, "student-login-btn")))
    button_login.click()

def out_login(wait):
    drop_down = wait.until(CO.element_to_be_clickable((By.CLASS_NAME, "dropdown-toggle")))
    drop_down.click()
    out = wait.until(CO.element_to_be_clickable((By.ID, "logout-btn")))
    out.click()