from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import random
import re
from bs4 import BeautifulSoup

# Cargar variables de entorno
load_dotenv()

USERNAME = "nico.proyecx6@gmail.com"
PASSWORD = os.getenv('PASSWORD')

# Solicitar el usuario a revisar
print("🔍 INSTAGRAM ACCOUNT CREATION DATE CHECKER")
print("="*50)
usuario_objetivo = input("👤 Ingresa el nombre de usuario de Instagram a revisar (sin @): ").strip()

# Validar entrada
if not usuario_objetivo:
    print("❌ Error: Debes ingresar un nombre de usuario válido")
    exit()

# Remover @ si lo incluyó el usuario
if usuario_objetivo.startswith('@'):
    usuario_objetivo = usuario_objetivo[1:]

print(f"🎯 Revisando fecha de creación de: @{usuario_objetivo}")
print("="*50)

# Ruta del chromedriver (ajustar según tu sistema)
chromedriver_path = "C:\\Users\\User\\OneDrive - Universidad Nacional de Colombia\\Escritorio\\codigo_Prueba\\chromedriver\\chromedriver-win64\\chromedriver.exe"

def obtener_fecha_creacion_cuenta(driver, username):
    """
    Obtiene la fecha de creación de una cuenta de Instagram usando Selenium y BeautifulSoup
    """
    try:
        print(f"📅 Obteniendo fecha de creación de @{username}...")
        perfil_url = f"https://www.instagram.com/{username}/"
        driver.get(perfil_url)
        sleep(random.uniform(4, 6))
        # Verificar que el perfil existe
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "header"))
            )
            print(f"✅ Perfil de @{username} encontrado")
        except:
            print(f"❌ No se pudo cargar el perfil de @{username}")
            return None
        # Hacer clic en el username usando el texto
        try:
            print(f"⌛ Buscando el elemento con el texto '{username}'...")
            username_elem = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[text()='{username}']"))
            )
            username_elem.click()
            print("✅ Click realizado sobre el username")
            sleep(2)
            driver.save_screenshot("modal_info.png")
            print("🖼️ Captura de pantalla guardada como modal_info.png")
        except Exception as e:
            print(f"❌ No se pudo hacer clic en el username: {e}")
            return None
        # Esperar a que aparezca el modal
        modal_selector = 'div[data-bloks-name="bk.components.Collection"].wbloks_1.wbloks_94.wbloks_92'
        try:
            print("⌛ Esperando a que aparezca el modal de información...")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, modal_selector))
            )
            sleep(1)
        except Exception as e:
            print(f"❌ No apareció el modal de información: {str(e)}")
            return None
        # Extraer la fecha de creación usando BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        modal = soup.select_one(modal_selector)
        if not modal:
            print("❌ No se encontró el modal en el HTML")
            return None
        # Buscar el texto de la fecha
        fecha = None
        for span in modal.find_all('span'):
            if 'Fecha en que se unió' in span.text or 'Fecha en la que te uniste' in span.text:
                # El siguiente span contiene la fecha
                next_span = span.find_next('span')
                if next_span:
                    fecha = next_span.text.strip()
                    break
        if fecha:
            print(f"✅ Fecha encontrada: {fecha}")
            return fecha
        else:
            print("❌ No se encontró la fecha en el modal")
            return None
    except Exception as e:
        print(f"❌ Error general: {str(e)}")
        return None
    finally:
        # Cerrar modales
        try:
            from selenium.webdriver.common.keys import Keys
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            sleep(1)
        except:
            pass

def iniciar_driver():
    """Inicializa el driver de Chrome con configuraciones anti-detección"""
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/136.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        print(f"❌ Error al iniciar el driver: {e}")
        print("💡 Verifica que la ruta del chromedriver sea correcta")
        exit()

# PROGRAMA PRINCIPAL
def main():
    print("🚀 Iniciando navegador...")
    driver = iniciar_driver()
    driver.maximize_window()

    try:
        # Ir a Instagram
        print("📱 Navegando a Instagram...")
        driver.get('https://www.instagram.com/')
        sleep(3)

        # Proceso de login
        print("🔐 Iniciando sesión...")
        try:
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'username'))
            )
            username_field.send_keys(USERNAME)

            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'password'))
            )
            password_field.send_keys(PASSWORD)

            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            login_button.click()

            print("⚠️ Si Instagram solicita verificación, ingrésala manualmente en el navegador.")
            input("Presiona Enter cuando hayas completado el login/verificación...")

            sleep(3)
            print("✅ Login completado")

        except Exception as e:
            print(f"❌ Error durante el login: {e}")
            driver.quit()
            return

        # Obtener fecha de creación
        print(f"\n🔍 Buscando información de @{usuario_objetivo}...")
        fecha_creacion = obtener_fecha_creacion_cuenta(driver, usuario_objetivo)
        
        # Mostrar resultados
        print("\n" + "="*60)
        print("📊 RESULTADO FINAL")
        print("="*60)
        
        if fecha_creacion:
            print(f"👤 Usuario: @{usuario_objetivo}")
            print(f"📅 Fecha de creación: {fecha_creacion}")
            print(f"⏰ Consultado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            print("✅ ¡Información obtenida exitosamente!")
        else:
            print(f"❌ No se pudo obtener la fecha de creación de @{usuario_objetivo}")
            print("💡 Posibles causas:")
            print("   - La cuenta es privada")
            print("   - La cuenta no existe")
            print("   - Instagram cambió su estructura")
            print("   - Los XPaths han cambiado")
        
        print("="*60)

    except Exception as e:
        print(f"❌ Error general: {e}")
    
    finally:
        print("\n🔚 Cerrando navegador...")
        driver.quit()
        print("✅ Proceso finalizado")

if __name__ == "__main__":
    main()