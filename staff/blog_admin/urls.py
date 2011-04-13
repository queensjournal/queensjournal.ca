"""
URLConf for Django user requests.

Recommended usage is to use a call to ``include()`` in your project's
root URLConf to include this URLConf for any URL begninning with
'/accounts/'.

"""

from django.conf.urls.defaults import *
from staff.blog_admin.views import *

urlpatterns = patterns('',
    (r'^$', all_blogs),
    (r'^ajax_preview/$', entry_ajax_preview),
    (r'^(?P<blog>[-\w]+)/$', dashboard),
    (r'^(?P<blog>[-\w]+)/profile/', profile_edit),
    (r'^(?P<blog>[-\w]+)/list/$', entries_index),
    (r'^(?P<blog>[-\w]+)/add/$', entry_add),
    (r'^(?P<blog>[-\w]+)/edit/(?P<e_id>\d+)/$', entry_edit),
)
