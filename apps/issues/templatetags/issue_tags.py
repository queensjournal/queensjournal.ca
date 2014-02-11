from django import template
from issues.models import Issue

register = template.Library()


@register.assignment_tag
def get_latest_issue():
    return Issue.objects.latest()
