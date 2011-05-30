from django import template
import re
register = template.Library()

def striplinebreaks(value):
    "Strips all carriage returns and line breaks from input."
    breaks_re = re.compile('(\r?\n|\r\n?)')
    value = breaks_re.sub(' ', value)
    return value

register.filter(striplinebreaks)
