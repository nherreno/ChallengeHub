from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from username_validator import limpiar_username, es_username_valido
from config import LIMITE_MAX, MAX_SIN_NUEVOS, MAX_SCROLLS

def navegar_a_perfil(driver, usuario_objetivo):
    driver.get(f'https://www.instagram.com/{usuario_objetivo}/')
    sleep(3)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "header")))
    return True

def navegar_a_perfil_desde_inicio(driver, usuario_objetivo):
    try:
        print(f"🏠 Volviendo al inicio de Instagram...")
        driver.get('https://www.instagram.com/')
        sleep(3)
        print(f"📱 Navegando al perfil de @{usuario_objetivo}...")
        profile_url = f'https://www.instagram.com/{usuario_objetivo}/'
        driver.get(profile_url)
        sleep(4)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "header"))
        )
        print(f"✅ Perfil de @{usuario_objetivo} cargado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al navegar al perfil: {e}")
        return False

def encontrar_boton_seguidores(driver, usuario_objetivo, max_intentos=3):
    estrategias = [
        (By.XPATH, "//a[contains(@href, '/followers/')]")
    ]
    for intento in range(max_intentos):
        if intento > 0:
            if not navegar_a_perfil_desde_inicio(driver, usuario_objetivo):
                continue
        for by, selector in estrategias:
            try:
                element = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((by, selector))
                )
                href = element.get_attribute('href')
                text = element.text
                if href and 'followers' in href:
                    return element
            except Exception:
                continue
    return None

def cargar_seguidores_completo(driver, usuario_objetivo, limite_max=LIMITE_MAX, max_intentos_carga=2):
    for intento_carga in range(max_intentos_carga):
        if intento_carga > 0:
            if not navegar_a_perfil_desde_inicio(driver, usuario_objetivo):
                continue
            driver.get(f"https://www.instagram.com/{usuario_objetivo}/followers/")
            sleep(4)
        seguidores_unicos = set()
        scroll_count = 0
        sin_nuevos_seguidores = 0
        total_links_procesados = 0
        links_filtrados = 0
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[role='dialog'], div[style*='overflow-y']"))
            )
        except:
            if intento_carga < max_intentos_carga - 1:
                continue
        try:
            while len(seguidores_unicos) < limite_max:
                scroll_count += 1
                count_anterior = len(seguidores_unicos)
                elementos = driver.find_elements(By.CSS_SELECTOR, "div[role='dialog'] a[href^='/']:not([href='/'])")
                for elemento in elementos:
                    link = elemento.get_attribute("href")
                    total_links_procesados += 1
                    username = limpiar_username(link)
                    if username and es_username_valido(username, usuario_objetivo):
                        seguidores_unicos.add(username)
                    else:
                        links_filtrados += 1
                nuevos_encontrados = len(seguidores_unicos) - count_anterior
                if nuevos_encontrados == 0:
                    sin_nuevos_seguidores += 1
                else:
                    sin_nuevos_seguidores = 0
                if sin_nuevos_seguidores >= MAX_SIN_NUEVOS:
                    break
                modal_containers = driver.find_elements(By.CSS_SELECTOR, "div[role='dialog']")
                if modal_containers:
                    driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight;",
                        modal_containers[0]
                    )
                else:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)
            if seguidores_unicos:
                return seguidores_unicos
        except Exception as e:
            if intento_carga < max_intentos_carga - 1:
                sleep(5)
                continue
    return set()
