import datetime
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response
from django.template import RequestContext
from structure.models import Volume, Issue


def archive_index(request):
    volumes = get_list_or_404(Volume.objects.order_by('-volume'))
    dates = {}
    for volume in volumes:
        try:
            first_issue = Issue.objects.filter(volume__volume=volume.volume).\
                order_by('pub_date')[0]
            last_issue = Issue.objects.filter(volume__volume=volume.volume).\
                order_by('-pub_date')[0]
            dates[volume.volume] = '%s - %s' % (first_issue.pub_date.strftime("%Y"), \
                last_issue.pub_date.strftime("%Y"))
        except IndexError:
            continue
    return render_to_response('archives/index.html',
                            {'volumes': volumes,
                            'dates': dates},
                            context_instance=RequestContext(request))

def archive_volume_index(request, volume):
    volume = get_object_or_404(Volume, volume=volume)
    issues = get_list_or_404(Issue, volume=volume, pub_date__lt=datetime.datetime.now())
    return render_to_response('archives/index_volume.html',
                            {'volume': volume,
                            'issues': issues,},
                            context_instance=RequestContext(request))
