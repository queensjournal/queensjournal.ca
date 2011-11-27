from django.conf.urls.defaults import patterns
from galleries.views import gallery_index, gallery_detail, gallery_photo_detail

urlpatterns = patterns('',
    (r'^$', gallery_index),
    (r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<slug>[-\w]+)/$', gallery_detail),
    (r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<slug>[-\w]+)/$', gallery_photo_detail),
)
