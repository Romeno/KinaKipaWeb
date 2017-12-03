from django.db import models
from django.db.models import (CharField, DateTimeField, FileField, ImageField,
                              PositiveSmallIntegerField, TextField, URLField)
from django.core.files.storage import FileSystemStorage
from django.utils import timezone


IMAGE_STORAGE = FileSystemStorage(location='layout/image')
VIDEO_STORAGE = FileSystemStorage(location='layout/video')


class Article(models.Model):
    title = CharField(max_length=200, verbose_name='article_title', help_text="Назва")
    content = TextField(verbose_name='article_content', help_text="Змест")
    published_date = DateTimeField(blank=True, null=True, help_text="Дата публікацыі")
    image = ImageField(storage=IMAGE_STORAGE, blank=True, null=True, help_text="Карцінка")
    video = FileField(storage=VIDEO_STORAGE, blank=True, null=True, help_text="Відэа")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Film(models.Model):

    GENRES_CHOICES = (
        ('action', 'Баявік'),
        ('adventure', 'Прыгода'),
        ('comedy', 'Камедыя'),
        ('crime', 'Злачынства'),
        ('drama', 'Драма'),
        ('epics/historical', 'Эпас / Гістарычны'),
        ('horror', 'Жахі'),
        ('musicals', 'Мюзікл'),
        ('science fiction', 'Навуковая фантастыка'),
        ('war', 'Ваенны'),
        ('westerns', 'Вестэрн')
    )

    name = CharField(max_length=200, verbose_name='film_name', help_text="Назва")
    director = CharField(max_length=200, help_text="Рэжысёр")
    year = PositiveSmallIntegerField(default=None, help_text="Год")
    genres = CharField(max_length=200, choices=GENRES_CHOICES, help_text="Жанры")
    video = FileField(storage=VIDEO_STORAGE, help_text="Відэа")
    length = PositiveSmallIntegerField(help_text="Працягласць")
    description = TextField(help_text="Апісанне")
    torrent_links = URLField(max_length=200, blank=True, help_text="Спасылка на торэнт")

    def __str__(self):
        return self.name
