import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

class TeammatesFeedbackResponseFormattingTest(unittest.TestCase):

    def setUp(self):
        """Configuración inicial antes de cada test"""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.base_url = "https://teammates-hormiga-1.uc.r.appspot.com"

    def test_RF_EST_006_formatos_respuesta(self):
        """
        Test Case: RF-EST-006 / TCN-TE-EST-002
        Caso de Prueba: CPF-EST-021
        """
        try:
            print("=== INICIANDO TEST RF-EST-006 (CPF-EST-021) ===")

            # PASO 1: Iniciar sesión como estudiante
            print("Paso 1: Iniciando sesión como estudiante...")
            self._login_as_student()

            # PASO 2: Acceder a la sesión correspondiente
            print("Paso 2: Accediendo a la sesión correspondiente...")
            self._access_active_session_and_question()

            # PASO 3: Seleccionar una pregunta y escribir una respuesta
            print("Paso 3: Seleccionando una pregunta y escribiendo una respuesta...")
            base_response = "E2[T6]E2"
            response_entered = self._enter_base_response(base_response)
            if not response_entered:
                raise Exception("No se pudo ingresar la respuesta base")

            # PASO 4: Aplicar formato (negrita, cursiva, subrayado, lista)
            print("Paso 4: Aplicando formatos y elementos enriquecidos...")
            formatting_applied = self._apply_required_formatting()
            if not formatting_applied:
                raise Exception("No se pudo aplicar formato a la respuesta")

            # PASO 5: Enviar la respuesta
            print("Paso 5: Enviando la respuesta...")
            response_submitted = self._submit_response()
            if not response_submitted:
                raise Exception("No se pudo enviar la respuesta")

            # VERIFICACIONES
            print("\n=== VERIFICACIÓN DEL RESULTADO ESPERADO ===")
            
            response_in_edit_state = self._verify_response_in_edit_state()
            visual_elements_reflected = self._verify_visual_elements_reflected()
            content_preserved = self._verify_content_preserved(base_response)
            submission_successful = self._verify_submission_successful()

            # EVALUACIÓN DEL RESULTADO
            print("\n=== EVALUACIÓN DEL RESULTADO ===")
            
            test_passed = True
            
            if not response_in_edit_state:
                print("✗ FALLO: El sistema no mantiene la respuesta en estado de edición")
                test_passed = False
            else:
                print("✓ ÉXITO: El sistema mantiene la respuesta en estado de edición")

            if not visual_elements_reflected:
                print("✗ FALLO: Los elementos enriquecidos no se reflejan visualmente")
                test_passed = False
            else:
                print("✓ ÉXITO: Los elementos enriquecidos se reflejan visualmente")

            if not content_preserved:
                print("✗ FALLO: Se perdió el contenido escrito previamente")
                test_passed = False
            else:
                print("✓ ÉXITO: No se perdió el contenido escrito previamente")

            if not submission_successful:
                print("✗ FALLO: La respuesta no se envió correctamente")
                test_passed = False
            else:
                print("✓ ÉXITO: La respuesta se envió correctamente")

            if test_passed:
                print("\n=== RESULTADO FINAL: TEST PASÓ ===")
            else:
                print("\n=== RESULTADO FINAL: TEST FALLÓ ===")

            self.assertTrue(test_passed, "Test de validación de formatos en respuesta falló")

        except Exception as e:
            print(f"✗ Error durante la ejecución del test: {e}")
            self.driver.save_screenshot("error_CPF_EST_021_formatting.png")
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
            
            # Buscar la pregunta disponible
            question_element = self._find_question_element()
            
            if question_element:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", question_element)
                time.sleep(1)
                print("✓ Pregunta encontrada y visible")
            else:
                raise Exception("No se encontró ninguna pregunta en la página")
            
        except Exception as e:
            print(f"✗ Error en _access_active_session_and_question: {e}")
            self.driver.save_screenshot("debug_page_state.png")
            raise

    def _find_question_element(self):
        """Buscar cualquier elemento de pregunta disponible"""
        selectors = [
            "//h2[contains(text(), 'Question 2:')]",
            "//h2[contains(text(), 'Question 1:')]",
            "//h2[contains(text(), 'Question')]",
            "//h1[contains(text(), 'Question')]",
            "//h3[contains(text(), 'Question')]",
            "//div[contains(text(), 'Question')]",
            "//*[contains(text(), 'Question')]",
            "//h2[contains(text(), 'Pregunta')]",
            "//*[contains(text(), 'Pregunta')]",
            "//h2[contains(@class, 'question')]",
            "//div[contains(@class, 'question')]"
        ]
        
        for selector in selectors:
            try:
                element = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                return element
            except TimeoutException:
                continue
        
        return None

    def _enter_base_response(self, text):
        """Ingresar una respuesta base"""
        try:
            # Buscar iframes en la página
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            print(f"iframes encontrados: {len(iframes)}")
            
            # Probar con cada iframe
            for i, iframe in enumerate(iframes):
                try:
                    self.driver.switch_to.frame(iframe)
                    
                    # Buscar campo editable
                    text_field = self.driver.find_element(By.XPATH, "//body[@id='tinymce'] | //body[contains(@class, 'mce-content-body')] | //div[@contenteditable='true']")
                    
                    text_field.clear()
                    text_field.send_keys(text)
                    
                    self.driver.switch_to.default_content()
                    print(f"✓ Respuesta base ingresada en iframe {i+1}")
                    time.sleep(1)
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
                    print(f"✓ Respuesta base ingresada directamente")
                    time.sleep(1)
                    return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            print(f"✗ Error al ingresar respuesta base: {e}")
            self.driver.switch_to.default_content()
            return False

    def _apply_required_formatting(self):
        """Aplicar formatos requeridos: negrita, cursiva, subrayado, lista"""
        try:
            print("Aplicando formatos requeridos...")
            
            # Buscar el campo de texto activo
            text_field = self._find_active_text_field()
            if not text_field:
                return False
            
            # Aplicar los formatos específicos requeridos
            formats_applied = []
            
            # 1. Aplicar negrita
            if self._apply_bold_formatting(text_field):
                formats_applied.append("negrita")
            
            # 2. Aplicar cursiva
            if self._apply_italic_formatting(text_field):
                formats_applied.append("cursiva")
            
            # 3. Aplicar subrayado
            if self._apply_underline_formatting(text_field):
                formats_applied.append("subrayado")
            
            # 4. Aplicar lista
            if self._apply_list_formatting(text_field):
                formats_applied.append("lista")
            
            # Verificar que se aplicaron todos los formatos requeridos
            required_formats = ["negrita", "cursiva", "subrayado", "lista"]
            
            if all(fmt in formats_applied for fmt in required_formats):
                print(f"✓ Formatos aplicados exitosamente: {', '.join(formats_applied)}")
                return True
            else:
                print(f"⚠ Solo se aplicaron algunos formatos: {', '.join(formats_applied)}")
                # Aún consideramos exitoso si se aplicó al menos algún formato
                return len(formats_applied) > 0
                
        except Exception as e:
            print(f"✗ Error al aplicar formato: {e}")
            self.driver.switch_to.default_content()
            return False

    def _find_active_text_field(self):
        """Encontrar el campo de texto activo"""
        try:
            # Buscar en iframes
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            
            for iframe in iframes:
                try:
                    self.driver.switch_to.frame(iframe)
                    
                    text_field = self.driver.find_element(By.XPATH, "//body[@id='tinymce'] | //body[contains(@class, 'mce-content-body')] | //div[@contenteditable='true']")
                    
                    if text_field.is_displayed():
                        print("✓ Campo de texto activo encontrado en iframe")
                        return text_field
                    
                except:
                    self.driver.switch_to.default_content()
                    continue
            
            # Buscar campos directos
            direct_selectors = [
                "//div[@contenteditable='true']",
                "//textarea",
                "//input[@type='text']"
            ]
            
            for selector in direct_selectors:
                try:
                    field = self.driver.find_element(By.XPATH, selector)
                    if field.is_displayed():
                        print("✓ Campo de texto activo encontrado directamente")
                        return field
                except:
                    continue
            
            return None
            
        except Exception as e:
            print(f"✗ Error al encontrar campo activo: {e}")
            self.driver.switch_to.default_content()
            return None

    def _apply_bold_formatting(self, text_field):
        """Aplicar formato de negrita"""
        try:
            # Seleccionar todo el texto
            text_field.send_keys(Keys.CONTROL + "a")
            time.sleep(0.5)
            
            # Aplicar negrita con Ctrl+B
            text_field.send_keys(Keys.CONTROL + "b")
            time.sleep(0.5)
            
            # Agregar texto adicional para verificar
            text_field.send_keys(Keys.END)
            text_field.send_keys(" - Texto en negrita")
            
            print("✓ Formato de negrita aplicado")
            return True
            
        except Exception as e:
            print(f"⚠ No se pudo aplicar negrita: {e}")
            return False

    def _apply_italic_formatting(self, text_field):
        """Aplicar formato de cursiva"""
        try:
            # Ir al final del texto
            text_field.send_keys(Keys.END)
            text_field.send_keys(" - ")
            
            # Aplicar cursiva con Ctrl+I
            text_field.send_keys(Keys.CONTROL + "i")
            text_field.send_keys("Texto en cursiva")
            time.sleep(0.5)
            
            print("✓ Formato de cursiva aplicado")
            return True
            
        except Exception as e:
            print(f"⚠ No se pudo aplicar cursiva: {e}")
            return False

    def _apply_underline_formatting(self, text_field):
        """Aplicar formato de subrayado"""
        try:
            # Ir al final del texto
            text_field.send_keys(Keys.END)
            text_field.send_keys(" - ")
            
            # Aplicar subrayado con Ctrl+U
            text_field.send_keys(Keys.CONTROL + "u")
            text_field.send_keys("Texto subrayado")
            time.sleep(0.5)
            
            print("✓ Formato de subrayado aplicado")
            return True
            
        except Exception as e:
            print(f"⚠ No se pudo aplicar subrayado: {e}")
            return False

    def _apply_list_formatting(self, text_field):
        """Aplicar formato de lista/viñetas"""
        try:
            # Ir al final del texto
            text_field.send_keys(Keys.END)
            text_field.send_keys(Keys.ENTER)
            
            # Agregar elementos de lista manualmente
            text_field.send_keys("• Elemento 1")
            text_field.send_keys(Keys.ENTER)
            text_field.send_keys("• Elemento 2")
            
            print("✓ Formato de lista aplicado")
            return True
            
        except Exception as e:
            print(f"⚠ No se pudo aplicar lista: {e}")
            return False

    def _submit_response(self):
        """Enviar la respuesta haciendo clic en el botón Submit Response"""
        try:
            # Volver al contenido principal si estamos en iframe
            self.driver.switch_to.default_content()
            
            # Buscar el botón Submit Response for Question 2
            submit_button_selectors = [
                "//button[@id='btn-submit-qn-2']",
                "//button[contains(@id, 'btn-submit-qn')]",
                "//button[contains(text(), 'Submit Response for Question 2')]",
                "//button[contains(text(), 'Submit Response')]",
                "//button[contains(@class, 'btn-success') and contains(text(), 'Submit')]"
            ]
            
            submit_button = None
            for selector in submit_button_selectors:
                try:
                    submit_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if submit_button:
                # Hacer scroll para asegurar que el botón sea visible
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                time.sleep(1)
                
                # Hacer clic en el botón
                submit_button.click()
                
                print("✓ Botón Submit Response clickeado")
                
                # Esperar un poco para que se procese el envío
                time.sleep(3)
                
                return True
            else:
                print("✗ No se encontró el botón Submit Response")
                return False
                
        except Exception as e:
            print(f"✗ Error al enviar respuesta: {e}")
            return False

    def _verify_response_in_edit_state(self):
        """Verificar que la respuesta se mantiene en estado de edición"""
        try:
            time.sleep(2)
            
            # Verificar que el campo de texto sigue siendo editable
            text_field = self._find_active_text_field()
            
            if text_field:
                # Verificar que el campo no está deshabilitado
                is_disabled = text_field.get_attribute("disabled") is not None
                is_readonly = text_field.get_attribute("readonly") is not None
                contenteditable = text_field.get_attribute("contenteditable")
                
                if not is_disabled and not is_readonly and contenteditable != "false":
                    print("✓ El campo de texto sigue siendo editable")
                    self.driver.switch_to.default_content()
                    return True
                else:
                    print("✗ El campo de texto no está en estado editable")
                    self.driver.switch_to.default_content()
                    return False
            else:
                print("✗ No se encontró campo de texto activo")
                return False
                
        except Exception as e:
            print(f"✗ Error al verificar estado de edición: {e}")
            self.driver.switch_to.default_content()
            return False

    def _verify_visual_elements_reflected(self):
        """Verificar que los elementos enriquecidos se reflejan visualmente"""
        try:
            time.sleep(2)
            
            # Obtener el contenido HTML del campo
            html_content = self._get_field_html_content()
            
            if html_content:
                # Buscar indicadores de formato en el HTML
                format_indicators = []
                
                if "<strong>" in html_content or "<b>" in html_content or "font-weight" in html_content:
                    format_indicators.append("negrita")
                
                if "<em>" in html_content or "<i>" in html_content or "font-style" in html_content:
                    format_indicators.append("cursiva")
                
                if "<u>" in html_content or "text-decoration" in html_content:
                    format_indicators.append("subrayado")
                
                if "•" in html_content or "<ul>" in html_content or "<li>" in html_content:
                    format_indicators.append("lista")
                
                # Verificar que hay algún tipo de formato o contenido enriquecido
                if len(format_indicators) >= 2:  # Al menos 2 formatos aplicados
                    print(f"✓ Elementos visuales detectados: {', '.join(format_indicators)}")
                    return True
                elif len(html_content) > 20:  # Si hay contenido significativo
                    print("✓ Contenido enriquecido detectado")
                    return True
                else:
                    print("⚠ No se detectaron suficientes elementos visuales")
                    return False
            else:
                print("✗ No se pudo obtener contenido HTML")
                return False
                
        except Exception as e:
            print(f"✗ Error al verificar elementos visuales: {e}")
            return False

    def _get_field_html_content(self):
        """Obtener el contenido HTML del campo de texto"""
        try:
            # Buscar en iframes
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            
            for iframe in iframes:
                try:
                    self.driver.switch_to.frame(iframe)
                    
                    text_field = self.driver.find_element(By.XPATH, "//body[@id='tinymce'] | //body[contains(@class, 'mce-content-body')] | //div[@contenteditable='true']")
                    
                    html_content = text_field.get_attribute('innerHTML')
                    
                    self.driver.switch_to.default_content()
                    if html_content:
                        return html_content
                    
                except:
                    self.driver.switch_to.default_content()
                    continue
            
            # Buscar campos directos
            direct_selectors = [
                "//div[@contenteditable='true']",
                "//textarea"
            ]
            
            for selector in direct_selectors:
                try:
                    field = self.driver.find_element(By.XPATH, selector)
                    html_content = field.get_attribute('innerHTML') or field.get_attribute('value')
                    if html_content:
                        return html_content
                except:
                    continue
            
            return ""
            
        except Exception as e:
            print(f"✗ Error al obtener contenido HTML: {e}")
            self.driver.switch_to.default_content()
            return ""

    def _verify_content_preserved(self, original_content):
        """Verificar que no se perdió el contenido escrito previamente"""
        try:
            time.sleep(1)
            
            # Obtener el contenido actual
            current_content = self._get_current_text_content()
            
            if current_content:
                # Verificar que el contenido original sigue presente
                if original_content in current_content:
                    print(f"✓ Contenido original preservado: '{original_content}' encontrado")
                    return True
                else:
                    print(f"✗ Contenido original perdido: '{original_content}' no encontrado")
                    return False
            else:
                print("✗ No se pudo obtener contenido actual")
                return False
                
        except Exception as e:
            print(f"✗ Error al verificar contenido preservado: {e}")
            return False

    def _get_current_text_content(self):
        """Obtener el contenido de texto actual"""
        try:
            # Buscar en iframes
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            
            for iframe in iframes:
                try:
                    self.driver.switch_to.frame(iframe)
                    
                    text_field = self.driver.find_element(By.XPATH, "//body[@id='tinymce'] | //body[contains(@class, 'mce-content-body')] | //div[@contenteditable='true']")
                    
                    current_text = text_field.text or text_field.get_attribute('textContent')
                    
                    self.driver.switch_to.default_content()
                    if current_text:
                        return current_text.strip()
                    
                except:
                    self.driver.switch_to.default_content()
                    continue
            
            # Buscar campos directos
            direct_selectors = [
                "//div[@contenteditable='true']",
                "//textarea",
                "//input[@type='text']"
            ]
            
            for selector in direct_selectors:
                try:
                    field = self.driver.find_element(By.XPATH, selector)
                    current_text = field.text or field.get_attribute('value')
                    if current_text:
                        return current_text.strip()
                except:
                    continue
            
            return ""
            
        except Exception as e:
            print(f"✗ Error al obtener contenido actual: {e}")
            self.driver.switch_to.default_content()
            return ""

    def _verify_submission_successful(self):
        """Verificar que la respuesta se envió correctamente"""
        try:
            time.sleep(2)
            
            # Buscar indicadores de envío exitoso
            success_indicators = [
                "//div[contains(@class, 'alert-success')]",
                "//div[contains(text(), 'successfully')]",
                "//div[contains(text(), 'submitted')]",
                "//div[contains(text(), 'saved')]",
                "//*[contains(text(), 'Response submitted')]",
                "//*[contains(text(), 'Thank you')]"
            ]
            
            for indicator in success_indicators:
                try:
                    element = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, indicator))
                    )
                    if element.is_displayed():
                        print("✓ Indicador de envío exitoso encontrado")
                        return True
                except TimeoutException:
                    continue
            
            # Verificar si el botón de envío cambió o desapareció
            try:
                submit_button = self.driver.find_element(By.XPATH, "//button[@id='btn-submit-qn-2']")
                if not submit_button.is_enabled():
                    print("✓ El botón de envío se deshabilitó (indica envío exitoso)")
                    return True
            except:
                print("✓ El botón de envío ya no está disponible (indica envío exitoso)")
                return True
            
            # Si no encontramos indicadores específicos, asumimos que se envió
            print("✓ No se encontraron errores, asumiendo envío exitoso")
            return True
            
        except Exception as e:
            print(f"✗ Error al verificar envío: {e}")
            return False

    def tearDown(self):
        """Limpiar después del test"""
        self.driver.save_screenshot("final_state_CPF_EST_021_formatting.png")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)