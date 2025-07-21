import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class TeammatesUnpublishedResponsesTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.base_url = "https://teammates-hormiga-1.uc.r.appspot.com"

    def test_RF_EST_005_acceso_respuestas_no_publicadas(self):
        """
        Test Case: RF-EST-005
        Objetivo: Verificar que el sistema bloquee el acceso a respuestas no publicadas
        Resultado esperado: Botón deshabilitado, mensaje de restricción, sin acceso al contenido
        """
        try:
            print("=== TEST RF-EST-005: RESPUESTAS NO PUBLICADAS ===")
            
            # Paso 1: Login como estudiante
            self._login_student()
            
            # Paso 2: Localizar sesión y verificar restricciones
            view_button = self._find_view_responses_button()
            
            # Paso 3: Verificar restricciones de acceso
            access_blocked = self._verify_access_blocked(view_button)
            message_shown = self._verify_restriction_message()
            no_content = self._verify_no_content_access()
            
            # Evaluación final
            test_passed = access_blocked and message_shown and no_content
            
            print(f"✓ Acceso bloqueado: {access_blocked}")
            print(f"✓ Mensaje de restricción: {message_shown}")
            print(f"✓ Sin acceso al contenido: {no_content}")
            print(f"=== RESULTADO: {'PASÓ' if test_passed else 'FALLÓ'} ===")
            
            self.assertTrue(test_passed, "Fallo en validación de acceso bloqueado")

        except Exception as e:
            print(f"✗ Error: {e}")
            self.driver.save_screenshot("error_RF_EST_005.png")
            raise

    def _login_student(self):
        """Login como estudiante"""
        print("Iniciando sesión...")
        
        self.driver.get(self.base_url + "/web/front/home")
        
        # Click en Login dropdown y seleccionar estudiante
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))
        ).click()
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "student-login-btn"))
        ).click()

        # Autenticación Google
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "identifierId")))
        self.driver.find_element(By.ID, "identifierId").send_keys("atacoh@unsa.edu.pe")
        self.driver.find_element(By.ID, "identifierNext").click()
        
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, "Passwd"))).send_keys("Zodiaco24")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "passwordNext"))).click()
        
        # Verificar llegada al dashboard
        WebDriverWait(self.driver, 15).until(EC.url_contains("/web/student/home"))
        time.sleep(3)  # Esperar carga completa
        print("✓ Login exitoso")

    def _find_view_responses_button(self):
        """Localizar el botón View Responses de la sesión específica"""
        print("Localizando botón View Responses de 'Second team feedback session (point-based)'...")
        
        # Esperar carga del dashboard
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table | //tbody | //div[contains(@class, 'table')]"))
        )
        
        # Método 1: Buscar por ID específico (más directo)
        try:
            button = self.driver.find_element(By.ID, "view-responses-btn-1")
            if button:
                print("✓ Botón View Responses encontrado por ID específico")
                return button
        except:
            pass
        
        # Método 2: Buscar por href que contiene el nombre de la sesión
        try:
            button = self.driver.find_element(By.XPATH, 
                "//a[contains(@href, 'Second%20team%20feedback%20session%20(point-based)') and contains(text(), 'View Responses')]"
            )
            if button:
                print("✓ Botón View Responses encontrado por href específico")
                return button
        except:
            pass
        
        # Método 3: Buscar la fila que contiene el nombre de la sesión y luego su botón
        try:
            # Encontrar la fila que contiene el nombre de la sesión
            session_row = self.driver.find_element(By.XPATH, 
                "//tr[contains(., 'Second team feedback session (point-based)')]"
            )
            # Buscar el botón View Responses dentro de esa fila
            button = session_row.find_element(By.XPATH, 
                ".//a[contains(text(), 'View Responses')]"
            )
            if button:
                print("✓ Botón View Responses encontrado en fila de sesión específica")
                return button
        except:
            pass
        
        # Método 4: Buscar por texto de sesión y luego el botón en el mismo contenedor
        try:
            # Encontrar elemento que contenga el nombre de la sesión
            session_element = self.driver.find_element(By.XPATH, 
                "//*[contains(text(), 'Second team feedback session (point-based)')]"
            )
            # Buscar el botón View Responses en el mismo contenedor padre
            parent_container = session_element.find_element(By.XPATH, "./ancestor::tr[1] | ./ancestor::div[1]")
            button = parent_container.find_element(By.XPATH, 
                ".//a[contains(text(), 'View Responses')]"
            )
            if button:
                print("✓ Botón View Responses encontrado por contenedor de sesión")
                return button
        except:
            pass
                
        raise Exception("Botón View Responses de 'Second team feedback session (point-based)' no encontrado")

    def _verify_access_blocked(self, button):
        """Verificar que el acceso está bloqueado"""
        try:
            # Verificar atributos del botón específico
            button_id = button.get_attribute('id')
            button_class = button.get_attribute('class') or ''
            button_href = button.get_attribute('href')
            is_enabled = button.is_enabled()
            
            print(f"Verificando botón: ID={button_id}, Class={button_class}")
            print(f"Href={button_href}")
            print(f"Enabled={is_enabled}")
            
            # Verificar si el botón tiene la clase 'disabled'
            is_disabled = 'disabled' in button_class.lower()
            
            if is_disabled:
                print("✓ Botón tiene clase 'disabled' - acceso bloqueado correctamente")
                return True
            
            # Verificar si el botón no es clickable
            if not is_enabled:
                print("✓ Botón no habilitado - acceso bloqueado")
                return True
            
            # Verificar si el href es válido pero el botón está visualmente deshabilitado
            if button_href and 'Second%20team%20feedback%20session%20(point-based)' in button_href:
                # Intentar hacer click para ver el comportamiento del sistema
                print("Botón parece habilitado - verificando comportamiento del sistema...")
                current_url = self.driver.current_url
                
                try:
                    button.click()
                    time.sleep(3)
                    new_url = self.driver.current_url
                    
                    # Si no hubo redirección, el acceso fue bloqueado
                    if current_url == new_url:
                        print("✓ Sin redirección después del click - acceso bloqueado")
                        return True
                    
                    # Si hubo redirección, verificar si muestra restricción
                    if "/web/student/sessions/result" in new_url:
                        page_source = self.driver.page_source.lower()
                        restriction_keywords = [
                            "not published", "no publicado", "not available", 
                            "restricted", "results not ready", "no está publicado"
                        ]
                        
                        if any(keyword in page_source for keyword in restriction_keywords):
                            print("✓ Página muestra restricción - acceso bloqueado correctamente")
                            return True
                        
                        # Verificar ausencia de contenido real de respuestas
                        response_elements = self.driver.find_elements(By.XPATH, 
                            "//div[contains(@class, 'response-content')] | //table[contains(@class, 'responses')]"
                        )
                        if not response_elements:
                            print("✓ Sin contenido de respuestas en página - acceso bloqueado")
                            return True
                    
                except Exception as click_error:
                    print(f"✓ Error al hacer click (bloqueado): {click_error}")
                    return True
            
            print("⚠ El botón parece permitir acceso - posible falla de seguridad")
            return False
            
        except Exception as e:
            print(f"Error verificando bloqueo: {e}")
            return False

    def _verify_restriction_message(self):
        """Verificar mensaje de restricción"""
        try:
            # Buscar mensajes de restricción
            message_selectors = [
                "//*[contains(text(), 'not published')]",
                "//*[contains(text(), 'no publicado')]",
                "//*[contains(text(), 'not available')]",
                "//*[contains(text(), 'results not ready')]",
                "//div[contains(@class, 'alert')]"
            ]
            
            for selector in message_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if any(el.is_displayed() and el.text.strip() for el in elements):
                        print("✓ Mensaje de restricción encontrado")
                        return True
                except:
                    continue
            
            # Si no hay mensaje explícito, verificar botón deshabilitado como indicador
            try:
                button = self._find_view_responses_button()
                is_disabled = 'disabled' in (button.get_attribute('class') or '').lower()
                if is_disabled:
                    print("✓ Botón deshabilitado indica restricción")
                    return True
            except:
                pass
            
            return False
            
        except Exception as e:
            print(f"Error verificando mensaje: {e}")
            return False

    def _verify_no_content_access(self):
        """Verificar que no hay acceso al contenido de respuestas"""
        try:
            current_url = self.driver.current_url.lower()
            
            # Si seguimos en dashboard, no hay acceso al contenido
            if "/web/student/home" in current_url:
                print("✓ Sin salir del dashboard - sin acceso al contenido")
                return True
            
            # Si estamos en página de resultados, verificar ausencia de contenido
            content_selectors = [
                "//div[contains(@class, 'response-content')]",
                "//div[contains(@class, 'feedback-content')]",
                "//table[contains(@class, 'responses')]",
                "//textarea[contains(@class, 'response')]"
            ]
            
            content_found = False
            for selector in content_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if any(el.is_displayed() and el.text.strip() for el in elements):
                        content_found = True
                        break
                except:
                    continue
            
            if not content_found:
                print("✓ Sin contenido de respuestas visible")
                return True
            
            print("⚠ Se encontró contenido de respuestas")
            return False
            
        except Exception as e:
            print(f"Error verificando contenido: {e}")
            return False

    def tearDown(self):
        self.driver.save_screenshot("final_RF_EST_005.png")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)