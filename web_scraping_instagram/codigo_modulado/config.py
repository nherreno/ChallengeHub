"""
Configuración y constantes del proyecto
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Credenciales de Instagram
USERNAME = "nico.proyecx6@gmail.com"
PASSWORD = os.getenv('PASSWORD')

# Configuración del WebDriver
CHROMEDRIVER_PATH = "C:\\Users\\User\\OneDrive - Universidad Nacional de Colombia\\Escritorio\\codigo_Prueba\\chromedriver\\chromedriver-win64\\chromedriver.exe"

# Configuración de scraping
DEFAULT_LIMIT = 100
MAX_LOAD_ATTEMPTS = 2
MAX_BUTTON_ATTEMPTS = 3
MAX_SCROLLS_WITHOUT_NEW = 5

# User Agent para Chrome
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/136.0.0.0 Safari/537.36"

# Páginas especiales de Instagram a excluir
SPECIAL_PAGES = {
    'explore', 'reels', 'tv', 'stories', 'accounts', 'direct', 'about',
    'followers', 'following', 'inbox', 'locations', 'lite',
    'help', 'legal', 'privacy', 'safety', 'api', 'blog',
    'business', 'community', 'developers', 'support', 'press',
    'careers', 'brand', 'download', 'create', 'features',
    '?entrypoint=web_footer', 'entrypoint=web_footer'
}

# Selectores CSS para encontrar seguidores
FOLLOWER_SELECTORS = [
    "div[role='dialog'] a[href^='/']:not([href='/'])",
    "[role='dialog'] a[href*='/']:not([href='/'])",
    "div[style*='overflow'] a[href^='/']:not([href='/'])",
    "a[href^='/']:not([href='/'])",
]

# Estrategias para encontrar el botón de seguidores
FOLLOWER_BUTTON_STRATEGIES = [
    (By.XPATH, "//a[contains(@href, '/followers/')]"),
    (By.XPATH, "//a[contains(text(), 'followers') or contains(text(), 'seguidores')]"),
    (By.XPATH, "//header//ul/li[2]//a"),
    (By.XPATH, "(//header//ul/li//a)[2]"),
    (By.CSS_SELECTOR, "header ul li:nth-child(2) a"),
    (By.XPATH, "//section/main/div/header//ul/li[2]/div/a"),
]

# Configuración de archivos de salida
OUTPUT_FOLDER = "resultados"
EXCEL_COLUMN_WIDTHS = [8, 20, 35, 20, 18]
STATS_COLUMN_WIDTHS = [35, 25]