# -*- coding: utf-8 -*-
"""KinaKipaWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from KinaKipa.views import (test_trans, get_server_info,
                            news, index, last_film, catalog, movie_screenings,
                            last_news, my_ajax, get_events, film)
from filebrowser.sites import site
import tagulous.views
from KinaKipa.models import Genre
from haystack.views import SearchView


urlpatterns = [
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),

    # url(r'^my_ajax/$', my_ajax),

    # Tagulous api to call autocomplete via JS
    url(
        r'^api/genres/$',
        tagulous.views.autocomplete,
        {'tag_model': Genre},
        name='film_genres_autocomplete',
    ),
]

# These urls will lead to pages that will be dependant on Language chosen by user
# Language setting will be in URL
urlpatterns += i18n_patterns(
    url(r'^pages/', include('django.contrib.flatpages.urls')),

    # main web pages
    url(r'^$', index, name='index'),
    url(r'^news/(?P<pk>\d+)/$', news, name='news_id'),
    url(r'^events/$', movie_screenings, name='movie_screenings'),
    url(r'^film/(?P<film_id>[0-9]+)$', film, name='film_id'),
    url(r'^catalog/$', catalog, name='catalog'),
    url(r'^search/$', SearchView(), name='search'),

    # ajax
    url(r'^api/events/$', get_events),






    # development tests
    url(r'^test_trans/$', test_trans),
    url(r'^server_info/$', get_server_info),

    url(r'^last_news/$', last_news),
    url(r'^last_film/$', last_film),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
