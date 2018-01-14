from django.db import models
from django.db.models import (CharField, DateTimeField, FileField, ImageField,
                              PositiveSmallIntegerField, TextField, URLField,
                              FloatField)
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.utils.translation import ugettext as _
from difflib import SequenceMatcher
import re
from Crawler.tools.html import clean_html

# Create your models here.
class Crawled_Film(models.Model):

    name = CharField(max_length=200, verbose_name='film_name', help_text="Назва", default='')
    name_origin = CharField(
        max_length=200, verbose_name='film_name_origin',
        default="", help_text="Назва арыгінала",
        null=True, blank=True
    )
    director = CharField(max_length=200, help_text="Рэжысёр", default="", blank=True)
    # year = PositiveSmallIntegerField(default=None, help_text="Год")
    year = CharField(max_length=4, help_text="Год", default="", blank=True)
    kp_rating = FloatField(default=0.0, blank=True)
    imdb_rating = FloatField(default=0.0, blank=True)
    genres = CharField(max_length=300, help_text="Жанры", default="", blank=True)
    stars = CharField(max_length=800, help_text="Акцёры", default="", blank=True)
    # video = FileField(storage=VIDEO_STORAGE, help_text="Відэа")
    video_html = TextField(help_text="html-код для проигрывания видео", default='', blank=True)
    length = CharField(max_length=30, help_text="Працягласць", default='', blank=True)
    description = TextField(help_text="Апісанне", default='', blank=True)
    torrent_link = URLField(max_length=200, help_text="Спасылка на торэнт", default='', blank=True)
    # image = ImageField(storage=IMAGE_STORAGE, blank=True, null=True, verbose_name=_('Film image'), help_text=_("Image of article when viewing article list on index or news page"))
    image_url = URLField(max_length=200, help_text="Спасылка на карцiнку", default='', blank=True)
    country = CharField(max_length=200, help_text="Краiна", default="", blank=True)
    # used to refresh ratings once in a while
    kp_link = URLField(max_length=200, help_text="Ссылка на .xml-файл с рейтингом с kp", default='', blank=True)

    def __eq__(self, other):
        # This function compares films-objects

        if not isinstance(other, self.__class__):
            return False
        if self.name == other.name:
            return True

        # Find similarity between film-names
        similarity = SequenceMatcher(None, self.name, other.name).ratio()
        if similarity > 0.75:
            return True

        # If not that similar, but has the same release-year or country:
        if ((self.year and other.year and
            self.year == other.year and
            similarity > 0.5) or (
            self.country and other.country and
            self.country == other.country and
            similarity > 0.6
            )):
            return True
        return False

    def __str__(self):
        return f"{self.name} / {self.name_origin} / {self.year}"

    def store_crawled(crawled_data):
        # check whether crawled_data could be saved of not
        temp_film = Crawled_Film.objects.create()
        for item in crawled_data.keys():
            if item not in temp_film.__dict__.keys():
                temp_film.delete()
                raise Exception
        temp_film.delete()

        print('*'*64, '\n')
        for item, value in crawled_data.items():
            print(' '*4,item.ljust(15), value)

        current_film = Crawled_Film.objects.create()
        for item, value in crawled_data.items():
            for attr in current_film.__dict__:
                if item == attr:
                    current_film.__dict__[item] = str(value)

        if current_film not in Crawled_Film.objects.all():
            current_film.save()
        else:
            current_film.update_similar()
            current_film.delete()

        print(
            f'\nSuccessfully stored.',
            ('*' * 64).ljust(64), sep='\n'
        )

    def get_similar(self):
        for film in Crawled_Film.objects.all():
            if film == self:
                return film

    def update_similar(self):
        other = self.get_similar()
        for key in self.__dict__.keys():
            if key == '_state' or key == 'id':
                continue

            old_value = other.__dict__[key]
            new_value = self.__dict__[key]

            if not new_value:
                continue

            if not old_value or len(new_value) > len(old_value):
                other.__dict__[key] = self.__dict__[key]
        other.save()


class Library():
    def clean_data(*args):
        for film in Crawled_Film.objects.all():
            for key, value in film.__dict__.items():

                if key == 'name' and not value:
                    film.delete()
                    break

                if not value:
                    continue

                if key == 'name_origin':
                    has_stopword = False
                    for stopword in ['rip', 'belsat','xvid', 'серы']:
                        if stopword in value.lower():
                            has_stopword = True

                    if (value == None or has_stopword):
                        film.__dict__[key] = ''
                        film.save()

                if key == 'description':
                    film.__dict__[key] = clean_html(value)
                    film.save()

                if key == 'genres':
                    film.__dict__[key] = Library.set_genre(value)
                    film.save()

    def set_genre(genres):
        # returns a list of cleared genres

        genres_text = genres.lower()
        genres_map = {
            'камедыя': r'кам[еэ]+',
            'фантастыка': r'(ф[аэ]нт|місты)',
            'гістарычны': r'гіст',
            'біяграфія': r'біяг',
            'дакументальны': r'дакумент',
            'кароткамэтражны': r'кароткам',
            'жахі': r'жах',
            'мюзікл': r'(муз|м\'?юз)',
            'драма': r'драм',
            'баявік': r'баявік',
            'прыгода': r'прыг',
            'вэстэрн': r'в[еэ]ст[аэе]рн',
            'дэтэктыў': r'дэтэктыу',
            'крымінальны': r'крымін',
            'серыял': r'сер.[а,я]л',
            'анімэ': r'анімэ',
        }

        cleared_genres = []
        for genre, pattern in genres_map.items():
            found = re.findall(pattern, genres_text)
            if found:
                cleared_genres.append(genre)
        return ', '.join(cleared_genres)

    def check(self, film):
        if not isinstance(film, Crawled_Film):
            return False
        if not film.name or not film.video_html:
            return False
        return True

    def count_ok(self):
        counter = 0
        for film in Crawled_Film.objects.all():
            counter += 1 if self.check(film) else 0
        return counter

    def send_to_db(self):
        for film in Crawled_Film.objects.all():
            if self.check(film):
                pass
