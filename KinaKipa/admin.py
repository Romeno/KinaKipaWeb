from django.contrib import admin
from .models import Article, Event, Film


admin.site.register(Article)
admin.site.register(Film)
admin.site.register(Event)