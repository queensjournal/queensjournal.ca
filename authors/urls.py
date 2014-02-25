from django.conf.urls import patterns, url
from authors.views import AuthorDetailView

urlpatterns = patterns('',
    url(r'^author/(?P<slug>[\w-]+)/$', AuthorDetailView.as_view(),
        name='author-detail'),
)
