import re
from config import SPECIAL_PAGES

def es_username_valido(username, usuario_objetivo):
    if not username or len(username) == 0:
        return False
    username_clean = username.lower().strip()
    if username_clean in SPECIAL_PAGES:
        return False
    if '?' in username or '&' in username or '=' in username:
        return False
    patron_id_temporal = re.compile(r'^[A-Z]{2,3}[A-Za-z0-9_-]{6,}$')
    if patron_id_temporal.match(username):
        return False
    if username.isdigit():
        return False
    if len(username) < 1 or len(username) > 30:
        return False
    if re.match(r'^[._-]+$', username):
        return False
    if username.startswith('.') or username.endswith('.'):
        return False
    if ' ' in username:
        return False
    patron_valido = re.compile(r'^[a-zA-Z0-9._]+$')
    if not patron_valido.match(username):
        return False
    if username.lower() == usuario_objetivo.lower():
        return False
    return True

def limpiar_username(link):
    try:
        if not link or not isinstance(link, str):
            return None
        if 'instagram.com/' in link:
            username = link.split('instagram.com/')[-1]
        else:
            username = link
        username = username.rstrip('/').split('?')[0].split('&')[0]
        if '/' in username:
            username = username.split('/')[0]
        return username.strip()
    except:
        return None
