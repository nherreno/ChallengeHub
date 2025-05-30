from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import random
import re

# Cargar variables de entorno
load_dotenv()

USERNAME = "nico.proyecx6@gmail.com"
PASSWORD = os.getenv('PASSWORD')

# Solicitar el usuario a revisar
print("🔍 INSTAGRAM ACCOUNT CREATION DATE CHECKER")
print("="*50)
usuario_objetivo = input("👤 Ingresa el nombre de usuario de Instagram a revisar (sin @): ").strip()

# Validar entrada
if not usuario_objetivo:
    print("❌ Error: Debes ingresar un nombre de usuario válido")
    exit()

# Remover @ si lo incluyó el usuario
if usuario_objetivo.startswith('@'):
    usuario_objetivo = usuario_objetivo[1:]

print(f"🎯 Revisando fecha de creación de: @{usuario_objetivo}")
print("="*50)

# Ruta del chromedriver (ajustar según tu sistema)
chromedriver_path = "C:\\Users\\User\\OneDrive - Universidad Nacional de Colombia\\Escritorio\\codigo_Prueba\\chromedriver\\chromedriver-win64\\chromedriver.exe"

def obtener_fecha_creacion_cuenta(driver, username):
    """
    Obtiene la fecha de creación de una cuenta de Instagram
    """
    try:
        print(f"📅 Obteniendo fecha de creación de @{username}...")
        
        # Navegar al perfil
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
        
        # DEBUG: Imprimir elementos SVG encontrados
        print("🔍 DEBUG: Buscando todos los elementos SVG en el header...")
        try:
            svg_elements = driver.find_elements(By.XPATH, "//header//svg")
            print(f"📊 Encontrados {len(svg_elements)} elementos SVG en el header")
            
            for i, svg in enumerate(svg_elements):
                try:
                    aria_label = svg.get_attribute('aria-label') or 'Sin aria-label'
                    parent_class = svg.find_element(By.XPATH, "..").get_attribute('class') or 'Sin clase'
                    print(f"  SVG {i+1}: aria-label='{aria_label}', parent_class='{parent_class[:50]}'")
                except:
                    print(f"  SVG {i+1}: Error obteniendo atributos")
        except Exception as e:
            print(f"❌ Error en debug de SVG: {e}")
        
        # DEBUG: Buscar botones en el header
        print("🔍 DEBUG: Buscando botones en el header...")
        try:
            buttons = driver.find_elements(By.XPATH, "//header//button")
            print(f"📊 Encontrados {len(buttons)} botones en el header")
            
            for i, btn in enumerate(buttons):
                try:
                    aria_label = btn.get_attribute('aria-label') or 'Sin aria-label'
                    class_name = btn.get_attribute('class') or 'Sin clase'
                    print(f"  Botón {i+1}: aria-label='{aria_label}', class='{class_name[:50]}'")
                except:
                    print(f"  Botón {i+1}: Error obteniendo atributos")
        except Exception as e:
            print(f"❌ Error en debug de botones: {e}")
        
        # Buscar el botón de opciones con múltiples estrategias
        try:
            print("🔍 Buscando botón de opciones...")
            
            # Estrategias más amplias para encontrar el botón de opciones
            estrategias_opciones = [
                # Estrategia 1: Por aria-label
                ("Por aria-label 'Options'", "//button[@aria-label='Options']"),
                ("Por aria-label 'Opciones'", "//button[@aria-label='Opciones']"),
                ("Por aria-label que contenga 'option'", "//button[contains(@aria-label, 'ption')]"),
                
                # Estrategia 2: Por SVG específicos
                ("SVG con tres puntos", "//svg[contains(@aria-label, 'Options')]//parent::button"),
                ("SVG con tres puntos v2", "//svg[contains(@aria-label, 'Opciones')]//parent::button"),
                
                # Estrategia 3: Por posición en el header
                ("Último botón del header", "//header//button[last()]"),
                ("Penúltimo botón del header", "//header//button[last()-1]"),
                
                # Estrategia 4: Por div clickeable
                ("Div role button en header", "//header//div[@role='button']"),
                
                # Estrategia 5: Botones sin aria-label específico
                ("Botones sin texto visible", "//header//button[not(text())]"),
                
                # Estrategia 6: Tu XPath original modificado
                ("XPath específico original", '//*[@id="mount_0_0_9l"]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[2]/div/div/div[3]/div/div/svg/..'),
                
                # Estrategia 7: Búsqueda más genérica
                ("Elementos clickeables en header", "//header//*[@role='button' or @tabindex='0']")
            ]
            
            boton_opciones = None
            for descripcion, selector in estrategias_opciones:
                try:
                    print(f"🔍 Probando: {descripcion}")
                    elementos = driver.find_elements(By.XPATH, selector)
                    
                    if elementos:
                        print(f"  ✅ Encontrados {len(elementos)} elementos")
                        # Intentar con cada elemento encontrado
                        for i, elemento in enumerate(elementos):
                            try:
                                # Verificar si es clickeable
                                if elemento.is_displayed() and elemento.is_enabled():
                                    boton_opciones = elemento
                                    print(f"  🎯 Elemento {i+1} es clickeable, usando este")
                                    break
                            except:
                                continue
                        
                        if boton_opciones:
                            break
                    else:
                        print(f"  ❌ No encontrado")
                        
                except Exception as e:
                    print(f"  ❌ Error: {str(e)[:50]}...")
                    continue
            
            if not boton_opciones:
                print(f"❌ No se pudo encontrar el botón de opciones para @{username}")
                print("💡 Intentando hacer screenshot para debug...")
                try:
                    driver.save_screenshot(f"debug_{username}.png")
                    print(f"📷 Screenshot guardado como debug_{username}.png")
                except:
                    pass
                return None
            
            print("🖱️ Haciendo clic en opciones...")
            # Scroll al elemento primero
            driver.execute_script("arguments[0].scrollIntoView(true);", boton_opciones)
            sleep(1)
            
            # Intentar clic normal primero, luego JavaScript
            try:
                boton_opciones.click()
            except:
                print("🔄 Clic normal falló, intentando con JavaScript...")
                driver.execute_script("arguments[0].click();", boton_opciones)
            
            sleep(random.uniform(3, 5))
            print("✅ Clic en opciones realizado")
            
        except Exception as e:
            print(f"❌ Error al hacer clic en opciones: {str(e)[:50]}...")
            return None

        # DEBUG: Ver qué modal se abrió
        print("🔍 DEBUG: Analizando modal abierto...")
        try:
            # Buscar cualquier modal o dialog abierto
            modals = driver.find_elements(By.XPATH, "//div[@role='dialog']")
            if modals:
                print(f"📊 Encontrados {len(modals)} modals abiertos")
                for i, modal in enumerate(modals):
                    try:
                        buttons_in_modal = modal.find_elements(By.TAG_NAME, "button")
                        print(f"  Modal {i+1}: {len(buttons_in_modal)} botones")
                        for j, btn in enumerate(buttons_in_modal):
                            try:
                                text = btn.text.strip() or 'Sin texto'
                                aria_label = btn.get_attribute('aria-label') or 'Sin aria-label'
                                print(f"    Botón {j+1}: '{text}' | aria-label: '{aria_label}'")
                            except:
                                print(f"    Botón {j+1}: Error obteniendo texto")
                    except:
                        print(f"  Modal {i+1}: Error analizando botones")
            else:
                print("❌ No se encontraron modals abiertos")
                
        except Exception as e:
            print(f"❌ Error en debug de modal: {e}")

        # Buscar el botón "Información de esta cuenta" con estrategias mejoradas
        try:
            print("🔍 Buscando botón 'Información de esta cuenta'...")
            
            # Estrategias para encontrar el botón de información
            estrategias_info = [
                # Texto exacto
                ("Texto 'Información de esta cuenta'", "//button[contains(text(), 'Información de esta cuenta')]"),
                ("Texto 'About this account'", "//button[contains(text(), 'About this account')]"),
                
                # Por posición en modal
                ("Botón 5 en dialog", "//div[@role='dialog']//button[5]"),
                ("Botón 4 en dialog", "//div[@role='dialog']//button[4]"),
                ("Botón 6 en dialog", "//div[@role='dialog']//button[6]"),
                
                # Tu XPath específico y variaciones
                ("XPath específico original", "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/button[5]"),
                ("XPath div[5]", "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div/button[5]"),
                ("XPath div[7]", "/html/body/div[7]/div[1]/div/div[2]/div/div/div/div/div/button[5]"),
                
                # Búsqueda más genérica
                ("Botones que contengan 'cuenta'", "//button[contains(text(), 'cuenta')]"),
                ("Botones que contengan 'account'", "//button[contains(text(), 'account')]"),
                ("Botones que contengan 'información'", "//button[contains(text(), 'información')]"),
                ("Botones que contengan 'about'", "//button[contains(text(), 'about')]"),
                
                # Por aria-label
                ("Aria-label información", "//button[contains(@aria-label, 'información')]"),
                ("Aria-label about", "//button[contains(@aria-label, 'about')]"),
            ]
            
            boton_info = None
            for descripcion, selector in estrategias_info:
                try:
                    print(f"🔍 Probando: {descripcion}")
                    elementos = driver.find_elements(By.XPATH, selector)
                    
                    if elementos:
                        print(f"  ✅ Encontrados {len(elementos)} elementos")
                        for i, elemento in enumerate(elementos):
                            try:
                                if elemento.is_displayed() and elemento.is_enabled():
                                    texto = elemento.text.strip()
                                    aria_label = elemento.get_attribute('aria-label') or ''
                                    print(f"    Elemento {i+1}: '{texto}' | aria: '{aria_label}'")
                                    
                                    # Verificar si es el botón correcto
                                    if ('información' in texto.lower() or 'about' in texto.lower() or 
                                        'información' in aria_label.lower() or 'about' in aria_label.lower()):
                                        boton_info = elemento
                                        print(f"  🎯 Este parece ser el botón correcto")
                                        break
                            except:
                                continue
                        
                        if not boton_info and elementos:
                            # Si no encontramos el botón específico pero hay elementos, usar el primero
                            boton_info = elementos[0]
                            print(f"  🔄 Usando el primer elemento encontrado")
                        
                        if boton_info:
                            break
                    else:
                        print(f"  ❌ No encontrado")
                        
                except Exception as e:
                    print(f"  ❌ Error: {str(e)[:50]}...")
                    continue
            
            if not boton_info:
                print("❌ No se pudo encontrar el botón 'Información de esta cuenta'")
                print("💡 Intentando hacer screenshot del modal...")
                try:
                    driver.save_screenshot(f"modal_debug_{username}.png")
                    print(f"📷 Screenshot del modal guardado como modal_debug_{username}.png")
                except:
                    pass
                return None
            
            print("🖱️ Haciendo clic en 'Información de esta cuenta'...")
            
            # Scroll al elemento
            driver.execute_script("arguments[0].scrollIntoView(true);", boton_info)
            sleep(1)
            
            # Intentar clic
            try:
                boton_info.click()
            except:
                print("🔄 Clic normal falló, intentando con JavaScript...")
                driver.execute_script("arguments[0].click();", boton_info)
            
            sleep(random.uniform(3, 5))
            print("✅ Clic en información de cuenta realizado")
            
        except Exception as e:
            print(f"❌ Error al hacer clic en información de cuenta: {str(e)[:50]}...")
            return None

        # Buscar la fecha en el HTML usando múltiples estrategias
        try:
            print("📅 Buscando fecha en la información de la cuenta...")
            
            # Estrategia 1: Buscar por texto específico
            selectores_fecha = [
                "//span[contains(text(),'Fecha en la que te uniste')]/following-sibling::span",
                "//span[contains(text(),'Date joined')]/following-sibling::span",
                "//span[contains(text(),'Mayo de') or contains(text(), 'Enero de') or contains(text(), 'Febrero de') or contains(text(), 'Marzo de') or contains(text(), 'Abril de') or contains(text(), 'Junio de') or contains(text(), 'Julio de') or contains(text(), 'Agosto de') or contains(text(), 'Septiembre de') or contains(text(), 'Octubre de') or contains(text(), 'Noviembre de') or contains(text(), 'Diciembre de')]",
                "//*[contains(text(), 'uniste')]/..//span[contains(text(), '20')]",
                "//*[contains(text(), 'joined')]/..//span[contains(text(), '20')]"
            ]
            
            fecha = None
            
            # Intentar encontrar la fecha con los selectores
            for i, selector in enumerate(selectores_fecha):
                try:
                    print(f"🔍 Probando selector fecha {i+1}/{len(selectores_fecha)}...")
                    fecha_elements = driver.find_elements(By.XPATH, selector)
                    
                    for element in fecha_elements:
                        texto = element.text.strip()
                        if texto and len(texto) > 3 and ('de' in texto.lower() or any(month in texto.lower() for month in ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'])):
                            fecha = texto
                            print(f"✅ Fecha encontrada con selector {i+1}: {fecha}")
                            break
                    
                    if fecha:
                        break
                        
                except Exception as e:
                    print(f"❌ Selector fecha {i+1} falló: {str(e)[:30]}...")
                    continue
            
            # Estrategia 2: Buscar en todo el HTML de la página si no encontramos con selectores específicos
            if not fecha:
                print("🔍 Buscando fecha en todo el HTML de la página...")
                try:
                    page_source = driver.page_source
                    
                    # Patrones de fecha en español
                    patrones_fecha = [
                        r'(Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre)\s+de\s+\d{4}',
                        r'\b(Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre)\s+\d{4}\b',
                        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b'
                    ]
                    
                    for patron in patrones_fecha:
                        matches = re.findall(patron, page_source, re.IGNORECASE)
                        if matches:
                            if isinstance(matches[0], tuple):
                                fecha = ' '.join(matches[0])
                            else:
                                fecha = matches[0]
                            print(f"✅ Fecha encontrada en HTML: {fecha}")
                            break
                
                except Exception as e:
                    print(f"❌ Error buscando en HTML: {str(e)[:50]}...")
            
            # Estrategia 3: Obtener el outerHTML de elementos que contengan fechas
            if not fecha:
                print("🔍 Analizando outerHTML de elementos con fechas...")
                try:
                    # Buscar elementos que puedan contener la fecha
                    elementos_fecha = driver.find_elements(By.XPATH, "//*[contains(text(), '201') or contains(text(), '202')]")
                    
                    for elemento in elementos_fecha:
                        try:
                            outer_html = elemento.get_attribute('outerHTML')
                            texto = elemento.text.strip()
                            
                            if texto and len(texto) > 4 and any(month in texto.lower() for month in ['mayo', 'enero', 'febrero', 'marzo', 'abril', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre', 'may', 'january', 'february', 'march', 'april', 'june', 'july', 'august', 'september', 'october', 'november', 'december']):
                                fecha = texto
                                print(f"✅ Fecha encontrada en outerHTML: {fecha}")
                                print(f"📝 OuterHTML: {outer_html[:200]}...")
                                break
                                
                        except:
                            continue
                            
                except Exception as e:
                    print(f"❌ Error analizando outerHTML: {str(e)[:50]}...")
            
            if fecha and len(fecha) > 3:
                # Cerrar modales
                try:
                    # Intentar cerrar con ESC
                    from selenium.webdriver.common.keys import Keys
                    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                    sleep(1)
                    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                    sleep(1)
                except:
                    pass
                    
                return fecha
            else:
                print(f"❌ No se pudo extraer la fecha de @{username}")
                return None
                
        except Exception as e:
            print(f"❌ Error al buscar fecha: {str(e)[:50]}...")
            return None
        
    except Exception as e:
        print(f"❌ Error general al obtener fecha de @{username}: {str(e)[:50]}...")
        return None
    finally:
        # Intentar cerrar cualquier modal abierto
        try:
            from selenium.webdriver.common.keys import Keys
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            sleep(1)
        except:
            pass

def iniciar_driver():
    """Inicializa el driver de Chrome con configuraciones anti-detección"""
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/136.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        print(f"❌ Error al iniciar el driver: {e}")
        print("💡 Verifica que la ruta del chromedriver sea correcta")
        exit()

# PROGRAMA PRINCIPAL
def main():
    print("🚀 Iniciando navegador...")
    driver = iniciar_driver()
    driver.maximize_window()

    try:
        # Ir a Instagram
        print("📱 Navegando a Instagram...")
        driver.get('https://www.instagram.com/')
        sleep(3)

        # Proceso de login
        print("🔐 Iniciando sesión...")
        try:
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'username'))
            )
            username_field.send_keys(USERNAME)

            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'password'))
            )
            password_field.send_keys(PASSWORD)

            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            login_button.click()

            print("⚠️ Si Instagram solicita verificación, ingrésala manualmente en el navegador.")
            input("Presiona Enter cuando hayas completado el login/verificación...")

            sleep(3)
            print("✅ Login completado")

        except Exception as e:
            print(f"❌ Error durante el login: {e}")
            driver.quit()
            return

        # Obtener fecha de creación
        print(f"\n🔍 Buscando información de @{usuario_objetivo}...")
        fecha_creacion = obtener_fecha_creacion_cuenta(driver, usuario_objetivo)
        
        # Mostrar resultados
        print("\n" + "="*60)
        print("📊 RESULTADO FINAL")
        print("="*60)
        
        if fecha_creacion:
            print(f"👤 Usuario: @{usuario_objetivo}")
            print(f"📅 Fecha de creación: {fecha_creacion}")
            print(f"⏰ Consultado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            print("✅ ¡Información obtenida exitosamente!")
        else:
            print(f"❌ No se pudo obtener la fecha de creación de @{usuario_objetivo}")
            print("💡 Posibles causas:")
            print("   - La cuenta es privada")
            print("   - La cuenta no existe")
            print("   - Instagram cambió su estructura")
            print("   - Problemas de conexión")
            print("   - Los XPaths han cambiado")
        
        print("="*60)

    except Exception as e:
        print(f"❌ Error general: {e}")
    
    finally:
        print("\n🔚 Cerrando navegador...")
        driver.quit()
        print("✅ Proceso finalizado")

if __name__ == "__main__":
    main()