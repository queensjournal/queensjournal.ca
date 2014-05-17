from django.conf.urls import url, patterns
from django.views.generic.base import TemplateView
from images.views import AddImagesView, images_add

urlpatterns = patterns('',
   url(r'^add/$', images_add),
   url(r'^list/$', TemplateView.as_view(template_name='images/widget_add.html')),
   url(r'^markup/(?P<image_id>\d+)/$', AddImagesView.as_view(
       template_name='images/widget_add_to_markup.html'
    )),
)
