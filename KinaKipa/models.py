from django.db import models
from django.db.models import CharField


class Article(models.Model):
    title = CharField(max_length=200, verbose_name='article_title')
