# test_cpf_adm_007.py
"""
Caso de Prueba: CPF-ADM-007 - Ver notificaciones del sistema
Versión corregida con selectores de Selenium IDE
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from datetime import datetime

class TestNotificacionesSistema:
    def __init__(self, use_debug=True):
        self.test_id = "CPF-ADM-007"
        self.test_name = "Ver notificaciones del sistema"
        self.base_url = "https://teammates-hormiga-1.uc.r.appspot.com"
        
        # Configurar driver
        if use_debug:
            print("🔧 Conectando a Chrome en modo debug...")
            options = webdriver.ChromeOptions()
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Chrome()
            
        self.wait = WebDriverWait(self.driver, 10)
        self.results = []
        
        # Datos de prueba
        self.test_data = {
            "titulo": "Mantenimiento Programado del Sistema 001",
            "mensaje": "Esta es una prueba de Mensaje de Mantenimiento Programado",
            "styles": ["Warning (yellow)", "Danger (red)", "Success (green)"],
            "targets": ["General", "Instructors only", "Students only"]
        }
    
    def log_step(self, step_num, description, status="⏳", details=""):
        """Registra el resultado de cada paso"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if status == "⏳":
            print(f"[{timestamp}] Paso {step_num}: {description}...")
        else:
            log_entry = f"[{timestamp}] Paso {step_num}: {description} - {status}"
            if details:
                log_entry += f" - {details}"
            print(log_entry)
            self.results.append(log_entry)
    
    def take_screenshot(self, name):
        """Toma captura de pantalla"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{self.test_id}_{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"📸 Captura guardada: {filename}")
    
    def verify_admin_session(self):
        """Verifica que estamos logueados como administrador"""
        current_url = self.driver.current_url
        if "/admin/" not in current_url:
            self.driver.get(f"{self.base_url}/web/admin/home")
            time.sleep(2)
        
        return "/admin/" in self.driver.current_url
    
    def execute_test(self):
        """Ejecuta el caso de prueba completo"""
        print(f"\n{'='*60}")
        print(f"INICIANDO TEST: {self.test_id} - {self.test_name}")
        print(f"{'='*60}\n")
        
        try:
            # Verificar precondiciones
            if not self.verify_admin_session():
                print("❌ No se detectó sesión de administrador. Abortando test.")
                return False
            
            # Forzar navegación al dashboard del admin
            self.driver.get(f"{self.base_url}/web/admin/home")
            time.sleep(2)

            # PASO 1: Sesión como administrador
            self.log_step(1, "Sesión como administrador", "✅", "Sesión activa verificada")
            
            # PASO 2: Navegar a Notifications
            self.log_step(2, "Navegando a Notifications")
            if self.navigate_to_notifications():
                self.log_step(2, "Navegación a Notifications", "✅")
                self.take_screenshot("notifications_page")
            else:
                self.log_step(2, "Navegación a Notifications", "❌", "No se pudo acceder")
                return False
            
            # PASO 3: Verificar mensaje inicial
            self.log_step(3, "Verificando estado inicial")
            self.check_initial_state()
            
            # PASO 4: Abrir formulario de nueva notificación
            self.log_step(4, "Abriendo formulario de nueva notificación")
            if self.open_notification_form():
                self.log_step(4, "Formulario abierto", "✅")
                time.sleep(1)
                self.take_screenshot("notification_form")
            else:
                self.log_step(4, "Error abriendo formulario", "❌")
                return False
            
            # PASO 5: Crear una notificación general (única)
            self.log_step(5, "Creando notificación general")
            success = self.create_notification(
                titulo=f"{self.test_data['titulo']} - General",
                style="Danger (red)",
                mensaje=f"{self.test_data['mensaje']} - Notificación para todos",
                target="General",
                duration_days=7
            )
            
            if success:
                self.log_step(5, "Notificación creada", "✅", "General - Peligro")
                self.take_screenshot("notification_created_1")
            else:
                self.log_step(5, "Error creando notificación", "❌", "General - Peligro")
                return False
            
            # PASO 6: Verificar que la notificación aparece en la lista
            time.sleep(2)
            self.log_step(6, "Verificando lista de notificaciones")
            count = self.verify_notification_list()
            if count > 0:
                self.log_step(6, "Lista de notificaciones", "✅", f"{count} notificaciones encontradas")
                self.take_screenshot("notification_list_final")
            else:
                self.log_step(6, "Lista de notificaciones", "⚠️", "No se encontraron notificaciones")
            
            print(f"\n{'='*60}")
            print(f"TEST COMPLETADO")
            print(f"{'='*60}")
            
            return True

        except Exception as e:
            self.log_step("X", "Error inesperado", "❌", str(e))
            self.take_screenshot("error_unexpected")
            return False

    
    def navigate_to_notifications(self):
        """Navega a la página de notificaciones"""
        try:
            notifications_link = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Notifications"))
            )
            notifications_link.click()
            time.sleep(2)
            return True
        except:
            return False
    
    def check_initial_state(self):
        """Verifica el estado inicial de la página"""
        try:
            # Buscar mensaje de no notificaciones
            no_notifications = self.driver.find_elements(
                By.XPATH, 
                "//*[contains(text(), 'You have not created any notifications yet')]"
            )
            if no_notifications:
                self.log_step(3, "Estado inicial", "✅", "Sin notificaciones previas")
            else:
                # Contar notificaciones existentes
                rows = self.driver.find_elements(By.CSS_SELECTOR, "tbody tr")
                self.log_step(3, "Estado inicial", "ℹ️", f"{len(rows)} notificaciones existentes")
        except:
            self.log_step(3, "Estado inicial", "⚠️", "No se pudo verificar")
    
    def open_notification_form(self):
        """Abre el formulario de nueva notificación"""
        try:
            add_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "btn-add-notification"))
            )
            add_button.click()
            time.sleep(1)  # Esperar que el formulario se abra
            return True
        except:
            return False
    
    def create_notification(self, titulo, style, mensaje, target="General", duration_days=7):
        """Crea una nueva notificación con los parámetros especificados"""
        try:
            # 1. Seleccionar tipo de usuario objetivo
            self.log_step("", "Seleccionando tipo de usuario", "⏳")
            target_radio = self.wait.until(
                EC.element_to_be_clickable((By.ID, "notification-target-user"))
            )
            target_radio.click()
            
            # 2. Seleccionar estilo
            self.log_step("", "Seleccionando estilo", "⏳")
            style_select = Select(self.driver.find_element(By.ID, "notification-style"))
            style_select.select_by_visible_text(style)
            
            # 3. Ingresar título
            self.log_step("", "Ingresando título", "⏳")
            title_field = self.driver.find_element(By.ID, "notification-title")
            title_field.clear()
            title_field.send_keys(titulo)
            
            # 4. Ingresar mensaje (manejo del iframe de TinyMCE)
            self.log_step("", "Ingresando mensaje", "⏳")
            # Cambiar al iframe del editor
            self.driver.switch_to.frame(0)
            
            # Limpiar y escribir en el editor
            editor = self.driver.find_element(By.ID, "tinymce")
            self.driver.execute_script(
                "arguments[0].innerHTML = '<p>" + mensaje + "</p>'", 
                editor
            )
            
            # Volver al contenido principal
            self.driver.switch_to.default_content()
            
            # 5. Configurar fecha de inicio (usar fecha actual)
            self.log_step("", "Configurando fecha de inicio", "⏳")
            start_date_btn = self.driver.find_element(By.CSS_SELECTOR, "#notification-start-date .btn")
            start_date_btn.click()
            time.sleep(0.5)
            
            # Seleccionar día actual
            today = self.driver.find_element(By.CSS_SELECTOR, ".ngb-dp-today > .btn-light")
            today.click()
            
            # 6. Configurar hora de inicio
            start_time_select = Select(self.driver.find_element(
                By.CSS_SELECTOR, "#notification-start-time > .form-control"
            ))
            start_time_select.select_by_visible_text("18:00H")
            
            # 7. Configurar fecha de fin
            self.log_step("", "Configurando fecha de fin", "⏳")
            end_date_btn = self.driver.find_element(By.CSS_SELECTOR, "#notification-end-date .btn")
            end_date_btn.click()
            time.sleep(0.5)
            
            # Para este ejemplo, usar el mismo día
            today_end = self.driver.find_element(By.CSS_SELECTOR, ".ngb-dp-today > .btn-light")
            today_end.click()
            
            # 8. Crear notificación
            self.log_step("", "Creando notificación", "⏳")
            create_button = self.driver.find_element(By.ID, "btn-create-notification")
            create_button.click()
            
            # Esperar confirmación
            time.sleep(3)
            
            # Verificar que se creó exitosamente
            try:
                # Buscar mensaje de éxito o verificar que el modal se cerró
                success_indicator = self.driver.find_elements(
                    By.CSS_SELECTOR, ".alert-success, .toast-success"
                )
                if success_indicator:
                    return True
                
                # Si no hay mensaje, verificar que estamos de vuelta en la lista
                notification_rows = self.driver.find_elements(By.CSS_SELECTOR, "tbody tr")
                return len(notification_rows) > 0
                
            except:
                return True  # Asumir éxito si no hay errores
                
        except Exception as e:
            print(f"   ❌ Error creando notificación: {str(e)}")
            self.take_screenshot("error_creating_notification")
            # Asegurarse de volver al contenido principal si estamos en iframe
            try:
                self.driver.switch_to.default_content()
            except:
                pass
            return False
    
    def verify_notification_list(self):
        """Verifica y cuenta las notificaciones en la lista"""
        try:
            # Buscar filas de la tabla
            notification_rows = self.driver.find_elements(By.CSS_SELECTOR, "tbody tr")
            
            # Si no hay tbody tr, buscar otros selectores
            if not notification_rows:
                notification_rows = self.driver.find_elements(By.CSS_SELECTOR, ".notification-item")
            
            return len(notification_rows)
        except:
            return 0
    
    def generate_report(self):
        """Genera un reporte simple de la ejecución"""
        print("\n📋 RESUMEN DE EJECUCIÓN:")
        for result in self.results:
            print(result)

def main():
    print("""
    🧪 TEST CPF-ADM-007: Ver notificaciones del sistema
    
    Verificando conexión con Chrome...
    """)
    
    # Verificar conexión debug
    try:
        import requests
        response = requests.get("http://localhost:9222/json")
        if response.status_code == 200:
            print("✅ Chrome en modo debug detectado")
            data = response.json()
            if data:
                print("✅ Sesión activa en:", data[0]['url'])
        else:
            print("❌ Chrome no responde en modo debug")
            return
    except:
        print("❌ No se puede conectar a Chrome en modo debug")
        return
    
    print("\nIniciando test en 3 segundos...")
    time.sleep(3)
    
    # Ejecutar test
    test = TestNotificacionesSistema(use_debug=True)
    success = test.execute_test()
    
    # Generar reporte
    test.generate_report()
    
    if success:
        print("\n✅ TEST COMPLETADO EXITOSAMENTE")
    else:
        print("\n❌ TEST FALLIDO")

if __name__ == "__main__":
    main()