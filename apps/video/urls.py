from django.conf.urls.defaults import patterns
from video.views import index_video, detail_video

urlpatterns = patterns('',
    (r'^$', index_video),
    (r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<slug>[-\w]+)/$', detail_video),
)
