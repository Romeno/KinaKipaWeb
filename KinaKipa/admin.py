# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from .models import Article, Event, Film, Banner, Genre, HeroSlide, MovieHeroSlide
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

        css = {
            'all': ('/static/css/content-1.01.css',),
        }


class FlatBlockForm2(FlatBlockForm):
    class Meta:
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30})
        }


class FlatBlockAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/static/js/tiny_mce/tiny_mce.js',
            '/static/js/tiny_mce/textareas.js',
        )

        css = {
            'all': ('/static/css/content-1.01.css',),
        }

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
admin.site.register(Film, TinyMCEAdmin)
admin.site.register(Event, TinyMCEAdmin)
admin.site.register(Banner)
admin.site.register(HeroSlide)
admin.site.register(MovieHeroSlide)

# # crawler
# admin.site.register(Crawled_Film)

# flatblocks
admin.site.unregister(FlatBlock)
admin.site.register(FlatBlock, FlatBlockAdmin)
