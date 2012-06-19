from django.conf.urls.defaults import *
from staff.views import *

urlpatterns = patterns('',
    (r'^$', index),
    (r'^login/$', user_login),
    (r'^logout/$', user_logout),
    (r'^requests/', include('staff.requests.urls')),
    )
