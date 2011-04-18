from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
from haystack.views import FacetedSearchView
from haystack.query import SearchQuerySet
from search.forms import SuperSearchForm
from haystack.utils import Highlighter

sqs = SearchQuerySet().facet('author').facet('tags').highlight()

urlpatterns = patterns('haystack.views',
    url(r'^$', FacetedSearchView(form_class=SuperSearchForm, searchqueryset=sqs), name='haystack_search'),
)
