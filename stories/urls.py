from django.conf.urls.defaults import *
from journal.stories.models import Story

urlpatterns = patterns('',
	(r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/$', 'journal.stories.views.index_issue_front'),
	(r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<section>[-\w]+)/$', 'journal.stories.views.index_issue_section'),
	(r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<section>[-\w]+)/(?P<slug>[-\w]+)/$', 'journal.stories.views.detail_story'),
	(r'^(?P<section>[-\w]+)/', 'journal.stories.views.index_section'),
)