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
    badge_image = FileBrowseField(max_length=500, extensions=settings.FILEBROWSER_EXTENSIONS['Image'],
                                  directory="images/", verbose_name=_('Badge image'),
                                  help_text=_('Image for the article that will be used on all list pages'))
    # news_icon_link = URLField(
    #     max_length=500, blank=True,
    #     verbose_name=_('Link to news icon'), help_text=_('Link to image for news icon'))
    content = HTMLField(verbose_name=_('Article content'), help_text=_('Article content'))
    published_date = DateTimeField(default=timezone.now, verbose_name=_('Publication date'),
                                   help_text=_('Publication date'))

    # video_link = CharField(
    #     max_length=500, blank=True,
    #     verbose_name=_('Video'), help_text=_('Link to video. Needs "iframe" tag'))

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

    # @film's names
    name = CharField(max_length=200, verbose_name=_('Movie name'), help_text=_('Movie name'), unique=True)
    name_origin = CharField(max_length=200, verbose_name=_('Original movie name'),
                            help_text=_('Name of the movie in the language of the original'), blank=True)

    # @people
    director = CharField(max_length=200, verbose_name=_('Director'), blank=True)
    stars = CharField(max_length=800, verbose_name=_('Actors'), blank=True)

    # @text information
    description = TextField(verbose_name=_('Description'), blank=True)
    country = CharField(max_length=200, verbose_name=_('Country'), help_text=_('Country of production'),blank=True)

    # @numeric values
    # >>> ratings are currently optional
    kp_rating = FloatField(default=0.0, verbose_name=_('Kinopoisk rating'),
                           help_text=_('Film ratings on kinopoisk.ru'), blank=True)
    imdb_rating = FloatField(default=0.0, verbose_name=_('Imdb rating'),
                             help_text=_('Film ratings on imdb.com'), blank=True)
    year = CharField(max_length=4, verbose_name=_('Year'),
                     help_text=_('Year of creation'), blank=True)
    length = CharField(max_length=30, verbose_name=_('Length'), help_text=_('Movie length'), blank=True)

    # @meta information
    genres = tagulous.models.TagField(to=Genre, verbose_name=_('Movie genres'),
                                      help_text=_('Genres can include spaces. Used like tags.'), blank=True)
    video_html = TextField(verbose_name=_('Video html code'),
                           help_text=_('html code for displaying the video'), blank=True)
    image = FileBrowseField(max_length=500, directory="images/poster", null=True, blank=True,
                            extensions=settings.FILEBROWSER_EXTENSIONS['Image'], verbose_name=_('Image'),
                            help_text=_('Image for the movie that will be used on all list pages'))
    torrent_link = URLField(max_length=2000, blank=True, verbose_name=_('Torrent link'), help_text=_('Torrent link'))

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
    title = CharField(max_length=200, verbose_name=_('Title'), help_text=_('Event title'))
    description = TextField(verbose_name=_('Description'), help_text=_('Event description'))
    start_date = DateTimeField(verbose_name=_('Start date'), help_text=_('Date and time when the event starts'))
    end_date = DateTimeField(verbose_name=_('End date'), help_text=_('Date and time when the event ends'))
    location = CharField(max_length=250, verbose_name=_('Location'), help_text=_('Event\s location'))

    def __str__(self):
        return self.title


class Banner(models.Model):
    BANNER_CHOICES = (
        ("index_top", _("top on index page")),
        ("index_right", _("right on index page")),
    )

    image = ImageField(storage=IMAGE_STORAGE, blank=True, null=True, verbose_name=_('Banner image'), help_text=_('Banner consists of image and link'))
    url = URLField(verbose_name=_('Url'), help_text=_('Url where banner will lead to'))
    position = models.CharField(max_length=255, choices=BANNER_CHOICES, verbose_name=_('Banner position'),
                                help_text=_("On which pages and where this banner will be positioned"))

