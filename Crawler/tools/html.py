import requests
import urllib.request
import bs4 as bs
import os
from time import sleep, time, ctime
from KinaKipa.models import FILM_IMAGE_STORAGE
from django.core.files import File
import unidecode
from django.core.files.base import ContentFile

# SILENT defines whether or not parsing information is displayed
SILENT = False


def clean_html(text):
    soup = bs.BeautifulSoup(text, 'html.parser')
    clean_text = soup.text
    return clean_text


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
            print(f'[{ctime()}] Opening url: {url}')
        self.time_opened = time()

        html = requests.get(url).text
        soup = bs.BeautifulSoup(html, 'html.parser')
        return (soup)

    def __exit__(self, *args, **kwargs):
        if not SILENT:
            time_passed = time() - self.time_opened
            print(f'[{ctime()}] Parsed successfully with {time_passed:.3} seconds\n')
