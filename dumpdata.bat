@echo off
python ./manage.py dumpdata KinaKipa flatpages --indent 4  --output KinaKipa\fixtures\initial_data1.json
PAUSE