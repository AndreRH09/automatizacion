# setup_chrome_debug.py
"""
Script auxiliar para configurar Chrome en modo debug
Esto mantiene la sesión iniciada para las pruebas
"""

import os
import subprocess
import platform
import time

def get_chrome_path():
    """Obtiene la ruta de Chrome según el sistema operativo"""
    system = platform.system()
    
    if system == "Windows":
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
        ]
        for path in paths:
            if os.path.exists(path):
                return path
                
    elif system == "Darwin":  # macOS
        return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        
    else:  # Linux
        return "google-chrome"
    
    return None

def start_chrome_debug():
    """Inicia Chrome en modo debug"""
    chrome_path = get_chrome_path()
    
    if not chrome_path:
        print("❌ No se pudo encontrar Chrome instalado")
        return False
    
    # Crear directorio temporal para el perfil
    temp_dir = os.path.join(os.path.expanduser("~"), "chrome_debug_teammates")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Comando para iniciar Chrome
    cmd = [
        chrome_path,
        "--remote-debugging-port=9222",
        f"--user-data-dir={temp_dir}",
        "https://teammates-hormiga-1.uc.r.appspot.com"
    ]
    
    print("🚀 Iniciando Chrome en modo debug...")
    print(f"📁 Perfil temporal en: {temp_dir}")
    
    try:
        # Iniciar Chrome
        subprocess.Popen(cmd)
        
        print("\n✅ Chrome iniciado exitosamente")
        print("\n📋 INSTRUCCIONES:")
        print("1. En la ventana de Chrome que se abrió:")
        print("   - Inicia sesión como ADMINISTRADOR en TEAMMATES")
        print("   - Mantén la ventana abierta")
        print("2. Una vez logueado, ejecuta tus pruebas")
        print("3. NO cierres Chrome hasta terminar todas las pruebas")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al iniciar Chrome: {e}")
        return False

def check_debug_connection():
    """Verifica si Chrome está en modo debug"""
    try:
        import requests
        response = requests.get("http://localhost:9222/json")
        if response.status_code == 200:
            print("✅ Chrome está en modo debug y accesible")
            return True
    except:
        pass
    
    print("❌ Chrome no está en modo debug o no es accesible")
    return False

if __name__ == "__main__":
    print("="*50)
    print("CONFIGURADOR DE CHROME PARA PRUEBAS TEAMMATES")
    print("="*50)
    
    # Verificar si ya está en modo debug
    if check_debug_connection():
        print("\n⚠️  Chrome ya está en modo debug")
        print("Puedes ejecutar tus pruebas directamente")
    else:
        # Iniciar Chrome
        if start_chrome_debug():
            print("\n⏳ Esperando 5 segundos para que Chrome cargue...")
            time.sleep(5)
            
            if check_debug_connection():
                print("\n✅ Todo listo para ejecutar pruebas")
            else:
                print("\n⚠️  Chrome se inició pero no responde en el puerto debug")