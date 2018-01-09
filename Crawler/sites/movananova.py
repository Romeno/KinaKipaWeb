import os
import bs4
import re
from KinaKipaWeb.settings import BASE_DIR
from time import sleep
from Crawler.sites.movananova_patterns import patterns

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
            crawled_items = {}
            soup = bs4.BeautifulSoup(page, 'html.parser')
            content = Library.make_soup(soup.find('div', {'class':'content'}))

            # find image-links
            links = [link.attrs['href'] for link in content.findChildren('a')]
            crawled_items['image_urls'] = list(filter(lambda st: st.endswith('.jpg'), links))
            # find title
            crawled_items['title'] = content.find('div', {'class': 'title'}).text
            # find video html
            crawled_items['video_html'] = content.find('iframe')

            # find other information from text only
            searched_with_patterns = Library.search_with_patterns(content)
            crawled_items.update(searched_with_patterns)

            return crawled_items


lib = Library()
for filename in lib.filenames:
    print('-'*100)
    print(filename)
    data = lib.get_film_data(filename)
    for item, value in data.items():
        print(item.rjust(40), value)