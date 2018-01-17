@echo off
python ./manage.py dumpdata KinaKipa --indent 4  --output KinaKipa\fixtures\db.json
PAUSE