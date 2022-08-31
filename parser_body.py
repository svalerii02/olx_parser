import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

offers = []
sections = {1: 'dopomoga', 2: 'detskiy-mir', 3: 'nedvizhimost', 4: 'transport',
            5: 'zapchasti-dlya-transporta', 6: 'rabota', 7: 'zhivotnye', 8: 'dom-i-sad',
            9: 'elektronika', 10: 'uslugi', 11: 'moda-i-stil', 12: 'hobbi-otdyh-i-sport'}
print('Hi! Choose the section to parse from OLX.ua entering its number from the sheet below.\n' + str(sections))
section_name = sections[int(input())]
for page_number in range(1, 4):
    url = f"https://www.olx.ua/d/uk/{section_name}/?page={page_number}"
    r = requests.get(url)
    sleep(1)
    soup = BeautifulSoup(r.text, 'lxml')
    cards = soup.findAll('div', class_='css-19ucd76')
    for card in cards:
        if card.find('a', class_='css-1bbgabe') in card:
            title = card.find('h6', class_='css-v3vynn-Text eu5v0x0').text
            price = card.find('p', class_='css-wpfvmn-Text eu5v0x0').text
            address = card.find('p', class_='css-p6wsjo-Text eu5v0x0').text
            link = "https://www.olx.ua" + card.find('a', class_='css-1bbgabe').get('href')
            offers.append([title, price, address, link])
        else:
            continue
headers = ['Title', 'Price', 'Address', 'Link']
offers_file = pd.DataFrame(offers, columns=headers)
offers_file.to_csv(r'\Users\south\PycharmProjects\Parser\offers_file.csv', sep=';', encoding='utf8')
