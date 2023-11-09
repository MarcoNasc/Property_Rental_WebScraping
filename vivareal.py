from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import math
import time
import os
import re

os.environ['PATH'] += r'C:/Users/marco/SeleniumDrivers'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

file_path = 'C:/Users/marco/Equatorial/Imoveis/data/imoveis_aluguel_belem_vivareal.csv'


driver = webdriver.Chrome()


time.sleep(5)

if not os.path.isfile(file_path):
    new_df = pd.DataFrame(columns=["id", "preco", "endereco", "numero", "bairro", "cidade", "estado",
                                    "area", "quartos", "banheiros", "link"])
    new_df.to_csv(file_path, sep=';', index=False)


url = 'https://www.vivareal.com.br/aluguel/para/belem/'
driver.get(url)

total_listings = driver.find_element(By.CLASS_NAME, value='results-summary__count').text
total_listings = int(total_listings.replace('.', ''))

print(total_listings)


n_pages = math.ceil(total_listings/36)


for page in range(1, n_pages+1):

    time.sleep(3)

    print(f"Analisando a página {page}...")
    #url = f'https://www.vivareal.com.br/aluguel/para/belem/?pagina={page}'
    url = f'https://www.vivareal.com.br/aluguel/para/belem/#onde=Brasil,Par%C3%A1,Bel%C3%A9m,,,,,,BR%3EPara%3ENULL%3EBelem,,,&pagina={page}'
    driver.get(url)

    time.sleep(2)

    properties = driver.find_elements(By.CSS_SELECTOR, value='[data-type="property"]')
    #print(properties)

    #address = driver.find_elements(By.CSS_SELECTOR, value='[class="property-card__address"]')
    #addresses = [place.text for place in address]
    #print(addresses)

    for place in properties:
            
        try:
            price_period = place.find_element(By.CLASS_NAME, value='property-card__price-period').text
            if price_period != '/mês':
                continue

            else:
                print('--------------------------------------')
                
                
                # Preço
                price_text = place.find_element(By.CLASS_NAME, value='property-card__price').text

                try:
                    price = re.search(r'\d{1,3}(?:[.,]\d{3})*', price_text)
                    price = float(price.group(0))
                    print(f"Preço: {price}")
                except:
                    print('Sem preço')

                # Endereço
                address = place.find_element(By.CLASS_NAME, value='property-card__address').text
                
                print(f"Endereço: {address}")

                # Número
                try:
                    number = re.search(r'(\b\d+\b)', address)
                    number = number.group(0)
                    print(f"Número: {number}")
                except:
                    print("Sem número")                
                
                # Bairro
                try:
                    neighborhood = re.search(r'(?<=-\s)(.*?)(?=\s*,\s*\w+\s*-\s*\w+)', address)
                    neighborhood = neighborhood.group(1)
                    print(f"Bairro: {neighborhood}")
                except:
                    print('Sem bairro')

                # Cidade
                try:
                    city = re.search(r'- (.*), (.*) -', address)
                    city = city.group(2)
                    print(f"Cidade: {city}")
                except:
                    print('Sem cidade')

                # Estado
                try:
                    state = re.search(r'- (.*), (.*) - (.*)', address)
                    state = state.group(3)
                    print(f"Estado: {state}")

                except:
                    print('Sem estado')

                # Área
                area = place.find_element(By.CLASS_NAME, value='property-card__detail-area').text
                
                try:
                    area = re.search(r'\d+', area)
                    area = float(area.group(0))
                    print(f'Área: {area}')
                except:
                    print('Sem área')

                # Quartos
                rooms_text = place.find_element(By.CLASS_NAME, value='property-card__detail-room').text

                try:
                    rooms = re.search(r'\d+', rooms_text)
                    rooms = int(rooms.group(0))
                    print(f'Quartos:{rooms}')
                except:
                    print('Sem quartos')

                # Banheiros
                bathrooms_text = place.find_element(By.CLASS_NAME, value='property-card__detail-bathroom').text

                try:
                    bathrooms = re.search(r'\d+', bathrooms_text)
                    bathrooms = int(bathrooms.group(0))
                    print(f'Banheiros: {bathrooms}')
                except:
                    print('Sem banheiros')

                # Link
                link_class = place.find_element(By.CLASS_NAME, value='property-card__content-link')
                link = link_class.get_attribute('href')
                print(f'Link: {link}')

                # Id
                try:
                    id = re.search(r'id-(\d+)/', link)
                    id_number = str(id.group(1))
                    print("ID Number:", id_number)
                except:
                    print("ID number not found in the URL.")


                df = pd.read_csv(file_path, sep=';')
                #print(type(id_number))
                #print(type(df['id'][0]))
                #print(list(df['id']))
                #print(df['id'].tolist()[0])
                #print(type([str(id) for id in df['id'].tolist()][0]))


                #print(df['id'].isin([id_number]).any())
                print(id_number in [str(id) for id in df['id'].tolist()])
                print(len(df['id']))

                #if df['id'].isin([id_number]).any():
                if id_number in [str(id) for id in df['id'].tolist()]:
                    print("Passei por aqui")
                    continue

                else:
                    data = [id_number, price, address,
                            number, neighborhood, city, state, 
                            area, rooms, bathrooms, link]
                    
                    data = pd.DataFrame([data])
                    
                    data.to_csv(file_path, sep=';', index=False, mode='a', header=False)
        except:
            print('Sem período de aluguel')
            continue

