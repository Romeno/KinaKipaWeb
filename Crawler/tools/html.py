import requests
import bs4 as bs
from time import sleep, time


# SILENT defines whether or not parsing information is displayed
SILENT = False


class Soup_opener():
    # This class allows to open urls as soup object.
    #
    # If variable SILENT is False, it shows enter-exit messages:
    #   ( -- Opening url: http://### -- )
    #   ( -- Parsed successfully with ### seconds -- )
    #
    # Example:
    # ----------------------------------------------------------------
    # >>> with Soup_opener('https://baravik.org/topic/1776/') as soup:
    # >>>     print(soup.title)
    # ----------------------------------------------------------------
    # ... ( -- Opening url: https://baravik.org/topic/1776/ -- )
    # ... <title>Палёт над гняздом зязюлі / One Flew Over t...</title>
    # ... ( -- Parsed successfully with 7.61 seconds -- )
    # ----------------------------------------------------------------
    def __init__(self, url):
        self.url = url

    def __enter__(self):
        url = self.url
        if not SILENT:
            print('( -- Opening url: {} -- )'.format(url))
        self.time_opened = time()

        html = requests.get(url).text
        soup = bs.BeautifulSoup(html, 'html.parser')
        return (soup)

    def __exit__(self, *args, **kwargs):
        if not SILENT:
            print('( -- Parsed successfully with {:.3} seconds -- )\n'.format(time() - self.time_opened))