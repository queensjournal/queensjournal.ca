from django.conf.urls import patterns, url


urlpatterns = patterns('',
    # this url has to stay at the top due to the way the dispatcher works we'll
    # eventually remove it when hits on /story/date go down
    url(r'^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})/$',
        'archive.views.legacy_archive_issue_detail', name='legacy-archive-issue-detail'),

    url(r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<section>[-\w]+)/$',
        'sections.views.section_detail', name='archive-section-index'),

    url(r'^(?P<datestring>\d{4}-\d{1,2}-\d{1,2})/(?P<section>[-\w]+)/(?P<slug>[-\w]+)(?:,(?P<pk>\d+))?/$',
        'stories.views.story_detail', name='story-detail'),

    url(r'^(?P<slug>[-\w]+)/$', 'sections.views.section_detail',
        name='stories-index-section'),
)
