import vk
import re
import time
import csv


login = input('vk_email: ')
password = input('vk_password: ')
vk_id = '6295734'

title = ("title", r'(^[\w\d][\w\d\s!\?\+ch-]+)[\\|]')
content = ("content", r'<br>[\s]{0,2}<br>([^</]*)<br>([^</]*)<br>[\s]{0,2}')
year = ("year", r'\s(\d{4})')
imdb = ("imdb", r'http[s]?://www.imdb.com[^\s<]*')
kinopoisk = ("kinopoisk", r'http[s]?://www.kinopoisk.ru[^\s<]*')
tags = ("tags", r'(#[\w]+)@')
voice_over = ("voice_over", r'[АаSB\d][гa\dD]\w+[:]?\s*(http[s]?:[^\s<]*)')
video_link = ("video_link", r'[Аа][н][л]\w+[:]?\s*(http[s]?:[^\s<]*)')

patterns = [
    title, content, year,
    tags, kinopoisk, imdb,
    voice_over, video_link
]

session = vk.AuthSession(app_id=vk_id, user_login=login, user_password=password, scope='wall,video')
vkapi = vk.API(session)
posts = vkapi.wall.get(owner_id='-136884833', filter='owner', count='20')


def search_in_posts(posts, patterns, vkapi):
    result = []
    for post in posts:
        if isinstance(post, dict):
            result.append(convert_post(post, patterns, vkapi))
    return result


def convert_post(post, patterns, vkapi):
    result = []
    attachments = post.get('attachments')
    result.append(find_patterns(patterns, post.get('text')))
    result[-1]["full_text"] = post.get('text')
    result.append(get_attachments(attachments, vkapi))
    return result


def find_patterns(patterns, post_text):

    response = dict.fromkeys([tup[0] for tup in patterns], None)

    for key_pattern in zip(response.keys(), patterns):
        response[key_pattern[0]] = re.findall(key_pattern[1][1], post_text)
    return response


def get_attachments(attachments, vkapi):
    photo = None
    video = None
    for att in attachments:
        if att["type"] == "photo":
            photo = get_photo(att)
        elif att["type"] == "video":
            video = get_video(att, vkapi)
    return photo, video


def get_photo(attachment):
    photo_links = {}
    photo_inf = attachment.get("photo")
    for item in photo_inf:
        if item[:3] == 'src':
            photo_links[item] = photo_inf[item]
    return photo_links


def get_video(attachment, vkapi):
    video_inf = attachment["video"]
    id = video_inf["vid"]
    owner_id = video_inf["owner_id"]
    width = 480
    height = 270
    try:
        link = get_video_link(owner_id, id)
    except vk.exceptions.VkAPIError as err:
        time.sleep(4)
        link = get_video_link(owner_id, id)
    return '<iframe src="{0}" width="{1}" height="{2}" frameborder="0" allowfullscreen></iframe>'.format(link,
                                                                                                         width,
                                                                                                         height)


def get_video_link(owner_id, id):
    try:
        link = (vkapi.video.get(owner_id=owner_id, videos="{}_{}".format(owner_id, id), count=1))[-1]["player"]
    except TypeError:
        return None
    return link


def del_not_film_posts(inf):
    result = []
    for post in inf:
        if len(post[0].get("imdb")) == 0 or len(post[0].get("kinopoisk")) == 0:
            pass
        else:
            result.append(post)
    return result


def write_inf_to_csv(inf):
    pass


if __name__ == "__main__":
    inf = search_in_posts(posts, patterns, vkapi)
    inf = del_not_film_posts(inf)
    for post in inf:
        print(post, sep='\n')
