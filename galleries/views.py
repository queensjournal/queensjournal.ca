from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from galleries.models import Gallery
import datetime

# TODO: refactor these to generics
def gallery_index(request):
    galleries = Gallery.objects.all().exclude(name__iexact="Issue in Photos", \
        pub_date__lt=datetime.datetime.now()).order_by('-pub_date')
    return render_to_response('photos/index.html',
                            {'galleries': galleries[5:],
                            'featured': galleries[:6],},
                            context_instance=RequestContext(request))

def gallery_detail(request, datestring, slug):
    gallery = get_object_or_404(Gallery, slug=slug)
    return render_to_response('photos/gallery_detail.html',
                            {'gallery': gallery,},
                            context_instance=RequestContext(request))

def gallery_photo_detail(request, datestring, slug):
    gallery = get_object_or_404(Gallery, slug=slug)
    return render_to_response('photos/gallery_photo_detail.html',
                            {'gallery': gallery,},
                            context_instance=RequestContext(request))
