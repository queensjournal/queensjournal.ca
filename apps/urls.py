from django.conf.urls.defaults import url, patterns, include
from django.conf import settings
from django.views.generic.simple import direct_to_template
from stories.views import Front
from feeds import LatestFeed, LatestStoriesFeed, LatestStoriesSectionFeed, \
    LatestPostsAllBlogsFeed, LatestPostsSingleBlogFeed, LatestVideosFeed

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^google9fc9f538545cc45e\.html$', direct_to_template, {'template': 'google9fc9f538545cc45e.html'}),
    (r'^robots\.txt$', direct_to_template, {
        'template': 'robots.txt',
        'mimetype': 'text/plain',}),
    (r'^polls/', include('polls.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^story/', include('stories.urls')),
    url(r'^$', Front.as_view()),
    (r'^blogs/', include('blog.urls')),
    (r'^video/', include('video.urls')),
    (r'^staff/', include('staff.urls')),
    (r'^images/', include('images.urls')),
    (r'^masthead/', include('masthead.urls')),
    (r'^search/', include('search.urls')),
    (r'^author/(?P<author>[\w-]+)/$', 'masthead.views.detail_author'),
    (r'^archives/', include('archive.urls')),
    (r'^photos/', include('galleries.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^tags/$', 'tags.views.tags'),
    (r'^tag/', include('tags.urls')),

    (r'^s/', include('shorturls.urls')),
)

urlpatterns += patterns('',
    (r'^rss/(?P<url>.*)/', LatestFeed()),
)

handler500 = 'stories.views.server_error'

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True}),
    )

urlpatterns += patterns('',
    (r'^(?P<section>[-\w]+)/$', 'stories.views.index_section'),
)
