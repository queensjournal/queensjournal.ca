from django.conf.urls import patterns, url
from masthead.views import MastheadDetailView, MastheadListView

urlpatterns = patterns('',
    url(r'^$', MastheadListView.as_view(), name='masthead_latest'),
    url(r'^(?P<vol_num>\d{1,3})/', MastheadDetailView.as_view(), name='masthead_single'),
    url(r'^archives/$', MastheadListView.as_view(), name='masthead_archives'),
)
