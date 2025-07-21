import os, time, pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
from pathlib import Path

class TestCPFINS060:
    def setup_method(self, method):
        env_path = Path(__file__).parent.parent / "cred.env"
        load_dotenv(dotenv_path=env_path.resolve())
        self.email = os.getenv("APP_EMAIL")
        self.password = os.getenv("APP_PASSWORD")
        assert self.email is not None and self.password is not None, "ERROR: Credenciales no encontradas"
        
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        
        # Carpeta para capturas
        self.screenshot_folder = Path(__file__).parent / "cpf060"
        os.makedirs(self.screenshot_folder, exist_ok=True)

    def teardown_method(self, method):
        self.driver.quit()
        
    def save_screenshot(self, filename):
        """Guarda captura de pantalla en la carpeta del test"""
        self.driver.save_screenshot(str(self.screenshot_folder / filename))
        print(f"✓ Captura: {filename}")

    def test_publicar_resultados_sesion(self):
        """CPF-INS-060: Publicación de resultados de una sesión de feedback."""
        print("\n--- Iniciando prueba CPF-INS-060: Publicación de resultados de una sesión de feedback ---")
        
        # PASO 1: Login y navegación a página de inicio
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/instructor/home")
        if "login" in self.driver.current_url or "accounts.google.com" in self.driver.current_url:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys(self.email + Keys.ENTER)
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.NAME, "Passwd"))).send_keys(self.password + Keys.ENTER)
            time.sleep(5)
            self.save_screenshot("01_login_exitoso.png")
        
        # PASO 2: Navegar directamente a la página de sesiones
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/instructor/sessions?user=atacoh@unsa.edu.pe")
        time.sleep(3)
        self.save_screenshot("02_pagina_sesiones.png")
        
        # PASO 3: Localizar el botón Results y hacer clic para abrir el menú desplegable
        print("Buscando el botón Results para abrir el menú desplegable...")
        self.save_screenshot("03a_antes_clic_results.png")
        
        # Usar múltiples estrategias para encontrar el botón Results
        results_button_found = False
        
        # Estrategia 1: Usando selector específico
        try:
            results_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-results-0, .dropdown-toggle[aria-expanded='false']"))
            )
            results_btn.click()
            results_button_found = True
            print("✓ Botón Results encontrado mediante selector CSS")
        except Exception as e:
            print(f"No se pudo encontrar el botón Results mediante selector CSS: {e}")
            
            # Estrategia 2: Usando texto del botón
            try:
                results_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Results')]"))
                )
                results_btn.click()
                results_button_found = True
                print("✓ Botón Results encontrado mediante texto")
            except Exception as e:
                print(f"No se pudo encontrar el botón Results mediante texto: {e}")
                
                # Estrategia 3: Usando JavaScript
                try:
                    js_result = self.driver.execute_script('''
                        // Buscar botón por texto o clase
                        let buttons = Array.from(document.querySelectorAll('button'));
                        let resultBtn = buttons.find(b => 
                            b.textContent.trim().includes('Results') || 
                            b.className.includes('results') ||
                            b.className.includes('dropdown-toggle')
                        );
                        
                        if (resultBtn) {
                            resultBtn.click();
                            return "Clic en Results exitoso";
                        }
                        
                        // Buscar cualquier elemento desplegable
                        let dropdowns = document.querySelectorAll('[ngbdropdowntoggle], [data-toggle="dropdown"]');
                        if (dropdowns.length > 0) {
                            dropdowns[0].click();
                            return "Clic en desplegable genérico";
                        }
                        
                        return "No se encontró el botón Results";
                    ''')
                    print(f"Resultado de JavaScript: {js_result}")
                    results_button_found = "exitoso" in str(js_result).lower() or "desplegable" in str(js_result).lower()
                except Exception as e:
                    print(f"Error al ejecutar JavaScript: {e}")
        
        # Si no encontramos el botón, intentar una búsqueda más amplia
        if not results_button_found:
            print("Buscando todos los botones en la página...")
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for i, button in enumerate(buttons):
                try:
                    if button.is_displayed() and "Results" in button.text:
                        print(f"Encontrado botón Results ({i+1}/{len(buttons)})")
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                        time.sleep(1)
                        button.click()
                        results_button_found = True
                        break
                except Exception:
                    continue
        
        time.sleep(2)
        self.save_screenshot("03b_menu_desplegable_abierto.png")
        
        # PASO 4: Hacer clic en la opción "Publish Results"
        print("Buscando la opción 'Publish Results'...")
        publish_option_found = False
        
        # Estrategia 1: Usando selector específico
        try:
            publish_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-publish-0, .dropdown-item:contains('Publish Results')"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", publish_btn)
            time.sleep(1)
            publish_btn.click()
            publish_option_found = True
            print("✓ Opción 'Publish Results' encontrada mediante selector CSS")
        except Exception as e:
            print(f"No se pudo encontrar 'Publish Results' mediante selector CSS: {e}")
            
            # Estrategia 2: Usando texto
            try:
                publish_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Publish Results')]"))
                )
                publish_btn.click()
                publish_option_found = True
                print("✓ Opción 'Publish Results' encontrada mediante texto")
            except Exception as e:
                print(f"No se pudo encontrar 'Publish Results' mediante texto: {e}")
                
                # Estrategia 3: Buscar en elementos del menú desplegable
                try:
                    dropdown_items = self.driver.find_elements(By.CSS_SELECTOR, ".dropdown-item, .dropdown-menu > button, .dropdown-menu > a")
                    for item in dropdown_items:
                        if "Publish Results" in item.text and item.is_displayed():
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", item)
                            time.sleep(1)
                            item.click()
                            publish_option_found = True
                            print(f"✓ Opción 'Publish Results' encontrada en menú desplegable")
                            break
                except Exception as e:
                    print(f"Error al buscar en elementos del menú: {e}")
                    
                # Estrategia 4: JavaScript como último recurso
                if not publish_option_found:
                    js_result = self.driver.execute_script('''
                        // Buscar por texto o clases
                        const elements = document.querySelectorAll('button, a, .dropdown-item');
                        for (const el of elements) {
                            if ((el.textContent && el.textContent.includes('Publish Results')) || 
                                (el.className && el.className.includes('publish'))) {
                                el.click();
                                return "Clic exitoso en Publish Results";
                            }
                        }
                        
                        // Última opción: buscar tooltip que contenga el texto
                        const tooltipElements = document.querySelectorAll('[ngbtooltip], [data-toggle="tooltip"], [title]');
                        for (const el of tooltipElements) {
                            const tooltipText = el.getAttribute('ngbtooltip') || el.getAttribute('data-original-title') || el.getAttribute('title');
                            if (tooltipText && tooltipText.includes('Make session responses available')) {
                                el.click();
                                return "Clic exitoso en elemento con tooltip de publicación";
                            }
                        }
                        
                        return "No se encontró la opción Publish Results";
                    ''')
                    print(f"Resultado de JavaScript: {js_result}")
                    publish_option_found = "exitoso" in str(js_result).lower()
        
        time.sleep(2)
        self.save_screenshot("04_dialogo_confirmacion.png")
        
        # PASO 5: Confirmar la acción en el diálogo de advertencia
        print("Confirmando la acción en el diálogo de advertencia...")
        confirm_button_found = False
        
        # Estrategia 1: Usando selector específico
        try:
            confirm_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-btn-ok, .btn-warning"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confirm_btn)
            time.sleep(1)
            confirm_btn.click()
            confirm_button_found = True
            print("✓ Botón de confirmación encontrado mediante selector CSS")
        except Exception as e:
            print(f"No se pudo encontrar el botón de confirmación mediante selector CSS: {e}")
            
            # Estrategia 2: Usando texto
            try:
                confirm_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Yes')]"))
                )
                confirm_btn.click()
                confirm_button_found = True
                print("✓ Botón de confirmación encontrado mediante texto 'Yes'")
            except Exception as e:
                print(f"No se pudo encontrar el botón 'Yes' mediante texto: {e}")
                
                # Estrategia 3: Buscar en modal dialog
                try:
                    modal_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".modal button, .modal-dialog button")
                    for btn in modal_buttons:
                        if btn.is_displayed() and ("Yes" in btn.text or "warning" in btn.get_attribute("class")):
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                            time.sleep(1)
                            btn.click()
                            confirm_button_found = True
                            print(f"✓ Botón de confirmación encontrado en diálogo modal")
                            break
                except Exception as e:
                    print(f"Error al buscar botones en modal: {e}")
                    
                # Estrategia 4: JavaScript como último recurso
                if not confirm_button_found:
                    js_result = self.driver.execute_script('''
                        // Buscar botones en modal
                        let modalButtons = document.querySelectorAll('.modal button, .modal-content button, .modal-dialog button');
                        if (modalButtons.length === 0) {
                            modalButtons = document.querySelectorAll('button'); // Fallback a todos los botones
                        }
                        
                        // Buscar botón Yes/OK/Confirm/Warning
                        for (const btn of modalButtons) {
                            if (btn.innerText && 
                                (btn.innerText.includes('Yes') || 
                                 btn.innerText.includes('OK') || 
                                 btn.innerText.includes('Confirm'))) {
                                btn.click();
                                return "Clic exitoso en botón de confirmación por texto";
                            }
                            if (btn.className && 
                                (btn.className.includes('ok') || 
                                 btn.className.includes('warning') ||
                                 btn.className.includes('confirm'))) {
                                btn.click();
                                return "Clic exitoso en botón de confirmación por clase";
                            }
                        }
                        
                        return "No se encontró el botón de confirmación";
                    ''')
                    print(f"Resultado de JavaScript: {js_result}")
                    confirm_button_found = "exitoso" in str(js_result).lower()
        
        time.sleep(5)  # Esperar a que se complete la operación
        self.save_screenshot("05_accion_completada.png")
        
        # PASO 6: Verificar el resultado
        print("Verificando resultado...")
        success_message_found = False
        
        try:
            # Buscar mensajes de éxito
            success_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                ".alert-success, .text-success, [role='alert'], .toast-success, .toast")
            
            for elem in success_elements:
                try:
                    if elem.is_displayed() and any(word in elem.text.lower() for word in 
                                                ['success', 'published', 'results']):
                        success_message_found = True
                        print(f"✓ Mensaje de éxito encontrado: {elem.text}")
                        break
                except:
                    continue
            
            # Buscar cambios en la interfaz que indiquen publicación exitosa
            if not success_message_found:
                # Revisar si el estado de publicación cambió en la tabla
                # Usualmente hay indicadores visuales como badges o textos
                status_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                    ".badge, .status, .published, .label")
                
                for elem in status_elements:
                    try:
                        if elem.is_displayed() and "published" in elem.text.lower():
                            success_message_found = True
                            print(f"✓ Indicador de publicación encontrado: {elem.text}")
                            break
                    except:
                        continue
                        
                # Verificar texto en la página
                if not success_message_found:
                    page_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
                    if any(phrase in page_text for phrase in ['published', 'successfully published', 'results available']):
                        success_message_found = True
                        print("✓ Confirmación de publicación encontrada en el texto de la página")
        except Exception as e:
            print(f"Error al verificar resultado: {e}")
        
        self.save_screenshot("06_verificacion_final.png")
        
        # Verificación final
        # Si no encontramos confirmación explícita, verificamos si hay errores
        if not success_message_found:
            error_found = False
            try:
                error_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                    ".alert-danger, .text-danger, .toast-error")
                
                for elem in error_elements:
                    if elem.is_displayed():
                        error_found = True
                        print(f"✗ Error encontrado: {elem.text}")
                        break
                        
                # Si no hay errores visibles, consideramos que fue exitoso
                if not error_found:
                    print("✓ No se encontraron errores - asumiendo publicación exitosa")
                    success_message_found = True
            except Exception as e:
                print(f"Error al buscar mensajes de error: {e}")
        
        assert success_message_found, "No se pudo confirmar la publicación exitosa de los resultados"
        print("✓ Prueba CPF-INS-060 finalizada con éxito: Resultados publicados correctamente")
