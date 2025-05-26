import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 🔹 MÓDULO 1: INICIAR WEBDRIVER
def iniciar_driver():
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/136.0.0.0 Safari/537.36")
    
    service = Service()
    return webdriver.Chrome(service=service, options=options)

# 🔹 MÓDULO 2: CARGAR PÁGINA Y ESPERAR PRODUCTOS
def cargar_pagina(driver, keyword):
    url = f"https://www.alkosto.com/search?text={keyword}"
    driver.get(url)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#js-hits > div > ol > li"))
    )

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

# 🔹 MÓDULO 3: EXTRAER PRODUCTOS Y ALMACENAR EN UN DATAFRAME
def extraer_productos(driver):
    productos = driver.find_elements(By.CSS_SELECTOR, "#js-hits > div > ol > li")[:5]
    data = []

    for idx, producto in enumerate(productos):
        try:
            # 🔹 Extraer el nombre correctamente
            nombre = "Nombre no disponible"
            try:
                nombre_elem = producto.find_element(By.CSS_SELECTOR, "h3.product__item__top__title")
                nombre = nombre_elem.text.strip()
            except:
                pass

            # 🔹 Extraer el enlace correctamente
            link = "Enlace no disponible"
            try:
                link_elem = producto.find_element(By.CSS_SELECTOR, "a.product__item__top__link")
                link = link_elem.get_attribute("href")
            except:
                pass

            # 🔹 Extraer el precio correctamente
            precio = "Precio no disponible"
            try:
                precio_cont = producto.find_element(By.CSS_SELECTOR, "p.product__price--discounts__price")
                precio_elem = precio_cont.find_element(By.CSS_SELECTOR, "span.price")
                precio = precio_elem.get_attribute("innerText").strip()
            except:
                pass

            data.append({"Nombre": nombre, "Precio": precio, "Link": link})

        except Exception as e:
            print(f"Error en producto {idx+1}: {e}")

    return pd.DataFrame(data)  # 🔹 Devolvemos los datos en formato DataFrame

# 🔹 MÓDULO 4: EJECUTAR SCRAPER Y MOSTRAR RESULTADOS EN DATAFRAME
def ejecutar_scraping(keyword):
    driver = iniciar_driver()
    cargar_pagina(driver, keyword)
    df_productos = extraer_productos(driver)
    driver.quit()

    # 🔹 Mostrar el DataFrame en consola
    print("\n---- Resultados obtenidos ----")
    print(df_productos)

    # 🔹 Opcional: Guardar los datos en un archivo CSV
    #df_productos.to_csv("productos.csv", index=False)
    #print("\nLos resultados han sido guardados en 'productos.csv'.")

# 🔹 PRUEBA CON "palabra clave"
ejecutar_scraping("computador")