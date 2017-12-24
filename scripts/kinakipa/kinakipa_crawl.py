import vk
import re


login = input('vk_email: ')
password = input('vk_password: ')
vk_id = '6295734'

session = vk.AuthSession(app_id=vk_id, user_login=login, user_password=password, scope='wall,video')
vkapi = vk.API(session)
posts = vkapi.wall.get(owner_id='-136884833', filter='owner', count='20')

title = r'(^[\w\d][\w\d\s-]+)[\\|]'
year = r'\s(\d{4})'
imdb = r'http[s]?://www.imdb.com[^\s<]*'
kinopoisk = r'http[s]?://www.kinopoisk.ru[^\s<]*'
tag = r'(#[\w]+)@'
voice_over = r'[АаSB\d][гa\dD]\w+[:]?\s*(http[s]?:[^\s<]*)'
video_link = r'[Аа][н][л]\w+[:]?\s*(http[s]?:[^\s<]*)'
url = r'http[s]?:[^\s]+'

pattern_list = [
    title, year, imdb, kinopoisk,
    tag, voice_over, video_link
]


def get_attachments(attachments, vkapi):
    photo = None
    video = None
    for att in attachments:
        if att["type"] == "photo":
            photo = get_photo(att)
        # elif att["type"] == "video":
            # video = get_video(att, vkapi)
    return photo


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
    link = vkapi.video.get(owner_id=owner_id, videos="{}_{}".format(owner_id, id), count=1)
    print(link)


def find_patterns(pattern_list, post_text):

    response = {
        'title': None,
        'year': None,
        'imdb': None,
        'kinopoisk': None,
        'tag': None,
        'voice_over': None,
        'video_link': None
    }

    for key_pattern in zip(response.keys(), pattern_list):
        response[key_pattern[0]] = re.findall(key_pattern[1], post_text)
    return response


def convert_post(post, pattern_list, vkapi):
    result = []
    attachments = post.get('attachments')
    result.append(find_patterns(pattern_list, post.get('text')))
    result[-1]["full_text"] = post.get('text')
    result.append(get_attachments(attachments, vkapi))
    return result


def search_in_posts(posts, pattern_list, vkapi):
    result = []
    for post in posts:
        if isinstance(post, dict):
            result.append(convert_post(post, pattern_list, vkapi))
    return result


if __name__ == "__main__":
    inf = search_in_posts(posts, pattern_list, vkapi)
    for post in inf:
        print(post, sep='\n')
