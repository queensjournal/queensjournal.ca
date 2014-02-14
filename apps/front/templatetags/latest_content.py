from itertools import chain
from operator import attrgetter
from django import template
from blog.models import Entry
from stories.models import Story

register = template.Library()


@register.assignment_tag
def get_latest_content(limit=6):
    stories = Story.objects.published()[:limit]
    entries = Entry.objects.published()[:limit]
    return sorted(chain(stories, entries), key=attrgetter('pub_date'))[:limit]
