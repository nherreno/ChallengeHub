from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Cargar variables de entorno
load_dotenv()

USERNAME = "nico.proyecx6@gmail.com"  # Reemplaza con tu nombre de usuario posdata no pude automatizar esta parte 
PASSWORD = os.getenv('PASSWORD')

# Ruta correcta del chromedriver
chromedriver_path = "C:\\Users\\User\\OneDrive - Universidad Nacional de Colombia\\Escritorio\\codigo_Prueba\\chromedriver\\chromedriver-win64\\chromedriver.exe"

# Función para inicializar el driver sin modo headless (para que veas el proceso)
def iniciar_driver():
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/136.0.0.0 Safari/537.36")  
    service = Service(chromedriver_path)

    try:
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Error al iniciar el driver: {e}")
        exit()

# Inicializar el driver con opciones personalizadas
driver = iniciar_driver()
driver.maximize_window()

insta_url = 'https://www.instagram.com/'
driver.get(insta_url)
sleep(3)

# Inicio de sesión
try:
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
    username_field.send_keys(USERNAME)

    sleep(1)

    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
    password_field.send_keys(PASSWORD)

    sleep(1)

    login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]')))
    login_button.click()

    print("⚠️ Instagram ha solicitado verificación. Ingresa el código manualmente en el navegador.")
    input("Presiona Enter cuando hayas completado la verificación en el navegador...")  # Espera hasta que ingreses el código

    sleep(5)  # Pequeña espera adicional para asegurar que Instagram procese la verificación
except Exception as e:
    print(f"Error durante el inicio de sesión: {e}")
    driver.quit()
    exit()

# Navegar al perfil de Cristiano Ronaldo
try:
    driver.get(insta_url + 'cristiano')
    sleep(5)

    ul = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'ul')))
    items = ul.find_elements(By.TAG_NAME, 'li')

    for li in items:
        print(li.text)
except Exception as e:
    print(f"Error al navegar o extraer información: {e}")

# Cerrar el navegador al finalizar
driver.quit()