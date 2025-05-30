# main.py
from web_driver_manager import WebDriverManager
from scraper import InstagramScraper
from excel_exporter import generar_excel_completo, mostrar_resumen_final
from selenium.webdriver.common.by import By



def main():
    print("\n🔍 INSTAGRAM FOLLOWERS SCRAPER")
    print("=" * 50)
    usuario_objetivo = input("👤 Ingresa el nombre de usuario de Instagram a buscar (sin @): ").strip().lstrip("@")

    if not usuario_objetivo:
        print("❌ Error: Debes ingresar un nombre de usuario válido")
        return

    driver_manager = WebDriverManager()
    driver = driver_manager.iniciar_driver()

    if not driver or not driver_manager.login_instagram():
        return

    if not driver_manager.navegar_a_perfil(usuario_objetivo) or not driver_manager.verificar_perfil_existe(usuario_objetivo):
        driver_manager.cerrar_driver()
        return

    scraper = InstagramScraper(driver)
    boton = scraper.encontrar_boton_seguidores(usuario_objetivo)
    if boton:
        try:
            boton.click()
        except:
            driver.get(f"https://www.instagram.com/{usuario_objetivo}/followers/")
    else:
        driver.get(f"https://www.instagram.com/{usuario_objetivo}/followers/")

    seguidores_data = scraper.cargar_seguidores_completo(usuario_objetivo, limite_max=100)
    if seguidores_data:
        filename, ok = generar_excel_completo(seguidores_data, usuario_objetivo)
        mostrar_resumen_final(seguidores_data, usuario_objetivo, filename if ok else None)

    driver_manager.cerrar_driver()


if __name__ == "__main__":
    main()
