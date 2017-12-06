import os
import pip
import requests
import sys
from django.shortcuts import render
from django.http import HttpResponse
from KinaKipaWeb.settings import BASE_DIR
from django.template.response import TemplateResponse


# Create your views here.


def test_view(req):
    return HttpResponse("Hello World!")


def test(req):
    return TemplateResponse(req, 'index.html', {})


def news(request):
    return TemplateResponse(request, 'news.html', {})


def get_server_info(req):
    python_version = "Python {}".format(sys.version[:5])
    site_packages = "\n".join([str(pac)for pac in pip.get_installed_distributions()])
    os_version = "{} Windows {}".format(sys.platform, sys.getwindowsversion().major)
    response = "{}\n{}\n{}".format(python_version, site_packages, os_version)

    return HttpResponse(response)


def get_local_dir(req):
    dir_tree = os.walk(os.path.join(BASE_DIR, "KinaKipaWeb"))
    response = [dir for dir in dir_tree]

    return HttpResponse(response)


def get_index_page(req):
    path = os.path.join(BASE_DIR, "layout", "index.html")
    response = []
    with open(path, 'r', encoding='utf8') as index_html:
        index_html = index_html
        for line in index_html.readlines():
            response.append(line)

    return HttpResponse(response)


def get_currency_rate(req):
    result = {'USD': '', 'EUR': ''}

    try:
        get_request = requests.get(
            "http://www.nbrb.by/API/ExRates/Rates?Periodicity=0"
        )
        for cur in get_request.json():
            if cur['Cur_Abbreviation'] == 'USD':
                result['USD'] = cur['Cur_OfficialRate']
            elif cur['Cur_Abbreviation'] == 'EUR':
                result['EUR'] = cur['Cur_OfficialRate']
    except:
        result['USD'] = 'Not Found'
        result['EUR'] = 'Not Found'

    response = ["{}: {}\n".format(item[0], item[1]) for item in result.items()]

    return HttpResponse(response)





