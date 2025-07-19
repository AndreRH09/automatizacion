# element_mapper.py
"""
Utilidad para identificar y mapear elementos en TEAMMATES
Ayuda a encontrar los selectores correctos para las pruebas
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import datetime

class ElementMapper:
    def __init__(self, use_debug=True):
        if use_debug:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Chrome()
        
        self.wait = WebDriverWait(self.driver, 10)
        self.elements_found = {}
    
    def map_notifications_page(self):
        """Mapea elementos de la página de notificaciones"""
        print("🔍 Mapeando elementos de la página de Notifications...")
        
        elements_to_find = {
            "add_notification_button": [
                "//button[contains(text(), 'Add New Notification')]",
                "//button[contains(@class, 'btn-primary')]",
                "//button[@id='add-notification']",
                "//a[contains(text(), 'Add New Notification')]"
            ],
            "notification_title_field": [
                "//input[@id='notification-title']",
                "//input[@name='title']",
                "//input[@placeholder*='Title']",
                "//label[contains(text(), 'Title')]/following-sibling::input"
            ],
            "notification_style_dropdown": [
                "//select[@id='notification-style']",
                "//select[@name='style']",
                "//label[contains(text(), 'Style')]/following-sibling::select"
            ],
            "notification_message_field": [
                "//textarea[@id='notification-message']",
                "//textarea[@name='message']",
                "//textarea[@placeholder*='Message']",
                "//label[contains(text(), 'Message')]/following-sibling::textarea"
            ],
            "notification_target_dropdown": [
                "//select[@id='notification-target']",
                "//select[@name='target']",
                "//label[contains(text(), 'Target')]/following-sibling::select"
            ],
            "create_button": [
                "//button[contains(text(), 'Create')]",
                "//button[contains(text(), 'Save')]",
                "//button[@type='submit']"
            ],
            "edit_button": [
                "//button[contains(text(), 'Edit')]",
                "//a[contains(text(), 'Edit')]",
                "//button[@class*='edit']"
            ],
            "delete_button": [
                "//button[contains(text(), 'Delete')]",
                "//a[contains(text(), 'Delete')]",
                "//button[@class*='delete']"
            ]
        }
        
        found_elements = {}
        
        for element_name, selectors in elements_to_find.items():
            print(f"\n🔎 Buscando: {element_name}")
            for selector in selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    if element.is_displayed():
                        found_elements[element_name] = {
                            "xpath": selector,
                            "found": True,
                            "tag": element.tag_name,
                            "id": element.get_attribute("id"),
                            "class": element.get_attribute("class"),
                            "name": element.get_attribute("name")
                        }
                        print(f"  ✅ Encontrado con: {selector}")
                        break
                except:
                    continue
            
            if element_name not in found_elements:
                print(f"  ❌ No encontrado")
                found_elements[element_name] = {"found": False}
        
        return found_elements
    
    def analyze_table_structure(self):
        """Analiza la estructura de tablas en la página"""
        print("\n📊 Analizando estructura de tablas...")
        
        tables = self.driver.find_elements(By.TAG_NAME, "table")
        table_info = []
        
        for i, table in enumerate(tables):
            info = {
                "index": i,
                "class": table.get_attribute("class"),
                "id": table.get_attribute("id")
            }
            
            # Contar filas y columnas
            rows = table.find_elements(By.TAG_NAME, "tr")
            if rows:
                cols = rows[0].find_elements(By.TAG_NAME, "th")
                if not cols:
                    cols = rows[0].find_elements(By.TAG_NAME, "td")
                
                info["rows"] = len(rows)
                info["columns"] = len(cols)
                
                # Obtener headers
                headers = []
                header_row = table.find_elements(By.TAG_NAME, "th")
                for header in header_row:
                    headers.append(header.text)
                info["headers"] = headers
            
            table_info.append(info)
            print(f"\nTabla {i}:")
            print(f"  - Clases: {info.get('class', 'N/A')}")
            print(f"  - ID: {info.get('id', 'N/A')}")
            print(f"  - Filas: {info.get('rows', 0)}")
            print(f"  - Columnas: {info.get('columns', 0)}")
            print(f"  - Headers: {info.get('headers', [])}")
        
        return table_info
    
    def find_form_elements(self):
        """Encuentra todos los elementos de formulario"""
        print("\n📝 Buscando elementos de formulario...")
        
        form_elements = {
            "inputs": [],
            "selects": [],
            "textareas": [],
            "buttons": []
        }
        
        # Inputs
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        for inp in inputs:
            if inp.get_attribute("type") not in ["hidden", "submit"]:
                form_elements["inputs"].append({
                    "id": inp.get_attribute("id"),
                    "name": inp.get_attribute("name"),
                    "type": inp.get_attribute("type"),
                    "placeholder": inp.get_attribute("placeholder"),
                    "class": inp.get_attribute("class")
                })
        
        # Selects
        selects = self.driver.find_elements(By.TAG_NAME, "select")
        for sel in selects:
            options = sel.find_elements(By.TAG_NAME, "option")
            form_elements["selects"].append({
                "id": sel.get_attribute("id"),
                "name": sel.get_attribute("name"),
                "options": [opt.text for opt in options],
                "class": sel.get_attribute("class")
            })
        
        # Textareas
        textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
        for txt in textareas:
            form_elements["textareas"].append({
                "id": txt.get_attribute("id"),
                "name": txt.get_attribute("name"),
                "placeholder": txt.get_attribute("placeholder"),
                "class": txt.get_attribute("class")
            })
        
        # Buttons
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        for btn in buttons:
            form_elements["buttons"].append({
                "text": btn.text,
                "type": btn.get_attribute("type"),
                "class": btn.get_attribute("class"),
                "onclick": btn.get_attribute("onclick")
            })
        
        return form_elements
    
    def save_mapping(self, filename="element_mapping.json"):
        """Guarda el mapeo en un archivo JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"element_mapping_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.elements_found, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Mapeo guardado en: {filename}")
    
    def run_full_mapping(self, url=None):
        """Ejecuta un mapeo completo de la página"""
        if url:
            self.driver.get(url)
            time.sleep(2)
        
        print("="*60)
        print("INICIANDO MAPEO DE ELEMENTOS")
        print("="*60)
        
        # Información general de la página
        print(f"\n📍 URL actual: {self.driver.current_url}")
        print(f"📄 Título: {self.driver.title}")
        
        # Mapear elementos específicos
        notification_elements = self.map_notifications_page()
        
        # Analizar tablas
        table_info = self.analyze_table_structure()
        
        # Encontrar elementos de formulario
        form_info = self.find_form_elements()
        
        # Compilar toda la información
        self.elements_found = {
            "url": self.driver.current_url,
            "timestamp": datetime.now().isoformat(),
            "notification_elements": notification_elements,
            "tables": table_info,
            "forms": form_info
        }
        
        # Guardar resultados
        self.save_mapping()
        
        print("\n✅ Mapeo completado")
        
        return self.elements_found

# Función de utilidad para uso rápido
def quick_map(page_url=None):
    """Mapea rápidamente una página"""
    mapper = ElementMapper(use_debug=True)
    return mapper.run_full_mapping(page_url)

if __name__ == "__main__":
    print("""
    🗺️  MAPEADOR DE ELEMENTOS TEAMMATES
    
    Este script te ayudará a identificar los selectores correctos
    para tus pruebas automatizadas.
    
    Asegúrate de:
    1. Tener Chrome en modo debug
    2. Estar en la página que quieres mapear
    3. Presiona Enter para continuar...
    """)
    
    input()
    
    mapper = ElementMapper(use_debug=True)
    mapper.run_full_mapping()