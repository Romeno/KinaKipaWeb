from django.http import HttpResponse
from django.conf import settings
from django.template.response import TemplateResponse
from django.shortcuts import render

# Create your views here.


def baravik_py(req):
    from .sites import baravik
    return HttpResponse("Crawled_Film imported and finished successfully!")