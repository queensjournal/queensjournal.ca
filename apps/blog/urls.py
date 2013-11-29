from django.conf.urls.defaults import patterns, url
from blog.views import BlogListView, BlogDetailView, EntryMonthView, \
    EntryDetail

urlpatterns = patterns('',
    # Remove:
    #url(r'^archived/$', all_blogs, {'active': False}, name='all_blogs_archived'),

    url(r'^$', BlogListView.as_view(), name='all_blogs'),

    url(r'^(?P<blog>[-_\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-_\w]+)/$',
        EntryDetail.as_view(), name="entry-detail"),

    url(r'^(?P<blog>[-_\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/page/(?P<page>\d{1,5})/$',
        EntryMonthView.as_view(), name='blog_archive_month_pages'),

    url(r'^(?P<blog>[-_\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/$',
        EntryMonthView.as_view(),
        name='blog_archive_month_front'),

    url(r'^(?P<slug>[-_\w]+)/page/(?P<page>\d{1,5})/$', BlogDetailView.as_view(),
        name='blog-index'),

    url(r'^(?P<slug>[-_\w]+)/$', BlogDetailView.as_view(), name='blog-index'),
)
