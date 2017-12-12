import os
import bs4
import re
from time import sleep

file_path = r'medyateka\bajeviki\16-kvartalau.html'

def make_soup(result):
    return bs4.BeautifulSoup(str(result), 'html.parser')

with open(file_path, 'r', encoding="UTF-8") as page:
    soup = bs4.BeautifulSoup(page, 'html.parser')
    content = make_soup(soup.find('div', {'class':'content'}))
    # find image-links
    links = [link.attrs['href'] for link in content.findChildren('a')]
    images = list(filter(lambda st: st.endswith('.jpg'), links))
    title = content.find('div', {'class': 'title'}).text
    # find other information from text only
    raw_text = content.text
    country = re.findall(r'Краіна:\s(.*)\n', raw_text)[0]
    length = re.findall(r'Працягласць:\s(.*)\n', raw_text)[0]
    director = re.findall(r'Рэжысёр:\s(.*)\n', raw_text)[0]
    stars = re.findall(r'Ролі выконваюць:\s(.*)\n', raw_text)[0]

    # somehow description isn't working now
    # description = re.findall(r'Пра фільм:[.\n]*</p>', content.__str__())
    # print(content.__str__())
