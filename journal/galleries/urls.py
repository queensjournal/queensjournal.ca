from django.conf.urls.defaults import *
from galleries.views import *

urlpatterns = patterns('',
	(r'^$', gallery_index),
	#(r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<slug>[-\w]+)/$', gallery_detail),
)