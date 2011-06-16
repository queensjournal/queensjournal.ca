from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from galleries.models import Gallery, PhotosPageOptions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def gallery_index(request):
    photographers = PhotosPageOptions.objects.get(pk=1).photographers
    galleries = Gallery.objects.all()
    return render_to_response('photos/index.html', 
                            {'photographers': photographers,
                            'galleries': galleries,},
                            context_instance=RequestContext(request))