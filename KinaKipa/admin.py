# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Article, Event, Film,  Baner


admin.site.register(Article)
admin.site.register(Film)
admin.site.register(Event)
admin.site.register(Baner)
