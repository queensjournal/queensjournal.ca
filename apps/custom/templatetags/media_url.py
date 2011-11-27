from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def media_url(value):
    """Searches for {{ MEDIA_URL }} and replaces it with the MEDIA_URL from settings.py"""
    return value.replace('{{ MEDIA_URL }}', settings.MEDIA_URL)
media_url.is_safe = True
