from django import template
import oembed
oembed.autodiscover()

register = template.Library()

def embed(value, max_width):
	resource = oembed.site.embed(value, maxwidth=max_width)
	embed = resource.get_data()
	return embed['html']

register.filter(embed)