@echo off
python ./manage.py makemessages -l ru -l be -v 3 --keep-pot --no-wrap --no-location  -i "locale" -i "layout" -i "*.bat" -i "*.png" -i "*.md" -i "requirements.txt"
PAUSE