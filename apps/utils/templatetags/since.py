from django import template
from django.utils.timesince import timesince

register = template.Library()


@register.filter
def since(value, delimiter=","):
    return timesince(value).split(delimiter)[0]
