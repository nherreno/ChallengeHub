##codigo en proceso no usar aun##


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import random
import logging
from typing import List, Dict, Optional
import re

class InstagramFollowersScraper:
    """Scraper de seguidores de Instagram usando Selenium"""
    
    def __init__(self, headless: bool = False):
        """
        Inicializa el scraper
        
        Args:
            headless: Si True, ejecuta Chrome sin interfaz gráfica
        """
        self.driver = None
        self.wait = None
        self.headless = headless
        self.setup_logging()
        self.setup_driver()
    
    def setup_logging(self):
        """Configura logging básico"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self):
        """Configura el driver de Chrome"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # Opciones para evitar detección
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 10)
            self.logger.info("Driver de Chrome inicializado correctamente")
        except Exception as e:
            self.logger.error(f"Error al inicializar Chrome driver: {e}")
            raise
    
    def navigate_to_profile(self, username: str) -> bool:
        """
        Navega al perfil de Instagram
        
        Args:
            username: Username de Instagram (sin @)
            
        Returns:
            True si navegó correctamente, False si error
        """
        try:
            url = f"https://www.instagram.com/{username}/"
            self.logger.info(f"Navegando a: {url}")
            
            self.driver.get(url)
            self.random_delay(2, 4)
            
            # Verificar que el perfil existe
            try:
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
                self.logger.info("Perfil cargado correctamente")
                return True
            except TimeoutException:
                self.logger.error(f"El perfil {username} no se pudo cargar o no existe")
                return False
                
        except Exception as e:
            self.logger.error(f"Error navegando al perfil: {e}")
            return False
    
    def click_followers_button(self) -> bool:
        """
        Hace clic en el botón de seguidores
        
        Returns:
            True si hizo clic correctamente, False si error
        """
        try:
            # Buscar el botón de seguidores - múltiples selectores posibles
            followers_selectors = [
                "a[href*='/followers/']",
                "//a[contains(@href, '/followers/')]",
                "//span[contains(text(), 'followers')]/parent::*",
                "//span[contains(text(), 'seguidores')]/parent::*"
            ]
            
            followers_button = None
            
            for selector in followers_selectors:
                try:
                    if selector.startswith('//'):
                        followers_button = self.driver.find_element(By.XPATH, selector)
                    else:
                        followers_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if not followers_button:
                self.logger.error("No se pudo encontrar el botón de seguidores")
                return False
            
            # Hacer scroll hasta el elemento
            self.driver.execute_script("arguments[0].scrollIntoView();", followers_button)
            self.random_delay(1, 2)
            
            # Hacer clic
            followers_button.click()
            self.logger.info("Clic en botón de seguidores realizado")
            
            # Esperar a que se abra el modal
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role='dialog']")))
            self.random_delay(2, 3)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error haciendo clic en seguidores: {e}")
            return False
    
    def scroll_followers_modal(self, limit: Optional[int] = None) -> List:
        """
        Hace scroll en el modal de seguidores para cargar todos
        
        Args:
            limit: Número máximo de seguidores a cargar
            
        Returns:
            Lista de elementos de seguidores
        """
        try:
            # Encontrar el contenedor del modal
            modal_selectors = [
                "[role='dialog'] div[style*='overflow']",
                "[role='dialog'] div[class*='scroll']",
                "[role='dialog'] > div > div > div:nth-child(2)"
            ]
            
            scroll_container = None
            for selector in modal_selectors:
                try:
                    scroll_container = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if not scroll_container:
                self.logger.warning("No se encontró contenedor de scroll, usando body")
                scroll_container = self.driver.find_element(By.TAG_NAME, "body")
            
            followers_loaded = 0
            last_height = 0
            no_change_count = 0
            
            self.logger.info("Iniciando scroll para cargar seguidores...")
            
            while True:
                # Hacer scroll hacia abajo en el modal
                self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight;", 
                    scroll_container
                )
                
                self.random_delay(1, 2)
                
                # Contar seguidores actuales
                current_followers = self.driver.find_elements(
                    By.CSS_SELECTOR, 
                    "[role='dialog'] div[class*='x1dm5mii'] div[class*='x9f619']"
                )
                
                new_followers_count = len(current_followers)
                
                # Verificar si se cargaron nuevos seguidores
                if new_followers_count > followers_loaded:
                    followers_loaded = new_followers_count
                    no_change_count = 0
                    self.logger.info(f"Seguidores cargados: {followers_loaded}")
                    
                    # Verificar límite
                    if limit and followers_loaded >= limit:
                        self.logger.info(f"Límite alcanzado: {limit}")
                        break
                else:
                    no_change_count += 1
                
                # Si no hay cambios después de varios intentos, terminar
                if no_change_count >= 3:
                    self.logger.info("No se cargan más seguidores, terminando scroll")
                    break
                
                # Verificar height del scroll
                current_height = self.driver.execute_script(
                    "return arguments[0].scrollHeight;", scroll_container
                )
                
                if current_height == last_height:
                    no_change_count += 1
                else:
                    last_height = current_height
            
            # Obtener elementos finales
            followers_elements = self.driver.find_elements(
                By.CSS_SELECTOR,
                "[role='dialog'] div[class*='x1dm5mii'] div[class*='x9f619']"
            )
            
            if limit:
                followers_elements = followers_elements[:limit]
            
            self.logger.info(f"Total de seguidores encontrados: {len(followers_elements)}")
            return followers_elements
            
        except Exception as e:
            self.logger.error(f"Error durante el scroll: {e}")
            return []
    
    def extract_follower_data(self, follower_element) -> Dict:
        """
        Extrae datos de un elemento de seguidor
        
        Args:
            follower_element: Elemento HTML del seguidor
            
        Returns:
            Diccionario con datos del seguidor
        """
        try:
            follower_data = {
                'username': None,
                'full_name': None,
                'bio': None,
                'followers_count': None,
                'following_count': None,
                'posts_count': None,
                'is_verified': False,
                'is_private': False,
                'profile_pic_url': None,
                'created_date': None,
                'first_post': None,
                'last_post': None
            }
            
            # Extraer username
            try:
                username_element = follower_element.find_element(
                    By.CSS_SELECTOR, 
                    "a[role='link'] span, a[role='link'] div"
                )
                follower_data['username'] = username_element.text.strip()
            except NoSuchElementException:
                pass
            
            # Extraer nombre completo
            try:
                name_elements = follower_element.find_elements(
                    By.CSS_SELECTOR, 
                    "span, div"
                )
                for element in name_elements:
                    text = element.text.strip()
                    if text and text != follower_data['username'] and len(text) > 1:
                        if not any(char in text for char in ['@', '#', 'following', 'followers']):
                            follower_data['full_name'] = text
                            break
            except NoSuchElementException:
                pass
            
            # Extraer foto de perfil
            try:
                img_element = follower_element.find_element(By.CSS_SELECTOR, "img")
                follower_data['profile_pic_url'] = img_element.get_attribute('src')
            except NoSuchElementException:
                pass
            
            # Verificar si está verificado (blue checkmark)
            try:
                follower_element.find_element(By.CSS_SELECTOR, "[data-testid='verified-icon']")
                follower_data['is_verified'] = True
            except NoSuchElementException:
                pass
            
            # Verificar si es privado
            try:
                follower_element.find_element(By.CSS_SELECTOR, "[data-testid='private-icon']")
                follower_data['is_private'] = True
            except NoSuchElementException:
                pass
            
            return follower_data
            
        except StaleElementReferenceException:
            self.logger.warning("Elemento obsoleto, saltando...")
            return None
        except Exception as e:
            self.logger.error(f"Error extrayendo datos del seguidor: {e}")
            return None
    
    def scrape_followers(self, username: str, limit: Optional[int] = None) -> List[Dict]:
        """
        Método principal para extraer seguidores
        
        Args:
            username: Username de Instagram
            limit: Número máximo de seguidores a extraer
            
        Returns:
            Lista de diccionarios con datos de seguidores
        """
        try:
            self.logger.info(f"Iniciando scraping de seguidores de @{username}")
            
            # Paso 1: Navegar al perfil
            if not self.navigate_to_profile(username):
                return []
            
            # Paso 2: Hacer clic en seguidores
            if not self.click_followers_button():
                return []
            
            # Paso 3: Cargar todos los seguidores
            followers_elements = self.scroll_followers_modal(limit)
            
            if not followers_elements:
                self.logger.warning("No se encontraron elementos de seguidores")
                return []
            
            # Paso 4: Extraer datos de cada seguidor
            followers_data = []
            
            self.logger.info("Extrayendo datos de seguidores...")
            
            for i, element in enumerate(followers_elements):
                try:
                    follower_data = self.extract_follower_data(element)
                    
                    if follower_data and follower_data['username']:
                        followers_data.append(follower_data)
                        
                        if (i + 1) % 50 == 0:
                            self.logger.info(f"Procesados {i + 1}/{len(followers_elements)} seguidores")
                    
                    # Delay pequeño entre extracciones
                    if i % 10 == 0:
                        self.random_delay(0.5, 1)
                        
                except Exception as e:
                    self.logger.error(f"Error procesando seguidor {i}: {e}")
                    continue
            
            self.logger.info(f"Extracción completada: {len(followers_data)} seguidores extraídos")
            return followers_data
            
        except Exception as e:
            self.logger.error(f"Error general en scraping: {e}")
            return []
    
    def random_delay(self, min_seconds: float, max_seconds: float):
        """Genera delay aleatorio para parecer más humano"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def close(self):
        """Cierra el driver"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Driver cerrado")

# Función de uso simplificado
def extract_instagram_followers_selenium(username: str, 
                                       limit: Optional[int] = None,
                                       headless: bool = False) -> List[Dict]:
    """
    Función simplificada para extraer seguidores con Selenium
    
    Args:
        username: Username de Instagram (sin @)
        limit: Número máximo de seguidores a extraer
        headless: Si True, ejecuta sin interfaz gráfica
        
    Returns:
        Lista de diccionarios con datos de seguidores
    """
    scraper = None
    try:
        scraper = InstagramFollowersScraper(headless=headless)
        followers = scraper.scrape_followers(username, limit)
        return followers
    except Exception as e:
        print(f"Error en extracción: {e}")
        return []
    finally:
        if scraper:
            scraper.close()

# Ejemplo de uso
if __name__ == "__main__":
    # Extraer seguidores de una cuenta
    username = "cocacola"
    max_followers = 100
    
    print(f"🚀 Extrayendo seguidores de @{username}...")
    
    followers = extract_instagram_followers_selenium(
        username=username,
        limit=max_followers,
        headless=False  # Cambiar a True para modo sin ventana
    )
    
    print(f"✅ Extraídos {len(followers)} seguidores")
    
    # Mostrar algunos ejemplos
    for i, follower in enumerate(followers[:3]):
        print(f"\n👤 Seguidor {i+1}:")
        print(f"  Username: {follower['username']}")
        print(f"  Nombre: {follower['full_name']}")
        print(f"  Verificado: {follower['is_verified']}")
        print(f"  Privado: {follower['is_private']}")
        
