from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^tag/(?P<tag>.*)/$','tags.views.with_tag'),
    (r'^tag/(?P<tag>.*)/page/(?P<id>[-\w]+)/$', 'tags.views.with_tag' ),
)
