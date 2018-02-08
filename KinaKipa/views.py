# -*- coding: utf-8 -*-
import os
import pip
import requests
import sys
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.translation import ugettext as _
from el_pagination.decorators import page_template
from .models import Article, Banner, Film, Event

# Create your views here.


def index(req):
    news = Article.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:4]
    films = Film.objects.order_by("-id")
    drama = films.filter(genres__name__in=['драма'])[:4]
    comedies = films.filter(genres__name__in=['камедыя']).exclude(genres__name__in=['драма'])[:4]
    crimes = films.filter(genres__name__in=['крымінальны']).exclude(genres__name__in=['камедыя'])[:4]
    fiction = films.filter(genres__name__in=['фантастыка']).exclude(genres__name__in=['крымінальны'])[:4]
    return TemplateResponse(
        req, 'index.html',{
            'news1': news[:2], 'news2': news[2:4],
            'drama1': drama[:2], 'drama2': drama[2:4],
            'comedies1': comedies[:2], 'comedies2': comedies[2:4],
            'crimes1': crimes[:2], 'crimes2': crimes[2:4],
            'fiction1': fiction[:2], 'fiction2': fiction[2:4]
        }
    )


def news(request, pk):
    news = get_object_or_404(Article, pk=pk)
    return render(request, 'news.html', {'news': news})


def last_news(request):
    l_news = Article.objects.last()
    format_time = l_news.published_date.strftime("%d-%m-%Y %H:%M")
    return render(request, 'news.html', {'last_news': l_news, 'time': format_time, 'range': range(0, 2)})


def my_ajax(request):
    return JsonResponse({'data': 'some data'})


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


@page_template('catalog_endless_pages.html')
def catalog(request, template='catalog.html', extra_context=None):
    films = Film.objects.order_by("id").reverse()
    context = {
        'films': films
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def p_film(request):
    return TemplateResponse(request,  'p_film.html')


def last_banner(request):
    banner_cursor = Banner.objects.last()
    return render(request, 'index.html', {'banner': banner_cursor})


MONTHS = {
    1: _('january'), 2: _('february'), 3: _('march'),
    4: _('april'), 5: _('may'), 6: _('june'),
    7: _('july'), 8: _('august'), 9: _('september'),
    10: _('october'), 11: _('november'), 12: _('december')
}


def get_events(request):
    events = Event.objects.filter(end_date__gte=timezone.now())
    result = []
    for event in events:
        result.append({
            'id': event.pk,
            'title': event.title,
            'balloon_description': event.balloon_description,
            'full_description': event.full_description,
            'start_date': event.start_date.strftime('%H:%M %d.{0}.%Y').format(_(MONTHS[event.start_date.month])),
            'end_date': event.end_date.strftime('%H:%M %d.{0}.%Y').format(_(MONTHS[event.end_date.month])),
            'location': event.location
        })
    return JsonResponse({'events': result})


def film(request, film_id):
    found = Film.objects.filter(id__exact=film_id)
    if not found:
        # return 404
        pass
    film = found[0] # for filter returns queryset, but film needed



    return render(request, 'film.html', {'film': film})