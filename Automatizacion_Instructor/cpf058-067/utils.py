
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_element(driver, by, selector, timeout=10):
  return WebDriverWait(driver, timeout).until(
      EC.presence_of_element_located((by, selector))
  )