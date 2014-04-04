from django import template
from stories.models import Story

register = template.Library()


@register.assignment_tag
def get_featured_section_content(section, limit=6):
    return section.get_featured_stories()[:limit]


@register.assignment_tag
def get_section_issue_content(section, issue, limit=6):
    featured = Story.objects.filter(section=section,
        featured=True)[:1].get()
    other = section.get_issue_stories(issue).exclude(pk=featured.pk)
    return {
        'featured': featured,
        'other': other,
    }
