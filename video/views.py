from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from video.models import Video
from stories.views import parse_date

def detail_video(request, datestring, slug):
	video_selected = get_object_or_404(Video, slug__exact=slug)
	latest_videos = Video.objects.filter(published=True).exclude(slug=slug)[:2]
	if request.session.get('vote') is None:
		request.session['vote'] = []
	return render_to_response('video/detail_video.html',
								{'video': video_selected,
								'latest_videos': latest_videos},
								context_instance=RequestContext(request))
								
def index_video(request):
	video_list = get_list_or_404(Video, published=True)
	latest_video = video_list[0]
	other_videos = video_list[1:9]
	return render_to_response('video/index_video.html',
								{'latest_video': latest_video,
								'other_videos': other_videos,},
								context_instance=RequestContext(request))