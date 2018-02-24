import csv
import vk
import re
import time
import sys
import os
import requests
sys.path.insert(0, os.getcwd())
import crawl_sett

count = crawl_sett.count_sett
login = crawl_sett.login_sett


def start_crawl(vkapi, csv_file, fields, patt, count, step, work_type):

    if work_type == 'w':
        with open(csv_file, work_type) as f:
            writer = csv.DictWriter(f, delimiter=';', fieldnames=fields)
            writer.writeheader()
    for posts_offset in range(count, -1, -step):
        posts = vkapi.wall.get(owner_id='-136884833', filter='owner', count=step, offset=posts_offset)
        inf = search_in_posts(posts, patt, vkapi)
        inf = del_not_film_posts(inf)
        write_inf_to_csv(inf, path=csv_file, fields=fields)
        time.sleep(4)


def log_in(sett=login):
    if sett:
        session = vk.AuthSession(
            sett.get('app_id'),
            sett.get('user_login'),
            sett.get('user_password'),
            scope='wall,video'
        )
    else:
        session = vk.AuthSession(
            app_id=input('vk_id: '),
            user_login=input('vk_email: '),
            user_password=input('vk_password: '),
            scope="wall,video"
        )
    vkApi = vk.API(session)
    return vkApi


def set_crawl(sett=count):
    if sett:
        post_count = sett.get('post_count')
        step = sett.get('step')
    else:
        post_count = input('post count: ')
        step = sett.get('step: ')

    work_type = ''
    for _ in range(3):
        work_type = input(
            "Input 'a' to add new results\n" +
            "or 'w' to erase all previous results and write again.\n" +
            "To exit without changes press 'Enter'\n"
            "Your input: "
        )

        if work_type != 'a' and work_type != 'w' and work_type != '':
            print('Error. Try again')
        elif work_type == 'w':
            with open('log.txt', 'w') as f:
                f.write('last_id:0\n')
            break
        elif work_type == '':
            exit()
        else:
            break

    return post_count, step, work_type


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
            time.sleep(1)
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
                try:
                    post[0][patt[0]] = "".join(s for s in post[0][patt[0]][0]).strip()
                except IndexError:
                    post[0][patt[0]] = ""
    for post in inf:
        new_post = dict()
        new_post["id"] = ID
        new_post.update(post[0])
        try:
            new_post.update(post[1][0])
            new_post["video"] = post[1][1]
        except TypeError:
            pass
        result.append(new_post)
        ID += 1
    return result


def write_inf_to_csv(data, path, fields):
    inf_to_write = prepare_inf_to_csv(data, patts)
    with open(path, 'a') as f:
        writer = csv.DictWriter(f, delimiter=';', fieldnames=fields)
        for row in inf_to_write:
            try:
                writer.writerow(row)
            except UnicodeEncodeError:
                pass
    with open('log.txt', 'a') as f:
        f.write('last_id:{0}\n'.format(ID))


if __name__ == "__main__":

    vkApi = log_in(sett=login)
    settings = set_crawl(sett=count)

    ID = crawl_sett.last_id
    file = crawl_sett.csv_file
    fields = crawl_sett.csv_fields
    patts = crawl_sett.patterns

    start_crawl(vkApi, file, fields, patts, *settings)
