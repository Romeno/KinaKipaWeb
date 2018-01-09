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

    name = CharField(max_length=200, verbose_name='film_name', help_text="Назва")
    name_origin = CharField(
        max_length=200, verbose_name='film_name_origin',
        default="", help_text="Назва арыгінала"
    )
    director = CharField(max_length=200, help_text="Рэжысёр", default="")
    # year = PositiveSmallIntegerField(default=None, help_text="Год")
    year = CharField(max_length=4, help_text="Год", default="")
    kp_rating = FloatField(null=True)
    imdb_rating = FloatField(null=True)
    genres = CharField(max_length=200, help_text="Жанры", default="")
    stars = CharField(max_length=200, help_text="Акцёры", default="")
    # video = FileField(storage=VIDEO_STORAGE, help_text="Відэа")
    video_html = TextField(help_text="html-код для проигрывания видео", default='')
    length = CharField(max_length=25, help_text="Працягласць", default='')
    description = TextField(help_text="Апісанне")
    torrent_link = URLField(max_length=200, blank=True, help_text="Спасылка на торэнт")
    # image = ImageField(storage=IMAGE_STORAGE, blank=True, null=True, verbose_name=_('Film image'), help_text=_("Image of article when viewing article list on index or news page"))
    image_url = URLField(max_length=200, blank=True, help_text="Спасылка на карцiнку")
    country = CharField(max_length=200, help_text="Краiна", default="")
    # used to refresh ratings once in a while
    kp_link = URLField(max_length=200, blank=True, help_text="Ссылка на .xml-файл с рейтингом с kp")

    def __eq__(self, other):
        # This function compares films-objects
        # using NAME-similarity and released year.
        if not isinstance(other, self.__class__):
            return False
        if self.name == other.name:
            return True
        similarity = SequenceMatcher(None, self.name, other.name).ratio()
        if similarity > 0.75:
            return True
        # If not that similar, but has the same release-year:
        if (self.year and other.year and
            self.year == other.year and similarity > 0.5):
            return True
        return False

    def __str__(self):
        return f"{self.name} / {self.name_origin} / {self.year}"

class Library(models.Model):
    film_lists = URLField(max_length=2000, help_text="Страницы, на которых находятся ссылки на фильмы")