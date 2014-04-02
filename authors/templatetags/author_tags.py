from django import template

register = template.Library()


@register.simple_tag
def get_author_role(author, date):
    return author.get_role(date)
