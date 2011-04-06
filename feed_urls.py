from django.conf.urls.defaults import *
from blog.views import *
from feeds import *

feeds = {
	'latest': LatestStories(),
	'section': LatestStoriesSection(),
	'allblogs': LatestPostsAllBlogs(),
	'blogs': LatestPostsSingleBlog(),
	'author': LatestPostsSingleAuthor(),
##	  'calendar': LatestCalendar,
}

urlpatterns = patterns('',
	url(r'^latest/$', LatestStories()),
	url(r'^section/(?P<url>.*)/', LatestStoriesSection()),
	url(r'^allblogs/$', LatestPostsAllBlogs()),
	url(r'^blogs/(?P<blog>.*)/', LatestPostsSingleBlog()),
	url(r'^author/(?P<url>.*)/', LatestPostsSingleAuthor()),
	)