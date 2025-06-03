from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random
from bs4 import BeautifulSoup

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
