import re
from django import template
from django.utils.encoding import smart_unicode
from htmlentitydefs import codepoint2name
register = template.Library()

def convert_entities(value):
    """
    Better conversion method from Unicode to HTML entities.
    """
    entities = list()
    for c in value:
        if ord(c) < 128:
            entities.append(c)
        else:
            try:
                entities.append('&%s;' % codepoint2name[ord(c)])
            except KeyError:
                continue
    return ''.join(entities)

def linebreakswithcode(value):
    """
    Inserts paragraph tags at line breaks, EXCEPT when an HTML element starts the
    next line.
    """
    INLINE_ELEMENTS = ['em','strong','q','cite','dfn','abbr','acronym',
                       'code','samp','kbd','var','sub','sup','del','ins','a',
                       'img','br','map','area','object','param','span']
    from django.utils.html import linebreaks
    inline_regex = '|'.join(INLINE_ELEMENTS)
    wrappedblockshtml_re = re.compile(r'(<p>|<br */>)+(<(?!' + inline_regex + ')([^>]*)>[^\r\n]+</\3>)(</p>|<br */>)+')
    trappedbreakshtml_re = re.compile(r'(</?(?!' + inline_regex + ')[^>]+>)<br */>(?=</?(?!' + inline_regex + ')[^>]+>)')
    value = linebreaks(value)
    value = wrappedblockshtml_re.sub(r'\2', value)
    value = trappedbreakshtml_re.sub(r'\1', value)
    return value

def stripspace(value):
    """
    Strips leading and trailing whitespace. (Why isn't this already a standard
    Django filter? The mind boggles.)
    """
    return value.strip()

register.filter(convert_entities)
register.filter(linebreakswithcode)
register.filter(stripspace)
