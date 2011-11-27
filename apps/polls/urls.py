from django.conf.urls.defaults import url, patterns
from django.views.generic.list_detail import object_detail
from polls.models import Poll
from polls.views import poll_cookie_debug, poll_vote

urlpatterns = patterns('',
    (r'^debug/$', poll_cookie_debug),
    (r'^vote/(?P<poll>[0-9]+)/$', poll_vote),
    url(r'^view/(?P<object_id>[0-9]+)/$', object_detail, {'queryset': Poll.objects.all()},\
        name='poll_results'),
)
