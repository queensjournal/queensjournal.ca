from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from galleries.models import Gallery, PhotosPageOptions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from stories.views import parse_date
import datetime

def gallery_index(request):
    photographers = PhotosPageOptions.objects.get(pk=1).photographers
    galleries = Gallery.objects.all().exclude(name__iexact="Issue in Photos", pub_date__lt=datetime.datetime.now()).order_by('-pub_date')
    return render_to_response('photos/index.html', 
                            {'photographers': photographers,
                            'galleries': galleries[5:],
                            'featured': galleries[:6],},
                            context_instance=RequestContext(request))
                            
def gallery_detail(request, datestring, slug):
    gallery = get_object_or_404(Gallery, slug=slug)
    return render_to_response('photos/gallery_detail.html',
                            {'gallery': gallery,},
                            context_instance=RequestContext(request))