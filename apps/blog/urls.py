from django.conf.urls.defaults import *
from blog.views import *

urlpatterns = patterns('',
    url(r'^archived/$', all_blogs, {'active': False}, name='all_blogs_archived'),
    url(r'^(?P<blog>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$', blog_detail),
    url(r'^(?P<blog>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/page/(?P<page>\d{1,5})/$', blog_archive_month, name='blog_archive_month_pages'),
    url(r'^(?P<blog>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/$', blog_archive_month, name='blog_archive_month_front'),           
    url(r'^(?P<blog>[-\w]+)/page/(?P<page>\d{1,5})/$', blog_index, name='blog_index_pages'),
    url(r'^(?P<blog>[-\w]+)/$', blog_index, name='blog_index_front'),
    url(r'^$', all_blogs, name='all_blogs'),
    )
