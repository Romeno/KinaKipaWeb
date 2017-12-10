@echo off
python ./manage.py dumpdata KinaKipa --indent 4  --output KinaKipa\fixtures\initial_data.json
PAUSE