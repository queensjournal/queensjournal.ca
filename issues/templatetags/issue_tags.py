from django import template
from issues.models import Issue

register = template.Library()


@register.assignment_tag
def get_latest_issue():
    try:
        return Issue.objects.latest()
    except Issue.DoesNotExist:
        return None
