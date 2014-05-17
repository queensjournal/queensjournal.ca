from django.conf.urls import url, patterns, include
from django.conf import settings
from django.views.generic.base import TemplateView
from front.views import FrontView
from sections.views import SectionDetailView
from feeds import LatestFeed, LatestStoriesFeed, LatestStoriesSectionFeed, \
    LatestPostsAllBlogsFeed, LatestPostsSingleBlogFeed, LatestVideosFeed

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Google webmaster tools
    url(r'^google9fc9f538545cc45e\.html$', TemplateView.as_view(
        template_name='google9fc9f538545cc45e.html')),

    # robots
    url(r'^robots\.txt$', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain',
    )),

    # front page
    url(r'^$', FrontView.as_view(), name='front'),

    # apps
    (r'^story/', include('stories.urls')),
    (r'^blogs/', include('blog.urls')),
    (r'^video/', include('video.urls')),
    (r'^images/', include('images.urls')),
    (r'^masthead/', include('masthead.urls')),
    (r'^search/', include('search.urls')),
    (r'^archives/', include('archive.urls')),
    (r'^issues/', include('issues.urls')),
    (r'^photos/', include('galleries.urls')),

    (r'^author/', include('authors.urls')),

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

    # selectable
    (r'^selectable/', include('selectable.urls')),
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

handler500 = 'utils.views.server_error'

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True}),
    )

# pattern has to be last in the lookup order, because of the way we
# look up dynamic section urls
urlpatterns += patterns('',
    url(r'^(?P<slug>[-\w]+)/$', SectionDetailView.as_view(),
        name='front-section'),
)
