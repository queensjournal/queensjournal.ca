from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^$', 'stories.views.index_archive'),
    (r'^(?P<volume>[0-999]+)/', 'stories.views.index_archive_volume'),
)
