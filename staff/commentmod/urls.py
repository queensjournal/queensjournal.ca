"""
URLConf for Django user requests.

Recommended usage is to use a call to ``include()`` in your project's
root URLConf to include this URLConf for any URL begninning with
'/accounts/'.

"""

from django.conf.urls.defaults import *
from staff.commentmod.views import *

urlpatterns = patterns('',
    (r'^$', comment_index),
    (r'^edit/(?P<c_id>\d+)/$', comment_edit),
    (r'^quickaction/$', comment_quickaction),
)
