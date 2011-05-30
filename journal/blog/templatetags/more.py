import re
from django import template
from blog.models import Entry

register = template.Library()

def more(value, blog_id):
    """
    Detects the presence of a <!--more--> tag and inserts a break at that
    point, linking to the interior of the blog post. Requires a blog_id string.

    {{ entry.content|...filters here...|more:entry.id }}
    """
    more_re = re.compile('(<!--more-->)')
    entry = Entry.objects.get(pk=blog_id)
    if more_re.search(value) is not None:
        val_chunks = more_re.split(value)
        return '%s(<a href="%s#more">more inside...</a>)' % (val_chunks[0], entry.get_absolute_url())
    else:
        return value

def more_interior(value):
    """
    Detects the presence of a <!--more--> tag and inserts an anchor
    at that point, allowing links from the blog index to point to the
    continuation of the blog post.

    {{ entry.content|...filters here...|more_interior }}
    """
    more_re = re.compile('<!--more-->')
    return more_re.sub('<a name="more"></a>', value)
    
register.filter(more)
register.filter(more_interior)
