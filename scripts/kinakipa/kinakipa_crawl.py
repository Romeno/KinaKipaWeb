import vk
import re


login = input('vk_email: ')
password = input('vk_password: ')
vk_id = '6295734'

session = vk.AuthSession(app_id=vk_id, user_login=login, user_password=password, scope='wall')
vkapi = vk.API(session)
posts = vkapi.wall.get(owner_id='-136884833', filter='owner', count='10')

photo = {}
video = {}

title = r'(^[\w\d][\w\d\s-]+)[\\|]'
year = r'\s(\d{4})'
imdb = r'[Ii][\w]{3}[:]?\s+http[s]?://[^\s<]*'
kinopoisk = r'[Kk][\w]{8}[:]?\s+http[s]?://[^\s<]*'
tag = r'(#[\w]+)@'
voice_over = r'[АаSB\d][гa\dD]\w+[:]?\s*(http[s]?:[^\s]+)'
video = r'[Аа][н][л]\w+[:]?\s*(http[s]?:[^\s]+)'
url = r'http[s]?:[^\s]+'

pattern_list = [
    title, year, imdb, kinopoisk,
    tag, voice_over, video
]


def get_attachments(attachments):
    for att in attachments:
        if att["type"] == "photo":
            photo = att.get("photo")
        elif att["type"] == "video":
            video = att.get("video")


def find_patterns(pattern_list, post_text):

    responce = {
        'title': None,
        'year': None,
        'imdb': None,
        'kinopoisk': None,
        'tag': None,
        'voice_over': None,
        'video_link': None
    }

    for key_pattern in zip(responce.keys(), pattern_list):
        responce[key_pattern[0]] = re.findall(key_pattern[1], post_text)
    return responce


def search_in_posts(posts, pattern_list):
    result = []
    for post in posts:
        if isinstance(post, dict):
            attachments = post.get('attachments')
            result.append(find_patterns(pattern_list, post.get('text')))
    return result


if __name__ == "__main__":
    inf = search_in_posts(posts, pattern_list)