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
from django.conf.urls import url
from django.contrib import admin
from KinaKipa.views import (get_currency_rate, get_index_page,
                            get_local_dir, get_server_info, hello_world,
                            news, index)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', index),
    url(r'^news/$', news),

    url(r'^server_info/$', get_server_info),
    url(r'^local_directory/$', get_local_dir),
    url(r'^index_test/$', get_index_page),
    url(r'^currency_courses/$', get_currency_rate),

    url(r'^hello_world/$', hello_world),
]
