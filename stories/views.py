# Create your views here.
from datetime import date, time, timedelta
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import Context, RequestContext, loader
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.sites.models import Site
from django.views.generic.list_detail import object_list
from tagging.models import Tag, TaggedItem
from stories.models import Story, StoryAuthor, Photo
from video.models import Video
from blog.models import Entry
from structure.models import *
from itertools import chain
from operator import attrgetter
from django.db.models import Q
from dependencies.multiquery import QuerySetChain

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
	section_config = get_object_or_404(SectionFrontConfig, section__slug__iexact=section)
	if section_config.template:
		template = section_config.template
	else:
		template = 'stories/index_section.html'
	featured = Story.objects.filter(section__slug__iexact=section, featured=True, status='p').exclude(storyphoto__isnull=True, gallery__isnull=True).order_by('-pub_date')[:5]
	story_set = Story.objects.filter(section__slug__iexact=section, status='p').order_by('-pub_date')
	latest_stories = story_set[:5]
	other_stories = story_set[5:13]
	latest_issue = Issue.objects.latest('pub_date')
	if request.session.get('vote') is None:
		request.session['vote'] = []
	return render_to_response(template,
							{'featured': featured,
							'latest_stories': latest_stories,
							'other_stories': other_stories,
							'config': section_config,
							'latest_issue': latest_issue,},
							context_instance=RequestContext(request))
							
def index_front(request):
	front_config = FrontConfig.objects.latest('pub_date')
	lstories = Story.objects.filter(status='p').order_by('-pub_date')[:5]
	latest_entries = Entry.objects.filter(is_published=True).order_by('-pub_date')[:5]
	latest_video = Video.objects.latest('pub_date')
	latest_stories = QuerySetChain(lstories, latest_entries, latest_video)[:5]
	latest_section = []
	for section in front_config.sections.flatplansection_set.all():
		latest_section.extend(Story.objects.filter(section=section.section, featured=True, storyphoto__isnull=False)[:1])
	if request.session.get('vote') is None:
		request.session['vote'] = []
	return render_to_response('stories/index_front.html',
							{'featured': front_config.featuredstory_set.all().order_by('-story__pub_date'),
							'latest_stories': latest_stories,
							'latest_entries': latest_entries,
							'latest_section': latest_section,
							'latest_video': latest_video,
							'config': front_config},
							context_instance=RequestContext(request))	

def detail_story(request, datestring, section, slug):
	## Set up a range of one day based on the datestring
	dt = datetime.combine(parse_date(datestring), time())
	dt2 = dt + timedelta(1) - datetime.resolution
	story_selected = get_object_or_404(Story, section__slug__exact=section, pub_date__range=(dt, dt2), slug__exact=slug)
	section_config = SectionFrontConfig.objects.get(section__slug=section)
	try:
		author = StoryAuthor.objects.filter(story__slug__exact=slug)[0]
		author_role = author.author.get_role(story_selected.pub_date)
	except IndexError:
		author_role = False
	if request.session.get('vote') is None:
		request.session['vote'] = []
	return render_to_response('stories/single_detail.html',
								{'story': story_selected,
								'author_role': author_role,
								'config': section_config},
								context_instance=RequestContext(request))
								
def detail_author(request, author):
	curr_author = get_object_or_404(Author, slug__exact=author)
	story_set = StoryAuthor.objects.filter(author__slug__exact=author).order_by('story__pub_date')
	entry_set = Entry.objects.filter(author__slug__exact=author).order_by('-pub_date')
	if request.session.get('vote') is None:
		request.session['vote'] = []
	return render_to_response('stories/author_detail.html',
								{'author': curr_author,
								'stories': story_set,
								'entries': entry_set,},
								context_instance=RequestContext(request))
								
def tags(request):
	return render_to_response("tags/tags.html", context_instance=RequestContext(request))
	
def with_tag(request, tag, object_id=None, page=1): 
	
	unslug = tag.replace('-', ' ')
	query_tag = Tag.objects.get(name=unslug)
	story_list = TaggedItem.objects.get_by_model(Story, query_tag).order_by('-pub_date')
	entry_list = TaggedItem.objects.get_by_model(Entry, query_tag).order_by('-pub_date')
	result_list = sorted(chain(story_list, entry_list), key=attrgetter('pub_date'))

	return render_to_response("tags/with_tag.html", {'tag': tag, 
								'stories': result_list},
								context_instance=RequestContext(request))
								
''' ------------  ARCHIVES ------------- '''

def index_issue_front(request, datestring):
	issue = get_object_or_404(Issue, pub_date=parse_date(datestring))
	#try:
	front_config = FrontPageConfig.objects.get(issue=issue)
	#except FrontPageConfig.DoesNotExist:
	#	front_config = FrontConfig.objects.get(issue=issue)
	featured = Story.objects.filter( Q(section_order=1) | Q(featured=True), status='p', issue=issue, storyphoto__isnull=False)[:5]
	latest_stories = Story.objects.filter(status='p', issue=issue).order_by('-pub_date')[:5]
	back_issue = True
	latest_section = []
	for section in issue.sections.flatplansection_set.all():
		latest_section.extend(Story.objects.filter(section=section.section, issue=issue)[:2])
	if request.session.get('vote') is None:
		request.session['vote'] = []
	return render_to_response('archives/index_front.html',
							  {'featured': featured,
								'latest_stories': latest_stories,
								'latest_section': latest_section,
								'config': front_config,
								'back_issue': back_issue,
								'issue': issue},
							  context_instance=RequestContext(request))
						
def index_issue_section(request, datestring, section):
	issue = get_object_or_404(Issue, pub_date=parse_date(datestring))
	try:
		front_config = FrontPageConfig.objects.get(issue=issue)
	except FrontPageConfig.DoesNotExist:
		front_config = FrontConfig.objects.get(issue=issue)
	section_config = get_object_or_404(SectionFrontConfig.objects.filter(section__slug__iexact=section))
	first_story = Story.objects.filter(section__slug__iexact=section, issue=issue, status='p').exclude(storyphoto__isnull=True).order_by('section_order')
	story_set = Story.objects.filter(issue=issue, section__slug__iexact=section).order_by('section_order')
	back_issue = True
	featured = []
	try:
		if first_story[0]:
			featured = first_story[0]
			other_stories = story_set[1:]	
	except IndexError:
		other_stories = story_set
	try:
		last_story = other_stories.reverse()[0]
		older_stories = Story.objects.filter(section__slug__iexact=section, pub_date__lt=last_story.pub_date).order_by('-pub_date')[:5]
	except IndexError:
		older_stories = Story.objects.filter(section__slug__iexact=section, pub_date__lt=featured.pub_date).order_by('-pub_date')[:5]
	if request.session.get('vote') is None:
		request.session['vote'] = []
	return render_to_response('archives/index_section.html',
							{'featured': featured,
							'other_stories': other_stories,
							'older_stories': older_stories,
							'config': front_config,
							'section_config': section_config,
							'back_issue': back_issue,
							'issue': issue},
							context_instance=RequestContext(request))
							
def index_archive(request):
	volumes = get_list_or_404(Volume.objects.order_by('-volume'))
	dates = {}
	for volume in volumes:
		first_issue = Issue.objects.filter(volume__volume=volume.volume).order_by('pub_date')[0]
		last_issue = Issue.objects.filter(volume__volume=volume.volume).order_by('-pub_date')[0]
		dates[volume.volume] = '%s - %s' % (first_issue.pub_date.strftime("%Y"), last_issue.pub_date.strftime("%Y"))
	return render_to_response('archives/index.html',
							{'volumes': volumes,
							'dates': dates},
							context_instance=RequestContext(request))
							
def index_archive_volume(request, volume):
	volume = get_object_or_404(Volume, volume=volume)
	issues = get_list_or_404(Issue, volume=volume)
	return render_to_response('archives/index_volume.html',
							{'volume': volume,
							'issues': issues,},
							context_instance=RequestContext(request))
							
def server_error(request, template_name='500.html'):
	return render_to_response(template_name, context_instance = RequestContext(request))