# -*- coding: utf-8 -*-
import os
import pip
import requests
import sys
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from .models import Film
from .models import Baner

# Create your views here.


def index(request):
    last_films = Film.objects.exclude(image=None)[:5]
    return render(request, 'index.html', {'last_films':last_films})


def news(request):
    return TemplateResponse(request, 'news.html', {})


def test_trans(req):
    from django.utils.translation import activate, get_language_info

    activate('be')
    li = get_language_info('be')
    resp = "Translating: "
    resp += _("Administration")
    resp += "<br>"
    for k, v in li.items():
        resp += f"{k}: {v} <br>"

    return HttpResponse(resp)


def get_server_info(req):
    """
    Написать обработчик на урл server_info, который будет выводить системную ифнормацию:
    версию питона
    версии сторонних библиотек питона, установленных на машине (включая джанго и другие)
    название и версию операционной системы"
    """
    from platform import platform, machine

    _modules = [str(x) for x in pip.get_installed_distributions()]

    installed_modules = 'Modules version: <br>' + '<br>'.join(_modules)
    version = 'Python version: <br>' + sys.version
    windows_version = 'Windows version: <br>' + platform() + ' ' + machine()

    response = f"""
    <ul style="font-family: helvetica, arial">
        <li><span>{version}</span></li>
        <li><span>{installed_modules}</span></li>
        <li><span>{windows_version}</span></li>
    </ul>
    """
    return HttpResponse(response)


def last_film(request):
    film_cursor = Film.objects.last()
    return render(request, 'film_page.html', {'film': film_cursor})


def catalog(requst):
    return TemplateResponse(requst, 'catalog.html')


def p_film(request):
    return TemplateResponse(request,  'p_film.html')


def last_baner(request):
    baner_cursor = Baner.objects.last()
    return render(request, 'index.html', {'baner':baner_cursor})
