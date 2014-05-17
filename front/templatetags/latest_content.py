from itertools import chain
from operator import attrgetter
from django import template
from blog.models import Entry
from stories.models import Story
from issues.models import Issue

register = template.Library()


@register.assignment_tag
def get_latest_content(limit=6):
    stories = Story.objects.published()[:limit]
    entries = Entry.objects.published()[:limit]
    return sorted(chain(stories, entries), key=attrgetter('pub_date'))[:limit]


@register.assignment_tag
def get_featured_stories_by_section():
    try:
        issue = Issue.objects.latest()
    except Issue.DoesNotExist:
        return None

    return issue.get_featured_stories()
