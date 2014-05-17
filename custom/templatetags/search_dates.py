from django import template
from datetime import date, timedelta

register = template.Library()

def this_week():
    '''
    {% this_week %}
    '''
    sd = str(date.today() - timedelta(7))
    return '&amp;start_date=' + sd

register.simple_tag(this_week)

def last_week():
    '''
    {% last_weef %}
    '''
    sd = str(date.today() - timedelta(14))
    ed = str(date.today() - timedelta(7))
    return '&amp;start_date=%s&amp;end_date=%s' % (sd, ed)

register.simple_tag(last_week)

def this_month():
    '''
    {% this_month %}
    Not every month has 31 days but who gives a shit?
    '''
    sd = str(date.today() - timedelta(31))
    return '&amp;start_date=' + sd

register.simple_tag(this_month)

def last_month():
    '''
    {% last_month %}
    '''
    sd = str(date.today() - timedelta(60))
    ed = str(date.today() - timedelta(31))
    return '&amp;start_date=%s&amp;end_date=%s' % (sd, ed)

register.simple_tag(last_month)
