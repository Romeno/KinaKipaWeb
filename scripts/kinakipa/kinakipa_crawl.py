import vk
import re


login = input('vk_email: ')
password = input('vk_password: ')
vk_id = '6295734'

session = vk.AuthSession(app_id=vk_id, user_login=login, user_password=password, scope='wall')
vkapi = vk.API(session)
# https://oauth.vk.com/authorize?client_id=6295734&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=wall,offline,groups&response_type=token&v=5.69
# token = ("1769cb8d03e2ba90196d6b48e559f09044b1256f79682d041f45d6b0d7d25b24d45a49ec4b01517f82caf")
posts = vkapi.wall.get(owner_id='-136884833', filter='owner', count='10')

print(posts[2])
attachments = None
photo = {}
video = {}
text_content = None


def get_attachments(attachments):
    for att in attachments:
        if att["type"] == "photo":
            photo = att.get("photo")
        elif att["type"] == "video":
            video = att.get("video")


def split_text(post_text):
    result = {}

    title_pattern = r'^([А-Я\d][а-яА-Я-.]+)\s{1,3}[\\|]'
    year_pattern = r'\d{4}'
    imdb_pattern = r'[Ii][\w]{3}[:]?\s+http[s]?://[^\s]*'
    kinopoisk_pattern = r'[Kk][\w]{8}[:]?\s+http[s]?://[^\s]*'
    tag_pattern = r'(#[\w]+)@'
    voice_over_pattern = r'[АаSB\d][гa\dD]\w+[:]?\s*(http[s]?:[^\s]+)'
    video_link = r'[Аа][н][л]\w+[:]?\s*(http[s]?:[^\s]+)'
    url_pattern = r'http[s]?:[^\s]+'

    try:
        result["title"] = re.search(title_pattern, post_text).group(0)
        result["year"] = (re.search(year_pattern, post_text)).group(0)
        result["imdb"] = (re.search(imdb_pattern, post_text)).group(0)
        result["kinopoisk"] = (re.search(kinopoisk_pattern, post_text)).group(0)
        result["tags"] = re.findall(tag_pattern, post_text)
        result["voice_over"] = re.findall(voice_over_pattern, post_text)
        result["video_link"] = re.findall(video_link, post_text)
    except AttributeError as err:
        print("Not match")
    finally:
        return result

for post in posts:
    if isinstance(post, dict):
        text_content = post.get('text')
        attachments = post.get('attachments')
        print(split_text(text_content))


