from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^(?P<tag>.*)/$', 'tags.views.with_tag'),
    url(r'^(?P<tag>.*)/page/(?P<id>[-\w]+)/$', 'tags.views.with_tag' ),
)
