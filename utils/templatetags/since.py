from django import template
from django.utils.timesince import timesince

register = template.Library()


@register.filter
def since(value, delimiter=","):
    try:
        return timesince(value).split(delimiter)[0]
    except AttributeError:
        return None
