# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.views.generic.list_detail import object_list
from structure.models import Volume
from masthead.models import Masthead

# helper functions
def section_order(x, y, sections):
    section_ids = [obj.section.id for obj in sections]
    index_x = -1
    index_y = -1
    for i in range(len(section_ids)):
        if section_ids[i] == x.section.id:
            index_x = i
        elif section_ids[i] == y.section.id:
            index_y = i
    if index_x == -1 or index_y == -1:
        return cmp(x._order, y._order)
    elif index_x == index_y:
        return cmp(x._order, y._order)
    else:
        return cmp(index_x, index_y)
    

def masthead_latest(request):
    try:
        masthead_obj = Masthead.objects.latest()
    except:
        raise Http404
    return masthead(request, masthead_obj.volume.volume)


def masthead(request, vol_num):
    # get volume, masthead objects
    volume_obj = get_object_or_404(Volume, volume=vol_num)
    masthead_obj = get_object_or_404(Masthead, volume=volume_obj.id)
    # get volume dates
    yearspan = list(volume_obj.get_years())
    if len(yearspan) == 0:
        yearstring = ""
    elif len(yearspan) == 1:
        yearstring = yearspan[0].year
    else:
        yearstring = "%s-%s" % (yearspan[0].year, yearspan[len(yearspan)-1].year)
    # get list of names and sort properly
    names = list(masthead_obj.mastheadname_set.all())
##    sections = list(masthead_obj.mastheadsectionwrapper_set.all())
##    names.sort(lambda x, y: section_order(x,y,sections))
    return render_to_response('masthead/index.html',
                              {'names': names,
                               'years': yearstring},
								context_instance=RequestContext(request))


def masthead_list(request):
    qs = Masthead.objects.order_by('volume')
    return object_list(request, queryset=qs)