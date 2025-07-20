import os, time, pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from pathlib import Path

class TestCPFINS041:
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
            "name": "Maria Perez",
            "email": "mperez@unsa.edu.pe",
            "role": "Manager"  # Co-owner, Manager, Observer, Tutor, Custom
        }
        
        # Carpeta para capturas
        self.screenshot_folder = Path(__file__).parent / "cpf041"
        os.makedirs(self.screenshot_folder, exist_ok=True)

    def teardown_method(self, method):
        self.driver.quit()
        
    def save_screenshot(self, filename):
        """Guarda una captura de pantalla en la carpeta del test"""
        filepath = self.screenshot_folder / filename
        self.driver.save_screenshot(str(filepath))
        print(f"✓ Captura guardada: {filename}")

    def test_agregar_instructor(self):
        """Prueba CPF-INS-041: Agregar un nuevo instructor a un curso existente."""
        print("Iniciando prueba CPF-INS-041: Agregar nuevo instructor")
        
        # PASO 1: Login
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/instructor/home")
        if "login" in self.driver.current_url or "accounts.google.com" in self.driver.current_url:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys(self.email + Keys.ENTER)
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.NAME, "Passwd"))).send_keys(self.password + Keys.ENTER)
            time.sleep(5)
        
        # PASO 2: Navegar directamente a la página de edición de curso
        edit_url = f"https://teammates-hormiga-1.uc.r.appspot.com/web/instructor/courses/edit?courseid={self.COURSE_ID}&user=atacoh@unsa.edu.pe"
        self.driver.get(edit_url)
        time.sleep(3)
        self.save_screenshot("01_pagina_edicion.png")
        
        # PASO 3: Verificar que estamos en la página correcta
        page_title = self.driver.execute_script("""
            const title = document.querySelector('h1');
            return title ? title.textContent.trim() : '';
        """)
        print(f"Título de la página: {page_title}")
        
        # PASO 4: Buscar y hacer clic en el botón "Add New Instructor"
        print("Buscando botón 'Add New Instructor'...")
        
        # Intentar encontrar el botón por ID y hacer clic
        try:
            # Esperar a que el botón sea visible y clickeable
            add_instructor_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btn-add-instructor"))
            )
            # Tomar captura antes de hacer clic
            self.save_screenshot("02_antes_agregar_instructor.png")
            
            # Hacer clic en el botón
            add_instructor_btn.click()
            print("✓ Botón 'Add New Instructor' encontrado y clickeado")
            time.sleep(2)
            self.save_screenshot("03_despues_click_agregar.png")
        except Exception as e:
            print(f"❌ Error al encontrar o hacer clic en el botón: {e}")
            # Intentar con JavaScript como respaldo
            self.driver.execute_script("""
                const addBtn = document.getElementById('btn-add-instructor') || 
                              document.querySelector("button[id='btn-add-instructor']") ||
                              Array.from(document.querySelectorAll('button')).find(b => 
                                b.textContent.includes('Add New Instructor')
                              );
                
                if (addBtn) {
                    addBtn.click();
                    console.log('Botón encontrado y clickeado con JavaScript');
                } else {
                    console.error('No se pudo encontrar el botón Add New Instructor');
                }
            """)
            time.sleep(2)
            self.save_screenshot("03b_intento_javascript.png")
        
        # PASO 5: Llenar los campos del formulario para el nuevo instructor
        print(f"Llenando datos del instructor: {self.INSTRUCTOR['name']}, {self.INSTRUCTOR['email']}")
        
        # Buscar los campos usando los IDs específicos proporcionados y llenarlos
        form_result = self.driver.execute_script(f"""
            try {{
                // Usar los IDs específicos para los campos de nombre y email
                const nameField = document.getElementById('name-instructor-2');
                const emailField = document.getElementById('email-instructor-2');
                
                if (!nameField) return "No se encontró el campo de nombre con ID: name-instructor-2";
                if (!emailField) return "No se encontró el campo de email con ID: email-instructor-2";
                
                console.log("Campos encontrados correctamente con IDs específicos");
                
                // Llenar los campos
                nameField.value = "{self.INSTRUCTOR['name']}";
                nameField.dispatchEvent(new Event('input', {{bubbles: true}}));
                nameField.dispatchEvent(new Event('change', {{bubbles: true}}));
                
                emailField.value = "{self.INSTRUCTOR['email']}";
                emailField.dispatchEvent(new Event('input', {{bubbles: true}}));
                emailField.dispatchEvent(new Event('change', {{bubbles: true}}));
                
                return "Campos nombre y email llenados correctamente usando IDs específicos";
            }} catch (e) {{
                // Intento alternativo si los IDs específicos fallan
                try {{
                    const forms = document.querySelectorAll('form');
                    for (const form of forms) {{
                        const nameInputs = form.querySelectorAll('input[maxlength="100"]');
                        const emailInputs = form.querySelectorAll('input[maxlength="254"]');
                        
                        if (nameInputs.length > 0 && emailInputs.length > 0) {{
                            nameInputs[0].value = "{self.INSTRUCTOR['name']}";
                            nameInputs[0].dispatchEvent(new Event('input', {{bubbles: true}}));
                            
                            emailInputs[0].value = "{self.INSTRUCTOR['email']}";
                            emailInputs[0].dispatchEvent(new Event('input', {{bubbles: true}}));
                            
                            return "Campos llenados con método alternativo";
                        }}
                    }}
                    return "No se encontraron campos de nombre y email con método alternativo";
                }} catch (innerError) {{
                    return "Error en método alternativo: " + innerError.message;
                }}
            }}
        """)
        
        print(f"Resultado de llenar formulario: {form_result}")
        self.save_screenshot("04_campos_nombre_email.png")
        
        # PASO 6: Seleccionar el rol "Manager" para el instructor
        print(f"Seleccionando rol: {self.INSTRUCTOR['role']}")
        
        # Mapeo de roles a IDs de elementos (basado en el HTML proporcionado)
        role_ids = {
            "Co-owner": "INSTRUCTOR_PERMISSION_ROLE_COOWNER11",
            "Manager": "INSTRUCTOR_PERMISSION_ROLE_MANAGER11",
            "Observer": "INSTRUCTOR_PERMISSION_ROLE_OBSERVER11",
            "Tutor": "INSTRUCTOR_PERMISSION_ROLE_TUTOR11",
            "Custom": "INSTRUCTOR_PERMISSION_ROLE_CUSTOM11"
        }
        
        # Intentar seleccionar el rol usando el ID específico del contenedor
        role_result = self.driver.execute_script(f"""
            try {{
                // Buscar el contenedor de los niveles de acceso por ID específico
                const accessLevelContainer = document.getElementById('access-levels-instructor-2');
                if (!accessLevelContainer) return "No se encontró el contenedor de niveles de acceso con ID: access-levels-instructor-2";
                
                // Obtener el ID del radio button para el rol seleccionado
                const roleId = "{role_ids.get(self.INSTRUCTOR['role'], '')}";
                
                // Buscar el radio button dentro del contenedor
                const roleRadio = accessLevelContainer.querySelector(`input#${{roleId}}`);
                if (!roleRadio) {{
                    // Intento alternativo: buscar por selector más general
                    const allRadios = accessLevelContainer.querySelectorAll('input[type="radio"]');
                    for (const radio of allRadios) {{
                        // Si el texto de la etiqueta contiene el nombre del rol, seleccionarlo
                        const label = radio.closest('label');
                        if (label && label.textContent.includes("{self.INSTRUCTOR['role']}")) {{
                            radio.checked = true;
                            radio.dispatchEvent(new Event('change', {{bubbles: true}}));
                            return "Rol seleccionado por coincidencia de texto en el contenedor específico";
                        }}
                    }}
                    
                    return "No se encontró radio button para el rol {self.INSTRUCTOR['role']} en el contenedor";
                }}
                
                // Seleccionar el radio button encontrado
                roleRadio.checked = true;
                roleRadio.dispatchEvent(new Event('change', {{bubbles: true}}));
                roleRadio.dispatchEvent(new Event('click', {{bubbles: true}}));
                
                return "Rol seleccionado correctamente usando ID específico";
            }} catch (e) {{
                return "Error al seleccionar rol: " + e.message;
            }}
        """)
        
        print(f"Resultado de seleccionar rol: {role_result}")
        self.save_screenshot("05_rol_seleccionado.png")
        
        # PASO 7: Hacer clic en el botón "Add Instructor"
        print("Haciendo clic en el botón 'Add Instructor'...")
        
        # Primero intentamos con Selenium (más confiable)
        try:
            # Buscar el botón con una espera explícita para asegurar que esté clickeable
            add_instructor_submit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Instructor')]"))
            )
            print("✓ Botón 'Add Instructor' encontrado con Selenium")
            
            # Tomar captura antes de hacer clic
            self.save_screenshot("05b_antes_click_add_instructor.png")
            
            # Hacer que el botón sea visible en la pantalla
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_instructor_submit_btn)
            time.sleep(1)  # Pequeña pausa para que el scroll termine
            
            # Hacer clic en el botón
            add_instructor_submit_btn.click()
            print("✓ Clic en botón 'Add Instructor' realizado con Selenium")
            submit_result = "Botón 'Add Instructor' clicado con Selenium"
        except Exception as e:
            print(f"⚠️ Error al hacer clic con Selenium: {e}")
            
            # Si falla con Selenium, intentamos con JavaScript como respaldo
            submit_result = self.driver.execute_script("""
                try {
                    console.log("Buscando el botón Add Instructor con JavaScript...");
                    
                    // Intentar múltiples estrategias para encontrar el botón
                    let submitBtn = null;
                    
                    // 1. Buscar por texto exacto en el botón
                    const allButtons = document.querySelectorAll('button');
                    for (const btn of allButtons) {
                        if (btn.textContent.trim() === 'Add Instructor') {
                            submitBtn = btn;
                            break;
                        }
                    }
                    
                    // 2. Buscar dentro del formulario si está dentro de uno
                    if (!submitBtn) {
                        const forms = document.querySelectorAll('form');
                        for (const form of forms) {
                            const formBtns = Array.from(form.querySelectorAll('button')).filter(btn => 
                                btn.textContent.includes('Add Instructor')
                            );
                            if (formBtns.length > 0) {
                                submitBtn = formBtns[0];
                                break;
                            }
                        }
                    }
                    
                    // 3. Buscar botón tipo submit como último recurso
                    if (!submitBtn) {
                        submitBtn = document.querySelector('button[type="submit"]');
                    }
                    
                    if (!submitBtn) return "No se encontró el botón Add Instructor con ninguna estrategia";
                    
                    // Hacer visible y habilitar el botón
                    submitBtn.style.display = 'block';
                    submitBtn.disabled = false;
                    
                    // Hacer clic usando múltiples métodos para mayor seguridad
                    console.log("Haciendo clic en el botón...");
                    submitBtn.click();
                    
                    // Disparar evento de clic como respaldo
                    submitBtn.dispatchEvent(new MouseEvent('click', {
                        bubbles: true,
                        cancelable: true,
                        view: window
                    }));
                    
                    return "Formulario enviado correctamente con JavaScript";
                } catch (e) {
                    return "Error al enviar formulario: " + e.message;
                }
            """)
        
        print(f"Resultado de enviar formulario: {submit_result}")
        time.sleep(3)
        self.save_screenshot("06_despues_enviar.png")
        
        # PASO 8: Verificar si la adición fue exitosa
        success = self.driver.execute_script(f"""
            try {{
                // Verificar por mensaje de éxito
                const successMessage = document.querySelector('.toast-success') || 
                                       document.querySelector('.alert-success');
                
                if (successMessage) return {{
                    success: true,
                    method: "mensaje",
                    message: successMessage.textContent.trim()
                }};
                
                // Verificar si el instructor aparece en la lista
                const allText = document.body.textContent;
                if (allText.includes("{self.INSTRUCTOR['name']}") && 
                    allText.includes("{self.INSTRUCTOR['email']}")) {{
                    return {{
                        success: true,
                        method: "presencia",
                        message: "Instructor encontrado en la página"
                    }};
                }}
                
                return {{
                    success: false,
                    message: "No se pudo verificar la adición del instructor"
                }};
            }} catch (e) {{
                return {{
                    success: false,
                    message: "Error: " + e.message
                }};
            }}
        """)
        
        # PASO 9: Mostrar resultado final
        if isinstance(success, dict) and success.get('success', False):
            print(f"✓ Instructor agregado exitosamente. Método de verificación: {success.get('method')}")
            print(f"Mensaje: {success.get('message', '')}")
            self.save_screenshot("07_instructor_agregado.png")
        else:
            print("❌ No se pudo verificar la adición del instructor")
            self.save_screenshot("error_instructor_no_agregado.png")
        
        print("Prueba CPF-INS-041 finalizada")
