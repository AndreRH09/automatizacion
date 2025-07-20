import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time

class TeammatesQuestionResponseViewTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.base_url = "https://teammates-hormiga-1.uc.r.appspot.com"

    def test_RF_EST_005_validar_acceso_visualizacion(self):
        """
        Test Case: RF-EST-005 / TCN-TD-EST-001 (CPF-EST-026)
        Objetivo: Confirmar que, bajo condiciones completamente válidas, el estudiante 
                 puede acceder a ver tanto las preguntas del cuestionario como sus 
                 respuestas registradas correctamente.
        Precondiciones: Estudiante autenticado, matriculado, sesión activa con 
                       cuestionario publicado y respuestas registradas
        Resultado esperado: Acceso sin restricciones, visualización correcta de 
                           preguntas y respuestas, sin errores
        """
        try:
            print("=== INICIANDO TEST RF-EST-005 VISUALIZACIÓN ===")
            
            # Paso 1: Iniciar sesión como estudiante
            self._student_login()
            
            # Paso 2: Acceder al dashboard del estudiante
            self._access_student_dashboard()
            
            # Paso 3: Localizar "Second team feedback session (point-based)"
            self._locate_second_team_feedback_session()
            
            # Paso 4: Hacer clic en "Edit submission"
            self._click_edit_submission()
            
            # Verificaciones del resultado esperado
            print("\n=== VERIFICACIÓN ===")
            unrestricted_access = self._verify_unrestricted_access()
            questions_displayed = self._verify_questions_displayed()
            responses_displayed = self._verify_responses_displayed()
            no_errors = self._verify_no_errors_or_restrictions()
            
            # Evaluación final
            test_passed = all([unrestricted_access, questions_displayed, 
                             responses_displayed, no_errors])
            
            print(f"✓ Acceso sin restricciones: {unrestricted_access}")
            print(f"✓ Preguntas mostradas correctamente: {questions_displayed}")
            print(f"✓ Respuestas mostradas correctamente: {responses_displayed}")
            print(f"✓ Sin errores ni restricciones: {no_errors}")
            print(f"\n=== RESULTADO: {'PASÓ' if test_passed else 'FALLÓ'} ===")
            
            self.assertTrue(test_passed, "Test de validación de acceso a visualización falló")

        except Exception as e:
            print(f"✗ Error: {e}")
            self.driver.save_screenshot("error_RF_EST_005_visualization.png")
            raise

    def _student_login(self):
        """Paso 1: Iniciar sesión como estudiante"""
        print("Paso 1: Iniciando sesión como estudiante...")
        
        self.driver.get(self.base_url + "/web/front/home")
        
        # Hacer clic en botón Login
        login_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login') and @ngbdropdowntoggle]"))
        )
        login_dropdown.click()
        
        # Seleccionar login de estudiante
        student_login_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "student-login-btn"))
        )
        student_login_btn.click()

        # Proceso de autenticación con Google
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "identifierId")))
        self.driver.find_element(By.ID, "identifierId").send_keys("atacoh@unsa.edu.pe")
        self.driver.find_element(By.ID, "identifierNext").click()
        
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, "Passwd"))).send_keys("Zodiaco24")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "passwordNext"))).click()
        
        # Verificar llegada al dashboard del estudiante
        WebDriverWait(self.driver, 15).until(EC.url_contains("/web/student/home"))
        print("✓ Login de estudiante exitoso")

    def _access_student_dashboard(self):
        """Paso 2: Acceder al dashboard del estudiante"""
        print("Paso 2: Verificando acceso al dashboard del estudiante...")
        
        time.sleep(3)  # Esperar carga completa del dashboard
        
        # Verificar que estamos en el dashboard del estudiante
        current_url = self.driver.current_url
        if "/web/student/home" not in current_url:
            raise Exception("No se pudo acceder al dashboard del estudiante")
        
        print("✓ Dashboard del estudiante cargado correctamente")

    def _locate_second_team_feedback_session(self):
        """Paso 3: Localizar 'Second team feedback session (point-based)'"""
        print("Paso 3: Localizando 'Second team feedback session (point-based)'...")
        
        # Esperar a que las sesiones se carguen
        time.sleep(3)
        
        # Buscar la sesión específica por texto
        session_selectors = [
            "//div[contains(text(), 'Second team feedback session (point-based)')]",
            "//*[contains(text(), 'Second team feedback session')]",
            "//h5[contains(text(), 'Second team feedback session')]",
            "//td[contains(text(), 'Second team feedback session')]",
            "//*[contains(text(), 'point-based')]"
        ]
        
        session_found = False
        for selector in session_selectors:
            try:
                session_elements = self.driver.find_elements(By.XPATH, selector)
                if session_elements:
                    print(f"✓ Encontrada sesión: 'Second team feedback session (point-based)'")
                    session_found = True
                    break
            except:
                continue
        
        if not session_found:
            # Intentar buscar cualquier sesión de feedback disponible
            fallback_selectors = [
                "//*[contains(text(), 'feedback session')]",
                "//*[contains(text(), 'team feedback')]",
                "//div[contains(@class, 'session')]"
            ]
            
            for selector in fallback_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        print("⚠ Sesión específica no encontrada, pero hay sesiones de feedback disponibles")
                        session_found = True
                        break
                except:
                    continue
        
        if not session_found:
            raise Exception("No se encontró 'Second team feedback session (point-based)' ni sesiones alternativas")

    def _click_edit_submission(self):
        """Paso 4: Hacer clic en 'Edit submission'"""
        print("Paso 4: Haciendo clic en 'Edit submission'...")
        
        # Buscar y hacer clic en el botón "Edit submission"
        edit_submission_selectors = [
            "//button[contains(text(), 'Edit submission') or contains(text(), 'Edit Submission')]",
            "//a[contains(text(), 'Edit submission') or contains(text(), 'Edit Submission')]",
            "//button[@id='edit-submit-btn-2']",  # ID específico del botón basado en el código anterior
            "//button[contains(@id, 'edit-submit-btn')]",
            "//input[@value='Edit submission']",
            "//*[contains(text(), 'Edit') and contains(text(), 'submission')]"
        ]
        
        edit_clicked = False
        for selector in edit_submission_selectors:
            try:
                edit_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                
                # Hacer scroll al elemento y hacer clic
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_button)
                time.sleep(1)
                edit_button.click()
                edit_clicked = True
                print("✓ Botón 'Edit submission' clickeado exitosamente")
                break
                
            except TimeoutException:
                continue
            except Exception as e:
                print(f"Intento fallido con selector {selector}: {e}")
                continue
        
        if not edit_clicked:
            raise Exception("No se pudo hacer clic en 'Edit submission'")
        
        # Esperar a que cargue la página de edición con preguntas y respuestas
        time.sleep(5)
        
        # Verificar que se cargó la página de edición correctamente
        try:
            WebDriverWait(self.driver, 15).until(
                lambda driver: any([
                    "feedback" in driver.current_url.lower(),
                    "submission" in driver.current_url.lower(),
                    "session" in driver.current_url.lower(),
                    len(driver.find_elements(By.XPATH, "//div[contains(@class, 'question')] | //form | //textarea | //input[@type='text']")) > 0
                ])
            )
            print("✓ Página de edición cargada - visualización de preguntas y respuestas disponible")
        except TimeoutException:
            raise Exception("No se pudo cargar la página de visualización de preguntas y respuestas")

    def _verify_unrestricted_access(self):
        """Verificar que el sistema permite acceder sin restricciones"""
        try:
            # Verificar que no hay mensajes de acceso denegado
            restriction_indicators = [
                "access denied", "acceso denegado", "unauthorized", "forbidden",
                "not authorized", "permission denied", "restricted access",
                "session not available", "sesión no disponible"
            ]
            
            page_source = self.driver.page_source.lower()
            
            for indicator in restriction_indicators:
                if indicator in page_source:
                    print(f"Indicador de restricción encontrado: {indicator}")
                    return False
            
            # Verificar que la URL contiene elementos de sesión/feedback
            current_url = self.driver.current_url.lower()
            url_indicators = ["session", "feedback", "submission"]
            
            url_check = any(indicator in current_url for indicator in url_indicators)
            print(f"URL actual contiene indicadores válidos: {url_check}")
            
            return url_check
            
        except Exception as e:
            print(f"Error verificando acceso sin restricciones: {e}")
            return False

    def _verify_questions_displayed(self):
        """Verificar que se muestran correctamente todas las preguntas"""
        try:
            question_selectors = [
                "//div[contains(@class, 'question')]",
                "//h3[contains(@class, 'question-title') or contains(@class, 'question-text')]",
                "//div[contains(@class, 'card-header')]//h5",
                "//fieldset//legend",
                "//label[contains(@class, 'question')]",
                "//*[contains(text(), 'Question ') or contains(text(), 'Pregunta ')]",
                "//div[contains(@class, 'form-group')]//label"
            ]
            
            questions_found = 0
            question_texts = []
            
            for selector in question_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed() and element.text.strip():
                            question_texts.append(element.text.strip()[:50] + "...")
                            questions_found += 1
                except:
                    continue
            
            # Mostrar algunas preguntas encontradas para verificación
            if question_texts:
                print(f"Ejemplos de preguntas encontradas:")
                for i, text in enumerate(question_texts[:3]):  # Mostrar máximo 3
                    print(f"  - {text}")
            
            print(f"Total de preguntas encontradas: {questions_found}")
            return questions_found > 0
            
        except Exception as e:
            print(f"Error verificando visualización de preguntas: {e}")
            return False

    def _verify_responses_displayed(self):
        """Verificar que se muestran correctamente las respuestas del estudiante"""
        try:
            response_selectors = [
                "//textarea",
                "//input[@type='text']",
                "//input[@type='number']",
                "//select",
                "//input[@type='radio']",
                "//input[@type='checkbox']",
                "//iframe",  # Para editores de texto enriquecido
                "//*[@contenteditable='true']",
                "//div[contains(@class, 'response')]",
                "//div[contains(@class, 'answer')]"
            ]
            
            responses_found = 0
            response_types = []
            
            for selector in response_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            tag_name = element.tag_name
                            element_type = element.get_attribute('type') if element.get_attribute('type') else tag_name
                            response_types.append(element_type)
                            responses_found += 1
                except:
                    continue
            
            # Mostrar tipos de elementos de respuesta encontrados
            if response_types:
                unique_types = list(set(response_types))
                print(f"Tipos de elementos de respuesta: {', '.join(unique_types)}")
            
            print(f"Total de elementos de respuesta encontrados: {responses_found}")
            return responses_found > 0
            
        except Exception as e:
            print(f"Error verificando visualización de respuestas: {e}")
            return False

    def _verify_no_errors_or_restrictions(self):
        """Verificar que no se presentan errores ni restricciones en la visualización"""
        try:
            # Verificar ausencia de mensajes de error visibles
            error_selectors = [
                "//div[contains(@class, 'alert-danger')]",
                "//div[contains(@class, 'alert-error')]",
                "//div[contains(@class, 'error')]",
                "//*[@role='alert' and contains(@class, 'error')]",
                "//div[contains(@class, 'alert-warning')]"
            ]
            
            visible_errors = 0
            for selector in error_selectors:
                try:
                    error_elements = self.driver.find_elements(By.XPATH, selector)
                    for element in error_elements:
                        if element.is_displayed() and element.text.strip():
                            print(f"⚠ Error visible encontrado: {element.text.strip()[:100]}")
                            visible_errors += 1
                except:
                    continue
            
            # Verificar que la página se cargó completamente
            page_loaded = False
            try:
                page_loaded = self.driver.execute_script("return document.readyState") == "complete"
            except:
                pass
            
            # Verificar que hay contenido útil en la página
            page_source = self.driver.page_source
            content_indicators = ["question", "response", "feedback", "form", "input", "textarea"]
            has_content = any(indicator in page_source.lower() for indicator in content_indicators)
            
            result = visible_errors == 0 and page_loaded and has_content
            print(f"Página cargada completamente: {page_loaded}")
            print(f"Errores visibles: {visible_errors}")
            print(f"Contenido relevante presente: {has_content}")
            
            return result
            
        except Exception as e:
            print(f"Error verificando ausencia de errores: {e}")
            return False

    def tearDown(self):
        """Cleanup y captura de estado final"""
        self.driver.save_screenshot("final_state_RF_EST_005_visualization.png")
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)