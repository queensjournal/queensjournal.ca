from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from video.models import Video


def video_detail(request, datestring, slug):
    video_selected = get_object_or_404(Video, slug__exact=slug,
        is_published=True)
    latest_videos = Video.objects.filter(is_published=True).exclude(slug=slug)[:2]
    if request.session.get('vote') is None:
        request.session['vote'] = []
    return render_to_response('video/video_detail.html',
        {'video': video_selected,
            'latest_videos': latest_videos},
        context_instance=RequestContext(request))


def video_index(request):
    video_list = get_list_or_404(Video, is_published=True)
    latest_video = video_list[0]
    other_videos = video_list[1:9]
    return render_to_response('video/video_index.html', {
            'latest_video': latest_video,
            'other_videos': other_videos,
        },
        context_instance=RequestContext(request))
