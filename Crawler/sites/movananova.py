import os
import bs4
import re
from time import sleep

def make_soup(result):
    return bs4.BeautifulSoup(str(result), 'html.parser')

def get_film_data(file_path):
    with open(file_path, 'r', encoding="UTF-8") as page:
        crawled_items = {}
        soup = bs4.BeautifulSoup(page, 'html.parser')
        content = make_soup(soup.find('div', {'class':'content'}))
        # find image-links
        links = [link.attrs['href'] for link in content.findChildren('a')]
        crawled_items['image_urls'] = list(filter(lambda st: st.endswith('.jpg'), links))
        crawled_items['title'] = content.find('div', {'class': 'title'}).text

        # find other information from text only
        raw_text = content.text
        crawled_items['country'] = re.findall(r'Краіна:(.*)\n', raw_text)[0]
        crawled_items['length'] = re.findall(r'Працягласць:(.*)\n', raw_text)[0]
        crawled_items['director'] = re.findall(r'Рэжысёр:(.*)\n', raw_text)[0]
        crawled_items['stars'] = re.findall(r'Ролі выконваюць:(.*)\n', raw_text)[0]
        crawled_items['description'] = re.findall(r'Пра фільм:(.*)<\/p>', content.__str__())[0]
        return crawled_items

file_path = r'medyateka\bajeviki\16-kvartalau.html'
if __name__ == '__main__':
    get_film_data(file_path)