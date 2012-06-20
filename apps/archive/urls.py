from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('archive.views',
    url(r'^$', 'archive_index', name='archive-index'),
    url(r'^(?P<volume>[0-999]+)/', 'archive_volume_index', name='archive-volume-index'),
)
