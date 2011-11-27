from django.conf.urls.defaults import patterns, url
from masthead.views import masthead_latest, masthead, masthead_list

urlpatterns = patterns('',
    url(r'^$', masthead_latest, name='masthead_latest'),
    url(r'^(?P<vol_num>\d{1,3})/', masthead, name='masthead_single'),
    url(r'^archives/$', masthead_list, name='masthead_archives'),
)
