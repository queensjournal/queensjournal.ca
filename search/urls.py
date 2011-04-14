from django.conf.urls.defaults import *
from haystack.views import FacetedSearchView
from haystack.query import SearchQuerySet
from haystack.forms import FacetedSearchForm
from haystack.utils import Highlighter

sqs = SearchQuerySet().facet('author').facet('tags').highlight()

urlpatterns = patterns('haystack.views',
    url(r'^$', FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs), name='haystack_search'),
)
