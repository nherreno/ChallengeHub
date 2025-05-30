"""
Lógica principal para el scraping de seguidores de Instagram
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random
from config import FOLLOWER_BUTTON_STRATEGIES, FOLLOWER_SELECTORS, MAX_SCROLLS_WITHOUT_NEW
from username_validator import UsernameValidator


class InstagramScraper:
    def __init__(self, driver):
        self.driver = driver
        self.validator = UsernameValidator()
    
    def obtener_fecha_union(self, username):
        """Obtiene la fecha de unión de un usuario a Instagram"""
        try:
            perfil_url = f"https://www.instagram.com/{username}/"
            print(f"📅 Obteniendo fecha de unión de @{username}...")
            self.driver.get(perfil_url)
            sleep(random.uniform(2, 3))

            # Buscar el botón de opciones
            boton_opciones = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@aria-label='Options' or @aria-label='Opciones']")
                )
            )
            boton_opciones.click()
            sleep(random.uniform(1.5, 2.5))

            # Buscar la fecha de unión
            fecha_xpath = "//span[contains(text(),'Fecha en la que te uniste')]/following-sibling::span"
            fecha_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, fecha_xpath))
            )
            fecha = fecha_element.text
            
            # Cerrar el menú
            self.driver.execute_script("document.body.click();")
            sleep(1)
            
            return fecha
        except Exception as e:
            print(f"⚠️ No se pudo obtener fecha de @{username}: {str(e)[:50]}...")
            
            try:
                self.driver.execute_script("document.body.click();")
                sleep(1)
            except:
                pass
                
            return "Fecha no encontrada"
    
    def encontrar_boton_seguidores(self, usuario_objetivo, max_intentos=3):
        """Intenta encontrar el botón de seguidores usando diferentes estrategias"""
        for intento in range(max_intentos):
            print(f"\n🔄 Intento {intento + 1}/{max_intentos} para encontrar botón de seguidores")
            
            # Si no es el primer intento, volver al perfil
            if intento > 0:
                print("🔄 Volviendo al perfil antes del nuevo intento...")
                self.driver.get(f'https://www.instagram.com/{usuario_objetivo}/')
                sleep(random.uniform(4, 6))
            
            # Intentar cada estrategia
            for i, (by, selector) in enumerate(FOLLOWER_BUTTON_STRATEGIES, 1):
                try:
                    print(f"Intentando estrategia {i}: {selector}")
                    element = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((by, selector))
                    )
                    
                    # Verificar que el elemento sea de seguidores
                    href = element.get_attribute('href')
                    text = element.text
                    if href and 'followers' in href:
                        print(f"✅ Estrategia {i} exitosa. Elemento encontrado: {text}")
                        return element
                    elif 'followers' in text.lower() or 'seguidores' in text.lower():
                        print(f"✅ Estrategia {i} exitosa por texto. Elemento encontrado: {text}")
                        return element
                except Exception as e:
                    print(f"❌ Estrategia {i} falló: {str(e)[:100]}")
                    continue
            
            print(f"❌ Intento {intento + 1} fallido. Todas las estrategias fallaron.")
            if intento < max_intentos - 1:
                sleep(random.uniform(5, 8))
        
        return None
    
    def cargar_seguidores_completo(self, usuario, limite_max=2000, max_intentos_carga=2):
        """Carga seguidores completos con fechas de unión"""
        print(f"📜 Iniciando carga de seguidores de @{usuario} (límite: {limite_max})...")
        
        for intento_carga in range(max_intentos_carga):
            print(f"\n🔄 Intento de carga {intento_carga + 1}/{max_intentos_carga}")
            
            # Si no es el primer intento, volver al inicio
            if intento_carga > 0:
                print("🔄 Navegando directamente a followers...")
                self.driver.get(f"https://www.instagram.com/{usuario}/followers/")
                sleep(random.uniform(4, 6))
            
            seguidores_unicos = dict()
            usernames_temporales = set()
            scroll_count = 0
            sin_nuevos_seguidores = 0
            
            # Contadores para estadísticas
            total_links_procesados = 0
            links_filtrados = 0
            
            # Esperar modal de seguidores
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "[role='dialog'], div[style*='overflow-y']")
                    )
                )
                print("✅ Modal de seguidores detectado")
            except:
                print("⚠️ Modal no detectado, continuando...")
                if intento_carga < max_intentos_carga - 1:
                    continue
            
            try:
                # Fase 1: Recolectar usernames
                print("🔍 Fase 1: Recolectando usernames de seguidores...")
                
                while len(usernames_temporales) < limite_max:
                    scroll_count += 1
                    count_anterior = len(usernames_temporales)
                    
                    print(f"🔄 Scroll #{scroll_count} - Usernames encontrados: {len(usernames_temporales)}")
                    
                    # Buscar nuevos seguidores
                    elementos_encontrados = []
                    for selector in FOLLOWER_SELECTORS:
                        try:
                            elementos = self.driver.find_elements(By.CSS_SELECTOR, selector)
                            if elementos:
                                elementos_encontrados.extend(elementos)
                        except Exception:
                            continue
                    
                    # Remover duplicados
                    elementos_unicos = []
                    hrefs_vistos = set()
                    for elemento in elementos_encontrados:
                        href = elemento.get_attribute("href")
                        if href and href not in hrefs_vistos:
                            hrefs_vistos.add(href)
                            elementos_unicos.append(elemento)
                    
                    # Procesar elementos
                    for elemento in elementos_unicos:
                        if len(usernames_temporales) >= limite_max:
                            break
                            
                        try:
                            link = elemento.get_attribute("href")
                            total_links_procesados += 1
                            
                            if link:
                                username = self.validator.limpiar_username(link)
                                
                                if username and self.validator.es_username_valido(username, usuario):
                                    if username not in usernames_temporales:
                                        usernames_temporales.add(username)
                                        if len(usernames_temporales) % 50 == 0:
                                            print(f"✅ Encontrado: @{username} (Total: {len(usernames_temporales)})")
                                else:
                                    links_filtrados += 1
                                    
                        except Exception:
                            continue
                    
                    # Verificar progreso
                    nuevos_encontrados = len(usernames_temporales) - count_anterior
                    if nuevos_encontrados == 0:
                        sin_nuevos_seguidores += 1
                        print(f"⚠️ No se encontraron nuevos seguidores válidos ({sin_nuevos_seguidores}/{MAX_SCROLLS_WITHOUT_NEW})")
                    else:
                        sin_nuevos_seguidores = 0
                        print(f"✅ Encontrados {nuevos_encontrados} nuevos seguidores válidos")
                    
                    # Parar si no hay nuevos seguidores
                    if sin_nuevos_seguidores >= MAX_SCROLLS_WITHOUT_NEW:
                        print(f"🛑 Deteniendo después de {MAX_SCROLLS_WITHOUT_NEW} intentos sin nuevos seguidores")
                        break
                    
                    # Scroll en el modal
                    try:
                        modal_containers = self.driver.find_elements(By.CSS_SELECTOR, "div[role='dialog']")
                        if modal_containers:
                            self.driver.execute_script(
                                "arguments[0].scrollTop = arguments[0].scrollHeight;", 
                                modal_containers[0]
                            )
                        else:
                            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    except Exception as e:
                        print(f"⚠️ Error en scroll: {e}")
                    
                    sleep(random.uniform(2, 4))
                
                # Fase 2: Obtener fechas de unión
                print(f"\n📅 Fase 2: Obteniendo fechas de unión para {len(usernames_temporales)} usuarios...")
                
                # Cerrar modal
                try:
                    self.driver.execute_script("document.body.click();")
                    sleep(2)
                except:
                    pass
                
                # Procesar fechas
                usernames_lista = list(usernames_temporales)
                for i, username in enumerate(usernames_lista, 1):
                    print(f"📅 Procesando {i}/{len(usernames_lista)}: @{username}")
                    fecha = self.obtener_fecha_union(username)
                    seguidores_unicos[username] = fecha
                    sleep(random.uniform(1, 2))
                    
                    if i % 10 == 0:
                        print(f"📊 Progreso fechas: {i}/{len(usernames_lista)} completados")
                
                # Resultado exitoso
                if seguidores_unicos:
                    print(f"✅ Carga exitosa en intento {intento_carga + 1}")
                    self._mostrar_estadisticas_carga(total_links_procesados, links_filtrados, seguidores_unicos)
                    return seguidores_unicos
                    
            except Exception as e:
                print(f"❌ Error durante la carga en intento {intento_carga + 1}: {e}")
                if intento_carga < max_intentos_carga - 1:
                    print("🔄 Reintentando desde el inicio...")
                    sleep(random.uniform(5, 8))
                    continue
        
        print(f"❌ No se pudo cargar seguidores después de {max_intentos_carga} intentos")
        return dict()
    
    def _mostrar_estadisticas_carga(self, total_links, links_filtrados, seguidores_data):
        """Muestra estadísticas de la carga"""
        fechas_exitosas = len([f for f in seguidores_data.values() if f != 'Fecha no encontrada'])
        
        print(f"📊 ESTADÍSTICAS FINALES:")
        print(f"   - Total links procesados: {total_links}")
        print(f"   - Links filtrados (no válidos): {links_filtrados}")
        print(f"   - Seguidores válidos encontrados: {len(seguidores_data)}")
        print(f"   - Fechas de unión obtenidas: {fechas_exitosas}")
        tasa_filtrado = (links_filtrados/total_links*100) if total_links > 0 else 0
        print(f"   - Tasa de filtrado: {tasa_filtrado:.1f}%")