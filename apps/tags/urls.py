from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^(?P<tag>.*)/$','tags.views.with_tag'),
    (r'^(?P<tag>.*)/page/(?P<id>[-\w]+)/$', 'tags.views.with_tag' ),
)
