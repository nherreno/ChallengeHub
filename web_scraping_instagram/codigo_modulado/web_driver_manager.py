"""
Gestión del WebDriver de Selenium
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random
from config import CHROMEDRIVER_PATH, USER_AGENT, USERNAME, PASSWORD


class WebDriverManager:
    def __init__(self):
        self.driver = None
    
    def iniciar_driver(self):
        """Inicializa y configura el driver de Chrome"""
        options = Options()
        options.add_argument(f"user-agent={USER_AGENT}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(CHROMEDRIVER_PATH)

        try:
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.maximize_window()
            return self.driver
        except Exception as e:
            print(f"Error al iniciar el driver: {e}")
            return None
    
    def login_instagram(self):
        """Realiza el login en Instagram"""
        if not self.driver:
            print("❌ Driver no inicializado")
            return False
        
        try:
            insta_url = 'https://www.instagram.com/'
            self.driver.get(insta_url)
            sleep(3)

            # Campos de login
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'username'))
            )
            username_field.send_keys(USERNAME)

            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'password'))
            )
            password_field.send_keys(PASSWORD)

            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            login_button.click()

            print("⚠️ Si Instagram solicita verificación, ingrésala manualmente en el navegador.")
            input("Presiona Enter cuando hayas completado el login/verificación en el navegador...")

            sleep(5)
            return True
            
        except Exception as e:
            print(f"Error durante el inicio de sesión: {e}")
            return False
    
    def navegar_a_perfil(self, usuario):
        """Navega al perfil de un usuario específico"""
        if not self.driver:
            return False
        
        try:
            print(f"📱 Navegando al perfil de @{usuario}...")
            profile_url = f'https://www.instagram.com/{usuario}/'
            self.driver.get(profile_url)
            sleep(random.uniform(4, 6))
            
            # Verificar que el perfil cargó correctamente
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "header"))
            )
            print(f"✅ Perfil de @{usuario} cargado correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error al navegar al perfil: {e}")
            return False
    
    def verificar_perfil_existe(self, usuario):
        """Verifica si el perfil del usuario existe"""
        try:
            page_title = self.driver.title.lower()
            current_url = self.driver.current_url.lower()
            
            if "page not found" in page_title or "sorry" in page_title or "error" in current_url:
                print(f"❌ Error: El usuario @{usuario} no existe o no es público")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error al verificar el perfil de @{usuario}: {e}")
            return False
    
    def cerrar_driver(self):
        """Cierra el driver de forma segura"""
        if self.driver:
            self.driver.quit()
            print("🔚 Driver cerrado correctamente")