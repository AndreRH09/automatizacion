from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from constants import BASE_URL

def get_driver_with_session():
    options = Options()
    options.add_argument("user-data-dir=C:/Users/Gabriel/SeleniumProfile")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("detach", True) #deja la ventana abierta al terminar

    driver = webdriver.Chrome(options=options)
    return driver

def is_logged_in(driver, test_url=BASE_URL):
    driver.get(test_url)
    time.sleep(2)

    # Aquí haces una verificación simple. Por ejemplo:
    try:
        driver.find_element("id", "logout-btn")
        print("✅ Sesión activa detectada")
        return True
    except:
        print("❌ No se detectó sesión activa")
        return False
