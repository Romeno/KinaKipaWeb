from django.db import models
from django.db.models import (CharField, DateTimeField, FileField, ImageField,
                              PositiveSmallIntegerField, TextField, URLField,
                              FloatField)
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.utils.translation import ugettext as _
from difflib import SequenceMatcher

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

class Library(models.Model):
    film_lists = URLField(max_length=2000, help_text="Страницы, на которых находятся ссылки на фильмы")