# Create your views here.
from datetime import date
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import Context, RequestContext, loader
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.sites.models import Site
from django.views.generic.list_detail import object_list
from stories.models import Story
from structure.models import *

def parse_date(datestring):
	return date(*[int(x) for x in datestring.split('-')])
	
def get_issue(request):
	section = 'news'
	issue = get_object_or_404(Issue, pk=request.GET.get('issue', ''))
	return HttpResponseRedirect('/story/%s/' % issue.pub_date)
	
def index_latest(request):
	try:
		issue = Issue.objects.pub_date.latest()
	except:
		issue = FrontPageConfig.objects.latest('pub_date')
	return index_front(request, issue.pub_date.strftime("%Y-%m-%d"))
	
def index_section(request, section):
	section_config = get_object_or_404(SectionFrontConfig.objects.filter(section__slug__iexact=section))
	front_config = get_object_or_404(FrontConfig.objects.latest('pub_date'))
	first_story = get_object_or_404(Story.objects.filter(section__slug__iexact=section, featured=True, status='p').order_by('-pub_date')[:1])
	story_set = Story.objects.filter(section__slug__iexact=section, status='p').order_by('-pub_date')[:10]
	if request.session.get('vote') is None:
		request.session['vote'] = []
	return render_to_response('stories/index_section.html',
							{'story': first_story,
							'latest': story_set,
							'config': section_config},
							context_instance=RequestContext(request))
							
def index_front(request):
	front_config = get_object_or_404(FrontConfig.objects.latest('pub_date'))
	if request.session.get('vote') is None:
		request.session['vote'] = []
	return render_to_response('stories/index_front.html',
							{'featured': front_config.featuredstory_set.all(),
							'config': front_config},
							context_instance=RequestContext(request))
							
def index_issue_front(request, datestring):
	issue = get_object_or_404(Issue, pub_date=parse_date(datestring))
	front_config = get_object_or_404(FrontPageConfig, issue=issue)
	if request.session.get('vote') is None:
		request.session['vote'] = []
	return render_to_response('stories/index_front.html',
							  {'story': front_config.frontpagetopstory_set.all()[0],
							   'config': front_config},
							  context_instance=RequestContext(request))
						
def index_issue_section(request, datestring, section):
	first_story = get_object_or_404(Story, issue__pub_date=parse_date(datestring), section__slug__iexact=section, section_order=1)
	story_set = Story.objects.filter(issue__pub_date=parse_date(datestring), section__slug__iexact=section).order_by('section_order')
	if request.session.get('vote') is None:
		request.session['vote'] = []
	return render_to_response('stories/index_section.html',
								{'story': first_story,
								'story_set': story_set},
								context_instance=RequestContext(request))		
'''
def index_section_latest(request, section):
	try:
		config = FlatPlanConfig.objects.filter(flatplansection__section__slug=section)
		issue = Issue.objects.published().filter(section__in=list(configs)).latest()
	except Issue.DoesNotExist, FlatPlanConfig.DoesNotExist:
		raise Http404
	return HttpResponseRedirect('/story/%s/%s/' % (issue.pub_date.strftime("%Y-%m-%d"), section))
'''	
def detail_story(request, datestring, section, slug):
	story_selected = get_object_or_404(Story, issue__pub_date=parse_date(datestring), section__slug__exact=section, slug__exact=slug)
	if request.session.get('vote') is None:
		request.session['vote'] = []
	return render_to_response('stories/single_detail.html',
								{'story': story_selected},
								context_instance=RequestContext(request))