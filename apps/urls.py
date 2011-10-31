from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from feeds import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

feeds = {
    'latest': Latest,
    'latest-stories': LatestStories,
    'section': LatestStoriesSection,
    'allblogs': LatestPostsAllBlogs,
    'blogs': LatestPostsSingleBlog,
    'video': LatestVideos
##    'calendar': LatestCalendar,
}

urlpatterns = patterns('',
    (r'^google9fc9f538545cc45e\.html$', direct_to_template, {'template': 'google9fc9f538545cc45e.html'}),
    (r'^robots\.txt$', direct_to_template, {'template': 'robots.txt'}),
    (r'^polls/', include('polls.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^story/', include('stories.urls')),
    (r'^$', 'stories.views.index_front'),
    (r'^blogs/', include('blog.urls')),
    (r'^video/', include('video.urls')),
    (r'^staff/', include('staff.urls')),
    (r'^images/', include('images.urls')),
    (r'^masthead/', include('masthead.urls')),
    (r'^search/', include('search.urls')),
    (r'^author/(?P<author>[\w-]+)/$', 'masthead.views.detail_author'),
    (r'^rss/(?P<url>.*)/', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^archives/', include('stories.archive_urls')),
    (r'^photos/', include('galleries.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^tags/$', 'stories.views.tags'),
    (r'^tag/(?P<tag>.*)/$','stories.views.with_tag'),
    (r'^tag/(?P<tag>.*)/page/(?P<id>[-\w]+)/$', 'stories.views.with_tag' ),

    (r'^s/', include('shorturls.urls')),

    # Because I have the URL regexing words as sections, this pattern needs to be last.
    # If you put anything after, the CONF will think it's a section and you won't get anywhere.
    ## THE FOLLOWING LINE MUST BE THE LAST URL IN THE CONF
    #(r'^(?P<section>[-\w]+)/$', 'stories.views.index_section'),
    ## DO NOT ADD ANY URLS AFTER THIS LINE
)

handler500 = 'stories.views.server_error'

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True}),
    )
