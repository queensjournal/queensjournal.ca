from django import template
from stories.models import Story

register = template.Library()


@register.assignment_tag
def get_latest_stories(section=None, limit=10, *args, **kwargs):
    if section:
        return section.get_latest_stories()[:limit]
    else:
        return Story.objects.latest()[:limit]


@register.assignment_tag
def get_last_updated():
    try:
        latest = Story.objects.latest().pub_date
    except Story.DoesNotExist:
        return None
    return latest
