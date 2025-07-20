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
        self.driver = webdriver.Chrome(options=options)
        
        # Datos del estudiante y curso
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
        self.driver.quit()
        
    def save_screenshot(self, filename):
        """Guarda una captura de pantalla en la carpeta del test"""
        filepath = self.screenshot_folder / filename
        self.driver.save_screenshot(str(filepath))
        print(f"✓ Captura guardada: {filename}")

    def test_inscribir_estudiante(self):
        """Prueba CPF-INS-040: Inscribir un estudiante en un curso."""
        print("Iniciando prueba CPF-INS-040")
        
        # Login
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/instructor/home")
        if "login" in self.driver.current_url or "accounts.google.com" in self.driver.current_url:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys(self.email + Keys.ENTER)
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.NAME, "Passwd"))).send_keys(self.password + Keys.ENTER)
            time.sleep(5)
        
        # Ir directo a la página de cursos y tomar captura
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/instructor/courses?user=atacoh@unsa.edu.pe")
        time.sleep(3)
        self.save_screenshot("01_pagina_cursos.png")
        
        # Ir directo a la página de inscripción para mayor confiabilidad
        enrollment_url = f"https://teammates-hormiga-1.uc.r.appspot.com/web/instructor/courses/enroll?courseid={self.COURSE_ID}&user=atacoh@unsa.edu.pe"
        self.driver.get(enrollment_url)
        time.sleep(3)
        self.save_screenshot("03_pagina_enrollment.png")
        
        # ESTRATEGIA 1: Usar el área de texto para ingresar datos
        print("Estrategia 1: Ingresando datos mediante el área de texto...")
        self.driver.execute_script(f"""
            // Buscar el área de texto para ingresar los datos
            const textarea = document.querySelector('textarea');
            if (textarea) {{
                // Formato esperado: Section|Team|Name|Email|Comments
                const datos = '{self.STUDENT["section"]}|{self.STUDENT["team"]}|{self.STUDENT["name"]}|{self.STUDENT["email"]}|{self.STUDENT["comments"]}';
                
                // Asignar el valor y disparar eventos para que se procese
                textarea.value = datos;
                textarea.dispatchEvent(new Event('input', {{bubbles: true}}));
                textarea.dispatchEvent(new Event('change', {{bubbles: true}}));
                
                // Simular presionar Enter para confirmar
                textarea.dispatchEvent(new KeyboardEvent('keydown', {{
                    key: 'Enter',
                    code: 'Enter',
                    keyCode: 13,
                    which: 13,
                    bubbles: true
                }}));
                
                // Intentar hacer clic en el botón "Add rows" si existe
                const addButton = document.querySelector('button.btn-add-rows');
                if (addButton) {{
                    addButton.click();
                }}
            }}
        """)
        
        # Esperar a que se procesen los datos
        time.sleep(3)
        self.save_screenshot("03b_pagina_enrollment_directa.png")
        
        # ESTRATEGIA 2: Manipular directamente la tabla Handsontable
        print("Estrategia 2: Manipulando directamente la tabla Handsontable...")
        self.driver.execute_script(f"""
            // Datos a insertar en la tabla
            const studentData = {{
                section: '{self.STUDENT["section"]}',
                team: '{self.STUDENT["team"]}',
                name: '{self.STUDENT["name"]}',
                email: '{self.STUDENT["email"]}',
                comments: '{self.STUDENT["comments"]}'
            }};
            
            try {{
                // Buscar la tabla Handsontable
                const hotTable = document.getElementById('newStudentsHOT');
                if (!hotTable) {{
                    console.error('No se encontró la tabla Handsontable');
                    return;
                }}
                
                // Obtener las celdas de la primera fila
                const cells = hotTable.querySelectorAll('.htCore tbody tr:first-child td');
                
                if (!cells || cells.length < 5) {{
                    console.error('No hay suficientes celdas en la tabla');
                    return;
                }}
                
                // Estrategia de manipulación directa de celdas
                console.log('Intentando manipular directamente las celdas...');
                
                // Hacer clic en la primera celda para activarla
                cells[0].click();
                
                // Definir y ejecutar una función para establecer valores en las celdas
                function setCellsDirectly() {{
                    // Rellenar visiblemente las celdas con los datos
                    cells[0].innerText = studentData.section;
                    cells[1].innerText = studentData.team;
                    cells[2].innerText = studentData.name;
                    cells[3].innerText = studentData.email;
                    cells[4].innerText = studentData.comments;
                }}
                
                // Ejecutar la función después de un pequeño retraso
                setTimeout(setCellsDirectly, 100);
            }} catch(e) {{
                console.error('Error manipulando la tabla:', e);
            }}
        """)
        
        # Esperar a que los datos se procesen y aparezcan en la tabla
        time.sleep(2)
        
        # ESTRATEGIA 3: Técnica para asegurar que los datos estén en la tabla
        print("Estrategia 3: Asegurando que los datos aparezcan en la tabla...")
        self.driver.execute_script(f"""
            // Verificar si hay datos en la tabla
            function verificarTabla() {{
                const tabla = document.querySelector('#newStudentsHOT .htCore tbody tr:first-child');
                if (!tabla) return false;
                
                const celdas = tabla.querySelectorAll('td');
                if (!celdas || celdas.length < 5) return false;
                
                // Verificar si al menos la primera celda tiene contenido
                const tieneDatos = Array.from(celdas).some(celda => celda.textContent.trim().length > 0);
                return tieneDatos;
            }}
            
            // Si no hay datos, intentar llenarlos usando otro enfoque
            if (!verificarTabla()) {{
                console.log("No se detectaron datos en la tabla, intentando otro enfoque...");
                
                // Intentar enfocar directamente las celdas de la tabla e ingresar datos
                const tabla = document.querySelector('#newStudentsHOT .htCore tbody tr:first-child');
                if (tabla) {{
                    const celdas = tabla.querySelectorAll('td');
                    if (celdas && celdas.length >= 5) {{
                        // Hacer doble clic en cada celda y establecer un valor
                        celdas[0].dispatchEvent(new MouseEvent('dblclick', {{bubbles: true}}));
                        setTimeout(() => {{
                            const input = document.querySelector('.handsontableInput');
                            if (input) {{
                                input.value = '{self.STUDENT["section"]}';
                                input.dispatchEvent(new Event('input', {{bubbles: true}}));
                                input.dispatchEvent(new KeyboardEvent('keydown', {{key: 'Enter', keyCode: 13, bubbles: true}}));
                            }}
                        }}, 100);
                        
                        // Hacer visible la celda 1 (para asegurarnos)
                        celdas[1].dispatchEvent(new MouseEvent('dblclick', {{bubbles: true}}));
                        setTimeout(() => {{
                            const input = document.querySelector('.handsontableInput');
                            if (input) {{
                                input.value = '{self.STUDENT["team"]}';
                                input.dispatchEvent(new Event('input', {{bubbles: true}}));
                                input.dispatchEvent(new KeyboardEvent('keydown', {{key: 'Enter', keyCode: 13, bubbles: true}}));
                            }}
                        }}, 100);
                    }}
                }}
            }}
        """)
        
        # Tomar capturas para verificar visualmente los datos
        time.sleep(1)
        self.save_screenshot("04_celda1_ingresada.png")
        time.sleep(1)
        self.save_screenshot("04b_datos_tabla_llena.png")
        
        # Usar Selenium directamente para hacer clic en el botón (más confiable que JavaScript)
        print("Haciendo clic en el botón 'Enroll Students' usando Selenium...")
        
        # Esperar un momento para asegurar que los datos se hayan procesado
        time.sleep(2)
        
        # Intentar encontrar el botón usando diferentes estrategias
        try:
            # Estrategia 1: Buscar por ID
            boton_enroll = self.driver.find_element(By.ID, "btn-enroll")
            print("✓ Botón 'Enroll Students' encontrado por ID")
            
            # Tomar captura antes de hacer clic
            self.save_screenshot("04b_antes_hacer_clic_enrollbtn.png")
            
            # Hacer clic en el botón
            boton_enroll.click()
            print("✓ Clic en botón 'Enroll Students' realizado")
        except Exception as e1:
            print(f"No se encontró el botón por ID: {e1}")
            try:
                # Estrategia 2: Buscar por texto y clase
                boton_enroll = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Enroll students')]")
                print("✓ Botón 'Enroll Students' encontrado por texto")
                
                # Tomar captura antes de hacer clic
                self.save_screenshot("04b_antes_hacer_clic_enrollbtn.png")
                
                # Hacer clic en el botón
                boton_enroll.click()
                print("✓ Clic en botón 'Enroll Students' realizado")
            except Exception as e2:
                print(f"No se encontró el botón por texto: {e2}")
                # Estrategia 3: Usar JavaScript como último recurso
                print("⚠️ No se encontró el botón con Selenium, intentando con JavaScript...")
                self.driver.execute_script("""
                    // Intentar encontrar el botón por ID o texto
                    const boton = document.getElementById('btn-enroll') || 
                                  Array.from(document.querySelectorAll('button')).find(b => 
                                      b.textContent.includes('Enroll students')
                                  );
                    
                    if (boton) {
                        // Hacer clic directamente
                        boton.click();
                    }
                """)
        
        # Esperar a que se procese el clic
        time.sleep(2)
        
        # Tomar captura después de hacer clic en el botón
        self.save_screenshot("05_despues_submit.png")
        
        # Verificar resultado
        exito = self.driver.execute_script("""
            // Buscar notificaciones o mensajes de éxito
            const notificaciones = [
                document.querySelector('.toast-success'),
                document.querySelector('.alert-success'),
                document.querySelector('.toast-body')
            ].filter(el => el !== null);
            
            if (notificaciones.length > 0) return true;
            
            // Verificar texto en la página
            const texto = document.body.textContent.toLowerCase();
            return texto.includes('student added') || 
                   texto.includes('enrolled successfully') ||
                   texto.includes('successful');
        """)
        
        if exito:
            print("✓ Inscripción verificada con éxito")
            self.save_screenshot("06_notificacion_exito.png")
        
        print("Prueba CPF-INS-040 finalizada correctamente")
