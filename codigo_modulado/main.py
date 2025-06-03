from config import USERNAME, PASSWORD
from web_driver_manager import iniciar_driver, login_instagram
from scraper import navegar_a_perfil_desde_inicio, encontrar_boton_seguidores, cargar_seguidores_completo
from fecha_union import obtener_fecha_creacion_cuenta
from excel_exporter import exportar_seguidores_excel

def main():
    print("\n🔍 INSTAGRAM FOLLOWERS SCRAPER (MODULADO)")
    print("=" * 50)
    username_login = input("✉️ Ingresa el usuario de Instagram con el que vas a ingresar (login): ").strip()
    if not username_login:
        print("❌ Error: Debes ingresar un usuario válido para login")
        return
    usuario_objetivo = input("👤 Ingresa el nombre de usuario de Instagram a buscar (sin @): ").strip()
    if not usuario_objetivo:
        print("❌ Error: Debes ingresar un nombre de usuario válido")
        return
    if usuario_objetivo.startswith('@'):
        usuario_objetivo = usuario_objetivo[1:]
    usuario_objetivo = usuario_objetivo.strip()
    if not usuario_objetivo:
        print("❌ Error: Debes ingresar un nombre de usuario válido")
        return
    if usuario_objetivo.lower() == username_login.lower():
        print("❌ El usuario objetivo no puede ser igual al usuario de login")
        return
    print(f"Usando usuario de login: {username_login}")
    print(f"Usuario objetivo: {usuario_objetivo}")
    driver = iniciar_driver()
    login_instagram(driver, username_login, PASSWORD)
    if not navegar_a_perfil_desde_inicio(driver, usuario_objetivo):
        print(f"❌ No se pudo navegar al perfil de @{usuario_objetivo}")
        driver.quit()
        return
    boton = encontrar_boton_seguidores(driver, usuario_objetivo)
    if boton:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", boton)
            boton.click()
        except Exception:
            driver.execute_script("arguments[0].click();", boton)
    else:
        print("❌ No se pudo encontrar el botón de seguidores")
        driver.quit()
        return
    seguidores = cargar_seguidores_completo(driver, usuario_objetivo)
    print(f"\n🎉 ¡Carga completada! Total de seguidores válidos de @{usuario_objetivo}: {len(seguidores)}")
    seguidores_info = []
    for i, username in enumerate(sorted(seguidores), 1):
        print(f"{i:4d}. 👤 @{username} - https://www.instagram.com/{username}/")
        fecha = obtener_fecha_creacion_cuenta(driver, username)
        if fecha:
            print(f"    📅 Fecha de unión: {fecha}")
        else:
            print(f"    ❌ No se pudo obtener la fecha de unión")
        seguidores_info.append((username, fecha))
    nombre_archivo = f"seguidores_de_{usuario_objetivo}.xlsx"
    exportar_seguidores_excel(nombre_archivo, usuario_objetivo, seguidores_info)
    driver.quit()

if __name__ == "__main__":
    main()
