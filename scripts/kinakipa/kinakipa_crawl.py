import vk
import re
import time
import requests


login = input('vk_email: ')
password = input('vk_password: ')
vk_id = '6295734'

title = ("title", r'(^[\w\d][\w\d\s!\?\+ch-]+)[\\|]')
description = ("description", r'<br>[\s]{0,2}<br>([^</]*)<br>([^</]*)<br>[\s]{0,2}')
year = ("year", r'\s(\d{4})')
imdb = ("imdb", r'http[s]?://www.imdb.com[^\s<]*')
kinopoisk = ("kinopoisk", r'http[s]?://www.kinopoisk.ru[^\s<]*')
tags = ("tags", r'(#[\w]+)@')
voice_over = ("voice_over", r'[АаSB\d][гa\dD]\w+[:]?\s*(http[s]?:[^\s<]*)')
video_link = ("video_link", r'[Аа][н][л]\w+[:]?\s*(http[s]?:[^\s<]*)')

patterns = [
    title, description, year,
    tags, kinopoisk, imdb,
    voice_over, video_link
]

CSV_FILENAME = "kinakipa_films.csv"

CSV_FIELDS = [
    "id",
    "title", "description", "year", "tags", "kinopoisk",
    "imdb", "voice_over", "video_link", "full_text",
    "src_small", "src", "src_big",
    "src_xbig", "src_xxbig", "src_xxxbig",
    "video"
]

session = vk.AuthSession(app_id=vk_id, user_login=login, user_password=password, scope='wall,video')
vkApi = vk.API(session)
POST_COUNT = 40
STEP = 20
ID = 0


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
    while requests.exceptions.ReadTimeout:
        time.sleep(1)
        try:
            link = get_video_link(owner_id, id, vkapi)
        except vk.exceptions.VkAPIError:
            link = get_video_link(owner_id, id, vkapi)
            return '<iframe src="{0}" width="{1}" height="{2}" frameborder="0" allowfullscreen></iframe>'.format(link,
                                                                                                                 width,
                                                                                                                 height)
        else:
            return '<iframe src="{0}" width="{1}" height="{2}" frameborder="0" allowfullscreen></iframe>'.format(link,
                                                                                                         width,
                                                                                                         height)


def get_video_link(owner_id, id, vkapi):
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


def prepare_inf_to_csv(inf, patterns):
    global ID
    result = []
    for post in inf:
        for patt in patterns:
            if patt[0] != "description":
                post[0][patt[0]] = ", ".join(post[0][patt[0]]).strip()
            else:
                post[0][patt[0]] = "".join(s for s in post[0][patt[0]][0]).strip()
    for post in inf:
        new_post = dict()
        new_post["id"] = ID
        new_post.update(post[0])
        new_post.update(post[1][0])
        new_post["video"] = post[1][1]
        result.append(new_post)
        ID += 1
    return result


def write_inf_to_csv(data, path, fields):
    inf_to_write = prepare_inf_to_csv(data, patterns)
    delimiter = ";"
    with open(path, "a") as f:
        for row in inf_to_write:
            for field in fields:
                try:
                    if type(row[field]) != str:
                        f.write("{0}{1}".format(str(row[field]), delimiter))
                    elif field == 'video':
                        f.write(row[field])
                    else:
                        f.write("{0}{1}".format(row[field], delimiter))
                except (UnicodeEncodeError, KeyError):
                    pass
            f.write("\n")


if __name__ == "__main__":
    with open(CSV_FILENAME, "w") as f:
        f.write("{0}\n".format(";".join(CSV_FIELDS)))
    for posts_offset in range(0, POST_COUNT+1, STEP):
        posts = vkApi.wall.get(owner_id='-136884833', filter='owner', count=STEP, offset=posts_offset)
        inf = search_in_posts(posts, patterns, vkApi)
        inf = del_not_film_posts(inf)
        write_inf_to_csv(inf, path=CSV_FILENAME, fields=CSV_FIELDS)
        time.sleep(4)
