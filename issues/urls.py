from django.conf.urls import patterns, url


urlpatterns = patterns('issues.views',
    url(r'^volume-(?P<volume>\d{1,3})/issue-(?P<issue>\d{1,2})/$',
        'issue_detail', name='issue-detail'),
)
