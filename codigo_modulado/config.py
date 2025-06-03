"""
Configuración y constantes del proyecto
"""
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

USERNAME = 'mille_i2025'
PASSWORD = os.getenv('PASSWORD')
CHROMEDRIVER_PATH = "C:\\Users\\User\\OneDrive - Universidad Nacional de Colombia\\Escritorio\\codigo_Prueba\\chromedriver\\chromedriver-win64\\chromedriver.exe"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/136.0.0.0 Safari/537.36"
MAX_SCROLLS = 2
MAX_SIN_NUEVOS = 5
LIMITE_MAX = 2000

SPECIAL_PAGES = {
    'explore', 'reels', 'tv', 'stories', 'accounts', 'direct', 'about',
    'followers', 'following', 'inbox', 'locations', 'lite',
    'help', 'legal', 'privacy', 'safety', 'api', 'blog',
    'business', 'community', 'developers', 'support', 'press',
    'careers', 'brand', 'download', 'create', 'features',
    '?entrypoint=web_footer', 'entrypoint=web_footer'
}
