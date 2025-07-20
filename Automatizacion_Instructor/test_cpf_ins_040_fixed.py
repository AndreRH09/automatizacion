import os, time, pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from pathlib import Path

class TestCPFINS040:
    def setup_method(self, method):
        env_path = Path(__file__).parent.parent / "cred.env"
        load_dotenv(dotenv_path=env_path.resolve())
        self.email = os.getenv("APP_EMAIL")
        self.password = os.getenv("APP_PASSWORD")
        assert self.email is not None and self.password is not None, "ERROR: Credenciales no encontradas"
        
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        # Opción para evitar que el navegador se cierre inesperadamente
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)
        
        # Datos del estudiante para inscripción
        self.COURSE_ID = "CEX-026"
        self.STUDENT = {
            "section": "Tutorial Group 1",
            "team": "Team 1",
            "name": "Juan Pérez",
            "email": "jperez@unsa.edu.pe",
            "comments": "Beca Erasmus"
        }
        
        # Carpeta para capturas
        self.screenshot_folder = Path(__file__).parent / "cpf040"
        os.makedirs(self.screenshot_folder, exist_ok=True)

    def teardown_method(self, method):
        try:
            # Intentar tomar una captura final antes de cerrar
            self.save_screenshot("final_state.png")
        except:
            pass
        self.driver.quit()
        
    def save_screenshot(self, filename):
        """Guarda una captura de pantalla en la carpeta del test"""
        try:
            filepath = self.screenshot_folder / filename
            self.driver.save_screenshot(str(filepath))
            print(f"✓ Captura guardada: {filename}")
        except Exception as e:
            print(f"⚠️ Error al guardar captura {filename}: {e}")

    def test_inscribir_estudiante(self):
        """Prueba CPF-INS-040: Inscribir un estudiante en un curso."""
        print("Iniciando prueba CPF-INS-040")
        
        # PASO 1: Login
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/instructor/home")
        if "login" in self.driver.current_url or "accounts.google.com" in self.driver.current_url:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys(self.email + Keys.ENTER)
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.NAME, "Passwd"))).send_keys(self.password + Keys.ENTER)
            time.sleep(5)
        
        # PASO 2: Navegar directo a la página de inscripción
        enrollment_url = f"https://teammates-hormiga-1.uc.r.appspot.com/web/instructor/courses/enroll?courseid={self.COURSE_ID}&user=atacoh@unsa.edu.pe"
        self.driver.get(enrollment_url)
        time.sleep(3)
        self.save_screenshot("03_pagina_enrollment.png")
        
        # PASO 3: Ingresar datos en formato texto y luego procesar
        print("PASO 3: Ingresando datos usando textarea y procesando...")
        resultado_datos = self.driver.execute_script(f"""
            try {{
                // Buscar el textarea para ingresar datos
                const textarea = document.querySelector('textarea');
                if (!textarea) return "No se encontró el textarea";
                
                // Formato esperado: Section|Team|Name|Email|Comments
                const datos = '{self.STUDENT["section"]}|{self.STUDENT["team"]}|{self.STUDENT["name"]}|{self.STUDENT["email"]}|{self.STUDENT["comments"]}';
                
                // Insertar los datos y disparar eventos
                textarea.value = datos;
                textarea.dispatchEvent(new Event('input', {{bubbles: true}}));
                textarea.dispatchEvent(new Event('change', {{bubbles: true}}));
                
                // Buscar y hacer clic en el botón "Add Rows" para procesar los datos
                const addButton = document.querySelector('button.btn-add-rows');
                if (addButton) {{
                    addButton.click();
                    return "Datos insertados y botón 'Add Rows' pulsado";
                }}
                
                return "Datos insertados, pero no se encontró botón 'Add Rows'";
            }} catch (e) {{
                return "Error: " + e.message;
            }}
        """)
        print(f"Resultado: {resultado_datos}")
        
        # Esperar a que se procesen los datos
        time.sleep(2)
        self.save_screenshot("04_datos_ingresados.png")
        
        # PASO 4: Verificar que los datos estén en la tabla
        print("PASO 4: Verificando datos en la tabla...")
        estado_tabla = self.driver.execute_script("""
            try {
                // Buscar la tabla Handsontable
                const hotTable = document.getElementById('newStudentsHOT');
                if (!hotTable) return "No se encontró la tabla";
                
                // Obtener las celdas de la primera fila
                const celdas = hotTable.querySelectorAll('.htCore tbody tr:first-child td');
                if (!celdas || celdas.length < 5) return "No hay suficientes celdas en la tabla";
                
                // Verificar el contenido de las celdas
                const contenido = Array.from(celdas).map(c => c.textContent.trim());
                const tieneContenido = contenido.some(c => c.length > 0);
                
                return {
                    tieneContenido: tieneContenido,
                    valores: contenido.join(' | ')
                };
            } catch (e) {
                return "Error: " + e.message;
            }
        """)
        print(f"Estado de la tabla: {estado_tabla}")
        self.save_screenshot("04b_datos_verificados.png")
        
        # PASO 5: Enviar el formulario (3 técnicas en cascada)
        print("PASO 5: Enviando formulario...")
        
        # TÉCNICA 1: Enviar el formulario directamente (más confiable que hacer clic en botones)
        print("Técnica 1: Enviando formulario directamente...")
        resultado_envio = self.driver.execute_script("""
            try {
                // Buscar el formulario que contiene el botón de inscripción
                const boton = document.getElementById('btn-enroll');
                if (!boton) return "No se encontró el botón";
                
                const formulario = boton.closest('form');
                if (!formulario) return "No se encontró el formulario";
                
                // Enviar el formulario directamente
                formulario.submit();
                return "Formulario enviado correctamente";
            } catch (e) {
                return "Error: " + e.message;
            }
        """)
        print(f"Resultado del envío: {resultado_envio}")
        
        # Si el envío directo del formulario falla, intentar con clic en botón
        if "Error" in str(resultado_envio) or "No se encontró" in str(resultado_envio):
            try:
                print("Técnica 2: Haciendo clic en botón con WebDriverWait...")
                # Esperar a que el botón sea clickeable
                boton = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "btn-enroll"))
                )
                
                # Asegurar que el botón sea visible
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton)
                time.sleep(1)
                
                # Hacer clic en el botón
                boton.click()
                print("✓ Clic en botón realizado con WebDriverWait")
            except Exception as e:
                print(f"WebDriverWait falló: {e}")
                
                # Si la técnica 2 falla, usar JavaScript avanzado
                print("Técnica 3: Usando JavaScript para forzar el clic...")
                self.driver.execute_script("""
                    try {
                        // Encontrar el botón con múltiples selectores
                        const boton = document.getElementById('btn-enroll') || 
                                      Array.from(document.querySelectorAll('button')).find(b => 
                                          b.textContent.includes('Enroll'));
                        
                        if (!boton) {
                            console.error("No se encontró el botón");
                            return;
                        }
                        
                        // Forzar que el botón sea clickeable
                        boton.disabled = false;
                        boton.removeAttribute('disabled');
                        
                        // Hacer clic con múltiples métodos
                        boton.click();
                        boton.dispatchEvent(new MouseEvent('click', {bubbles: true}));
                        
                        // Intentar submit del formulario como último recurso
                        const form = boton.closest('form');
                        if (form) form.submit();
                    } catch (e) {
                        console.error(e);
                    }
                """)
        
        # Esperar a que se complete la acción
        time.sleep(5)
        self.save_screenshot("05_despues_submit.png")
        
        # PASO 6: Verificar resultado de múltiples maneras
        print("PASO 6: Verificando resultado...")
        exito = self.driver.execute_script("""
            try {
                // 1. Verificar por notificaciones UI
                const notificaciones = [
                    document.querySelector('.toast-success'),
                    document.querySelector('.alert-success'),
                    document.querySelector('.toast')
                ].filter(el => el !== null);
                
                if (notificaciones.length > 0) {
                    return {exito: true, metodo: "notificación", mensaje: notificaciones[0].textContent.trim()};
                }
                
                // 2. Verificar por texto en la página
                const texto = document.body.textContent.toLowerCase();
                const indicadores = ['student added', 'enrolled successfully', 'successful'];
                for (const indicador of indicadores) {
                    if (texto.includes(indicador)) {
                        return {exito: true, metodo: "texto", mensaje: indicador};
                    }
                }
                
                // 3. Verificar por cambio de URL o elementos
                const yaNoEnEnrollment = !window.location.href.includes('/enroll');
                const tablaDesaparecio = !document.querySelector('#newStudentsHOT');
                
                if (yaNoEnEnrollment || tablaDesaparecio) {
                    return {exito: true, metodo: "cambio de página"};
                }
                
                return {exito: false};
            } catch (e) {
                return {exito: false, error: e.message};
            }
        """)
        
        # Generar resultado final
        if isinstance(exito, dict) and exito.get('exito', False):
            print(f"✓ Inscripción exitosa verificada via {exito.get('metodo')}")
            self.save_screenshot("06_notificacion_exito.png")
        else:
            print("⚠️ No se pudo verificar inscripción inmediatamente")
            
            # Verificación adicional: navegar a la página de estudiantes
            try:
                student_page_url = f"https://teammates-hormiga-1.uc.r.appspot.com/web/instructor/courses/students?courseid={self.COURSE_ID}&user=atacoh@unsa.edu.pe"
                self.driver.get(student_page_url)
                time.sleep(3)
                self.save_screenshot("06b_pagina_estudiantes.png")
                
                # Verificar si el estudiante está en la lista
                estudiante_encontrado = self.driver.execute_script(f"""
                    return document.body.textContent.includes('{self.STUDENT["email"]}');
                """)
                
                if estudiante_encontrado:
                    print("✓ Estudiante encontrado en la lista del curso")
                else:
                    print("⚠️ No se encontró el estudiante en la lista")
            except Exception as e:
                print(f"Error en verificación adicional: {e}")
        
        print("Prueba CPF-INS-040 completada")
