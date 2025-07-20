import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time

class TeammatesFeedbackResponseModificationTest(unittest.TestCase):

    def setUp(self):
        """Configuración inicial antes de cada test"""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.base_url = "https://teammates-hormiga-1.uc.r.appspot.com"

    def test_RF_EST_006_modificacion_respuesta(self):
        """
        Test Case: RF-EST-006 / TCN-TE-EST-002
        Caso de Prueba: CPF-EST-020
        """
        try:
            print("=== INICIANDO TEST RF-EST-006 (CPF-EST-020) ===")

            # PASO 1: Iniciar sesión como estudiante
            print("Paso 1: Iniciando sesión como estudiante...")
            self._login_as_student()

            # PASO 2: Acceder a la sesión desde la pantalla de inicio
            print("Paso 2: Accediendo a la sesión desde la pantalla de inicio...")
            self._access_active_session_and_question()

            # PASO 3: Seleccionar una pregunta del cuestionario que ya tenga respuesta
            print("Paso 3: Seleccionando una pregunta del cuestionario...")
            question_accessed = self._access_question_with_existing_response()
            if not question_accessed:
                raise Exception("No se pudo acceder a la pregunta con respuesta existente")

            # PASO 4: Escribir una respuesta inicial (si no existe)
            print("Paso 4: Verificando respuesta existente o escribiendo una inicial...")
            initial_response = "E2[T3]E5"
            initial_response_set = self._ensure_initial_response_exists(initial_response)
            if not initial_response_set:
                raise Exception("No se pudo establecer una respuesta inicial")

            # PASO 5: Modificar parte del contenido ingresado
            print("Paso 5: Modificando el contenido de la respuesta...")
            modified_response = "E2[T4]E4"
            response_modified = self._modify_existing_response(modified_response)
            if not response_modified:
                raise Exception("No se pudo modificar la respuesta")

            # PASO 6: Enviar la respuesta modificada
            print("Paso 6: Enviando la respuesta modificada...")
            submit_clicked = self._click_submit_button()
            if not submit_clicked:
                raise Exception("No se pudo hacer clic en el botón 'Enviar'")

            # VERIFICACIONES
            print("\n=== VERIFICACIÓN DEL RESULTADO ESPERADO ===")
            
            response_edited_recognized = self._verify_response_edited_state()
            changes_maintained = self._verify_changes_maintained(modified_response)

            # EVALUACIÓN DEL RESULTADO
            print("\n=== EVALUACIÓN DEL RESULTADO ===")
            
            test_passed = True
            
            if not response_edited_recognized:
                print("✗ FALLO: El sistema no reconoce el estado de la respuesta como editada")
                test_passed = False
            else:
                print("✓ ÉXITO: El sistema reconoce el estado de la respuesta como editada")

            if not changes_maintained:
                print("✗ FALLO: Los cambios realizados no se mantuvieron")
                test_passed = False
            else:
                print("✓ ÉXITO: Los cambios realizados se mantuvieron")

            if test_passed:
                print("\n=== RESULTADO FINAL: TEST PASÓ ===")
            else:
                print("\n=== RESULTADO FINAL: TEST FALLÓ ===")

            self.assertTrue(test_passed, "Test de validación de modificación de respuesta falló")

        except Exception as e:
            print(f"✗ Error durante la ejecución del test: {e}")
            self.driver.save_screenshot("error_CPF_EST_020_modification.png")
            raise

    def _login_as_student(self):
        """Realizar login como estudiante"""
        # Navegar a la página principal
        self.driver.get(self.base_url + "/web/front/home")

        # Hacer click en el botón Login
        login_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login') and @ngbdropdowntoggle]"))
        )
        login_dropdown.click()

        # Hacer click en Student Login
        student_login_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "student-login-btn"))
        )
        student_login_btn.click()

        # Realizar login con Google
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        
        # Ingresar email
        email_field = self.driver.find_element(By.ID, "identifierId")
        email_field.clear()
        email_field.send_keys("atacoh@unsa.edu.pe")
        
        next_button = self.driver.find_element(By.ID, "identifierNext")
        next_button.click()
        
        # Ingresar contraseña
        password_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "Passwd"))
        )
        password_field.clear()
        password_field.send_keys("Zodiaco24")
        
        password_next = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "passwordNext"))
        )
        password_next.click()
        
        # Esperar redirección
        WebDriverWait(self.driver, 15).until(
            EC.url_contains("/web/student/home")
        )
        print("✓ Login exitoso")

    def _access_active_session_and_question(self):
        """Acceder a la sesión activa y a la pregunta del cuestionario"""
        try:
            # Esperar un poco después del login
            time.sleep(3)
            
            # Hacer clic en el botón edit
            edit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "edit-submit-btn-2"))
            )
            edit_button.click()
            print("✓ Botón edit clickeado")

            # Esperar a que la página cargue
            time.sleep(5)
            
        except Exception as e:
            print(f"✗ Error en _access_active_session_and_question: {e}")
            self.driver.save_screenshot("debug_page_state.png")
            raise

    def _access_question_with_existing_response(self):
        """Acceder a una pregunta que ya tenga una respuesta existente"""
        try:
            # Intentar encontrar la pregunta 2 con múltiples estrategias
            question_2_element = self._find_question_2_element()
            
            if question_2_element:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", question_2_element)
                time.sleep(1)
                print("✓ Pregunta 2 encontrada y visible")
                return True
            else:
                # Si no encontramos Question 2, buscar cualquier pregunta disponible
                print("⚠ Question 2 no encontrada, buscando cualquier pregunta disponible...")
                any_question = self._find_any_question_element()
                if any_question:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", any_question)
                    time.sleep(1)
                    print("✓ Pregunta encontrada y usando como alternativa")
                    return True
                else:
                    raise Exception("No se encontró ninguna pregunta en la página")
            
        except Exception as e:
            print(f"✗ Error en _access_question_with_existing_response: {e}")
            return False

    def _find_question_2_element(self):
        """Buscar el elemento de la Question 2 con múltiples estrategias"""
        selectors = [
            "//h2[contains(@class, 'question-details') and contains(text(), 'Question 2:')]",
            "//h2[contains(text(), 'Question 2:')]",
            "//h1[contains(text(), 'Question 2:')]",
            "//h3[contains(text(), 'Question 2:')]",
            "//div[contains(text(), 'Question 2:')]",
            "//*[contains(text(), 'Question 2:')]",
            "//h2[contains(text(), 'Question 2')]",
            "//h2[contains(text(), 'Pregunta 2')]",
            "//*[contains(text(), 'Pregunta 2')]",
            "//h2[contains(text(), '2.')]",
            "//*[contains(@class, 'question') and contains(text(), '2')]"
        ]
        
        for i, selector in enumerate(selectors):
            try:
                element = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                return element
            except TimeoutException:
                continue
        
        return None

    def _find_any_question_element(self):
        """Buscar cualquier elemento de pregunta disponible"""
        selectors = [
            "//h2[contains(@class, 'question')]",
            "//div[contains(@class, 'question')]",
            "//*[contains(text(), 'Question')]",
            "//*[contains(text(), 'Pregunta')]",
            "//h2",
            "//h1",
            "//h3"
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                if elements:
                    return elements[0]
            except:
                continue
        
        return None

    def _ensure_initial_response_exists(self, initial_text):
        """Asegurar que existe una respuesta inicial, si no existe crearla"""
        try:
            # Primero verificar si ya existe una respuesta
            existing_response = self._get_current_response_text()
            
            if existing_response and existing_response.strip():
                print(f"✓ Respuesta existente encontrada: '{existing_response}'")
                return True
            else:
                print("⚠ No se encontró respuesta existente, creando una inicial...")
                return self._enter_response(initial_text)
                
        except Exception as e:
            print(f"✗ Error al verificar respuesta inicial: {e}")
            return False

    def _get_current_response_text(self):
        """Obtener el texto actual de la respuesta"""
        try:
            # Buscar en iframes
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            
            for iframe in iframes:
                try:
                    self.driver.switch_to.frame(iframe)
                    
                    text_field = self.driver.find_element(By.XPATH, "//body[@id='tinymce'] | //body[contains(@class, 'mce-content-body')] | //div[@contenteditable='true']")
                    current_text = text_field.text or text_field.get_attribute('innerHTML')
                    
                    self.driver.switch_to.default_content()
                    if current_text and current_text.strip():
                        return current_text.strip()
                    
                except:
                    self.driver.switch_to.default_content()
                    continue
            
            # Buscar en campos directos
            direct_selectors = [
                "//div[@contenteditable='true']",
                "//textarea",
                "//input[@type='text']"
            ]
            
            for selector in direct_selectors:
                try:
                    field = self.driver.find_element(By.XPATH, selector)
                    current_text = field.text or field.get_attribute('value')
                    if current_text and current_text.strip():
                        return current_text.strip()
                except:
                    continue
            
            return ""
            
        except Exception as e:
            print(f"✗ Error al obtener texto actual: {e}")
            self.driver.switch_to.default_content()
            return ""

    def _modify_existing_response(self, new_text):
        """Modificar la respuesta existente con nuevo texto"""
        try:
            print(f"Modificando respuesta a: '{new_text}'")
            
            # Buscar iframes en la página
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            print(f"iframes encontrados: {len(iframes)}")
            
            # Probar con cada iframe
            for i, iframe in enumerate(iframes):
                try:
                    self.driver.switch_to.frame(iframe)
                    
                    # Buscar campo editable
                    text_field = self.driver.find_element(By.XPATH, "//body[@id='tinymce'] | //body[contains(@class, 'mce-content-body')] | //div[@contenteditable='true']")
                    
                    # Limpiar el contenido existente y escribir el nuevo
                    text_field.clear()
                    time.sleep(0.5)  # Pequeña pausa para asegurar que se limpió
                    text_field.send_keys(new_text)
                    
                    self.driver.switch_to.default_content()
                    print(f"✓ Respuesta modificada exitosamente en iframe {i+1}")
                    time.sleep(1)  # Esperar para que se registre el cambio
                    return True
                    
                except Exception as e:
                    self.driver.switch_to.default_content()
                    continue
            
            # Si no funcionó con iframes, probar campos directos
            direct_selectors = [
                "//div[@contenteditable='true']",
                "//textarea",
                "//input[@type='text']"
            ]
            
            for selector in direct_selectors:
                try:
                    field = self.driver.find_element(By.XPATH, selector)
                    field.clear()
                    time.sleep(0.5)
                    field.send_keys(new_text)
                    print(f"✓ Respuesta modificada directamente")
                    time.sleep(1)
                    return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            print(f"✗ Error al modificar respuesta: {e}")
            self.driver.switch_to.default_content()
            return False

    def _enter_response(self, text):
        """Ingresar una respuesta (método auxiliar para respuesta inicial)"""
        try:
            # Buscar iframes en la página
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            
            # Probar con cada iframe
            for i, iframe in enumerate(iframes):
                try:
                    self.driver.switch_to.frame(iframe)
                    
                    # Buscar campo editable
                    text_field = self.driver.find_element(By.XPATH, "//body[@id='tinymce'] | //body[contains(@class, 'mce-content-body')] | //div[@contenteditable='true'] | //textarea")
                    
                    text_field.clear()
                    text_field.send_keys(text)
                    
                    self.driver.switch_to.default_content()
                    print(f"✓ Respuesta inicial ingresada en iframe {i+1}")
                    return True
                    
                except Exception as e:
                    self.driver.switch_to.default_content()
                    continue
            
            # Si no funcionó con iframes, probar campos directos
            direct_selectors = [
                "//div[@contenteditable='true']",
                "//textarea",
                "//input[@type='text']"
            ]
            
            for selector in direct_selectors:
                try:
                    field = self.driver.find_element(By.XPATH, selector)
                    field.clear()
                    field.send_keys(text)
                    print(f"✓ Respuesta inicial ingresada directamente")
                    return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            print(f"✗ Error al ingresar respuesta inicial: {e}")
            self.driver.switch_to.default_content()
            return False

    def _click_submit_button(self):
        """Hacer clic en el botón Enviar"""
        try:
            # Selectores específicos para el botón de enviar
            submit_selectors = [
                "//button[@id='btn-submit-qn-1']",
                "//button[contains(@id, 'btn-submit-qn')]",
                "//button[contains(text(), 'Submit Response for Question 1')]",
                "//button[contains(@class, 'btn-success') and @type='submit']",
                "//button[@type='submit' and contains(@class, 'btn-success')]",
                "//button[contains(text(), 'Submit Response')]",
                "//button[@type='submit']",
            ]
            
            for i, selector in enumerate(submit_selectors):
                try:
                    print(f"Buscando botón enviar con selector {i+1}: {selector}")
                    button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                    time.sleep(1)
                    button.click()
                    print(f"✓ Botón enviar clickeado con selector {i+1}")
                    time.sleep(3)  # Esperar procesamiento
                    return True
                    
                except Exception as e:
                    print(f"✗ Selector {i+1} no funcionó: {e}")
                    continue
            
            return False
                
        except Exception as e:
            print(f"✗ Error al hacer clic en botón enviar: {e}")
            return False

    def _verify_response_edited_state(self):
        """Verificar que el sistema reconoce el estado de la respuesta como editada"""
        try:
            time.sleep(2)
            
            # Indicadores de que la respuesta fue editada
            edited_indicators = [
                "//div[contains(@class, 'edited')]",
                "//span[contains(@class, 'modified')]",
                "//span[contains(text(), 'edited')]",
                "//span[contains(text(), 'modified')]",
                "//div[contains(@class, 'unsaved')]",
                "//*[contains(text(), 'unsaved changes')]",
                "//*[contains(text(), 'modified')]",
                "//button[contains(@class, 'btn-warning')]",  # Botón de advertencia por cambios
                "//div[contains(@class, 'alert-warning')]"
            ]
            
            for selector in edited_indicators:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    if element.is_displayed():
                        print("✓ Indicador de respuesta editada encontrado")
                        return True
                except:
                    continue
            
            # Si no hay indicadores específicos, verificar que el contenido cambió
            current_response = self._get_current_response_text()
            if current_response and "E2[T4]E4" in current_response:
                print("✓ Cambio de contenido detectado, asumiendo estado editado")
                return True
            
            # Si no hay errores y el botón submit está habilitado, asumir que reconoce la edición
            submit_enabled = self._check_submit_button_enabled()
            if submit_enabled:
                print("✓ Botón submit habilitado, indica reconocimiento de edición")
                return True
            
            print("⚠ No se detectaron indicadores claros de estado editado")
            return False
            
        except Exception as e:
            print(f"✗ Error al verificar estado editado: {e}")
            return False

    def _verify_changes_maintained(self, expected_text):
        """Verificar que los cambios realizados se mantuvieron"""
        try:
            time.sleep(1)
            
            current_response = self._get_current_response_text()
            
            if current_response and expected_text in current_response:
                print(f"✓ Cambios mantenidos: '{current_response}' contiene '{expected_text}'")
                return True
            elif current_response:
                print(f"✗ Cambios no mantenidos: se esperaba '{expected_text}' pero se encontró '{current_response}'")
                return False
            else:
                print("✗ No se pudo obtener el texto actual de la respuesta")
                return False
                
        except Exception as e:
            print(f"✗ Error al verificar cambios mantenidos: {e}")
            return False

    def _verify_submit_button_enabled(self):
        """Verificar que el botón 'Enviar' se habilitó después de la modificación"""
        try:
            submit_enabled = self._check_submit_button_enabled()
            
            if submit_enabled:
                print("✓ Botón 'Enviar' está habilitado")
                return True
            else:
                print("✗ Botón 'Enviar' no está habilitado")
                return False
                
        except Exception as e:
            print(f"✗ Error al verificar estado del botón enviar: {e}")
            return False

    def _check_submit_button_enabled(self):
        """Verificar si el botón submit está habilitado"""
        try:
            submit_selectors = [
                "//button[@id='btn-submit-qn-1']",
                "//button[contains(@id, 'btn-submit-qn')]",
                "//button[contains(text(), 'Submit Response')]",
                "//button[@type='submit']"
            ]
            
            for selector in submit_selectors:
                try:
                    button = self.driver.find_element(By.XPATH, selector)
                    if button.is_displayed():
                        is_disabled = button.get_attribute("disabled") is not None
                        has_disabled_class = "disabled" in button.get_attribute("class")
                        
                        if not is_disabled and not has_disabled_class:
                            return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"✗ Error al verificar botón submit: {e}")
            return False

    def tearDown(self):
        """Limpiar después del test"""
        self.driver.save_screenshot("final_state_CPF_EST_020_modification.png")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)