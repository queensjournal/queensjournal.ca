from django.conf.urls.defaults import url, patterns, include
from django.conf import settings
from django.views.generic.simple import direct_to_template
from front.views import FrontView
from feeds import LatestFeed, LatestStoriesFeed, LatestStoriesSectionFeed, \
    LatestPostsAllBlogsFeed, LatestPostsSingleBlogFeed, LatestVideosFeed

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Google webmaster tools
    (r'^google9fc9f538545cc45e\.html$', direct_to_template, {'template': 'google9fc9f538545cc45e.html'}),

    # robots
    (r'^robots\.txt$', direct_to_template, {
        'template': 'robots.txt',
        'mimetype': 'text/plain',
        }),

    # front page
    url(r'^$', FrontView.as_view(), name='front'),

    # apps
    (r'^story/', include('stories.urls')),
    (r'^blogs/', include('blog.urls')),
    (r'^video/', include('video.urls')),
    (r'^staff/', include('staff.urls')),
    (r'^images/', include('images.urls')),
    (r'^masthead/', include('masthead.urls')),
    (r'^search/', include('search.urls')),
    (r'^archives/', include('archive.urls')),
    (r'^photos/', include('galleries.urls')),

    (r'^author/(?P<author>[\w-]+)/$', 'masthead.views.detail_author'),

    # admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    # tags
    url(r'^tags/$', 'tags.views.tags', name='tag-index'),
    (r'^tag/', include('tags.urls')),

    # bento
    (r'^boxes/', include('bento.urls')),

    # shorturls
    (r'^s/', include('shorturls.urls')),
)

urlpatterns += patterns('',
    (r'^rss/latest/$', LatestFeed()),
    (r'^rss/latest-stories/$', LatestFeed()),  # preserve old url
    (r'^rss/stories/$', LatestStoriesFeed()),
    (r'^rss/video/$', LatestVideosFeed()),
    (r'^rss/section/(?P<slug>.*)/', LatestStoriesSectionFeed()),
    (r'^rss/allblogs/$', LatestPostsAllBlogsFeed()),
    (r'^rss/blogs/(?P<slug>.*)/$', LatestPostsSingleBlogFeed()),
)

handler500 = 'stories.views.server_error'

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True}),
    )

# pattern has to be last in the lookup order, because of the way we
# look up dynamic section urls
urlpatterns += patterns('',
    url(r'^(?P<section>[-\w]+)/$', 'stories.views.index_section',
        name='front-section'),
)
