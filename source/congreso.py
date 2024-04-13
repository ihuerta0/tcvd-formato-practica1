from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from fake_useragent import UserAgent
import requests

# URL de la pàgina web
url = 'https://www.congreso.es/es/busqueda-de-diputados'

# Especifiquem capçalera
ua = UserAgent()
# Determinem un UserAgent aleatori
print(ua.random)
ua1 = ua.random

# Especifico la resta de la capçalera
headers = {'User-Agent': 'ua1',
           'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Referer': 'https://www.google.com'}

# Creem la sol·licitud amb les capçaleres especificades
response = requests.get(url, headers=headers)

# Capturar el codi d'estat de la resposta HTTP
status_code = response.status_code

# Comprovar si la sol·licitud ha estat satisfactòria (codi d'estat 200)
if status_code != 200:
    print(f"No s'ha pogut obtenir el codi font de la pàgina web. Codi d'estat: {status_code}")
else:
    # Configurem Selenium
    # Utilitza la ruta
    firefox_path = '/snap/bin/geckodriver'
    
    # Configurem el servei del driver de Firefox amb la ruta de l'executable
    firefox_service = Service(firefox_path)

    # Inicialitzem el driver de Firefox amb el servei configurat
    driver = webdriver.Firefox(service=firefox_service)

    # Naveguem a la pàgina web
    driver.get(url)

    # Esperem a que s'executi el JavaScript
    driver.implicitly_wait(10)

    # Obtenim el contingut de la pàgina després de l'execució de JavaScript
    page_content = driver.page_source

    # Creem un objecte BeautifulSoup amb el contingut de la página
    soup = BeautifulSoup(page_content, 'html.parser')

    # Prettify the HTML content
    pretty_page_content = soup.prettify()

    # Imprimim el codi font de la pàgina web formatejat
    # print(pretty_page_content)

    # Tanquem el navegador
    driver.quit()

    # Escrivim el contingut de la pàgina a un arxiu .txt
    with open('page_content.txt', 'w', encoding='utf-8') as file:
        file.write(pretty_page_content)

    print("Contingut de la pàgina guardat correctament en page_content.txt")

