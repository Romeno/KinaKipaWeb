# -*- coding: utf-8 -*-
import os
import pip
import requests
import sys
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.template.response import TemplateResponse


# Create your views here.


def hello_world(req):
    return HttpResponse("Hello World!")


def index(req):
    return TemplateResponse(req, 'index.html', {})


def news(request):
    return TemplateResponse(request, 'news.html', {})


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


def get_local_directory(req):
    """
    "Написать обработчик на урл local_directory,
    который будет выводить: содержимое дерева
    директорий папки KinaKipaWeb"
    """
    def search(current_dir=settings.BASE_DIR):
        items_name = os.listdir(current_dir)
        items_path = [os.path.join(current_dir, item) for item in items_name]
        for i, item_path in enumerate(items_path):
            try:
                is_files_inside = len(os.listdir(item_path)) > 0
                items_path[i] = search(item_path) if is_files_inside else item_path
            except NotADirectoryError:
                items_path[i] = item_path
        return items_path

    # спиздил flatten() функцию
    def flatten(container):
        for i in container:
            if isinstance(i, (list, tuple)):
                for j in flatten(i):
                    yield j
            else:
                yield i

    response = '<br>'.join(flatten(search()))

    return HttpResponse(response)


def get_index_test(req):
    """
    Написать обработчик на урл index_test, который будет
    выводить: прочитает старницу index.html из файла и
    отдаст её в запросе, так чтобы она вернулась в запросе
    """
    filepath = os.path.join(settings.BASE_DIR, 'layout', 'index.html')

    with open(filepath, encoding='utf-8') as file:
        html = file.readlines()

    response = [line for line in html]
    return HttpResponse(response)


def get_currency_courses(req):
    """
    Написать обработчик на урл currency_courses, который
    будет выводить курс рубля к доллару и евро на сегодня.
    Для получения данных использовать бибилиотеку requests
    и любой сайт, который предоставляет эти сведения.
    """
    link_usd = 'http://www.nbrb.by/API/ExRates/Rates/USD?ParamMode=2'
    link_eur = 'http://www.nbrb.by/API/ExRates/Rates/EUR?ParamMode=2'

    usd = requests.get(link_usd)
    eur = requests.get(link_eur)

    rate_usd = usd.json()['Cur_OfficialRate']
    rate_eur = eur.json()['Cur_OfficialRate']

    response = f"""
    <h2>Оффициальный курс белорусского рубля</h2>
    <p>По отношению к доллару: {rate_usd}</p>
    <p>По отношению к евро: {rate_eur}</p>
    """
    return HttpResponse(response)
