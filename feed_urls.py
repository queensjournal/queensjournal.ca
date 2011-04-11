from django.conf.urls.defaults import *
from blog.views import *
from feeds import *

urlpatterns = patterns('',
	url(r'^latest/$', LatestStories()),
	url(r'^section/(?P<url>.*)/', LatestStoriesSection()),
	url(r'^allblogs/$', LatestPostsAllBlogs()),
	url(r'^blogs/(?P<blog>.*)/', LatestPostsSingleBlog()),
	url(r'^author/(?P<url>.*)/', LatestPostsSingleAuthor()),
	url(r'^video/$', LatestVideo())
	)