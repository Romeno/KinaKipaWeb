import os
# import django
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KinaKipaWeb.settings")
# django.setup()

import bs4
import re
from KinaKipaWeb.settings import BASE_DIR
from time import sleep, ctime
from random import randint
from Crawler.sites.movananova_patterns import patterns
from Crawler.models import Crawled_Film


class Library():
    def __init__(self):
        self.filenames = Library.get_film_paths()

    def get_film_paths():
        lib_path = os.path.join(BASE_DIR, 'Crawler', 'sites', 'medyateka')
        found_htmls = []
        for base, dirs, filenames in os.walk(lib_path):
            for filename in filenames:
                if filename.endswith('.html'):
                    found_htmls.append(os.path.join(base, filename))
        return found_htmls

    def make_soup(result):
        return bs4.BeautifulSoup(str(result), 'html.parser')

    def search_with_patterns(content):
        main_content = content.text
        special_content = content.__str__()

        found_items = {}
        for item, item_patterns in patterns.items():
            current_content = (
                main_content if item != 'description' else special_content
            )
            for pattern in item_patterns:
                found = re.findall(pattern, current_content)
                found_items[item] = found[0].strip() if found else ''
                if found:
                    break
        return found_items

    def get_film_data(self, file_path):
        with open(file_path, 'r', encoding="UTF-8") as page:
            crawled_data = {}
            soup = bs4.BeautifulSoup(page, 'html.parser')
            content = Library.make_soup(soup.find('div', {'class':'content'}))

            # find image-links
            links = [link.attrs['href'] for link in content.findChildren('a')]
            links = list(filter(lambda st: st.endswith('.jpg'), links))
            link = links[0] if links else ''
            crawled_data['image_url'] = link

            # find title
            crawled_data['name'] = content.find('div', {'class': 'title'}).text
            # find video html
            crawled_data['video_html'] = content.find('iframe')

            # find other information from text only
            searched_with_patterns = Library.search_with_patterns(content)
            crawled_data.update(searched_with_patterns)

            return crawled_data

    def store_in_model(self):
        for index, filename in enumerate(self.filenames):
            try:
                print(f'[{ctime()}] Open: {filename}')
                film_data = self.get_film_data(filename)

                Crawled_Film.store_crawled(film_data)
                with open('movananova_passed.log', 'a') as log:
                    log.write(filename)
            except:
                with open('movananova_failed.log', 'a') as log:
                    log.write(filename)


if __name__ == '__main__':
    lib = Library()
    lib.store_in_model()