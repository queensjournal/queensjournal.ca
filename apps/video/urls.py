from django.conf.urls.defaults import *
from video.views import *

urlpatterns = patterns('',
	(r'^$', index_video),
	(r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<slug>[-\w]+)/$', detail_video),
	)