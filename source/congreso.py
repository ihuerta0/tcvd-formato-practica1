import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from fake_useragent import UserAgent


# URL de la pàgina web
url = 'https://www.congreso.es/es/busqueda-de-diputados?p_p_id=diputadomodule&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_diputadomodule_mostrarFicha=true&codParlamentario=1&idLegislatura=XV&mostrarAgenda=false'

# Especifica les capçaleres amb un User Agent aleatori
ua = UserAgent()
ua1 = ua.random
headers = {'User-Agent': 'ua1',
           'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Referer': 'https://www.google.com'}

# Crea la sol·licitud amb les capçaleres especificades
response = requests.get(url, headers=headers)
status_code = response.status_code  # Captura el codi d'estat

# Comprova si la sol·licitud ha estat satisfactòria (codi d'estat 200)
if status_code != 200:
    print(f"No s'ha pogut obtenir el codi font de la pàgina web. Codi d'estat: {status_code}")
else:
    # Configura Selenium
    firefox_path = '/snap/bin/geckodriver'
    firefox_service = Service(firefox_path)
    driver = webdriver.Firefox(service=firefox_service)

    # Navega a la pàgina web
    driver.get(url)
    driver.implicitly_wait(10)

    # Obte el contingut de la pàgina després de l'execució de JavaScript
    page_content = driver.page_source

    # Crea un objecte BeautifulSoup amb el contingut de la pàgina
    soup = BeautifulSoup(page_content, 'html.parser')

    # URL de la imatge
    url_image = 'https://www.congreso.es/docu/imgweb/diputados/1_15.jpg'

    # Crea la sol·licitud amb les capçaleres especificades
    response = requests.get(url_image, headers=headers)
    status_code = response.status_code  # Captura el codi d'estat

    # Comprova si la sol·licitud ha estat satisfactòria (codi d'estat 200)
    if status_code != 200:
        print(f"No s'ha pogut obtenir el codi font de la pàgina web\
            d'obtenció de la imatge. Codi d'estat: {status_code}")
    else:
        # Descarrega la imatge
        with open('image.jpg', 'wb') as file:
            file.write(response.content)
        print("Imatge descarregada correctament com a 'image.jpg'")

    # Prettify the HTML content
    pretty_page_content = soup.prettify()

    # Tanca el navegador
    driver.quit()

    # Escribe el contingut de la pàgina a un arxiu .txt
    with open('page_content.txt', 'w', encoding='utf-8') as file:
        file.write(pretty_page_content)

    print("Contingut de la pàgina guardat correctament en page_content.txt")
