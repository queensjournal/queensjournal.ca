from django.conf.urls import patterns, url

urlpatterns = patterns('archive.views',
    url(r'^$', 'archive_volume_list',
        name='archive-volume-list'),

    url(r'^(?P<volume>[0-999]+)/$',
        'archive_volume_detail',
        name='archive-volume-detail'),
)
