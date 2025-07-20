import os, time, pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from pathlib import Path

class TestCPFINS042:
    def setup_method(self, method):
        env_path = Path(__file__).parent.parent / "cred.env"
        load_dotenv(dotenv_path=env_path.resolve())
        self.email = os.getenv("APP_EMAIL")
        self.password = os.getenv("APP_PASSWORD")
        assert self.email is not None and self.password is not None, "ERROR: Credenciales no encontradas"
        
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        
        # Constantes para la prueba
        self.COURSE_ID = "CEX-026"
        self.INSTRUCTOR = {
            "name": "%%masdi",  # Nombre inválido que comienza con caracteres no alfanuméricos
            "email": "maria.perez@unsa.edu.pe",
            "role": "Manager"  # Co-owner, Manager, Observer, Tutor, Custom
        }
        
        # IDs específicos de los campos del formulario
        self.FIELD_IDS = {
            "name": "name-instructor-3",
            "email": "email-instructor-3",
            "accessLevels": "access-levels-instructor-3",
            "roleManager": "INSTRUCTOR_PERMISSION_ROLE_MANAGER21"
        }
        
        # Carpeta para capturas
        self.screenshot_folder = Path(__file__).parent / "cpf042"
        os.makedirs(self.screenshot_folder, exist_ok=True)

    def teardown_method(self, method):
        self.driver.quit()
        
    def save_screenshot(self, filename):
        """Guarda una captura de pantalla en la carpeta del test"""
        filepath = self.screenshot_folder / filename
        self.driver.save_screenshot(str(filepath))
        print(f"✓ Captura guardada: {filename}")

    def test_validar_campo_name_instructor(self):
        """Prueba CPF-INS-042: Validación de campo Name al crear un instructor individual."""
        print("Iniciando prueba CPF-INS-042: Validación de campo Name al crear un instructor individual")
        
        # PASO 1: Login como instructor
        print("PASO 1: Iniciando sesión como instructor...")
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/instructor/home")
        if "login" in self.driver.current_url or "accounts.google.com" in self.driver.current_url:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys(self.email + Keys.ENTER)
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.NAME, "Passwd"))).send_keys(self.password + Keys.ENTER)
            time.sleep(5)
        
        # PASO 2: Navegar directamente a la página de edición de curso
        print("PASO 2: Navegando a la página de edición de curso...")
        edit_url = f"https://teammates-hormiga-1.uc.r.appspot.com/web/instructor/courses/edit?courseid={self.COURSE_ID}&user=atacoh@unsa.edu.pe"
        self.driver.get(edit_url)
        time.sleep(3)
        self.save_screenshot("01_pagina_edicion.png")
        
        # PASO 3: Hacer clic en el botón "Add New Instructor"
        print("PASO 3: Haciendo clic en 'Add New Instructor'...")
        try:
            # Esperar a que el botón sea visible y clickeable
            add_instructor_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btn-add-instructor"))
            )
            self.save_screenshot("02_antes_agregar_instructor.png")
            
            # Hacer clic en el botón
            add_instructor_btn.click()
            print("✓ Botón 'Add New Instructor' encontrado y clickeado")
        except Exception as e:
            print(f"Error al encontrar o hacer clic en el botón: {e}")
            # Intentar con JavaScript como respaldo
            self.driver.execute_script("""
                const addBtn = document.getElementById('btn-add-instructor') || 
                              Array.from(document.querySelectorAll('button')).find(b => 
                                b.textContent.includes('Add New Instructor')
                              );
                
                if (addBtn) {
                    addBtn.click();
                    console.log('Botón encontrado y clickeado con JavaScript');
                }
            """)
        
        time.sleep(2)
        self.save_screenshot("03_despues_click_agregar.png")
        
        # PASO 4: Llenar el formulario con datos incluyendo un nombre inválido (con %)
        print(f"PASO 4: Llenando formulario con nombre inválido: {self.INSTRUCTOR['name']}...")
        
        form_fill_result = self.driver.execute_script(f"""
            try {{
                // 1. Llenar campo de nombre con valor inválido
                const nameField = document.getElementById('{self.FIELD_IDS["name"]}');
                if (!nameField) return "No se encontró el campo de nombre";
                
                nameField.value = "{self.INSTRUCTOR['name']}";
                nameField.dispatchEvent(new Event('input', {{bubbles: true}}));
                nameField.dispatchEvent(new Event('change', {{bubbles: true}}));
                
                // 2. Llenar campo de email
                const emailField = document.getElementById('{self.FIELD_IDS["email"]}');
                if (!emailField) return "No se encontró el campo de email";
                
                emailField.value = "{self.INSTRUCTOR['email']}";
                emailField.dispatchEvent(new Event('input', {{bubbles: true}}));
                emailField.dispatchEvent(new Event('change', {{bubbles: true}}));
                
                // 3. Seleccionar rol de acceso Manager
                const accessContainer = document.getElementById('{self.FIELD_IDS["accessLevels"]}');
                if (!accessContainer) return "No se encontró el contenedor de niveles de acceso";
                
                const managerRadio = document.getElementById('{self.FIELD_IDS["roleManager"]}');
                if (managerRadio) {{
                    managerRadio.checked = true;
                    managerRadio.dispatchEvent(new Event('change', {{bubbles: true}}));
                }} else {{
                    // Intento alternativo: buscar por texto
                    const allRadios = accessContainer.querySelectorAll('input[type="radio"]');
                    let roleFound = false;
                    
                    for (const radio of allRadios) {{
                        const label = radio.closest('label');
                        if (label && label.textContent.includes('Manager')) {{
                            radio.checked = true;
                            radio.dispatchEvent(new Event('change', {{bubbles: true}}));
                            roleFound = true;
                            break;
                        }}
                    }}
                    
                    if (!roleFound) return "No se pudo seleccionar el rol Manager";
                }}
                
                return "Formulario llenado correctamente";
            }} catch (e) {{
                return "Error: " + e.message;
            }}
        """)
        
        print(f"Resultado de llenar formulario: {form_fill_result}")
        self.save_screenshot("04_campos_formulario.png")
        
        # PASO 5: Hacer clic en el botón "Add Instructor"
        print("PASO 5: Haciendo clic en el botón 'Add Instructor'...")
        
        try:
            # Buscar el botón con espera explícita
            add_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Instructor')]"))
            )
            # Asegurar que el botón sea visible
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_btn)
            time.sleep(1)
            
            # Hacer clic en el botón
            add_btn.click()
            print("✓ Clic en botón 'Add Instructor' realizado")
        except Exception as e:
            print(f"Error al hacer clic en el botón 'Add Instructor' con Selenium: {e}")
            
            # Intentar con JavaScript como respaldo
            self.driver.execute_script("""
                const addBtn = Array.from(document.querySelectorAll('button')).find(btn => 
                    btn.textContent.includes('Add Instructor')
                );
                
                if (addBtn) {
                    addBtn.scrollIntoView({block: 'center'});
                    addBtn.click();
                }
            """)
            print("Intento de clic realizado con JavaScript")
        
        # Esperar a que aparezca el mensaje de error
        time.sleep(3)
        self.save_screenshot("error_validacion_fallida.png")
        
        # PASO 6: Verificar el mensaje de error
        print("PASO 6: Verificando mensaje de error...")
        
        # Mensaje de error exacto para nombre que comienza con '%'
        expected_error = '"%%masdi" is not acceptable to TEAMMATES as a/an person name because it starts with a non-alphanumeric character. A/An person name must start with an alphanumeric character, and cannot contain any vertical bar (|) or percent sign (%).'
        
        error_message = self.driver.execute_script("""
            try {
                // Buscar mensaje de error en diferentes elementos
                const errorElements = [
                    document.querySelector('.alert-danger'),
                    document.querySelector('.toast-error'),
                    document.querySelector('.text-danger'),
                    document.querySelector('[role="alert"]'),
                    // También buscar por los elementos que contienen el mensaje de validación
                    Array.from(document.querySelectorAll('.ng-star-inserted')).find(el => 
                        el.textContent.includes('not acceptable') && 
                        (el.textContent.includes('percent sign') || el.textContent.includes('non-alphanumeric character'))
                    )
                ].filter(el => el !== null);
                
                if (errorElements.length > 0) {
                    return {
                        found: true,
                        message: errorElements[0].textContent.trim(),
                        elementType: errorElements[0].tagName
                    };
                }
                
                // Buscar en todo el texto de la página para mayor seguridad
                const pageText = document.body.textContent;
                
                // Buscar por patrones de texto que se incluyen en el mensaje de error
                const errorPatterns = [
                    'is not acceptable to TEAMMATES as a/an person name',
                    'starts with a non-alphanumeric character',
                    'must start with an alphanumeric character',
                    'cannot contain any vertical bar (|) or percent sign (%)'
                ];
                
                // Verificar si al menos 2 patrones están presentes en la página
                const matchingPatterns = errorPatterns.filter(pattern => pageText.includes(pattern));
                if (matchingPatterns.length >= 2) {
                    return {
                        found: true,
                        message: pageText.substring(pageText.indexOf(matchingPatterns[0]), pageText.indexOf(matchingPatterns[0]) + 200), // Extraer aproximadamente el mensaje
                        fullPageSearch: true
                    };
                }
                
                return {
                    found: false,
                    message: "No se encontró mensaje de error"
                };
            } catch (e) {
                return {
                    found: false,
                    error: e.message
                };
            }
        """)
        
        # PASO 7: Mostrar resultados de la validación
        print("\n=== RESULTADO DE LA VALIDACIÓN ===")
        
        # Patrones clave que deben estar en el mensaje de error
        error_patterns = [
            'not acceptable to TEAMMATES',
            'person name',
            'alphanumeric character',
            'percent sign (%)'
        ]
        
        if isinstance(error_message, dict) and error_message.get('found', False):
            print("✓ Mensaje de error encontrado:")
            print(f"  - Elemento: {error_message.get('elementType', 'N/A')}")
            if error_message.get('message'):
                print(f"  - Mensaje: {error_message.get('message')}")
                
            print("\n- VERIFICACIÓN DEL MENSAJE DE ERROR -")
            error_msg = error_message.get('message', '')
            
            # Verificar que el mensaje contiene las partes esenciales
            matching_patterns = [pattern for pattern in error_patterns if pattern in error_msg]
            if len(matching_patterns) >= 2:  # Al menos 2 patrones deben coincidir
                print("✓ El mensaje de error es correcto")
                print("✓ Prueba EXITOSA: Se validó correctamente el campo Name")
                
                # Destacar las partes encontradas
                for pattern in matching_patterns:
                    print(f"  - Encontrado: '{pattern}'")
            else:
                print("❌ El mensaje de error no contiene la información esperada")
                print("Esperado: mensaje con patrones sobre nombre no aceptable y caracteres inválidos")
                print(f"Actual: {error_msg}")
                
                # Mostrar qué patrones faltan
                missing_patterns = [pattern for pattern in error_patterns if pattern not in error_msg]
                for pattern in missing_patterns:
                    print(f"  - Falta: '{pattern}'")
        else:
            print("❌ No se encontró mensaje de error")
            print("  - La validación del campo Name ha fallado")
        
        print("=== FIN DE LA PRUEBA ===")
        
        # Verificación final (assertion)
        if isinstance(error_message, dict):
            assert error_message.get('found', False), "No se encontró mensaje de error para el nombre inválido"
            
            if error_message.get('message'):
                error_msg = error_message.get('message', '')
                # Verificar que al menos 2 patrones clave estén presentes en el mensaje
                matching_patterns = [pattern for pattern in error_patterns if pattern in error_msg]
                assert len(matching_patterns) >= 2, "El mensaje de error no contiene suficientes partes del mensaje esperado"
        
        print("Prueba CPF-INS-042 finalizada correctamente")
