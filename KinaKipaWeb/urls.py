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
from KinaKipa.views import (get_index_test, test_trans,get_server_info,
                            news, index, catalog)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    # sort logically later
    url(r'^$', index, name='index'),
    url(r'^news/$', news),
    url(r'^server_info/$', get_server_info),
    url(r'^index_test/$', get_index_test),
    url(r'^test_trans/$', test_trans),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'catalog/', catalog, name='catalog')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
