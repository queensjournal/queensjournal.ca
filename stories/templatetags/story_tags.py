from django import template
from stories.models import Story

register = template.Library()


@register.assignment_tag
def get_latest_stories(section=None, *args, **kwargs):
    if section:
        return section.get_latest_stories()
    else:
        return Story.objects.latest()
