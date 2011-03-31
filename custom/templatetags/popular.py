from django import template
from django.utils import simplejson as json
from dependencies.disqus import DisqusClient

register = template.Library()

def disqus_popular():
	client = DisqusClient()
	forum_list = client.get_most_commented_threads(user_api_key=settings.DISQUS_API_KEY)
	try:
		forum = [f for f in forum_list\
				 if f['shortname'] == settings.DISQUS_WEBSITE_SHORTNAME][0]
		return forum
	except IndexError:
		raise CommandError("Could not find forum. " +
									   "Please check your " +
									   "'DISQUS_WEBSITE_SHORTNAME' setting.")

register.filter(disqus_popular)