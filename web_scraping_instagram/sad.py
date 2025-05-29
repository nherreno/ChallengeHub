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

USERNAME = "misusuariodeinstagram@gmail.com"
PASSWORD = os.getenv('PASSWORD')

# Ruta correcta del chromedriver
chromedriver_path = "C:\\Users\\User\\OneDrive - Universidad Nacional de Colombia\\Escritorio\\codigo_Prueba\\chromedriver\\chromedriver-win64\\chromedriver.exe"

# Función para inicializar el driver
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

# Inicializar el driver
driver = iniciar_driver()
driver.maximize_window()

insta_url = 'https://www.instagram.com/'
driver.get(insta_url)
sleep(3)

# Inicio de sesión
try:
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
    username_field.send_keys(USERNAME)

    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
    password_field.send_keys(PASSWORD)

    login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]')))
    login_button.click()

    print("⚠️ Instagram ha solicitado verificación. Ingresa el código manualmente en el navegador.")
    input("Presiona Enter cuando hayas completado la verificación en el navegador...")

    sleep(5)
except Exception as e:
    print(f"Error durante el inicio de sesión: {e}")
    driver.quit()
    exit()

# Navegar al perfil de Cristiano Ronaldo
driver.get(insta_url + 'cristiano')
sleep(5)

# Intentar acceder al botón de seguidores con CSS Selector
try:
    seguidores_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#mount_0_0_HS > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div:nth-child(2) > div > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x17snn68.x6osk4m.x1porb0y.x8vgawa > section > main > div > header > section.xc3tme8.x1xdureb.x18wylqe.x13vxnyz.xvxrpd7 > ul > li:nth-child(2) > div > a > span > span > span")
        )
    )
    print(f"Texto del botón de seguidores: {seguidores_button.text}")
    seguidores_button.click()
    sleep(5)
except Exception as e:
    print(f"Error al acceder al botón de seguidores. Navegando directamente a la URL de seguidores.")
    driver.get("https://www.instagram.com/cristiano/followers/")
    sleep(5)

# Extraer los nombres de usuario y sus enlaces
try:
    seguidores = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div > div > span > div > a"))
    )

    print("\n🔹 Lista de seguidores:")
    for seguidor in seguidores:
        username = seguidor.text
        link = seguidor.get_attribute("href")
        print(f"{username}: {link}")
except Exception as e:
    print(f"Error al extraer seguidores: {e}")

# Cerrar el navegador
driver.quit()
