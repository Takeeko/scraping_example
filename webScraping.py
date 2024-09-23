from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Ruta a tu ChromeDriver
chrome_driver_path = "./chromedriver.exe"  # Reemplaza con la ruta correcta a tu ChromeDriver

# Configurar el servicio de Selenium
service = Service(chrome_driver_path)

# Configurar opciones de Chrome
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")

# Crear una instancia del navegador con las opciones
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL del sitio que deseamos scrapear
url = "https://www.falabella.com/falabella-cl/category/cat2069/Perfumes?sred=perfumes"

# Abrimos la página
driver.get(url)

# Esperamos hasta que los productos se carguen
try:
    # Espera a que un producto específico esté presente
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'grid-pod'))
    )
except Exception as e:
    print("Los productos no se cargaron a tiempo.", e)
    driver.quit()
    exit()

# Obtenemos el HTML renderizado
html = driver.page_source

# Parseamos el contenido con BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Buscamos los contenedores de los productos
products = soup.find_all('div', class_='grid-pod')

# Cerramos el navegador
driver.quit()

if not products:
    print("No se encontraron productos. Verifica el selector CSS.")
    exit()

# Recorremos los productos y extraemos los datos deseados
for product in products[:4]:  # Limita a los primeros 4 productos
    try:
        # Extraemos la marca
        brand = product.find('b', class_='pod-title').get_text(strip=True)

        # Extraemos el nombre
        name = product.find('b', class_='pod-subTitle').get_text(strip=True)

        # Extraemos el precio
        price = product.find('span', class_='copy10').get_text(strip=True)

        # Mostramos los datos
        print(f"Marca: {brand}")
        print(f"Nombre: {name}")
        print(f"Precio: {price}\n")
    except AttributeError:
        # Si no se encuentra alguno de los elementos, se omite el producto
        print("Producto con información incompleta. Continuando con el siguiente...\n")
