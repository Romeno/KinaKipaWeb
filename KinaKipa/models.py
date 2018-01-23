# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import (CharField, DateTimeField, FileField, ImageField,
                              PositiveSmallIntegerField, TextField, URLField,
                              FloatField)
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.conf import settings
from tinymce.models import HTMLField
from filebrowser.fields import FileBrowseField
import tagulous.models

import re
import requests
import unidecode
from time import sleep, strftime

IMAGE_STORAGE = FileSystemStorage(location='layout/image')
FILM_IMAGE_STORAGE = FileSystemStorage(location='layout/image/poster')
FILM_GENRES = [
    'камедыя',
    'фантастыка',
    'гістарычны',
    'біяграфія',
    'дакументальны',
    'кароткамэтражны',
    'жахі',
    'мюзікл',
    'драма',
    'баявік',
    'прыгода',
    'вэстэрн',
    'дэтэктыў',
    'крымінальны',
    'серыял',
    'анімэ'
]


class Article(models.Model):

    title = CharField(max_length=200, verbose_name=_('Title'), help_text=_("Article title"))
    badge_image = FileBrowseField(_("Badge image"), max_length=500, directory="images/",
                                extensions=settings.FILEBROWSER_EXTENSIONS['Image'],
                                help_text=_('Article badge image'))
    # news_icon_link = URLField(
    #     max_length=500, blank=True,
    #     verbose_name=_('Link to news icon'), help_text=_('Link to image for news icon'))
    content = HTMLField(
        default='Content', verbose_name=_('Article content'), help_text=_("Article content")
    )
    published_date = DateTimeField(
        default=timezone.now, verbose_name=_('Publication date'), help_text=_("Publication date")
    )

    video_link = CharField(
        max_length=500, blank=True,
        verbose_name=_('Video'), help_text=_('Link to video. Needs "iframe" tag'))

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # def save(self, *args, **kwargs):
    #     if not self.news_icon:
    #         self.news_icon_link = re.findall("<img\s{0,2}src=\"([^\s]*)\"", str(self.content))[0]
    #     else:
    #         self.news_icon_link = "../static/img/kinakipa-logo.jpg"
    #     super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Genre(tagulous.models.TagTreeModel):
    class TagMeta:
        initial = ', '.join(FILM_GENRES)
        force_lowercase = True
        space_delimiter = False
        autocomplete_view = 'film_genres_autocomplete'


class Film(models.Model):

    # GENRES_CHOICES = (
    #     ('action', 'Баявік'),
    #     ('adventure', 'Прыгода'),
    #     ('comedy', 'Камедыя'),
    #     ('crime', 'Злачынства'),
    #     ('drama', 'Драма'),
    #     ('epics/historical', 'Эпас / Гістарычны'),
    #     ('horror', 'Жахі'),
    #     ('musicals', 'Мюзікл'),
    #     ('science fiction', 'Навуковая фантастыка'),
    #     ('war', 'Ваенны'),
    #     ('westerns', 'Вестэрн')
    # )

    # @film's names
    name = CharField(max_length=200, verbose_name='film_name', help_text="Назва", unique=True)
    name_origin = CharField(max_length=200, verbose_name='film_name_origin',
                            default='', help_text="Назва арыгінала", blank=True)

    # @people
    director = CharField(max_length=200, help_text="Рэжысёр", blank=True)
    stars = CharField(max_length=800, help_text="Акцёры", blank=True)

    # @text information
    description = TextField(help_text="Апісанне", blank=True)
    country = CharField(max_length=200, help_text="Краiна", default="", blank=True)

    # @numeric values
    # >>> ratings are currently optional
    kp_rating = FloatField(default=0.0, blank=True)
    imdb_rating = FloatField(default=0.0, blank=True)
    year = CharField(max_length=4, help_text="Год", default="", blank=True)
    length = CharField(max_length=30, help_text="Працягласць", default='', blank=True)

    # @meta information
    genres = tagulous.models.TagField(to=Genre, help_text='Жанры могут включать в себя пробелы', blank=True)
    video_html = TextField(help_text="html-код для проигрывания видео", default='')
    image = ImageField(storage=FILM_IMAGE_STORAGE, blank=True, null=True, verbose_name=_('Film image'))
    torrent_link = URLField(max_length=2000, blank=True, help_text="Спасылка на торэнт")

    def download_image(self, url):
        name = unidecode.unidecode(self.name)
        format_position = url.rfind('.')
        img_format = url[format_position:]
        filename = name + img_format

        img_data = requests.get(url)
        if not img_data.ok:
            return None

        self.image.save(
            filename,
            ContentFile(img_data.content),
            save=True
        )
        self.save()
        sleep(5)

    def __str__(self):
        return f'{self.name} / {self.name_origin} / {self.year}'


class Event(models.Model):
    title = CharField(max_length=200, help_text="Назва")
    description = TextField(help_text="Апісанне")
    start_date = DateTimeField(help_text="Дата пачатку")
    end_date = DateTimeField(help_text="Дата канца")
    location = CharField(max_length=250, help_text="Адрас")

    def __str__(self):
        return self.title


class Banner(models.Model):
    BANNER_CHOICES = (
        ("index_top", _("top on index page")),
        ("index_right", _("right on index page")),
    )

    image = ImageField(storage=IMAGE_STORAGE, blank=True, null=True, help_text="")
    position = models.CharField(max_length=255, choices=BANNER_CHOICES, default='',
                                help_text=_("position for the banner"))

