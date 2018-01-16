@echo off
python ./manage.py dumpdata Crawler --indent 4  --output KinaKipa\fixtures\crawled_films.json
PAUSE