# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from .models import Article, Event, Film, Baner

class TinyMCEAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/static/js/tiny_mce/tiny_mce.js',
            '/static/js/tiny_mce/textareas.js',
        )

# tinymce models
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, TinyMCEAdmin)
admin.site.register(Article, TinyMCEAdmin)

# django models
admin.site.register(Film)
admin.site.register(Event)
admin.site.register(Baner)