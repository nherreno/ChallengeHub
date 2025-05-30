"""
Utilidades para validar y limpiar usernames de Instagram
"""
import re
from config import SPECIAL_PAGES


class UsernameValidator:
    @staticmethod
    def es_username_valido(username, usuario_objetivo=None):
        """
        Valida si un username es válido según las reglas de Instagram
        """
        if not username or len(username) == 0:
            return False
        
        # Normalizar username
        username_clean = username.lower().strip()
        
        # 1. Verificar si es una página especial
        if username_clean in SPECIAL_PAGES:
            return False
        
        # 2. Verificar si contiene parámetros de URL
        if '?' in username or '&' in username or '=' in username:
            return False
        
        # 3. Verificar patrones de IDs temporales
        patron_id_temporal = re.compile(r'^[A-Z]{2,3}[A-Za-z0-9_-]{6,}$')
        if patron_id_temporal.match(username):
            return False
        
        # 4. Verificar usernames que son solo números
        if username.isdigit():
            return False
        
        # 5. Verificar longitud (Instagram permite 1-30 caracteres)
        if len(username) < 1 or len(username) > 30:
            return False
        
        # 6. Verificar que no contenga solo caracteres especiales
        if re.match(r'^[._-]+$', username):
            return False
        
        # 7. Verificar que no empiece o termine con punto
        if username.startswith('.') or username.endswith('.'):
            return False
        
        # 8. Verificar que no contenga espacios
        if ' ' in username:
            return False
        
        # 9. Verificar caracteres válidos para Instagram
        patron_valido = re.compile(r'^[a-zA-Z0-9._]+$')
        if not patron_valido.match(username):
            return False
        
        # 10. Verificar que no sea el propio usuario objetivo
        if usuario_objetivo and username.lower() == usuario_objetivo.lower():
            return False
        
        return True
    
    @staticmethod
    def limpiar_username(link):
        """
        Extrae y limpia el username de un enlace de Instagram
        """
        try:
            if not link or not isinstance(link, str):
                return None
            
            # Remover protocolo y dominio si están presentes
            if 'instagram.com/' in link:
                username = link.split('instagram.com/')[-1]
            else:
                username = link
            
            # Remover barra final y parámetros
            username = username.rstrip('/').split('?')[0].split('&')[0]
            
            # Remover barras adicionales
            if '/' in username:
                username = username.split('/')[0]
            
            return username.strip()
        except:
            return None
    
    @staticmethod
    def validar_entrada_usuario(usuario_input):
        """
        Valida y limpia la entrada del usuario
        """
        if not usuario_input:
            return None, "Debes ingresar un nombre de usuario válido"
        
        usuario_limpio = usuario_input.strip()
        
        # Remover @ si lo incluyó el usuario
        if usuario_limpio.startswith('@'):
            usuario_limpio = usuario_limpio[1:]
        
        if not usuario_limpio:
            return None, "Nombre de usuario vacío después de limpiar"
        
        return usuario_limpio, None