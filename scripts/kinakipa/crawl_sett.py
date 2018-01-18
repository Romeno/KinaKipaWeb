def get_last_id():
    with open('log.txt') as f:
        id = (f.readlines()[-1]).split(':')[-1]
    return int(id)


def get_local_settings():
    with open('local_setting.txt')as f:
        file = f.readlines()
        id = file[0].strip('\n')
        login = file[1].strip('\n')
        password = file[-1].strip('\n')
    return id, login, password


last_id = get_last_id()
app_id, user_login, user_password = get_local_settings()

login_sett = {
    'app_id': app_id,
    'user_login': user_login,
    'user_password': user_password
}

count_sett = {
    'post_count': 1000,
    'step': 20
}

csv_file = "kinakipa_films.csv"

csv_fields = [
    "id", "title", "origin_title", "description", "year",
    "tags", "kinopoisk", "imdb", "torrent_link",
    "full_text", "src_small", "src", "src_big",
    "src_xbig", "src_xxbig", "src_xxxbig", "video"
]

title = ("title", r"(^[\w\d][,.:()'\w\d\s!\?\+ch-]+)[\\|]")
origin_title = ("origin_title", r'\|\s{0,3}(.*)\s{0,3}\|\s')
description = ("description", r'<br>[\s]{0,2}<br>([^#</]*)<br>([^#</]*)<br>[\s]{0,2}')
year = ("year", r'\s(\d{4})\s{0,2}<')
imdb = ("imdb", r'http[s]?://www.imdb.com[^\s<]*')
kinopoisk = ("kinopoisk", r'http[s]?://www.kinopoisk.ru[^\s<]*')
tags = ("tags", r'(#[\w\_]+)@?')
voice_over = ("voice_over", r'[АаSB\d][гa\dD]\w+[:]?\s*(http[s]?:[^\s<]*)')
video_link = ("video_link", r'[Аа][н][л]\w+[:]?\s*(http[s]?:[^\s<]*)')
torrent_link = ("torrent_link", r'http[s]?://w{0,3}\.?baravik[^\s<(]*')

patterns = [
    title, origin_title, description, year,
    tags, kinopoisk, imdb, torrent_link
]