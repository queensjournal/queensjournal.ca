import re
from django.utils.http import urlquote
from django import template
from htmlentitydefs import codepoint2name
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ungettext, ugettext
from datetime import datetime

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

def choptext(value, char='20'):
   count = int(char)
   if len(value) > count:
      count = count - 1
      exp = r'^\s*(.{0,%s}[^\s])\b\s*(.*)' % char
      m = re.compile(exp).match(value)
      result = '<span class="chopped">%s<span> %s</span></span>' % (conditional_escape(m.group(1)), conditional_escape(m.group(2)))
      return mark_safe(result)
   else:
      return value

def date_diff(timestamp, to=None):
    if not timestamp:
        return ""

    compare_with = to or datetime.now()
    delta = timestamp - compare_with

    if delta.days == 0: return u"today"
    elif delta.days == -1: return u"yesterday"
    elif delta.days == 1: return u"tomorrow"

    chunks = (
        (365.0, lambda n: ungettext('year', 'years', n)),
        (30.0, lambda n: ungettext('month', 'months', n)),
        (7.0, lambda n : ungettext('week', 'weeks', n)),
        (1.0, lambda n : ungettext('day', 'days', n)),
    )

    for i, (chunk, name) in enumerate(chunks):
        if abs(delta.days) >= chunk:
            count = abs(round(delta.days / chunk, 0))
            break

    date_str = ugettext('%(number)d %(type)s') % {'number': count, 'type': name(count)}

    if delta.days > 0: return "in " + date_str
    else: return date_str + " ago"

def timesince(start_time):
    delta = datetime.datetime.now() - start_time

    plural = lambda x: 's' if x != 1 else ''

    num_years = delta.days / 365
    if (num_years > 0):
        return "%d year%s" % (num_years, plural(num_years))

    num_weeks = delta.days / 7
    if (num_weeks > 0):
        return "%d week%s" % (num_weeks, plural(num_weeks))

    if (delta.days > 0):
        return "%d day%s" % (delta.days, plural(delta.days))

    num_hours = delta.seconds / 3600
    if (num_hours > 0):
        return "%d hour%s" % (num_hours, plural(num_hours))

    num_minutes = delta.seconds / 60
    if (num_minutes > 0):
        return "%d minute%s" % (num_minutes, plural(num_minutes))

    return "a few seconds"

def truncatesmart(value, limit=80):
    """
    Truncates a string after a given number of chars keeping whole words.

    Usage:
        {{ string|truncatesmart }}
        {{ string|truncatesmart:50 }}
    """

    try:
        limit = int(limit)
    # invalid literal for int()
    except ValueError:
        # Fail silently.
        return value

    # Make sure it's unicode
    value = unicode(value)

    # Return the string itself if length is smaller or equal to the limit
    if len(value) <= limit:
        return value

    # Cut the string
    value = value[:limit]

    # Break into words and remove the last
    words = value.split(' ')[:-1]

    # Join the words and return
    return ' '.join(words) + '...'

def striplabel(value, delimiter=','):
    """
    Strips and returns the first tag out of a TagField for our "Story Label" display
    """
    value = unicode(value)

    if delimiter in value:
        value = value.split(',')[0]
        return value
    else:
        return value

def possessive(value):
    """
    Returns a possessive form of a name according to English rules
    Mike returns Mike's, while James returns James'
    """
    if value[-1] == 's':
        return "%s'" % value
    return "%s's" % value

def urlencode(value):
    return urlquote(value)

def paragraphs(var, arg):
    '''
    Returns a index of paragraphs. E.g. {{ content|paragraphs:'3:' }} will return the fourth paragraph and on.

    '''
    ints = arg.split(':')
    for i, c in enumerate(ints):
        if c == '':
            del ints[i]
    paras = var.replace("\r\n", "\n").split("\n\n")
    if len(ints) > 1:
        return "\n\n".join(paras[int(ints[0]):int(ints[1])])
    else:
        return "\n\n".join(paras[int(ints[0]):])

register.filter(convert_entities)
register.filter(linebreakswithcode)
register.filter(stripspace)
register.filter(choptext)
register.filter(date_diff)
register.filter(striplabel)
register.filter(possessive)
register.filter(urlencode)
register.filter(paragraphs)
register.filter(timesince)
