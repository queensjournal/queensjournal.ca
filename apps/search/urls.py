from django.conf.urls.defaults import url, patterns
from haystack.views import FacetedSearchView
from haystack.query import SearchQuerySet
from search.forms import SuperSearchForm

sqs = SearchQuerySet().facet('author').facet('tags').highlight()

urlpatterns = patterns('haystack.views',
    url(r'^$', FacetedSearchView(form_class=SuperSearchForm, searchqueryset=sqs), name='haystack_search'),
)
