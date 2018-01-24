# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from .models import Article, Event, Film, Banner, Genre
from Crawler.models import Crawled_Film
from flatblocks.models import FlatBlock
from flatblocks.forms import FlatBlockForm
from tinymce.widgets import TinyMCE


class TinyMCEAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/static/js/tiny_mce/tiny_mce.js',
            '/static/js/tiny_mce/textareas.js',
        )


class FlatBlockForm2(FlatBlockForm):
    class Meta:
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30})
        }


class FlatBlockAdmin(admin.ModelAdmin):
    ordering = ['slug', ]
    list_display = ('slug', 'header')
    search_fields = ('slug', 'header', 'content')
    form = FlatBlockForm2


# tagulous models
admin.site.register(Genre)

# tinymce models
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, TinyMCEAdmin)
admin.site.register(Article, TinyMCEAdmin)

# django models
admin.site.register(Film)
admin.site.register(Event)
admin.site.register(Banner)

# # crawler
# admin.site.register(Crawled_Film)

# flatblocks
admin.site.unregister(FlatBlock)
admin.site.register(FlatBlock, FlatBlockAdmin)
