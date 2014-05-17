from BeautifulSoup import BeautifulSoup, Comment
from django import template
import re

register = template.Library()

def sanitize_html(value, allowed):
    """
    Strips all [X]HTML tags except the list of tags and attributes passed
    by the filter.

    {{ element_to_cleanse|sanitize:"strong em a p,href src" }}
    """
    tags, attrs = allowed.split(',')
    valid_tags = tags.split()
    valid_attrs = attrs.split()
    soup = BeautifulSoup(value)
    for comment in soup.findAll(
        text=lambda text: isinstance(text, Comment)):
        comment.extract()
    for tag in soup.findAll(True):
        if tag.name not in valid_tags:
            tag.hidden = True
        if len(valid_attrs) != 0:
            tag.attrs = [(attr, val) for attr, val in tag.attrs
                         if attr in valid_attrs]
        else:
            tag.attrs = [(attr, val) for attr, val in tag.attrs]
    javascript_re = re.compile('j[\s]*(&#x.{1,7})?a[\s]*(&#x.{1,7})?v[\s]*(&#x.{1,7})?a[\s]*(&#x.{1,7})?s[\s]*(&#x.{1,7})?c[\s]*(&#x.{1,7})?r[\s]*(&#x.{1,7})?i[\s]*(&#x.{1,7})?p[\s]*(&#x.{1,7})?t[\s]*(&#x.{1,7})?:', re.IGNORECASE)
    return javascript_re.sub('', soup.renderContents().decode('utf8'))

register.filter('sanitize', sanitize_html)
