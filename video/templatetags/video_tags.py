from django import template
from ..models import Video

register = template.Library()


@register.assignment_tag
def get_featured_video():
    return Video.objects.featured()
