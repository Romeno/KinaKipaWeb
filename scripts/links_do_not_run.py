# http://www.movananova.by/medyateka/videa-medyateka/inshazemnae-kino-pa-belarusku/

import os
import re
import requests
import bs4

def full_url(local_url):
    head = 'http://www.movananova.by/medyateka/videa-\
            medyateka/inshazemnae-kino-pa-belarusku/'
    return head + local_url

def get_page(url, storage='memory'):
    content = requests.get(url).text
    if storage == 'memory':
        return content
    else:
        with open(storage, "w+", encoding='utf-8') as _file:
            _file.write(content)
        return storage

def get_films_links(genre):
    url = full_url(genre)
    storage = (
        os.getcwd() + '\\genres\\' +
        genre.replace('/', '\\') + 
        'main.html'
        )
    page = get_page(url, storage)
    
genres = (
    'kamiedyi/',
    'bajeviki/',
    'fantastycnyja-filmy/',
    'meladramy/',
    'trylery/',
    'filmy-zachau/',
    'dramy/'
    )
    
films = dict.fromkeys(genres)
for genre in genres:
    get_films_links(genre)

def parse_genre(genre):
    storage = (
        os.getcwd() + '\\genres\\' +
        genre.replace('/', '\\') + 
        'main.html'
        )
    with open(storage, 'r') as page:
        soup = bs4.BeautifulSoup(page, 'html.parser')
        pattern = r"http://www.movananova.by/medyateka/\s*"
        all_links = [link.get('href') for link in soup.find_all('a')]
        links = [link for link in all_links if re.findall(pattern, link)]
    return links

megalinks = dict.fromkeys(genres)
for genre in megalinks:
    megalinks[genre] = parse_genre(genre)

for i in megalinks:
    print(i.ljust(25, '.'), len(megalinks[i]))

with open('filmlinks.txt', 'w+') as _file:
    import json
    _file.write(json.dumps(megalinks))
