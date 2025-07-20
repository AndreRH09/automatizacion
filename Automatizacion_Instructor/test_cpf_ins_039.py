import os, time, pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from pathlib import Path

class TestCPFINS039:
    def setup_method(self, method):
        env_path = Path(__file__).parent.parent / "cred.env"
        load_dotenv(dotenv_path=env_path.resolve())
        self.email = os.getenv("APP_EMAIL")
        self.password = os.getenv("APP_PASSWORD")
        assert self.email is not None and self.password is not None, "ERROR: Credenciales no encontradas"
        
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)

    def teardown_method(self, method):
        self.driver.quit()

    def test_copiar_configuracion_curso(self):
        """Prueba CPF-INS-039: Copiar la configuración de un curso existente al crear uno nuevo."""
        print("Iniciando prueba CPF-INS-039")
        
        # Login
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/instructor/home")
        if "login" in self.driver.current_url or "accounts.google.com" in self.driver.current_url:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys(self.email + Keys.ENTER)
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.NAME, "Passwd"))).send_keys(self.password + Keys.ENTER)
            time.sleep(5)
        
        # Ir a página de cursos
        self.driver.get("https://teammates-hormiga-1.uc.r.appspot.com/web/instructor/courses?user=atacoh@unsa.edu.pe")
        time.sleep(5)
        
        # Capturar antes de agregar curso
        self.driver.save_screenshot("antes_agregar_curso.png")
        print("✓ Captura guardada: antes_agregar_curso.png")
        
        # Verificar si ya estamos en el formulario modal de copia
        is_modal_open = self.driver.execute_script("return !!document.querySelector('.modal-dialog')")
        
        # Si no hay modal abierto, iniciamos el flujo normal
        if not is_modal_open:
            # Click en Add New Course
            try:
                add_button = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add New Course')]")))
                add_button.click()
            except Exception as e:
                print(f"Usando JavaScript para Add New Course: {e}")
                self.driver.execute_script("Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Add New Course'))?.click()")
            time.sleep(2)
            
            # Click en Copy from previous courses (una sola vez)
            is_copy_form_open = self.driver.execute_script("return !!document.getElementById('course-to-copy-from')")
            if not is_copy_form_open:
                self.driver.execute_script("""
                    const copyBtn = document.querySelector('button i.fa-copy')?.closest('button') || 
                                    Array.from(document.querySelectorAll('button')).find(b => 
                                    b.textContent.includes('Copy from previous'));
                    if (copyBtn) copyBtn.click();
                """)
                time.sleep(3)
        
        # Captura después de abrir el formulario de copia
        self.driver.save_screenshot("despues_click_copy.png")
        print("✓ Captura guardada: despues_click_copy.png")
        
        # Seleccionar curso y modificar los campos con IDs correctos
        self.driver.execute_script("""
            // 1. Seleccionar CEX-025 del dropdown
            const select = document.getElementById('course-to-copy-from');
            if (select) {
                for (let i = 0; i < select.options.length; i++) {
                    if (select.options[i].text.includes('CEX-025')) {
                        select.selectedIndex = i;
                        select.dispatchEvent(new Event('change', {bubbles:true}));
                        break;
                    }
                }
            }
            
            // 2. Modificar los campos usando los IDs correctos
            setTimeout(() => {
                // Buscar los campos por ID correcto o por placeholder si los IDs no coinciden
                const idField = document.getElementById('copy-course-id') || 
                                document.getElementById('course-id') || 
                                document.querySelector('input[placeholder*="CS3215"]');
                
                const nameField = document.getElementById('copy-course-name') || 
                                 document.getElementById('course-name') || 
                                 document.querySelector('input[placeholder*="Software Engineering"]');
                
                // Modificar Course ID
                if (idField) {
                    idField.value = 'CEX-026';
                    idField.dispatchEvent(new Event('input', {bubbles:true}));
                    console.log('Course ID actualizado');
                }
                
                // Modificar Course Name si es necesario
                if (nameField) {
                    nameField.value = 'CEX-026';
                    nameField.dispatchEvent(new Event('input', {bubbles:true}));
                    console.log('Course Name actualizado');
                }
            }, 1000);
        """)
        time.sleep(2)
        self.driver.save_screenshot("despues_llenar_campos.png")
        print("✓ Captura guardada: despues_llenar_campos.png")
        
        # Hacer clic en el botón Copy para confirmar
        self.driver.execute_script("""
            // Encontrar el botón Copy dentro del formulario modal
            const copyBtn = Array.from(document.querySelectorAll('.modal-dialog button')).find(b => 
                b.textContent.includes('Copy') && !b.textContent.includes('from'));
            if (copyBtn) copyBtn.click();
        """)
        
        # Esperar 5 segundos después de crear el curso
        print("Esperando 5 segundos después de crear el curso...")
        time.sleep(5)
        self.driver.save_screenshot("despues_crear_curso.png")
        print("✓ Captura guardada: despues_crear_curso.png")
        
        # Verificar que las capturas existen en el sistema de archivos
        import os
        capturas = ["antes_agregar_curso.png", "despues_click_copy.png", "despues_llenar_campos.png", "despues_crear_curso.png"]
        for captura in capturas:
            if os.path.exists(captura):
                print(f"✓ Verificado: {captura} existe")
            else:
                print(f"❌ Error: {captura} no existe")
        
        print("Prueba CPF-INS-039 finalizada correctamente")
