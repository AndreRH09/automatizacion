"""
Ayudante para manejar diferentes tipos de login
"""
class LoginHelper:
    @staticmethod
    def setup_chrome_debug_session():
        """
        Instrucciones para configurar Chrome en modo debug
        """
        print("""
        === CONFIGURAR CHROME EN MODO DEBUG ===
        
        1. Cierra todas las ventanas de Chrome
        
        2. Abre una terminal/cmd y ejecuta:
        
        Windows:
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\\temp\\chrome_debug"
        
        Mac:
        /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_debug"
        
        Linux:
        google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_debug"
        
        3. En la ventana de Chrome que se abre:
           - Navega a TEAMMATES
           - Inicia sesión manualmente
           - Deja la ventana abierta
        
        4. Ahora ejecuta tus pruebas con use_debug_mode=True
        """)