from django.conf.urls.defaults import patterns
from images.views import images_add, images_list, images_add_to_markup

urlpatterns = patterns('',
   (r'^add/$', images_add),
   (r'^list/$', images_list),
   (r'^markup/(?P<image_id>\d+)/$', images_add_to_markup),
)
