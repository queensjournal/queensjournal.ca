from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/$', 'stories.views.index_issue_front'),
    (r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<section>[-\w]+)/$',
        'stories.views.index_issue_section'),
    (r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<section>[-\w]+)/(?P<slug>[-\w]+)/$',
        'stories.views.detail_story'),
    (r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<section>[-\w]+)/(?P<slug>[-\w]+)/email/$',
        'stories.views.email_story'),
    (r'^(?P<section>[-\w]+)/$', 'stories.views.index_section'),
)
