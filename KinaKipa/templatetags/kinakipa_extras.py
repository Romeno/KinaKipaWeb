import re
from django import template
from django.utils import timezone
from django.utils.translation import ugettext as _


register = template.Library()


@register.filter(name='format_latest_date')
def format_news_date(date):
    if (timezone.now() - date).days > 0:
        return date.strftime("%d.%m.%Y %H:%M")
    hours = (timezone.now() - date).seconds // 3600
    if hours > 0:
        message = _('hours ago')
        return "{0} {1}".format(hours, message)
    else:
        minutes = (timezone.now() - date).seconds // 60 - hours
        message_true = _('minutes ago')
        message_false = _('just now')
        answer = "{0} {1}".format(minutes, message_true) if minutes > 10 else message_false
        return answer


@register.filter(name='clean_text')
def clean_text(html_field):
    html_field = re.sub(r"<br.*? />", "\n", html_field)
    html_field = re.sub(r"&[a-z]{1,10};", " ", html_field)
    html_field = re.sub(
        r"<[a-z]{0,10}[\sA-z=\"-:;,#%?]*>|\\r|<img.*/>",
        "", html_field
    )
    return re.sub(r"[\n]{1,5}", "<br />", html_field)
