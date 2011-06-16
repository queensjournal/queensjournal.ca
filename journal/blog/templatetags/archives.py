from django import template
from blog.models import Entry

register = template.Library()

class BlogByDateNode(template.Node):
	"""
	Returns a context variable containing all the months the blog entries cover.
	"""
	def __init__(self, blog, varname):
		self.blog = blog
		self.varname = varname

	def render(self, context):
		blog_slug = template.resolve_variable(self.blog, context)
		context[self.varname] = Entry.objects.published_on_blog(blog_slug).dates('pub_date','month','DESC')
		return ''

def do_blog_dates(parser, token):
	"""
	{% blog_dates blog.slug as dates %}
	"""
	bits = token.contents.split()
	if len(bits) != 4:
		raise template.TemplateSyntaxError, "'%s' tag takes three arguments" % bits[0]
	if bits[2] != 'as':
		raise template.TemplateSyntaxError, "Second argument to '%s' tag must be 'as'" % bits[0]
	return BlogByDateNode(bits[1], bits[3])
	
register.tag('blog_dates', do_blog_dates)
