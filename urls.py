from django.conf.urls.defaults import *
from feeds import *

feeds = {
    'latest': LatestStories,
    'section': LatestStoriesSection,
    'allblogs': LatestPostsAllBlogs,
    'blogs': LatestPostsSingleBlog,
    'blog-author': LatestPostsSingleAuthor,
##    'calendar': LatestCalendar,
}

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
	
urlpatterns = patterns('',
	(r'^polls/', include('polls.urls')),
	(r'^comments/', include('django.contrib.comments.urls')),
	(r'^story/', include('stories.urls')),
	(r'^$', 'stories.views.index_front'),
	(r'^blogs/', include('blog.urls')),
	(r'^staff/', include('journal.staff.urls')),
	#(r'^rss/(?P<url>.*)/', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
	
	# Uncomment the admin/doc line below to enable admin documentation:
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
	
	(r'^(?P<section>[-\w]+)/', 'journal.stories.views.index_section'),
)