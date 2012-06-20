from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('video.views',
    url(r'^$', 'video_index', name='video-index'),
    url(r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<slug>[-\w]+)/$', 'video_detail',
        name='video-detail'),
)
