from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    (r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/$', 'stories.views.index_issue_front'),
    (r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<section>[-\w]+)/$',
        'stories.views.index_issue_section'),
    url(r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<section>[-\w]+)/(?P<slug>[-\w]+)/$',
        'stories.views.detail_story', name='story-detail'),
    (r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<section>[-\w]+)/(?P<slug>[-\w]+)/email/$',
        'stories.views.email_story'),
    (r'^(?P<section>[-\w]+)/$', 'stories.views.index_section'),
)
