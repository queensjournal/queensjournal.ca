from django import template
from django.contrib.contenttypes.models import ContentType
from blog.models import Entry
import feedparser

register = template.Library()

class LatestEntriesNode(template.Node):
    """
    Returns a context dictionary containing the last x nodes.
    """
    def __init__(self, varname, blog, num):
        self.varname = varname
        self.blog = blog
        self.num = int(num)

    def render(self, context):
        blog_slug = template.resolve_variable(self.blog, context)
        context[self.varname] = Entry.objects.published_on_blog(blog_slug).order_by('-pub_date')[:self.num]
        return ''


class LatestLinksNode(template.Node):
    """
    Returns a context dictionary containing the last x incoming links.
    """
    def __init__(self, varname, num, url):
        self.varname = varname
        self.num = int(num)
        self.url = url.strip('"')

    def render(self, context):
        feed = feedparser.parse(self.url)
        context[self.varname] = feed.entries[:self.num]
        return ''

def do_latest_entries(parser, token):
    """
    {% latest_entries blog.slug 10 as entries %}
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError, "'%s' tag takes three arguments" % bits[0]
    if bits[3] != 'as':
        raise template.TemplateSyntaxError, "Second argument to '%s' tag must be 'as'" % bits[0]
    return LatestEntriesNode(bits[4], bits[1], bits[2])

def do_latest_links(parser, token):
    """
    {% latest_links "http://feeds.technorati.com/search/www.queensjournal.ca"+blog.get_absolute_url 10 as entries %}
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError, "'%s' tag takes four arguments" % bits[0]
    if bits[3] != 'as':
        raise template.TemplateSyntaxError, "Third argument to '%s' tag must be 'as'" % bits[0]
    return LatestLinksNode(bits[4], bits[2], bits[1])

register.tag('latest_entries', do_latest_entries)
register.tag('latest_links', do_latest_links)
