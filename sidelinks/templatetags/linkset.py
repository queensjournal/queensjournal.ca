from django import template
from sidelinks.models import SidebarLinkset

register = template.Library()

class SidebarLinksNode(template.Node):
    def __init__(self, slug, var):
        self.slug, self.var = slug, var

    def render(self, context):
        try:
            linkset = SidebarLinkset.objects.get(slug__exact=self.slug.strip("'").strip('"'))
        except SidebarLinkset.DoesNotExist:
            return None
        context[self.var] = linkset.link_set.filter(active=True)
        return ''

def do_sidebar_linkset(parser, token):
    """
    {% linkset linkset_slug as links %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError, '%s takes two arguments' % bits[0]
    if bits[2] != 'as':
        raise template.TemplateSyntaxError, 'Second argument of %s should be "as"' % bits[0]
    return SidebarLinksNode(bits[1], bits[3])

register.tag('linkset', do_sidebar_linkset)
