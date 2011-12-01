from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('archive.views',
    url(r'^$', 'index_archive'),
    url(r'^(?P<volume>[0-999]+)/', 'index_archive_volume'),
)
