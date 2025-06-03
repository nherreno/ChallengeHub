from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from config import CHROMEDRIVER_PATH, USER_AGENT

def iniciar_driver():
    options = Options()
    options.add_argument(f"user-agent={USER_AGENT}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def login_instagram(driver, username, password):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from time import sleep
    driver.get('https://www.instagram.com/')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    print("⚠️ Si Instagram solicita verificación, ingrésala manualmente en el navegador.")
    input("Presiona Enter cuando hayas completado el login/verificación en el navegador...")
    sleep(5)
    return True
