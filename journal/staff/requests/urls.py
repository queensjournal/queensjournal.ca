"""
URLConf for Django user requests.

Recommended usage is to use a call to ``include()`` in your project's
root URLConf to include this URLConf for any URL begninning with
'/accounts/'.

"""

from django.conf.urls.defaults import *
##from django.views.generic.simple import direct_to_template
##from django.contrib.auth.views import login, logout
##from requests.views import activate, register
from staff.requests.views import *

urlpatterns = patterns('',
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]+ because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
##                       (r'^$', 'journal.requests.views.index_view'),
##                       (r'^activate/(?P<activation_key>\w+)/$', activate),
##                       (r'^login/$', login, {'template_name': 'requests/login.html'}),
##                       (r'^logout/$', logout, {'template_name': 'requests/logout.html'}),
##                       (r'^register/$', register),
##                       (r'^register/complete/$', direct_to_template, {'template': 'requests/registration_complete.html'}),
    (r'^$', user_index),
    (r'^add/$', request_add),
    (r'^view/(?P<r_id>\d+)/$', request_view),
    (r'^edit/(?P<r_id>\d+)/$', request_edit),
)
