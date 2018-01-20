import os
import json
import requests
import bs4
from time import sleep


def load_data(file_path):
    with open(file_path, 'r') as _file:
        return json.loads(_file.read())


def store_page(url, genre):
    filename = url[url.rfind('/')+1:]
    storage = ( os.getcwd() + '\\medyateka\\' + 
                genre.replace('/', '\\') + filename )
    content = requests.get(url).text
    with open(storage, "w+", encoding='utf-8') as _file:
        _file.write(content)
    return storage


def parse_page():
    pass


urls = load_data('movananova_dict.json')
downloaded_urls = dict.fromkeys(urls.keys(), [])
for genre in urls:
    for url in urls[genre]:
        downloaded_urls[genre].append(store_page(url, genre))
        sleep(10)
        print('Successefully stored:', url)
