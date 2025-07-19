"""
Configuración del driver con múltiples opciones
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

def get_driver(use_debug_mode=False, headless=False):
    """
    Obtiene el driver de Chrome con diferentes configuraciones
    
    Args:
        use_debug_mode (bool): Si True, conecta a Chrome en modo depuración
        headless (bool): Si True, ejecuta sin interfaz gráfica
    """
    options = webdriver.ChromeOptions()
    
    # Configuraciones básicas
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    if headless:
        options.add_argument('--headless')
    
    if use_debug_mode:
        # Conectar a Chrome existente (mantiene sesión)
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome(options=options)
    else:
        # Crear nueva instancia (sin sesión previa)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    
    driver.implicitly_wait(10)
    return driver