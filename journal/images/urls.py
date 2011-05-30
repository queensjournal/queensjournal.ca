from django.conf.urls.defaults import *
from images.views import *

urlpatterns = patterns('',
                       (r'^add/$', images_add),
                       (r'^list/$', images_list),
                       (r'^markup/(?P<image_id>\d+)/$', images_add_to_markup),
                       )
