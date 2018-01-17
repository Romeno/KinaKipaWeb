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
from KinaKipa.views import (test_trans, get_server_info,
                            news, index, last_film, catalog, p_film, last_baner)

import tagulous.views
from KinaKipa.models import Genre


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^pages/', include('django.contrib.flatpages.urls')),

    # main web pages
    url(r'^$', index, name='index'),
    url(r'^news/$', news),
    url(r'^last_film/$', last_film),
    url(r'^p_film/$', p_film, name='p_film'),

    # development tests
    url(r'^test_trans/$', test_trans),
    url(r'^server_info/$', get_server_info),
    url(r'^catalog/$', catalog, name='catalog'),
    url(r'^p_film/$', p_film, name='p_film'),

    # Tagulous api to call autocomplete via JS
    url(
        r'^api/genres/$',
        tagulous.views.autocomplete,
        {'tag_model': Genre},
        name='film_genres_autocomplete',
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
